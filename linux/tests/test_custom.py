"""其他（兼容 OpenAI）for self-hosted models (AIProviderTests.swift): plain http on the local network,
thinking turned off through the chat template (and left out for a server that refuses it), the
check's real sentence and what it says about a thinking model, and the hear model at an address of
its own."""
from __future__ import annotations

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from test_providers import Base, Fake, reply  # noqa: E402

from cicada.core import aicheck, jsonfmt, providers  # noqa: E402
from cicada.core.ling import OK, TRANSLATE, LingError, Response, silence_wav  # noqa: E402
from cicada.core.settings import AppSettings  # noqa: E402


def custom(**kw):
    kw.setdefault("aiCustomBase", "http://192.168.1.20:8000/v1")
    kw.setdefault("aiModels", {"custom": "qwen3:14b"})
    kw.setdefault("aiHearModels", {"custom": "qwen3-omni"})
    return dict(kw)


def answer(content="周五发布。", **message):
    m = {"content": content, **message}
    return Response(200, jsonfmt.write({"choices": [{"message": m, "finish_reason": "stop"}]}, pretty=False))


class Nearby(unittest.TestCase):
    def test_the_local_network_may_use_plain_http(self):
        for ok in ("http://192.168.1.20:8000/v1", "10.0.0.5:8000/v1", "http://172.20.1.1/v1", "http://100.101.102.103:8000/v1",
                   "http://169.254.3.4/v1", "http://gpu.local:30000/v1", "http://[fd12:3456::1]:8000/v1", "http://[::1]:8000/v1",
                   "http://[fe80::1]/v1", "http://localhost:11434/v1"):
            self.assertTrue((providers.custom_base(ok) or "").startswith("http://"), ok)
        for no in ("http://172.32.0.1/v1", "http://172.15.0.1/v1", "http://100.128.0.1/v1", "http://100.63.0.1/v1",
                   "http://8.8.8.8/v1", "http://192.169.1.1/v1", "http://gpu.example.com/v1", "http://10.0.0.5.evil.com/v1",
                   "http://10.0.0.256/v1", "http://[2001:db8::1]/v1"):
            self.assertIsNone(providers.custom_base(no), no)
        self.assertEqual("http://192.168.1.20:8000/v1/", providers.custom_base("192.168.1.20:8000/v1"))
        self.assertEqual("https://10.0.0.5.evil.com/v1/", providers.custom_base("10.0.0.5.evil.com/v1"))
        self.assertEqual("https://gpu.example.com/v1/", providers.custom_base("https://gpu.example.com/v1"))
        self.assertTrue(providers.is_nearby("http://192.168.1.20:8000/v1/"))
        self.assertFalse(providers.is_local("http://192.168.1.20:8000/v1/"))
        self.assertIsNone(providers.custom_base("  "))

    def test_a_nearby_service_needs_no_key(self):
        from cicada.core.ling import AIKey, LingClient
        s = AppSettings(aiProvider="custom", **custom())
        ling = LingClient(AIKey(path=os.path.join(HERE, "no-such-key")), Fake(lambda u, b: answer()), config=s.ai_config)
        self.assertEqual("", ling.current_key())
        s.aiCustomBase = "https://gpu.example.com/v1"
        self.assertIsNone(ling.current_key())


