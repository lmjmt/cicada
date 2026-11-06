// cicada-cli: the Windows engines without Windows.
//
//   cicada-cli listen <file.wav> [--target zh-CN] [--speed 1|0] [--notes]
//       Plays the file into ListenEngine as if the PC were playing it, prints each line as it is
//       recorded, then the record's folder. --speed 0 feeds it as fast as it can; --notes waits
//       for the final notes and prints them. --room <mic.wav> hears that file as the room mic too
//       (电脑和会议室: two engines, the echo gate and EchoMatch); --room-only hears it alone (会议室).
//   cicada-cli check                     the AI service's key check: state, hears, catalog sizes
//   cicada-cli speak <text> <out.wav>    the service's voice for <text>, as a 24 kHz WAV
//   cicada-cli segments <file.wav>       where the segmenter cuts (compare with ming_asr.py)
//   cicada-cli roundtrip <session.json>…  reads and writes records, says if anything changed
//
// --provider ling|openrouter|zenmux|custom (default ling) and --hear / --text <model> pick the AI
// service. Records go to CICADA_HOME (default: a temp folder). The key comes from CICADA_KEY_FILE,
// else the Mac app's dev or release key file for that service; it is never printed.
using System.Text.Json.Nodes;
using Cicada;

var args_ = args.ToList();
if (args_.Count == 0) { Console.WriteLine("usage: cicada-cli listen|segments|roundtrip …"); return 2; }
string Opt(string name, string fallback) { int i = args_.IndexOf(name); return i >= 0 && i + 1 < args_.Count ? args_[i + 1] : fallback; }
Strings.Load(Path.Combine(AppContext.BaseDirectory, "Resources"), Opt("--ui", "zh-Hans"));
var provider = Opt("--provider", "ling");
var cliSettings = new AppSettings { Target = Opt("--target", "zh-CN"), AiProvider = provider };
if (Opt("--hear", "") is { Length: > 0 } hearModel) cliSettings.AiHearModels[provider] = hearModel;
if (Opt("--text", "") is { Length: > 0 } textModel) cliSettings.AiModels[provider] = textModel;
var keyFile = Environment.GetEnvironmentVariable("CICADA_KEY_FILE")
    ?? new[] { "LiveSubs Dev", "LiveSubs" }.Select(d => Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Library/Application Support", d,
        provider == "ling" ? "ling-api-key" : "ai-key-" + provider)).FirstOrDefault(File.Exists);
LingClient Client() => new(new AIKey(new PlainProtector(), keyFile), config: cliSettings.AIConfig);

