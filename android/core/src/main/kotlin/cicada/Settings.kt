package cicada

import java.util.Locale

/// The app's settings, in settings.json beside the records (never the Ling key: that has its own file).
class AppSettings(
    /// What subtitles translate into; "system" follows the phone's language.
    var target: String = "system",
    /// 纪要语言: the notes' language code; "system" is the same as the subtitles'.
    var notesLanguage: String = "system",
    /// Ling's text model (the other services' are in aiModels).
    var model: String = LingClient.DEFAULT_MODEL,
    /// AI 服务 (Settings.swift's keys): the service, and per service the models chosen over its
    /// recommended ones. aiHearModels is the ports' own: what hears the audio (Ming on Ling).
    var aiProvider: String = "ling",
    var aiModels: MutableMap<String, String> = mutableMapOf(),
    var aiHearModels: MutableMap<String, String> = mutableMapOf(),
    var aiVoiceModels: MutableMap<String, String> = mutableMapOf(),
    var aiCustomBase: String = "",
    var aiCustomVoiceBase: String = "",
    var aiCustomVoice: String = "",
    /// The custom service's hear model's own address (the Mac's aiCustomHearBase); empty: the text model's.
    var aiCustomHearBase: String = "",
    /// 语音和文字只发给你的服务: with the custom service, Google Translate is never asked. Kept when
    /// another service is picked, but only acts on the custom one (`customOnly`).
    var aiCustomOnly: Boolean = false,
    /// "notes" (live notes, default) or "subtitles" (the subtitle bar), for the floating window.
    var view: String = "notes",
    /// 共享屏幕时让对方看到: let the floating window show up in screenshots and screen recording.
    var showInCapture: Boolean = false,
    var onboarded: Boolean = false,
    /// The UI language: "system", "zh-Hans", "en", "ja" or "ko".
    var uiLanguage: String = "system",
    /// Where listening hears from: "playback" (what the phone plays) or "mic" (面对面).
    var source: String = "playback",
    /// Whether the floating window shows while listening (it needs 显示在其他应用上层).
    var overlay: Boolean = true,
    /// 没人说话时: "prompt" (count down, then end), "end" (end at once) or "off" (keep recording).
    var silenceEnd: String = "prompt",
    /// 多久算没人说话, in minutes: 5, 10, 15 or 30.
    var silenceMinutes: Double = 10.0,
    /// 说话人识别: number the other side's voices in records and exports (the Mac's speakerVoices).
    var speakerVoices: Boolean = true,
    /// 保存会议录音: keep what was heard as system.m4a beside the record (the Mac's recordAudio).
    var recordAudio: Boolean = true,
    /// 把我说的翻译给对方: 按住说话 in 面对面 (the Mac's 同声传译 switch).
    var speakBack: Boolean = true,
    /// When GitHub Releases last answered an update check (epoch ms; UpdateChecker).
    var updateLastChecked: Long? = null,
    /// The newest version a notification was posted for, so each one is announced once.
    var updateNotified: String? = null,
) {
    /// My language: the translate-to choice, or under "follow system" the Mac's myLanguage
    /// (Chinese when the system list has it, else the first). 我说, notes and the UI start from it.
    val targetCode: String get() = if (target == "system") Languages.myLanguage(systemLanguages()) else target
    val notesCode: String get() = if (notesLanguage == "system") targetCode else notesLanguage

    /// What subtitles translate `source` into: under "follow system", my language unless that is
    /// what they speak, then the next system language (the Mac's followSystemTarget).
    fun targetFor(source: String?): String =
        if (target == "system") Languages.followSystemTarget(source, systemLanguages()) else target

    /// The AI service in use, its address and models (what LingClient calls with).
    fun aiConfig(): AIConfig = Providers.configFrom(this)

    /// 语音和文字只发给你的服务 in effect: on, and the custom service in use.
    val customOnly: Boolean get() = aiCustomOnly && aiProvider == "custom"

    fun toJson(): Map<String, Any?> = mapOf(
        "target" to target, "notesLanguage" to notesLanguage, "model" to model, "view" to view,
        "aiProvider" to aiProvider, "aiModels" to aiModels.toSortedMap(), "aiHearModels" to aiHearModels.toSortedMap(),
        "aiVoiceModels" to aiVoiceModels.toSortedMap(), "aiCustomBase" to aiCustomBase,
        "aiCustomVoiceBase" to aiCustomVoiceBase, "aiCustomVoice" to aiCustomVoice,
        "aiCustomHearBase" to aiCustomHearBase, "aiCustomOnly" to aiCustomOnly,
        "showInCapture" to showInCapture, "onboarded" to onboarded, "uiLanguage" to uiLanguage,
        "source" to source, "overlay" to overlay, "silenceEnd" to silenceEnd, "silenceMinutes" to silenceMinutes,
        "speakerVoices" to speakerVoices, "recordAudio" to recordAudio, "speakBack" to speakBack,
        "updateLastChecked" to updateLastChecked, "updateNotified" to updateNotified,
    )

    fun save() {
        try {
            Paths.root.mkdirs()
            Paths.settings.writeText(Json.write(toJson()))
        } catch (e: Exception) { Log.d("settings: save failed ${e.javaClass.simpleName}") }
    }

    companion object {
        /// The phone's languages, most preferred first (the app reads the system's list; the
        /// JVM's default locale stands in for tests and the CLI).
        @Volatile var systemLanguages: () -> List<String> = { listOf(Locale.getDefault().toLanguageTag()) }

        fun load(): AppSettings {
            try {
                if (Paths.settings.isFile) {
                    val o = Json.parseObject(Paths.settings.readText())
                    if (o != null) {
                        val d = AppSettings()
                        return AppSettings(
                            target = o["target"].str() ?: d.target, notesLanguage = o["notesLanguage"].str() ?: d.notesLanguage,
                            model = o["model"].str() ?: d.model, view = o["view"].str() ?: d.view,
                            aiProvider = o["aiProvider"].str() ?: d.aiProvider,
                            aiModels = strings(o["aiModels"]), aiHearModels = strings(o["aiHearModels"]),
                            aiVoiceModels = strings(o["aiVoiceModels"]), aiCustomBase = o["aiCustomBase"].str() ?: "",
                            aiCustomVoiceBase = o["aiCustomVoiceBase"].str() ?: "", aiCustomVoice = o["aiCustomVoice"].str() ?: "",
                            aiCustomHearBase = o["aiCustomHearBase"].str() ?: "", aiCustomOnly = o["aiCustomOnly"].bool() ?: false,
                            showInCapture = o["showInCapture"].bool() ?: false, onboarded = o["onboarded"].bool() ?: false,
                            uiLanguage = o["uiLanguage"].str() ?: d.uiLanguage, source = o["source"].str() ?: d.source,
                            overlay = o["overlay"].bool() ?: true,
                            silenceEnd = o["silenceEnd"].str() ?: d.silenceEnd,
                            silenceMinutes = (o["silenceMinutes"] as? Number)?.toDouble() ?: d.silenceMinutes,
                            speakerVoices = o["speakerVoices"].bool() ?: true, recordAudio = o["recordAudio"].bool() ?: true,
                            speakBack = o["speakBack"].bool() ?: true,
                            updateLastChecked = (o["updateLastChecked"] as? Number)?.toLong(), updateNotified = o["updateNotified"].str(),
                        )
                    }
                }
            } catch (e: Exception) { Log.d("settings: unreadable, defaults used (${e.javaClass.simpleName})") }
            return AppSettings()
        }

        private fun strings(v: Any?): MutableMap<String, String> =
            v.obj()?.mapNotNull { (k, x) -> x.str()?.let { k to it } }?.toMap(mutableMapOf()) ?: mutableMapOf()
    }
}
