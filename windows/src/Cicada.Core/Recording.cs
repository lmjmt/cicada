namespace Cicada;

/// 保存会议录音: what was heard goes into `system.m4a` beside session.json, as on the Mac
/// (AudioFiles.swift). While the meeting runs it is written as ADTS (`system.aac`), which stays
/// readable up to its last frame if the app is killed; when the meeting ends it is rewrapped into
/// the .m4a, and a partial file left by a crash is rewrapped at the next launch. The encoder is
/// the app's (Media Foundation); Core only decides what goes in and when.
public interface IAudioFiles
{
    /// An AAC (ADTS) file at `path` for 16 kHz mono; null when this PC can't encode.
    IAudioWriter? Open(string path);
    /// `from` (ADTS) into the .m4a `to`, the first `until` seconds only when given. False on failure.
    bool Rewrap(string from, string to, double? until);
}

public interface IAudioWriter
{
    void Write(ReadOnlySpan<short> pcm);
    /// Writes what is buffered and closes the file.
    void Close();
}

public static class Recording
{
    public static string SystemAudio(string sessionId) => Path.Combine(Paths.Sessions, sessionId, "system.m4a");
    public static string Partial(string m4a) => Path.ChangeExtension(m4a, ".aac");

    /// The file a record plays: its own recording, or an imported file's where it still is.
    public static string? Playable(Session s)
    {
        var own = SystemAudio(s.Id);
        if (File.Exists(own)) return own;
        if (s.SourcePath is { Length: > 0 } p && File.Exists(p)) return p;
        return null;
    }

    /// Samples of silence that go in before a buffer so the recording keeps the meeting's clock:
    /// loopback capture sends nothing while the PC is silent (SystemAudioTap fills only what it
    /// notices), a source switch leaves a gap, and a line's `t` is its time since the meeting began.
    /// `at`: meeting seconds when the buffer arrived; `fed`: samples already given; `count`: the
    /// buffer's. Nothing while the stream is within LoopbackGap.Late of the clock, so a packet that
    /// is merely late never puts a gap in a sentence.
    public static int Behind(double at, long fed, int count)
    {
        var lag = at - (fed + count) / (double)Segmenter.Rate;
        return lag >= LoopbackGap.Late ? (int)(lag * Segmenter.Rate) : 0;
    }
}