class Shape(unittest.TestCase):
    def test_custom_turns_thinking_off_through_the_template(self):
        c = providers.AIConfig(providers.CUSTOM, "http://localhost/v1/", "m", "h")
        body = {}
        c.shape(body, 50)
        self.assertEqual({"enable_thinking": False}, body["chat_template_kwargs"])
        self.assertNotIn("thinking", body)
        plain = {}
        c.shape(plain, 50, template_kwargs=False)
        self.assertNotIn("chat_template_kwargs", plain)
        for p in (providers.LING, providers.ZENMUX, providers.OPENROUTER):
            other = {}
            providers.AIConfig(p, p.base, "m", "h").shape(other, 50)
            self.assertNotIn("chat_template_kwargs", other, p.id)

    def test_a_thinking_model_is_seen_from_its_reply(self):
        def r(message, usage=None):
            root = {"choices": [{"message": message}]}
            if usage is not None:
                root["usage"] = usage
            return root
        self.assertFalse(providers.thought(r({"content": "周五发布。"})))
        self.assertTrue(providers.thought(r({"content": "周五发布。", "reasoning_content": "The user wants…"})))
        # A reasoning parser on the server: the answer itself sits in reasoning_content.
        self.assertTrue(providers.thought(r({"content": "", "reasoning_content": "周五发布。"})))
        self.assertTrue(providers.thought(r({"content": "周五发布。", "reasoning": "hmm"})))
        self.assertTrue(providers.thought(r({"content": "<think>hmm</think>周五发布。"})))
        self.assertTrue(providers.thought(r({"content": "周五发布。"}, {"completion_tokens_details": {"reasoning_tokens": 212}})))
        self.assertFalse(providers.thought(r({"content": "周五发布。", "reasoning_content": "  "},
                                             {"completion_tokens_details": {"reasoning_tokens": 0}})))
        self.assertFalse(providers.thought({}))

    def test_a_slow_sentence_is_flagged(self):
        self.assertFalse(aicheck.Speed(0.4, False).slow)
        self.assertTrue(aicheck.Speed(0.4, True).slow)
        self.assertTrue(aicheck.Speed(3.0, False).slow)
        self.assertTrue(aicheck.Speed(6.4, False).slow)
        r = aicheck.AICheck()
        r.pass_up_to("hear", 1.0)
        r.translate = aicheck.Speed(4.2, True)
        self.assertTrue(r.slow)
        self.assertIn("4.2", r.slow_line())
        self.assertIn("思考", r.slow_line())
        self.assertIn("Google", r.slow_line())
        # 语音和文字只发给你的服务: no Google to fall back on, the sentence is given up on.
        self.assertNotIn("Google", r.slow_line(google_off=True))
        self.assertIn("不等它了", r.slow_line(google_off=True))
        self.assertIn("思考", r.slow_line(google_off=True))
        r.translate = aicheck.Speed(3.5, False)
        self.assertNotIn("思考", r.slow_line())
        self.assertIn("不等它了", r.slow_line(google_off=True))
        self.assertNotIn("思考", r.slow_line(google_off=True))
        r.translate = aicheck.Speed(0.5, False)
        self.assertIsNone(r.slow_line())
        self.assertIn("translate=0.5s", r.summary())
        # The hear model is a job of its own: not filled in yet, it doesn't hide a thinking text model.
        r = aicheck.AICheck()
        r.pass_up_to("text", 4.2)
        r.translate = aicheck.Speed(4.2, True)
        r.fail("hear", aicheck.DEAF)
        self.assertTrue(r.slow)
        r = aicheck.AICheck()
        r.translate = aicheck.Speed(4.2, True)
        r.fail("text", aicheck.NO_JSON)
        self.assertFalse(r.slow)

    def test_no_hear_model_yet_names_the_service(self):
        from cicada.core import problem
        r = aicheck.AICheck()
        r.fail("hear", aicheck.DEAF)
        self.assertEqual("这个服务 听不了声音。", r.message("这个服务", "10.0.2.2", "qwen3-8b", ""))
        self.assertEqual("这个服务 听不了声音。", problem.title(aicheck.DEAF, "这个服务", "qwen3-8b", ""))
        self.assertEqual("qwen3-omni 听不了声音。", r.message("这个服务", "10.0.2.2", "qwen3-8b", "qwen3-omni"))


class TemplateKwargs(Base):
    def test_a_server_that_refuses_it_is_asked_again_without(self):
        def respond(url, body):
            return Response(422, "{}") if "chat_template_kwargs" in body else answer()
        fake = Fake(respond)
        ling, s = self.client(fake, "custom", key=None, **custom())
        self.assertEqual("周五发布。", ling.chat("x", "Translate.", TRANSLATE))
        self.assertEqual(2, len(fake.sent))
        self.assertIn("chat_template_kwargs", fake.sent[0][1])
        self.assertNotIn("chat_template_kwargs", fake.sent[1][1])
        # Not sent there again…
        ling.chat("x", "Translate.", TRANSLATE)
        self.assertEqual(3, len(fake.sent))
        self.assertNotIn("chat_template_kwargs", fake.sent[2][1])
        # …until settings change.
        ling.key_changed()
        ling.chat("x", "Translate.", TRANSLATE)
        self.assertIn("chat_template_kwargs", fake.sent[3][1])
        # A refused request never showed as a missing model.
        self.assertIsNone(ling.check_result.failure)

    def test_a_400_both_ways_is_not_the_field(self):
        fake = Fake(lambda u, b: Response(400, "{}"))
        ling, _ = self.client(fake, "custom", key=None, **custom())
        with self.assertRaises(LingError) as e:
            ling.chat("x", "Translate.", TRANSLATE)
        self.assertEqual(400, e.exception.status)
        self.assertEqual(2, len(fake.sent))
        fake.respond = lambda u, b: answer()
        ling.chat("x", "Translate.", TRANSLATE)
        self.assertIn("chat_template_kwargs", fake.sent[-1][1])  # nothing remembered

    def test_other_errors_are_not_retried(self):
        fake = Fake(lambda u, b: Response(500, "{}"))
        ling, _ = self.client(fake, "custom", key=None, **custom())
        with self.assertRaises(LingError):
            ling.chat("x", "Translate.", TRANSLATE)
        self.assertEqual(1, len(fake.sent))


