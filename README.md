<p align="center">
  <img src="docs/icon.png" width="128" height="128" alt="知了图标">
</p>

<h1 align="center">知了 · Cicada</h1>

<p align="center">
  任何会议、任何直播，没有语言障碍。<br>
  听得懂，说得出，记得住。Mac、Windows、Linux 和 Android 上的实时纪要、双语文字记录、字幕与同声传译。
</p>

<p align="center">
  <a href="https://cicada.indaloop.app"><img src="https://img.shields.io/badge/官网-cicada.indaloop.app-E8552B?style=for-the-badge" alt="官网 cicada.indaloop.app" height="36"></a>
  &nbsp;
  <a href="https://cicada.indaloop.app/download/"><img src="https://img.shields.io/badge/下载-Mac%20·%20Windows%20·%20Linux%20·%20Android-15171C?style=for-the-badge" alt="下载 Mac、Windows、Linux、Android 版" height="36"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/macOS-14.4%2B-black" alt="macOS 14.4+">
  <img src="https://img.shields.io/badge/Windows-10%202004%2B-black" alt="Windows 10 2004+">
  <img src="https://img.shields.io/badge/Ubuntu-22.04%2B-black" alt="Ubuntu 22.04+">
  <img src="https://img.shields.io/badge/Android-10%2B-black" alt="Android 10+">
  <img src="https://img.shields.io/badge/license-Apache--2.0-blue" alt="Apache-2.0">
</p>

<p align="center"><a href="README.md">简体中文</a> · <a href="README.en.md">English</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a></p>

无论是用 Zoom、飞书、腾讯会议开会，还是听 X Spaces 和 YouTube 直播，知了都能实时给出双语字幕、边听边写结构化纪要。遇到需要发言的时候，按住说话键（Mac 上是右 `⌥`，Windows 上是右 `Ctrl`）开口，对方就能在会里直接听到翻译好的语音。知了直接读取系统声音，不用往会里塞机器人，对方完全无感；在 Apple 芯片的 Mac 上还全部在本机识别，声音不出电脑。

<p align="center">
  <img src="docs/demo.gif" width="800" alt="YouTube 播着 Bloomberg 英文直播，右边是知了实时整理的中文纪要、议题与鱼骨图，底部是双语字幕">
</p>

## 平台

| 平台 | 系统要求 | 说明 |
|---|---|---|
| Mac | macOS 14.4+，Apple 芯片 / Intel | 功能最全；Apple 芯片本机识别（不填 key 也能用），Intel 版需要 Ling key（识别走 Ming） |
| Windows | Windows 10 2004+，x64 / ARM64 | 需要 Ling key（用不了 Ling 时可换 OpenRouter、ZenMux 等）；见 [windows/](windows/README.md) |
| Linux | Ubuntu 22.04 / 24.04 桌面版 | 需要 Ling 或其他 AI 服务的 key；纪要窗会被屏幕共享看到；见 [linux/](linux/README.md) |
| Android | Android 10+ | 需要 Ling 或其他 AI 服务的 key；视频与直播字幕、面对面互译；见 [android/](android/README.md) |

