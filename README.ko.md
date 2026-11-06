<p align="center">
  <img src="docs/icon.png" width="128" height="128" alt="Cicada 아이콘">
</p>

<h1 align="center">Cicada · 知了</h1>

<p align="center">
  어떤 회의도, 어떤 방송도 언어 장벽 없이.<br>
  알아듣고, 말하고, 기록합니다. Mac, Windows, Linux, Android에서 실시간 회의록, 이중 언어 기록, 자막, 동시통역을 제공합니다.
</p>

<p align="center">
  <a href="https://cicada.indaloop.app/ko/"><img src="https://img.shields.io/badge/%EC%9B%B9%EC%82%AC%EC%9D%B4%ED%8A%B8-cicada.indaloop.app-E8552B?style=for-the-badge" alt="웹사이트: cicada.indaloop.app" height="36"></a>
  &nbsp;
  <a href="https://cicada.indaloop.app/ko/download/"><img src="https://img.shields.io/badge/%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C-Mac%20·%20Windows%20·%20Linux%20·%20Android-15171C?style=for-the-badge" alt="Mac, Windows, Linux, Android 다운로드" height="36"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/macOS-14.4%2B-black" alt="macOS 14.4+">
  <img src="https://img.shields.io/badge/Windows-10%202004%2B-black" alt="Windows 10 2004+">
  <img src="https://img.shields.io/badge/Ubuntu-22.04%2B-black" alt="Ubuntu 22.04+">
  <img src="https://img.shields.io/badge/Android-10%2B-black" alt="Android 10+">
  <img src="https://img.shields.io/badge/%EB%9D%BC%EC%9D%B4%EC%84%A0%EC%8A%A4-Apache--2.0-blue" alt="Apache-2.0">
</p>

<p align="center"><a href="README.md">简体中文</a> · <a href="README.en.md">English</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a></p>

Zoom, Teams, Feishu 회의부터 X Spaces, Discord 스테이지, YouTube 라이브 방송까지 컴퓨터에서 재생되는 모든 소리에 작동합니다. 시스템 오디오를 직접 듣기 때문에 회의에 봇을 넣거나 다른 사람에게 설치를 부탁할 필요 없이 실시간 이중 언어 자막과 체계적인 회의록을 보여줍니다. 발언할 때는 말하기 키(Mac은 오른쪽 `⌥`, Windows는 오른쪽 `Ctrl`)를 누른 채 말하면 번역된 음성이 회의실로 바로 전달됩니다. Mac에서는 음성 인식이 기기 안에서 처리되어 오디오가 밖으로 나가지 않습니다.

<p align="center">
  <img src="docs/demo.gif" width="800" alt="YouTube에서 재생 중인 Bloomberg 영어 라이브 방송과 오른쪽의 Cicada 실시간 회의록, 안건, 피시본 다이어그램, 하단의 이중 언어 자막">
</p>

## 지원 플랫폼

| 플랫폼 | 요구 사항 | 비고 |
|---|---|---|
| Mac | macOS 14.4+, Apple silicon / Intel | 모든 기능 지원. Apple silicon은 기기 내 음성 인식(키 없이도 사용 가능), Intel 버전은 Ling 키 필요(Ming으로 음성 인식) |
| Windows | Windows 10 2004+, x64 / ARM64 | Ling 키 필요(쓸 수 없으면 OpenRouter, ZenMux 등도 가능). [windows/](windows/README.md) 참고 |
| Linux | Ubuntu 22.04 / 24.04 데스크톱 | Ling 또는 다른 AI 서비스 키 필요. 화면 공유 시 회의록 창이 보임. [linux/](linux/README.md) 참고 |
| Android | Android 10+ | Ling 또는 다른 AI 서비스 키 필요. 동영상·라이브 자막, 대면 통역. [android/](android/README.md) 참고 |