class Check(Base):
    def test_the_check_translates_a_real_sentence(self):
        fake = Fake(lambda u, b: Response(404, "") if u.endswith("/models") else answer())
        ling, _ = self.client(fake, "custom", key=None, **custom())
        self.assertEqual(OK, ling.check())
        first = jsonfmt.parse_object(fake.sent[0][1])
        self.assertIn("We will ship the new version on Friday", first["messages"][0]["content"])
        self.assertEqual("Translate.", first["messages"][1]["content"])
        self.assertEqual(120, first["max_tokens"])
        r = ling.check_result
        self.assertIsNotNone(r.translate)
        self.assertFalse(r.translate.thinks)
        self.assertFalse(r.slow)
        self.assertIn("translate=", r.summary())

    def test_a_thinking_model_is_slow(self):
        def respond(url, body):
            if url.endswith("/models"):
                return Response(404, "")
            return answer(reasoning_content="Let me think…")
        ling, _ = self.client(Fake(respond), "custom", key=None, **custom())
        ling.check()
        r = ling.check_result
        self.assertTrue(r.translate.thinks)
        self.assertTrue(r.slow)
        self.assertIn("思考", r.slow_line())

    def test_bad_address_words_the_local_network(self):
        ling, _ = self.client(Fake(lambda u, b: answer()), "custom", key="sk-x", aiCustomBase="http://gpu.example.com/v1")
        ling.check()
        self.assertEqual(aicheck.BAD_ADDRESS, ling.check_result.reason)
        self.assertIn("局域网", ling.message())


class HearAddress(Base):
    def test_the_hear_address_falls_back_to_the_text_one(self):
        c = AppSettings(aiProvider="custom", **custom()).ai_config()
        self.assertEqual("http://192.168.1.20:8000/v1/", c.hear_url)
        self.assertFalse(c.own_hear_address)
        c = AppSettings(aiProvider="custom", **custom(aiCustomHearBase="192.168.1.30:8001/v1")).ai_config()
        self.assertEqual("http://192.168.1.30:8001/v1/", c.hear_url)
        self.assertEqual("http://192.168.1.20:8000/v1/", c.base)
        self.assertTrue(c.own_hear_address)
        # Typed but not valid: nowhere to send audio (not the text address).
        c = AppSettings(aiProvider="custom", **custom(aiCustomHearBase="http://gpu.example.com/v1")).ai_config()
        self.assertIsNone(c.hear_url)
        z = AppSettings(aiProvider="zenmux", aiCustomHearBase="http://192.168.1.30/v1").ai_config()
        self.assertEqual(z.base, z.hear_url)

    def test_hear_calls_and_the_check_go_to_the_hear_address(self):
        def respond(url, body):
            if url.endswith("/models"):
                return Response(404, "")
            return answer("NONE" if "input_audio" in body else "周五发布。")
        fake = Fake(respond)
        ling, _ = self.client(fake, "custom", key=None, **custom(aiCustomHearBase="http://192.168.1.30:8001/v1"))
        self.assertEqual(OK, ling.check())
        audio = [u for u, b in fake.sent if "input_audio" in b]
        text = [u for u, b in fake.sent if "chat/completions" in u and "input_audio" not in b]
        self.assertEqual(["http://192.168.1.30:8001/v1/chat/completions"], audio)
        self.assertTrue(text and all(u.startswith("http://192.168.1.20:8000/v1/") for u in text))
        self.assertEqual("ok", ling.check_result["hear"].kind)
        ling.chat("x", "y", TRANSLATE, model="qwen3-omni", audio=silence_wav())
        self.assertEqual("http://192.168.1.30:8001/v1/chat/completions", fake.sent[-1][0])

    def test_an_unreachable_hear_address_leaves_text_working(self):
        def respond(url, body):
            if "192.168.1.30" in url:
                raise OSError("no route")
            return Response(404, "") if url.endswith("/models") else answer()
        ling, _ = self.client(Fake(respond), "custom", key=None, **custom(aiCustomHearBase="http://192.168.1.30:8001/v1"))
        self.assertEqual(OK, ling.check())
        r = ling.check_result
        self.assertEqual(("hear", aicheck.UNREACHABLE, None), r.failure)
        self.assertFalse(r.down)
        self.assertIn("192.168.1.30", ling.message())
        self.assertEqual("192.168.1.30", ling.hear_host)

    def test_an_invalid_hear_address_fails_the_hear_step(self):
        fake = Fake(lambda u, b: Response(404, "") if u.endswith("/models") else answer())
        ling, _ = self.client(fake, "custom", key=None, **custom(aiCustomHearBase="http://gpu.example.com/v1"))
        ling.check()
        self.assertEqual(("hear", aicheck.BAD_ADDRESS, None), ling.check_result.failure)
        self.assertFalse(any("input_audio" in b for _u, b in fake.sent))