四个平台共用一个版本号和同一种会议记录格式，安装包都在 [官网下载页](https://cicada.indaloop.app/download/) 和 [Releases](https://github.com/wquguru/cicada/releases)。下面的功能说明以 Mac 版为准。

## 主要功能

### 实时纪要与双语文字记录

开会时纪要窗口边听边整理总结、议题要点、结论、待办、鱼骨图和人名术语表，点一下结论或待办就能跳回双语文字记录里的原话。纪要会统一文中人名和术语的写法并记下听错的变体，按 `⌘F` 搜索时能连同识别错的写法一起搜出来。AI 服务出了只有你能修的问题（key、余额、模型）时，纪要窗口会说明，菜单栏图标多一个橙点；打开了麦克风却没拿到麦克风权限时，纪要窗口、字幕条和菜单栏图标都会提示。

### 实时字幕与语言识别

对方开口几秒钟就能在本地自动认出语言并翻成你的系统语言，按 `⌃⌥S` 可以在纪要窗口、字幕条和不显示之间切换。字幕条只在有人说话时出现，鼠标划过时自动变透明，不会挡住底下的按钮。

### 线下会议

在会议室里开会时，点菜单栏面板或纪要窗口里的“打开麦克风”，知了就用 Mac 的麦克风听桌边的人说话，字幕、纪要和会议记录跟线上会议一样；电脑里的声音照常在听，电脑没声音时就只记桌边的人。同声传译念译文的时候麦克风暂时不听，不会把译文再记成别人的话。每次启动麦克风都是关着的。

有人在会议室、有人在线上时也是这一个按钮：线上的人从电脑声音听，桌边的人从麦克风听，两边各认各的语言，记在同一份会议记录里（macOS 14 和 15 上打开麦克风改为只听桌边）。扬声器放出来的线上声音会被麦克风再听到一遍，知了会测出扬声器的声音有没有传到麦克风：传到了，线上有人说话的那一会儿桌边先不听；戴耳机或用会议麦克风时不用避让，两边同时说话也都能记下；电脑在放音乐时也不避让。最后还会比一遍文字，跟电脑声音里刚说过的话几乎一样的那句不再记第二遍。

这样的会议里，每句话都标着是“现场”还是“线上”。外接麦克风中途被拔掉，知了改用剩下的麦克风并说一声；麦克风开着却一直没有声音，会先重开一次，还不行就在纪要窗口提示换一个。Windows 和 Linux 上也是同一个“打开麦克风”和同样的规则。

### 同声传译

按住键盘右边的 `⌥` 键说话，对方在会议软件里就能直接听到翻译后的语音，打开同声传译时知了会自动把系统麦克风切到一键安装的虚拟驱动 BlackHole 2ch。填了 Ling API key 后可以用自然人声或用 8 到 30 秒录音克隆你自己的声音，不填也能用 Mac 自带语音。

<p align="center">
  <img src="docs/interpreting.png" width="640" alt="同声传译设置页，包含按住右 Option 键说话、目标语言、Ming 声音试听与本机声音选择">
</p>

### 会议记录

每场会议的双语文字记录、纪要和原始录音都保存在本机，会后在会议记录里就能回放录音，点一句的时间就从那里放，正在放的那句会亮起；还能按声音区分对方不同的说话人并在有 Ling key 时填上名字，认错了在实时纪要窗口里就能改名、合并或把某段话改给别人。会议软件挂断或 10 分钟没人说话时会自动结束并截掉空白，会后随时可以补生成纪要，或导出成 Markdown、Word 和 SRT 字幕。已有的录音或视频也能拖进会议记录窗口（或用“文件 › 导入录音或视频…”），在本机比实时快得多地转成一场双语记录，点时间就从那一句开始播放原文件。当时没听出是哪种语言的会议也会留下录音，选好语言就能重新转写。目前记录里的你只包含按住说话键说的话，会上直接开口的部分见[路线图](#路线图)。

<p align="center">
  <img src="docs/records.png" width="640" alt="会议记录窗口，显示识别出的说话人名字和逐句英中双语文字记录">
</p>

## 隐私与权限

在 Apple 芯片的 Mac 上，声音采集、语言识别、语音识别（Apple SpeechAnalyzer，macOS 14.4–15 上是 SFSpeechRecognizer 的本机模式）和会议录音全部在本机完成。会离开电脑的只有识别出来的文字（发去做翻译和生成纪要），以及填了 Ling API key 并按住说话键用同声传译时你说的那几句语音；语音模型下载太慢时如果你点了“先用 Ling 听”，模型装好之前的会议声音也会交给 Ling 识别；在“设置 › AI 服务”里把语音识别改成自建服务时，会议声音会发到你那台机器。不填 API key 时，实时字幕、翻译（走 Google 或退回 Apple 本机翻译，本机翻译只在 macOS 26 上有）、会议记录和同声传译都能正常用。实时纪要、一步语音翻译和声音克隆需要你自己的 Ling（蚂蚁集团的大模型服务）API key（配置方法见[下文](#配置-ling-api-key)），开一小时会大约花 0.15 到 1 元人民币，Ling 每月赠送 10 元额度，约够 10 到 50 小时会议。

Intel 版 Mac 以及 Windows、Linux 和 Android 版在云端识别：说话的声音分段发给 Ling 的 Ming（Windows、Linux、Android 也可换成 OpenRouter、ZenMux 等服务），所以必须填 AI 服务的 key；录音和会议记录同样只存在本机。

下面说的是 Mac 版。知了只在用到某项功能时才请求对应的权限，拒绝后其他功能照常可用。

| 权限 | 用来做什么 | 什么时候问 | 不给的话 |
|---|---|---|---|
| 录制系统声音（屏幕与系统录音） | 听 Mac 正在播放的声音来出字幕，不录屏幕，也不听知了自己的声音 | 新手引导第一步，或第一次开始听 | 字幕和纪要都用不了 |
| 麦克风 | 按住说话键时录你说的话做同声传译；点了“打开麦克风”时听屋里的人 | 打开同声传译或第一次打开麦克风时 | 不能说话翻译，也不能听会议室 |
| 输入监控 | 只用来判断右 `⌥` 是否被单独按下（只监听、不拦截、不记录别的按键） | 第一次用右 `⌥` 说话时 | 在设置里改成 `⌃`/`⌘` 组合键，就不需要这个权限 |
| 管理员密码 | 安装虚拟麦克风 BlackHole 2ch，并重启系统音频服务 | 在引导或设置里点“安装”时，只问一次 | 不能让对方听到翻译，其余照常 |

- **联网与虚拟麦克风**。只有翻译（`translate.googleapis.com`）、填了 key 后的 Ling / Ming（`api.ant-ling.com`）或你选的其他 AI 服务、下载 BlackHole 驱动和每天去 GitHub 检查一次新版本会联网。BlackHole 从官方下载已经过苹果公证的安装包，安装前会核对代码里写死的 SHA-256。
- **没有统计和自建服务器**。应用没有统计、没有埋点，也没有我们自己的服务器，诊断功能只把耗时和次数记在本机会议文件夹里。
- **本机数据位置**。会议记录、录音和纪要存在 `~/Library/Application Support/LiveSubs`。Ling key 和你录的声音样本只对当前系统账户可读，不进 Time Machine 备份，也不写进日志和导出文件。
- **共享屏幕看不到纪要窗口**。屏幕共享、录屏和截图都拍不到它，要录演示时可以打开“共享屏幕时让对方看到”。

## 用到的模型

不填 Ling key 时全部由 Apple 本机模型加 Google 翻译完成，填了 key 后由 Ling 和 Ming 模型负责并支持失败自动退回。正在说的半句话一直用 Google 翻译；用自己的服务（“其他（兼容 OpenAI）”）时，可以在“设置 › AI 服务”打开“语音和文字只发给你的服务”，语音和文字就都不经过 Google。

| 功能 | 填了 Ling key | 不填 key / 退回 |
|---|---|---|
| 语音识别、语言识别 | Apple `SpeechAnalyzer` / `SpeechTranscriber`（本机）；macOS 14.4–15 是 `SFSpeechRecognizer`（本机，要打开听写） | 同左 |
| 整句翻译 | Ling `Ling-3.1-flash`（可在“设置 › AI 服务”改为 `Ling-3.0-flash`） | Google 翻译 → Apple `Translation`（本机，仅 macOS 26） |
| 正在说的半句话的翻译 | Google 翻译（不占 Ling 的频率额度；用自己的服务时可以关掉） | 无：只显示原文，说完一句换成整句翻译；连不上时暂停一分钟再试 |
| 实时纪要、会后完整版 | Ling `Ling-3.1-flash`（同上设置） | 不可用 |
| 检查 key 是否有效 | Ling `Ling-3.0-tiny`（只用一个 token） | — |
| 同声传译：听懂并翻译你说的话 | Ming `Ming-3.0-audio-flash`，一步完成 | Apple 本机识别，再走上面的翻译链 |
| 同声传译：对方听到的声音、声音克隆 | Ming `Ming-3.0-tts-0.5B` | Mac 自带语音（`AVSpeechSynthesizer`），不能克隆 |
| 说话人识别（默认打开） | WeSpeaker ResNet34-LM 声纹模型，随 app 附带，本机运行（Core ML） | 同左 |

## 配置 Ling API key

1. 打开 [Ling 开放平台](https://chat.ant-ling.com/platform/api)，注册或登录。
2. 点创建令牌，复制以 `sk-` 开头的那串 key。
3. 在知了里打开设置里的 AI 服务，粘贴后点保存并检查，也可以直接粘贴到纪要窗口顶部的提示框里。知了会发一个只用一个 token 的请求确认 key 可用。
4. 同一页面可以选模型（默认 `Ling-3.1-flash`），每种语言用哪个 Ming 声音在同声传译设置里选。想移除 key，在同一页面点移除即可。

**注册不了 Ling？**可以在“设置 › AI 服务”右上角换成 OpenRouter、ZenMux、OpenAI，或填任何 OpenAI 兼容服务的地址（比如本机跑的模型）。实时纪要和整句翻译都能用，模型已经按效果和价格选好，也可以自己换；OpenRouter 和 ZenMux 还能用 Gemini 的自然人声做同传。一步语音翻译和声音克隆只有 Ling 有，其他服务下，Apple 芯片的 Mac 同传先在本机识别再翻译（Intel 版听和说都要 Ling）。每个服务的 key 各存一份，切换时不用重填。自己部署的模型（Ollama、vLLM、SGLang 等）按功能分开填：翻译和纪要、同传声音、语音识别各自可以接不同的机器，局域网里的地址也能用 http；检查时会真翻一句，模型先思考或太慢都会直说（Qwen3 这类模型知了会请它别思考）。Mac 的语音识别可以改交给你的 Qwen3-ASR、Whisper 等（默认仍在本机，连不上时自动换回）；Windows、Linux、Android 上“听对方”的模型也可以填单独的地址。Windows、Linux、Android 版也能换：在引导里点“用不了 Ling？”或在设置 › AI 服务里选，听对方也交给这家服务，字幕比 Ling 晚 1–2 秒。连不上或 key、模型有问题时，设置里会一步步说清坏在哪、怎么修：是没开代理、代理软件没接管系统代理，还是开了代理也不通（知了不会自己改代理，说明见网站的[设置页](https://cicada.indaloop.app/start/#proxy)）；用 OpenRouter 时余额快用完会提前提醒。

## 系统要求与安装

### Mac

需要 macOS 14.4 或更新版本（支持 Apple 芯片与 Intel）。Apple 芯片 Mac 在 macOS 26 上用新的本机语音识别，更准；14.4–15 上用系统较早的识别，要在系统设置 › 键盘里打开“听写”，并把要听的语言加进听写语言；Intel 版 Mac 则通过云端 Ming 模型识别语音，需要配置 Ling key。界面有中文、英文、日文和韩文，默认跟随系统语言，也可以在系统设置的语言与地区里单独给知了指定。

从 [Releases 页面](https://github.com/wquguru/cicada/releases/latest) 或 [官网](https://cicada.indaloop.app) 下载 `Cicada-<版本>-macOS-AppleSilicon.dmg`（Apple 芯片）或 `Cicada-<版本>-macOS-Intel.dmg`（Intel），打开后把知了拖进应用程序文件夹。应用目前是本地签名，还没有苹果公证（见[路线图](#路线图)），第一次打开被拦下时，去系统设置的隐私与安全性里点仍要打开。下载页同时提供 `checksums.txt`，可以用 `shasum -a 256 Cicada-*.dmg` 核对。有疑问可以去 X 找作者 [@wquguru](https://x.com/wquguru)。

打开后跟着首次引导开一个权限、听一段双人示例会议直接看字幕效果、接上 Ling key（也可以先跳过），要用同声传译时再装虚拟麦克风。之后有新版本时菜单栏图标会出现橙点，点一下就能更新，权限不会丢。

<p align="center">
  <img src="docs/onboarding.png" width="640" alt="首次引导第二步，播放双人示例会议并实时显示双语字幕">
</p>

### Windows

需要 Windows 10 2004 或更新版本。下载 Windows 安装包（大多数电脑选 x64，骁龙笔记本选 ARM64），双击就装好，不用管理员权限；安装程序还没有代码签名，SmartScreen 拦下时点更多信息 › 仍要运行。打开就是主窗口，列着还差哪几步：接上 Ling key、放一段测试声音、看示例会议；同声传译要装免费的 VB-Cable 虚拟麦克风，引导会带你装。新版本在知了里提示，点一下就升级。

### Linux

需要 Ubuntu 22.04 或 24.04 桌面版（x86_64 或 arm64）。下载 `Cicada-<版本>-Linux.tar.gz`，在终端里运行 `tar xzf Cicada-<版本>-Linux.tar.gz && cicada-linux/install.sh`，知了会出现在应用菜单里。同声传译会自己建一个“知了 麦克风”，不用装驱动。Linux 没法让窗口避开屏幕共享，纪要窗会一直标着“共享屏幕时此窗口可见”。会议录音要用 AAC 编码器，Ubuntu 默认没有：装了第三方媒体格式（比如 `ubuntu-restricted-extras`）后，“设置 › 通用 › 保存会议录音”才能打开，录音可以在会议记录里回放，点一句的时间就从那里放；没装时这个开关是灰的，其他功能照常。

### Android

需要 Android 10 或更新版本。在手机上下载 `Cicada-<版本>-Android.apk` 打开安装，按提示允许安装未知应用；第一次打开悬浮字幕时，Android 15 起要先在应用信息里允许受限制的设置。微信通话和会议 app 的声音系统不让录，这时开外放、改选“面对面”。

每个平台的安装包都能用 Releases 页面里的 `checksums.txt` 核对 SHA-256。

## 路线图

按先后排，想要哪一项欢迎在 Issues 里说。

- **记录我的发言**，开会时持续听麦克风并做回声消除，把你直接开口说的话也记进文字记录和纪要。
- **正式签名与公证**，首次打开不再需要点仍要打开，AI key 也能放回系统钥匙串；Windows 安装程序也加上代码签名。
- **声纹识别**，在现有的说话人识别基础上，在本机记住常一起开会的人的声音，下次开会也能自动认出。
- **不用 key 也有纪要**，在支持的 Mac 上用 Apple 本机模型整理纪要。
- **Android 上架应用商店**，不用再从浏览器装 APK。
- **iPhone 和 iPad**，系统不允许采集其他 app 的声音，所以先做听会议室、面对面互译和会议记录。

每项的细节和取舍见 [docs/ROADMAP.zh-CN.md](docs/ROADMAP.zh-CN.md)。

## 卸载

退出知了，去应用程序文件夹里把它拖进废纸篓即可。会议记录和录音都在 `~/Library/Application Support/LiveSubs` 文件夹里，不需要的话可以手动删掉。想清除软件设置可以运行：

```bash
defaults delete com.wquguru.cicada
```

## 开发

Mac 版从源码构建只需要安装 Xcode Command Line Tools（`xcode-select --install`），项目没有任何第三方依赖。在 macOS 27 上如果编译时报 `SwiftUIMacros` 缺失，说明这一版 Command Line Tools 不带 SwiftUI 的宏插件，安装完整的 Xcode 并运行 `sudo xcode-select -s /Applications/Xcode.app` 即可。Windows、Linux、Android 的构建方法见 [windows/README.md](windows/README.md)、[linux/README.md](linux/README.md)、[android/README.md](android/README.md)。

```bash
scripts/build.sh            # 编译开发版 → build/Cicada.app（名为 Cicada Dev，可与正式版同时运行）
open build/Cicada.app
scripts/package.sh          # 打包正式版 DMG、zip 和 SHA-256 校验值
```

代码架构等说明写在 [AGENTS.md](AGENTS.md) 里。官网源码放在 `site/` 目录，由 `scripts/site.py` 生成。历次更新记录见 [CHANGELOG.md](CHANGELOG.md) 或官网的[更新日志页](https://cicada.indaloop.app/changelog/)。

## 开源协议

本项目采用 [Apache-2.0](LICENSE) 协议开源。同声传译用到的虚拟麦克风驱动 BlackHole 2ch 采用 GPL 协议，知了安装包里不打包它，在你点安装时直接从它的官方发布地址下载。随 app 附带的声纹模型是 [WeSpeaker](https://github.com/wenet-e2e/wespeaker) 在 VoxCeleb 上训练的 ResNet34-LM，采用 CC BY 4.0 协议，由 `scripts/convert-voiceprint.py` 转成 Core ML。