> **AI 서비스:** Mac에서는 회의록과 자연스러운 음성에 OpenRouter(추천), Ling, ZenMux, OpenAI를 쓸 수 있습니다([설정 방법](#ling-api-key)). Windows, Linux, Android 버전도 같은 서비스를 쓸 수 있으며, 이때는 상대방 음성 인식도 그 서비스가 맡아 자막이 Ling보다 1~2초 늦습니다.

네 플랫폼 모두 같은 버전 번호와 회의 기록 형식을 공유합니다. 설치 파일은 [웹사이트](https://cicada.indaloop.app/ko/download/)와 [Releases](https://github.com/wquguru/cicada/releases)에서 받을 수 있습니다. 아래 기능 설명은 Mac 앱 기준입니다.

## 주요 기능

### 실시간 회의록 및 이중 언어 기록

회의가 진행되는 동안 회의록 창에서 요약, 안건 및 요점, 결론, 할 일, 피시본 다이어그램, 인명·용어집을 실시간으로 정리합니다. 결론이나 할 일을 클릭하면 이중 언어 기록의 해당 발언으로 바로 이동합니다. 회의록 전체에서 인명과 용어 표기를 통일하고 잘못 인식된 표기도 기억하므로, `⌘F`로 검색하면 표준 표기와 오인식된 변형을 함께 찾아줍니다. AI 서비스에 내가 직접 고쳐야 하는 문제(키, 잔액, 모델)가 생기면 회의록 창이 알려 주고 메뉴 막대 아이콘에 주황색 점이 붙습니다. 마이크를 켰는데 마이크를 쓸 수 없을 때는 회의록 창, 자막 바, 메뉴 막대 아이콘 모두에서 알려 줍니다.

### 실시간 자막 및 언어 감지

상대방이 말하기 시작하면 몇 초 안에 기기에서 언어를 감지해 시스템 언어로 번역합니다. `⌃⌥S`를 누르면 회의록 창, 자막 바, 숨김 상태를 오갈 수 있습니다. 자막 바는 누군가 말할 때만 나타나며, 마우스 포인터를 올리면 투명해져 아래에 있는 버튼을 그대로 클릭할 수 있습니다.

### 오프라인 회의

회의실에 모여 회의할 때는 메뉴 막대 패널이나 회의록 창에서 **마이크 켜기**를 누르세요. Mac 마이크로 테이블에 있는 사람들의 말을 듣고 온라인 회의와 똑같이 자막, 회의록, 기록을 남깁니다. Mac 소리도 계속 듣고, 아무 소리도 나지 않으면 테이블의 말만 기록합니다. 동시통역이 번역을 읽어 주는 동안에는 마이크가 듣지 않아 번역이 다른 사람의 말로 기록되지 않습니다. 앱을 실행할 때마다 마이크는 꺼진 상태로 시작합니다.

회의실에 있는 사람과 온라인 참석자가 섞인 회의도 같은 버튼입니다. 온라인 참석자는 컴퓨터 소리로, 테이블의 사람은 마이크로 듣고, 각자의 언어로 하나의 회의 기록에 남깁니다(macOS 14와 15에서는 마이크가 Mac 소리를 대신합니다). 스피커에서 나온 온라인 목소리는 마이크에도 들어가므로, Cicada는 그 소리가 마이크에 닿는지 측정합니다. 닿으면 온라인 참석자가 말하는 동안만 마이크를 멈추고, 헤드폰이나 회의용 마이크를 쓰면 멈추지 않아 동시에 말해도 모두 남습니다. Mac에서 음악이 나올 때도 멈추지 않습니다. 마지막으로 글자를 비교해, Mac 소리에서 방금 나온 말과 거의 같은 회의실 줄은 두 번 기록하지 않습니다.

이런 회의에서는 줄마다 **현장**인지 **온라인**인지 표시됩니다. 회의 중에 외장 마이크가 빠지면 남은 마이크로 바꾸고 알려 줍니다. 마이크가 계속 조용하면 한 번 다시 열고, 그래도 안 되면 회의록 창에서 마이크를 바꾸라고 알려 줍니다. Windows와 Linux에도 같은 **마이크 켜기**와 같은 규칙이 있습니다.

### 상대방 언어로 말하기

오른쪽 `⌥` 키를 누른 채 말하면 번역된 음성이 가상 마이크인 BlackHole 2ch를 통해 회의 앱으로 전달됩니다. BlackHole 2ch는 앱에서 클릭 한 번으로 설치할 수 있으며, 동시통역을 켜면 Cicada가 자동으로 마이크를 전환합니다. AI 서비스 키를 설정하면 자연스러운 음성(OpenRouter나 ZenMux의 Gemini, Ling의 Ming)을 쓸 수 있고, Ling에서는 8~30초 분량의 녹음으로 내 목소리를 복제할 수도 있습니다. 키가 없어도 macOS 기본 음성을 사용할 수 있습니다.

<p align="center">
  <img src="docs/interpreting.png" width="640" alt="오른쪽 Option 말하기 키, 대상 언어, Ming 음성 미리 듣기, macOS 음성이 표시된 동시통역 설정 화면">
</p>

### 회의 기록

모든 회의의 이중 언어 기록, 회의록, 원본 녹음은 Mac에 저장됩니다. 회의가 끝나면 기록에서 녹음을 다시 들을 수 있고, 시간을 클릭하면 그 문장부터 재생되며 재생 중인 문장이 강조됩니다. 목소리로 상대방 화자를 구분하고 Ling 키가 있으면 이름도 채워 넣습니다. 잘못 구분된 화자는 실시간 회의록 창에서 바로 이름을 바꾸거나 합치거나 다른 사람의 발언으로 바꿀 수 있습니다. 통화가 끝나거나 10분 동안 침묵이 이어지면 자동으로 회의를 마치고 뒷부분의 무음을 잘라냅니다. 회의가 끝난 뒤 언제든 회의록을 다시 생성하거나 Markdown, Word, SRT 자막으로 내보낼 수 있습니다. 기존 녹음이나 동영상 파일을 회의 기록 창에 끌어다 놓으면(또는 **파일 › 녹음 또는 동영상 가져오기…** 사용) Mac에서 실시간보다 훨씬 빠르게 이중 언어 기록으로 받아씁니다. 시간을 클릭하면 원본 파일의 해당 위치부터 재생됩니다. 당시 언어를 인식하지 못한 회의도 녹음은 남으므로, 언어를 선택하고 **다시 받아쓰기**를 누르면 됩니다. 현재 기록에 남는 내 발언은 말하기 키를 누르고 말한 내용뿐이며, 회의에서 그냥 말한 내용을 기록하는 기능은 [로드맵](#로드맵)에 있습니다.

<p align="center">
  <img src="docs/records.png" width="640" alt="구분된 화자 이름과 문장별 영중 이중 언어 기록이 표시된 회의 기록 창">
</p>

## 개인정보 보호 및 권한

Mac에서는 오디오 캡처, 언어 감지, 음성 인식(Apple SpeechAnalyzer, macOS 14.4–15에서는 SFSpeechRecognizer 기기 내 모드), 회의 녹음이 모두 컴퓨터 안에서 이루어집니다. 기기 밖으로 나가는 데이터는 번역과 회의록 생성을 위해 전송되는 인식된 텍스트와, Ling API 키를 쓴 채 말하기 키를 누르고 말한 짧은 음성뿐입니다. 음성 모델 다운로드가 느릴 때 "먼저 Ling 사용하기"를 고르면 모델이 설치될 때까지 회의 음성도 Ling이 인식합니다. "설정 › AI 서비스"에서 음성 인식을 "내 서비스"로 바꾸면 회의 음성이 그 머신으로 전송됩니다. API 키가 없어도 자막, 번역(Google 번역 사용, macOS 26에서는 실패 시 Apple 기기 내 번역으로 전환), 회의 기록, 동시통역 모두 작동합니다. 실시간 회의록에는 사용자의 AI 서비스 키가 필요합니다. OpenRouter(추천)나 Ling(Ant Group의 모델 서비스)을 쓸 수 있습니다([아래 설명](#ling-api-key) 참고). 원스텝 음성 번역과 목소리 복제는 Ling에서만 지원됩니다. Ling을 쓰면 1시간 회의 기준 현재 요금으로 약 0.15~1위안이 들며, Ling에서 매달 제공하는 무료 크레딧 10위안으로 약 10~50시간 동안 회의할 수 있습니다.

Windows, Linux, Android 버전은 클라우드에서 음성을 인식합니다. 말소리를 짧게 나누어 Ling의 Ming(또는 바꾼 OpenRouter, ZenMux 등의 서비스)으로 보내므로 AI 서비스 키가 꼭 필요합니다. 녹음과 회의 기록은 이 플랫폼들에서도 기기에만 저장됩니다.

아래는 Mac 앱 기준 설명입니다. Cicada는 해당 기능을 실제로 쓸 때만 권한을 요청하며, 거부하더라도 나머지 기능은 그대로 쓸 수 있습니다.

| 권한 | 용도 | 요청 시점 | 허용하지 않을 경우 |
|---|---|---|---|
| 시스템 오디오 녹음(화면 및 시스템 오디오 녹음) | Mac에서 재생되는 소리를 듣고 자막 생성. 화면이나 Cicada 자체 소리는 녹음하지 않음 | 초기 안내 1단계 또는 처음 듣기를 시작할 때 | 자막과 회의록 사용 불가 |
| 마이크 | 말하기 키를 누르고 말할 때 동시통역용 녹음, **마이크 켜기**를 눌렀을 때 주변 소리 듣기 | 동시통역을 켜거나 처음 마이크를 켤 때 | 말하기 통역 및 회의실 듣기 불가 |
| 입력 모니터링 | 오른쪽 `⌥` 키가 단독으로 눌렸는지 확인(감지만 하며 다른 키 입력을 막거나 기록하지 않음) | 오른쪽 `⌥` 키로 처음 말할 때 | 설정에서 `⌃`/`⌘` 조합 키로 바꾸면 이 권한 없이 사용 가능 |
| 관리자 암호 | 가상 마이크 BlackHole 2ch 설치 및 시스템 오디오 서비스 재시작 | 초기 안내나 설정에서 설치를 누를 때 한 번 | 상대방에게 번역 음성을 들려줄 수 없음, 다른 기능은 정상 작동 |

- **네트워크 및 가상 마이크**. Cicada는 Google 번역(`translate.googleapis.com`), 키 설정 시 Ling / Ming(`api.ant-ling.com`) 또는 선택한 다른 AI 서비스, BlackHole 공식 다운로드, 그리고 하루 한 번 GitHub 업데이트 확인에만 연결합니다. BlackHole은 Apple 공증을 받은 공식 패키지를 내려받으며, 설치 전에 코드에 고정된 SHA-256 체크섬을 대조합니다.
- **자체 분석 도구나 서버 없음**. 사용 통계 수집, 추적, 자체 백엔드 서버가 전혀 없습니다. 진단 기능은 소요 시간과 횟수만 기기의 회의 폴더에 기록합니다.
- **로컬 저장소**. 회의 기록, 녹음, 회의록은 `~/Library/Application Support/LiveSubs`에 저장됩니다. Ling 키와 목소리 샘플은 현재 사용자 계정만 읽을 수 있고, Time Machine 백업에서 제외되며, 로그나 내보낸 파일에 절대 기록되지 않습니다.
- **화면 공유 시 숨겨지는 회의록 창**. 시연 영상을 찍기 위해 화면 공유 시 표시 옵션을 켜지 않는 한, 화면 공유, 화면 기록, 스크린샷에 찍히지 않습니다.

## 사용 모델

키가 없으면 Apple 기기 내 모델과 Google 번역만으로 작동합니다. Ling 키를 입력하면 아래 작업을 Ling과 Ming 모델이 처리하고, 요청이 실패하면 자동으로 대체 수단으로 넘어갑니다. OpenRouter, ZenMux, OpenAI를 쓰면 번역과 회의록은 해당 서비스에서 고른 모델이 Ling을 대신하고, 동시통역 시 내 말은 Mac에서 직접 인식합니다. 말하는 중인 문장은 항상 Google 번역을 사용합니다. 내 서비스(기타(OpenAI 호환))를 쓸 때는 "설정 › AI 서비스"에서 "음성과 텍스트를 내 서비스로만 전송"을 켜면 음성과 텍스트 모두 Google을 거치지 않습니다.

| 기능 | Ling 키 사용 시 | 키 없음 / 대체 작동 시 |
|---|---|---|
| 음성 인식 및 언어 감지 | Apple `SpeechAnalyzer` / `SpeechTranscriber`(기기 내), macOS 14.4–15: `SFSpeechRecognizer`(기기 내, 받아쓰기 켜야 함) | 왼쪽과 같음 |
| 끝난 문장 번역 | Ling `Ling-3.1-flash`(또는 **설정 › AI 서비스**에서 `Ling-3.0-flash`로 변경 가능) | Google 번역 → Apple `Translation`(기기 내, macOS 26 전용) |
| 말하는 중인 문장 번역 | Google 번역(Ling 호출 한도 절약, 내 서비스를 쓸 때는 끌 수 있음) | 없음: 문장이 끝나 번역될 때까지 원문 표시. Google에 연결되지 않으면 1분 일시중지 |
| 실시간 회의록 및 최종본 | Ling `Ling-3.1-flash`(위 설정과 같음) | 사용 불가 |
| 키 유효성 확인 | Ling `Ling-3.0-tiny`(1토큰 사용) | — |
| 동시통역: 내 말 인식 및 번역 | Ming `Ming-3.0-audio-flash`, 원스텝 처리 | Apple 기기 내 음성 인식 후 위 번역 순서대로 처리 |
| 동시통역: 상대방이 듣는 음성, 목소리 복제 | Ming `Ming-3.0-tts-0.5B` | macOS 시스템 음성(`AVSpeechSynthesizer`), 복제 불가 |
| 화자 구분(说话人识别, 기본 켜짐) | 앱에 포함된 WeSpeaker ResNet34-LM 성문 모델, 기기 내 실행(Core ML) | 왼쪽과 같음 |

<a id="ling-api-key"></a>
## AI 서비스 키 설정

어느 서비스든 괜찮습니다. 가입할 수 있는 쪽을 고르세요. **OpenRouter**(추천)는 같은 Ling 텍스트 모델과 자연스러운 Gemini 음성을 모두 제공합니다.

1. [OpenRouter](https://openrouter.ai/settings/keys)에서 키를 만듭니다.
2. Cicada에서 **설정 › AI 서비스**를 열고 오른쪽 위 메뉴에서 **OpenRouter**를 고른 뒤, 키를 붙여넣고 **저장 및 확인**을 클릭합니다(초기 안내 화면에서는 **Ling을 사용할 수 없나요?** 클릭).
3. 품질과 가격을 고려한 기본 모델이 이미 선택되어 있으며, 같은 화면에서 원하는 모델로 바꿀 수 있습니다.

같은 메뉴에서 ZenMux, OpenAI 또는 OpenAI 호환 서비스 주소(예: Mac에서 로컬로 실행 중인 모델)도 똑같은 방식으로 쓸 수 있으며, ZenMux 역시 Gemini 음성을 지원합니다. 실시간 회의록과 문장 번역은 모든 서비스에서 작동합니다. 원스텝 음성 번역과 목소리 복제는 Ling 전용이며, 다른 서비스에서는 Apple 실리콘 Mac이 먼저 음성을 인식한 뒤 번역합니다(Intel 버전은 듣기와 통역 모두 Ling이 필요합니다). 서비스마다 키가 따로 저장되므로 다시 입력할 필요 없이 전환할 수 있습니다. 직접 운영하는 모델(Ollama, vLLM, SGLang 등)은 기능별로 설정합니다. 번역과 회의록, 통역 음성, 음성 인식을 각각 다른 컴퓨터에 둘 수 있고, 로컬 네트워크 주소는 http도 쓸 수 있습니다. 확인할 때 실제 문장 하나를 번역해 보고, 모델이 먼저 생각하거나 너무 느리면 그대로 알려 줍니다(Qwen3 같은 모델에는 생각하지 말라고 요청합니다). Mac의 음성 인식은 내 Qwen3-ASR, Whisper 등에 맡길 수도 있습니다(기본은 Mac이며, 연결되지 않으면 자동으로 돌아옵니다). Windows, Linux, Android에서는 듣기 모델에 별도 주소를 넣을 수 있습니다. 서비스에 연결할 수 없거나 키·모델에 문제가 있으면 설정에서 어느 단계가 막혔는지와 해결 방법을 차례로 보여 줍니다. 프록시가 꺼져 있는지, 프록시 앱이 시스템 프록시로 설정되지 않았는지, 프록시를 켜도 연결되지 않는지까지 구분합니다(Cicada는 프록시 설정을 직접 바꾸지 않습니다. [설정 페이지](https://cicada.indaloop.app/ko/start/#proxy) 참고). OpenRouter에서는 잔액이 거의 떨어지기 전에 미리 알려 줍니다.

**Ling**(Ant Group의 모델 서비스)은 내 목소리를 포함한 모든 기능을 쓸 수 있고, 매달 ¥10 크레딧을 제공합니다:

1. [Ling 오픈 플랫폼](https://chat.ant-ling.com/platform/api)에서 가입하거나 로그인합니다.
2. **创建令牌**(토큰 생성)을 클릭하고 `sk-`로 시작하는 키를 복사합니다.
3. Cicada에서 **설정 › AI 서비스**를 열고 키를 붙여넣은 뒤 **저장 및 확인**을 클릭합니다(또는 회의록 창 상단 입력란에 바로 붙여넣기). 1토큰짜리 요청을 보내 키가 작동하는지 확인합니다.
4. 필요한 경우 같은 화면에서 모델(기본값 `Ling-3.1-flash`)을 고르고, **설정 › 동시통역**에서 언어별 Ming 음성을 선택합니다. 키를 지우려면 같은 화면에서 **제거**를 클릭하세요.

## 시스템 요구 사항 및 설치

### Mac

**Apple silicon 또는 Intel**이 탑재된 Mac과 **macOS 14.4 이상**이 필요합니다. Apple silicon Mac의 경우 macOS 26에서는 더 정확한 최신 기기 내 음성 인식을 사용하며, 14.4–15에서는 이전 시스템 음성 인식을 쓰므로 **시스템 설정 › 키보드**에서 **받아쓰기**를 켜고 인식할 언어를 받아쓰기 언어에 추가해야 합니다. Intel 버전 Mac에서는 클라우드 Ming 모델로 음성을 인식하므로 Ling 키가 필요합니다. 인터페이스는 한국어, 영어, 중국어, 일본어를 지원하며, macOS 기본 언어를 따르거나 **시스템 설정 › 일반 › 언어 및 지역**에서 앱별로 지정할 수 있습니다.

[Releases](https://github.com/wquguru/cicada/releases/latest)나 [웹사이트](https://cicada.indaloop.app/ko/)에서 `Cicada-<version>-macOS-AppleSilicon.dmg`(Apple silicon) 또는 `Cicada-<version>-macOS-Intel.dmg`(Intel)를 내려받아 열고 **Cicada**를 **응용 프로그램**으로 끌어다 놓으세요. 현재 빌드는 로컬 서명만 되어 있고 아직 Apple 공증을 받지 않았으므로([로드맵](#로드맵) 참고), 처음 실행할 때 macOS가 차단하면 **시스템 설정 › 개인정보 보호 및 보안**을 열고 **확인 없이 열기**를 클릭하세요. 릴리스마다 `checksums.txt`가 함께 제공되며 `shasum -a 256 Cicada-*.dmg` 명령으로 검증할 수 있습니다. 궁금한 점은 X에서 개발자 [@wquguru](https://x.com/wquguru)에게 문의해 주세요.

처음 실행하면 안내에 따라 권한 하나를 허용하고, 짧은 2인 샘플 회의를 재생해 실시간 자막을 바로 확인한 뒤, AI 서비스 키를 연결(건너뛰기 가능)하고, 동시통역을 쓸 경우 가상 마이크를 설치합니다. 이후 새 버전이 나오면 메뉴 막대 아이콘에 주황색 점이 표시되며, 클릭 한 번으로 기존 권한을 유지한 채 업데이트됩니다.

<p align="center">
  <img src="docs/onboarding.png" width="640" alt="2인 샘플 회의를 재생하며 실시간 이중 언어 자막을 보여주는 초기 안내 2단계">
</p>

### Windows

**Windows 10 2004** 이상이 필요합니다. Windows 설치 파일(대부분의 PC는 x64, Snapdragon 노트북은 ARM64)를 내려받아 더블 클릭하면 관리자 권한 없이 바로 설치됩니다. 설치 파일에 아직 코드 서명이 없으므로 SmartScreen이 실행을 막으면 **추가 정보 › 실행**을 클릭하세요. 앱을 열면 메인 창에 남은 설정 단계(Ling 키 연결, 테스트 소리 재생, 샘플 회의 보기)가 표시됩니다. 동시통역에는 무료 가상 마이크인 VB-Cable이 필요하며 안내에 따라 설치할 수 있습니다. 새 버전이 나오면 앱 안에서 알려주며 클릭 한 번으로 업데이트됩니다.

### Linux

**Ubuntu 22.04 또는 24.04 데스크톱**(x86_64 또는 arm64)이 필요합니다. `Cicada-<version>-Linux.tar.gz`를 내려받고 터미널에서 `tar xzf Cicada-<version>-Linux.tar.gz && cicada-linux/install.sh`를 실행하면 앱 메뉴에 Cicada가 나타납니다. 동시통역은 별도 드라이버 설치 없이 자체적으로 "Cicada 마이크"를 만듭니다. Linux에서는 화면 공유 시 특정 창을 숨길 수 없으므로, 회의록 창에 화면 공유 시 보인다는 안내가 항상 표시됩니다. 회의 녹음에는 AAC 인코더가 필요한데 Ubuntu에는 기본으로 없습니다. 서드파티 미디어 형식(예: `ubuntu-restricted-extras`)을 설치하면 "설정 › 일반 › 회의 녹음 저장"을 켤 수 있고, 녹음은 회의 기록에서 각 문장의 시간부터 다시 들을 수 있습니다. 설치하지 않으면 이 스위치는 회색으로 표시되며 다른 기능은 그대로 쓸 수 있습니다.

### Android

**Android 10** 이상이 필요합니다. 휴대폰에서 `Cicada-<version>-Android.apk`를 내려받아 열고 안내에 따라 알 수 없는 앱 설치를 허용하세요. Android 15 이상에서는 플로팅 자막을 처음 켤 때 앱 정보에서 제한된 설정 허용이 먼저 필요합니다. 전화나 회의 앱의 소리는 시스템이 다른 앱에서 녹음하지 못하게 막으므로, 스피커폰을 켜고 **대면** 모드로 전환해 사용하세요.

모든 플랫폼의 설치 파일은 Releases 페이지의 `checksums.txt`로 SHA-256을 검증할 수 있습니다.

## 로드맵

대략적인 우선순위 순이며, 필요한 기능은 Issues에 남겨 주세요.

- **내 발언 기록**: 회의 중 반향을 제거하며 마이크를 계속 들어, 내가 직접 말한 제안이나 할 일도 기록과 회의록에 포함.
- **Developer ID 서명 및 공증**: 첫 실행 시 "확인 없이 열기"를 누를 필요가 없도록 하고 AI 키를 macOS 키체인에 보관. Windows 설치 프로그램에도 코드 서명 추가.
- **화자 인식**: 현재의 화자 구분 기능을 발전시켜 자주 함께 회의하는 사람의 목소리를 Mac에 기억하고 다음 회의에서도 자동으로 이름을 표시.
- **API 키 없는 로컬 회의록**: 지원되는 Mac에서 Apple 기기 내 모델로 회의록 작성.
- **Android 앱 스토어 출시**: 브라우저에서 APK를 받지 않고 바로 설치.
- **iPhone 및 iPad**: iOS는 다른 앱의 오디오를 캡처할 수 없으므로 회의실 듣기, 대면 통역, 회의 기록부터 지원.

각 항목의 자세한 내용과 기술적 고려 사항은 [docs/ROADMAP.md](docs/ROADMAP.md)에서 볼 수 있습니다.

## 제거

Cicada를 종료하고 **응용 프로그램** 폴더에서 휴지통으로 끌어다 놓으세요. 저장된 모든 기록, 회의록, 오디오 녹음을 지우려면 `~/Library/Application Support/LiveSubs` 폴더를 삭제하면 됩니다. 환경설정을 초기화하려면 다음 명령을 실행하세요.

```bash
defaults delete com.wquguru.cicada
```

## 개발

소스에서 Mac 앱을 빌드하려면 Xcode Command Line Tools(`xcode-select --install`)만 있으면 됩니다. Cicada는 외부 라이브러리 의존성 없이 macOS 시스템 프레임워크만으로 빌드됩니다. macOS 27에서 `SwiftUIMacros`가 없다며 빌드에 실패하면 해당 Command Line Tools 버전에 SwiftUI 매크로 플러그인이 빠진 것이므로, 전체 Xcode를 설치하고 `sudo xcode-select -s /Applications/Xcode.app`을 실행하세요. Windows, Linux, Android 빌드 방법은 [windows/README.md](windows/README.md), [linux/README.md](linux/README.md), [android/README.md](android/README.md)를 참고하세요.

```bash
scripts/build.sh            # 개발 빌드 → build/Cicada.app ("Cicada Dev", 설치된 정식 버전과 동시에 실행 가능)
open build/Cicada.app
scripts/package.sh          # 릴리스용 DMG + zip + 체크섬 패키징
```

아키텍처와 릴리스 과정은 [AGENTS.md](AGENTS.md)에 정리되어 있습니다. 웹사이트 소스는 `site/`에 있으며 `scripts/site.py`로 생성합니다. 변경 내역은 [CHANGELOG.md](CHANGELOG.md)와 웹사이트의 [cicada.indaloop.app/ko/changelog](https://cicada.indaloop.app/ko/changelog/)에서 확인할 수 있습니다.

## 라이선스

[Apache-2.0](LICENSE) 라이선스를 따릅니다. BlackHole 2ch 가상 오디오 드라이버는 GPL 라이선스이며, Cicada에 포함되지 않고 사용자가 설치를 선택할 때 공식 릴리스에서 직접 내려받습니다. 앱에 포함된 성문 모델은 [WeSpeaker](https://github.com/wenet-e2e/wespeaker)가 VoxCeleb으로 학습한 ResNet34-LM(CC BY 4.0 라이선스)을 `scripts/convert-voiceprint.py`로 Core ML 형식으로 변환한 것입니다.