class StubLing:
    """The service, for the translator alone: answers each sentence, or fails."""

    def __init__(self, answer=None):
        self.usable = True
        self.answer = answer  # None: the service can't be reached
        self.asked = []
        self.check_result = aicheck.AICheck()  # not checked yet: every sentence is tried

    def chat(self, prompt, user, priority, **kw):
        self.asked.append(prompt)
        if self.answer is None:
            raise LingError("unreachable")
        return self.answer


GOOGLE = Response(200, '[[["周五发布。","We ship on Friday",null,null,1]]]')


class GoogleOff(unittest.TestCase):
    """语音和文字只发给你的服务 (issue #15, TranslatorTests.swift › GoogleOffTests): Google is never asked."""

    def translator(self, ling, google=GOOGLE):
        from cicada.core.translator import Translator
        fake = Fake(lambda u, b: google)
        return Translator(ling, transport=fake), fake

    def test_partial_lines_show_the_original_without_asking_anyone(self):
        from cicada.core.translator import Translator
        ling = StubLing("周五发布。")
        t, fake = self.translator(ling)
        t.google_off = True
        for _ in range(3):
            self.assertIsNone(t.translate("We ship on Friday", "en", "zh-CN", Translator.DRAFT))
        self.assertEqual([], fake.sent)
        self.assertEqual([], ling.asked)  # partial text never goes to the AI service either
        self.assertFalse(t.sentences_untranslated)

    def test_finished_sentences_go_to_the_service_only(self):
        from cicada.core.translator import Translator
        ling = StubLing("周五发布。")
        t, fake = self.translator(ling)
        t.google_off = True
        self.assertEqual("周五发布。", t.translate("We ship on Friday", "en", "zh-CN", Translator.SENTENCE))
        self.assertFalse(t.sentences_untranslated)
        ling.answer = None
        self.assertIsNone(t.translate("We ship on Friday", "en", "zh-CN", Translator.SENTENCE))
        self.assertTrue(t.sentences_untranslated)
        self.assertEqual([], fake.sent)

    def test_off_google_still_stands_in(self):
        from cicada.core.translator import Translator
        t, fake = self.translator(StubLing(None))
        self.assertEqual("周五发布。", t.translate("We ship on Friday", "en", "zh-CN", Translator.SENTENCE))
        self.assertEqual("周五发布。", t.translate("We ship on Friday", "en", "zh-CN", Translator.DRAFT))
        self.assertEqual(2, len(fake.sent))

    def test_flipping_it_clears_a_stale_google_backoff(self):
        from cicada.core.translator import Translator
        t, fake = self.translator(StubLing(None), google=Response(429, ""))
        self.assertIsNone(t.translate("Hello", "en", "zh-CN", Translator.DRAFT))
        self.assertGreater(t._google_backoff_until, 0)
        t.google_off = True
        self.assertEqual(0.0, t._google_backoff_until)
        t.translate("Hello", "en", "zh-CN", Translator.SENTENCE)
        self.assertTrue(t.sentences_untranslated)
        t.google_off = False
        self.assertFalse(t.sentences_untranslated)
        fake.respond = lambda u, b: GOOGLE
        self.assertEqual("周五发布。", t.translate("Hello", "en", "zh-CN", Translator.DRAFT))

    def test_only_with_the_custom_service(self):
        s = AppSettings(aiProvider="custom", aiCustomOnly=True, **custom())
        self.assertTrue(s.google_off)
        s.aiProvider = "ling"
        self.assertFalse(s.google_off)  # kept, but inert
        self.assertTrue(s.aiCustomOnly)
        self.assertFalse(AppSettings(aiProvider="custom", **custom()).google_off)

    def test_the_footnote_names_one_host_only_when_every_use_shares_it(self):
        s = AppSettings(aiProvider="custom", **custom())
        self.assertEqual("192.168.1.20", providers.only_host(s.ai_config()))
        s.aiCustomHearBase = "http://192.168.1.30:8000/v1"
        self.assertIsNone(providers.only_host(s.ai_config()))
        s.aiCustomHearBase = ""
        s.aiVoiceModels = {"custom": "qwen3-tts"}
        s.aiCustomVoiceBase = "http://192.168.1.40:8000/v1"
        self.assertIsNone(providers.only_host(s.ai_config()))


if __name__ == "__main__":
    unittest.main()
