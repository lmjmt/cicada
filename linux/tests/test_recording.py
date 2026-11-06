"""保存会议录音's parts that need no GStreamer: the ADTS file (core/aac.py), the record's hasAudio, and
the listening engine handing the recorder every sample the lines are timed by."""
from __future__ import annotations

import os
import sys
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import test_core as tc  # noqa: E402 - its helpers; a module import, so its tests aren't collected twice
from cicada.core import aac  # noqa: E402
from cicada.core.audio import RATE, PcmAudioSource  # noqa: E402
from cicada.core.listen import ListenEngine  # noqa: E402
from cicada.core.models import TranscriptLine  # noqa: E402
from cicada.core.notes import NotesEngine  # noqa: E402
from cicada.core.session_store import SessionStore  # noqa: E402
from cicada.core.settings import AppSettings  # noqa: E402
from cicada.core.translator import Translator  # noqa: E402


def adts(n: int, rate_index: int = 8, body: int = 20) -> bytes:
    """n ADTS frames (16 kHz by default) with `body` bytes each."""
    length = 7 + body
    head = bytes([0xFF, 0xF1, 0x40 | (rate_index << 2), 0x40 | ((length >> 11) & 0x03),
                  (length >> 3) & 0xFF, ((length & 0x07) << 5) | 0x1F, 0xFC])
    return (head + bytes(body)) * n


class Adts(unittest.TestCase):
    def test_reads_frames_and_their_length(self):
        data = adts(250)
        self.assertEqual(250, len(list(aac.frames(data))))
        self.assertAlmostEqual(250 * 1024 / 16000, aac.seconds(data))

    def test_a_torn_last_frame_goes(self):
        data = adts(10) + adts(1)[:12]  # killed mid-write
        self.assertEqual(adts(10), aac.cut(data, None))

    def test_cuts_at_the_meetings_end(self):
        data = adts(100)  # 6.4 s
        kept = aac.cut(data, 3.0)
        self.assertAlmostEqual(3.008, aac.seconds(kept), places=3)  # whole frames, up to the first one past 3 s
        self.assertEqual(data, aac.cut(data, 60))

    def test_partial_name(self):
        self.assertEqual("/x/20261106-101010/system.aac", aac.partial("/x/20261106-101010/system.m4a"))


class HasAudio(tc.Base):
    def test_a_meeting_with_a_recording_says_so(self):
        store = SessionStore()
        s = store.begin(datetime(2026, 1, 1, 2, tzinfo=timezone.utc))
        store.append(s.id, TranscriptLine(id="h1-1", src="hi", srcLang="en", dstLang="zh-CN"))
        os.makedirs(os.path.dirname(store.audio_path(s.id)), exist_ok=True)
        with open(aac.partial(store.audio_path(s.id)), "wb") as f:
            f.write(adts(5))
        store.end(s.id)
        self.assertTrue(store.get(s.id).hasAudio)
        with open(os.path.join(os.path.dirname(store.audio_path(s.id)), "session.json"), encoding="utf-8") as f:
            self.assertIn('"hasAudio" : true', f.read())
        # The app quit before rewrapping: the next launch finds it.
        self.assertEqual([s.id], SessionStore().unfinished_audio())

    def test_without_one_it_says_none(self):
        store = SessionStore()
        s = store.begin(datetime(2026, 1, 1, 2, tzinfo=timezone.utc))
        store.append(s.id, TranscriptLine(id="h1-1", src="hi", srcLang="en", dstLang="zh-CN"))
        store.end(s.id)
        self.assertFalse(store.get(s.id).hasAudio)
        self.assertEqual([], store.unfinished_audio())


class FakeRecorder:
    def __init__(self):
        self.samples = 0
        self.closed = False
        self.finished = threading.Event()
        self.until = "unset"

    def write(self, buf):
        assert not self.closed
        self.samples += len(buf)

    def close(self):
        self.closed = True

    def finish(self, until):
        self.until = until
        self.finished.set()


class Recording(tc.Base):
    def engine(self):
        ling = tc.client(tc.Fake(lambda body: tc.reply("LANG: en\nORIGINAL: Hello.\nTRANSLATION: 你好。")
                                 if "Ming-3.0-audio-flash" in body else tc.reply("{}")))
        tc.LingClient.spacing = 0.05
        store = SessionStore()
        return store, ListenEngine(ling, Translator(ling), store, NotesEngine(ling, store), AppSettings(target="zh-CN"))

    def run_meeting(self, engine, ended_at=None):
        rec = FakeRecorder()
        engine.recorder = lambda sid: rec
        src = PcmAudioSource(lambda: tc.concat(tc.tone(1.0), tc.silence(1.5)), speed=0)
        done = threading.Event()
        src.on_ended = lambda why: done.set()
        engine.start(src, "file")
        self.assertTrue(engine.recording)
        done.wait(10)
        time.sleep(0.5)
        heard = engine.heard_seconds
        engine.stop(ended_at)
        return rec, heard

    def test_every_sample_heard_is_written_then_rewrapped(self):
        store, engine = self.engine()
        rec, heard = self.run_meeting(engine)
        self.assertTrue(rec.closed)
        # The lines' clock is the samples the lane heard: the file holds exactly those.
        self.assertEqual(round(heard * RATE), rec.samples)
        self.assertTrue(rec.finished.wait(5))
        self.assertIsNone(rec.until)
        self.assertFalse(engine.recording)

    def test_a_meeting_that_ended_by_itself_is_cut_there(self):
        store, engine = self.engine()
        rec, _ = self.run_meeting(engine, ended_at=datetime.now(timezone.utc) + timedelta(seconds=-0.5))
        self.assertTrue(rec.finished.wait(5))
        s = store.get(engine.session_id)
        self.assertIsNotNone(s, "a line was heard, so the meeting is kept")
        self.assertAlmostEqual(s.duration, rec.until, places=3)

    def test_no_recorder_no_recording(self):
        _store, engine = self.engine()
        engine.recorder = lambda sid: None
        src = PcmAudioSource(lambda: tc.silence(0.3), speed=0)
        engine.start(src, "file")
        self.assertFalse(engine.recording)
        engine.stop()


if __name__ == "__main__":
    unittest.main()