switch (args_[0])
{
    case "segments":
    {
        var pcm = Wav.Read(args_[1]);
        var seg = new Segmenter();
        var list = new List<Segment>();
        seg.Emitted += list.Add;
        for (int i = 0; i < pcm.Length; i += 1600) seg.Feed(pcm.AsSpan(i, Math.Min(1600, pcm.Length - i)));
        seg.Flush();
        foreach (var s in list) Console.WriteLine($"{s.Index,3} {s.Start,7:F2}s {s.Seconds,5:F2}s");
        Console.WriteLine($"{list.Count} segments, {list.Sum(s => s.Seconds):F1}s of speech");
        return 0;
    }
    case "roundtrip":
    {
        int changed = 0;
        foreach (var file in args_.Skip(1))
        {
            var original = File.ReadAllText(file);
            var session = Json.Read<Session>(original)!;
            var written = Json.Write(session);
            bool same = JsonNode.DeepEquals(JsonNode.Parse(original), JsonNode.Parse(written));
            if (!same) changed++;
            Console.WriteLine($"{(same ? "same   " : "CHANGED")} {file} ({session.Lines.Count} lines{(session.Notes is null ? "" : ", notes")})");
            if (!same && args_.Contains("--diff")) Console.WriteLine(written);
        }
        return changed == 0 ? 0 : 1;
    }
    case "check":
    {
        var ling = Client();
        var (state, seconds) = await ling.Check();
        var h = ling.Health;
        var problem = h.Message(ling.ServiceName, ling.ServiceHost, ling.Config.TextModel, ling.HearName) ?? "-";
        Console.WriteLine($"{provider}: {state} in {seconds:F1} s, text {ling.Config.TextModel}, hear {ling.Config.HearModel}, catalog {ling.TextCatalog.Count}/{ling.HearCatalog.Count}");
        Console.WriteLine($"  {h.Summary}");
        Console.WriteLine($"  problem {problem}{(h.ProxyLine(ling.ServiceName, ling.ServiceHost) is { } px ? " / " + px : "")}");
        return h.Passed ? 0 : 1;
    }
    case "speak":
    {
        var ling = Client();
        var pcm = new List<byte>();
        var started = DateTime.UtcNow;
        await foreach (var chunk in ling.Speech(args_[1], Opt("--voice", "") is { Length: > 0 } v ? v : null)) pcm.AddRange(chunk);
        var samples = new short[pcm.Count / 2];
        Buffer.BlockCopy(pcm.ToArray(), 0, samples, 0, samples.Length * 2);
        File.WriteAllBytes(args_[2], Wav.Bytes(samples, 24000));
        Console.WriteLine($"{provider}: {ling.Config.VoiceModel} {samples.Length / 24000.0:F1} s of audio in {(DateTime.UtcNow - started).TotalSeconds:F1} s");
        return samples.Length > 0 ? 0 : 1;
    }
    case "hear":
    {
        // One file to the hear model (Ming on Ling), raw reply printed: for checking the prompt.
        var ling = Client();
        var target = Opt("--target", "zh-CN");
        var reply = await ling.Chat(Translator.HearPrompt(target, null, []), Translator.HearInstruction(target), Priority.Translate,
                                    maxTokens: 800, timeout: 20, model: ling.Config.HearModel, audio: Wav.Bytes(Wav.Read(args_[1])));
        Console.WriteLine(reply);
        Console.WriteLine($"-> {Translator.ParseHeard(reply, target, null)}");
        return 0;
    }
    case "listen":
    {
        if (Environment.GetEnvironmentVariable("CICADA_HOME") is null)
            Environment.SetEnvironmentVariable("CICADA_HOME", Path.Combine(Path.GetTempPath(), "cicada-cli"));
        Log.Echo = args_.Contains("--log");
        var settings = cliSettings;
        var ling = Client();
        if (!ling.HasKey) { Console.WriteLine($"no {provider} key (set CICADA_KEY_FILE)"); return 2; }
        Console.WriteLine($"{provider}: hear {ling.Config.HearModel}, text {ling.Config.TextModel}");
        var store = new SessionStore();
        var notes = new NotesEngine(ling, store);
        var engine = new ListenEngine(ling, new Translator(ling) { GoogleOff = settings.GoogleOff }, store, notes, settings);
        var roomFile = Opt("--room", "");
        var roomOnly = args_.Contains("--room-only");
        var roomEngine = roomFile.Length > 0 && !roomOnly ? new ListenEngine(ling, new Translator(ling) { GoogleOff = settings.GoogleOff }, store, notes, settings, roomSide: true) : null;

        var printed = new HashSet<string>();
        var shown = new Dictionary<string, string>();
        var started = DateTime.UtcNow;
        void show()
        {
            if (engine.SessionId is null || store.Get(engine.SessionId) is not { } s) return;
            lock (shown)
            {
                foreach (var l in s.Lines)
                {
                    var text = $"{l.Src}\n{"",17}→ {l.Dst ?? "…"}";
                    if (shown.TryGetValue(l.Id, out var before) && before == text) continue;
                    var tag = shown.ContainsKey(l.Id) ? "upd" : "new";
                    shown[l.Id] = text;
                    Console.WriteLine($"[{(DateTime.UtcNow - started).TotalSeconds,5:F1}] {tag} {Languages.Clock(l.T)} {(l.Via == "room" ? "现场" : roomEngine is null ? "" : "线上"),-2} {l.SrcLang,-5} {text}");
                }
            }
        }
        engine.Changed += show;
        var speed = double.Parse(Opt("--speed", "1"), System.Globalization.CultureInfo.InvariantCulture);
        IAudioSource source = new FileAudioSource(roomOnly ? roomFile : args_[1], speed);
        if (roomOnly) source = new GatedSource(source);
        var ended = new TaskCompletionSource();
        source.Ended += _ => ended.TrySetResult();
        engine.Start(source, room: roomOnly);
        var roomEnded = Task.CompletedTask;
        if (roomEngine is not null)
        {
            var echo = new EchoFilter(new EchoGate());
            engine.Echo = echo; roomEngine.Echo = echo;
            var mic = new GatedSource(new FileAudioSource(roomFile, speed)) { Silenced = () => echo.Gate.Closed };
            var done = new TaskCompletionSource();
            mic.Ended += _ => done.TrySetResult();
            roomEnded = done.Task;
            roomEngine.Changed += show;
            roomEngine.Join(mic, engine.SessionId!, store.Get(engine.SessionId!)!.StartedAt);
        }
        await Task.WhenAll(ended.Task, roomEnded);
        await Task.Delay(TimeSpan.FromSeconds(1.5 + (roomEngine is null ? 0 : EchoMatch.Hold)));
        if (roomEngine is not null) await roomEngine.Stop();
        await engine.Stop();
        var id = engine.SessionId!;
        if (args_.Contains("--notes"))
        {
            await notes.Finish();
            for (int i = 0; i < 120 && !(store.Get(id)?.Notes?.Final ?? false); i++) await Task.Delay(1000);
        }
        store.Flush();
        var record = store.Get(id);
        Console.WriteLine($"\n{record?.Lines.Count ?? 0} lines in {Path.Combine(Paths.Sessions, id)}");
        if (record?.Notes is { } n)
        {
            Console.WriteLine($"notes{(n.Final ? " (final)" : "")}: {n.Title}\n  {n.Summary}");
            foreach (var t in n.Topics) Console.WriteLine($"  {Languages.Clock(t.Start)} {t.Title}: {string.Join(" / ", t.Points)}");
            foreach (var t in n.Todos) Console.WriteLine($"  [ ] {t.Text} ({t.Owner})");
        }
        return 0;
    }
}
Console.WriteLine($"unknown command {args_[0]}");
return 2;
