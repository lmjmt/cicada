# 同声传译: what I say into the meeting

What 279d045, 08f316b and 7106021 were measured with. `scripts/speak-round.sh <label> [quiet|meeting|silent] [volume]`, env `VP` (`speakVP`, default on as in the app), `MIC` (打开麦克风 during the round), `SPEAKMIC` (the talk key's mic, default the MacBook's), `OUT`. Three presses, about 50 s a round. It needs a working AI service (`lsctl aiState`; Ling speaks with Ming).

## The conversation

| Press | Key held for | ESP32 (me, 10 cm from the mic) | Speakers |
|---|---|---|---|
| 1 | about 4 s | 我们下周三之前可以把测试做完。 | `quiet`: nothing; `meeting`: `meeting.wav`, English without a break, through all three presses |
| 2 | about 4 s | 价格方面我需要先和财务确认一下。 | same |
| 3 | about 4 s | 这个问题我会后发邮件给大家。 | same |

`silent` holds the key the same way with nobody speaking (and the meeting playing, or at volume 0 for a quiet room). `MIC=on` adds the room mic: my sentences must not show up as room lines, since the room mic hears silence while I hold the key and while the translation is read out.

## Reading a round

```
== meeting: presses=3 sent=3 failed=0 me_lines=3 mine_heard: 86% 100% 100% english_in_mine=0 voiced=3 skipped_silent=0 in_room_lines: 0% 0% 0%
   release→text 2.97s, text→translation 0.00s
   voice: 8 chunks to BlackHole 2ch, first audio 4.12s after release
   me| 我们下周三之前可以把这个任务做完。  =>  We can finish this task by next Wednesday.
```

`mine_heard` is how much of each of my sentences is in what was sent; `english_in_mine` the meeting's words in it (its echo, interpreted as me). `voiced` counts the voices that reached BlackHole (`spoke … chunks`); `skipped_silent` the presses PressSpeech found nobody speaking in. Ming answers recognition and translation together: `text→translation` is 0 and `release→text` is the whole call.

## Pass line (2026-11-06, MacBook Pro 14, speakers at 56 %)

| Round | Command | Pass |
|---|---|---|
| Quiet | `speak-round.sh quiet quiet 56` | sent 3; mine ≥ 90 %; voiced 3 |
| Meeting playing | `speak-round.sh meeting meeting 56` | mine ≥ 80 %; `english_in_mine` 0 and no meeting content in the `me|` lines |
| Silent, meeting playing | `speak-round.sh sm silent 56` | sent 0 |
| Silent, quiet room | `speak-round.sh sq silent 0` | sent 0 (see below) |
| Room mic on | `MIC=on speak-round.sh mm meeting 56` | as meeting; `in_room_lines` 0 % |

What it found: with the plain mic (`VP=off`) the meeting's English came back from the speakers and Ming interpreted it as me — my sentences 50/27/23 %, the meeting sent back into itself, and a silent press sent the meeting back 3 of 3 times. Through echo cancellation: 86–100 %, none of the meeting. A silent press in a quiet room came back as 嗯 → "Hmm." until PressSpeech and the filler check.

## Open

- **Sounds that aren't speech.** In a quiet room a silent press with typing nearby went out as "The sound of typing on a computer keyboard." (Ming described the sound). The on-device recognizer can't vote it down: it heard 0 characters of a real sentence too.
- **Voice output stalls.** Now and then a sentence's voice to BlackHole stops until the next one's stall check rebuilds the output (`voice output stalled … rebuilt`): seen with echo cancellation on and off, once a sentence going out 8 s late. Count `voiced` against `sent`.
- **The ports** have no echo cancellation on the talk key: Windows (b155b46) and Linux drop a press the computer played through for more than half, so talking over the other side isn't sent there. Their silent-press and filler checks are unit-tested and, on Windows, checked in the VM with `cicadactl speak silence.wav` / `me-zh.wav`; real echo needs a real PC.
- **Not measured yet:** a real voice; AirPods as the talk mic (only that it no longer crashes); Windows and Linux (no audio in the VMs).
