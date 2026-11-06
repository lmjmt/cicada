#if compiler(<6.0)
import Foundation
import SwiftUI
import AVFoundation
import CoreMedia

public struct PointerStyle {
    public static let link = PointerStyle()
}

extension View {
    public func pointerStyle(_ style: PointerStyle) -> some View { self }
    public func onScrollGeometryChange<T: Equatable>(for type: T.Type, of transform: @escaping (ScrollGeometry) -> T, action: @escaping (T, T) -> Void) -> some View { self }
    public func onGeometryChange<T: Equatable>(for type: T.Type, of transform: @escaping (GeometryProxy) -> T, action: @escaping (T) -> Void) -> some View { self }
}

public struct ScrollGeometry {
    public var contentOffset: CGPoint = .zero
    public var contentSize: CGSize = .zero
    public var containerSize: CGSize = .zero
}

public final class SpeechAnalyzer {
    public static func bestAvailableAudioFormat(compatibleWith: [Any]) async -> AVAudioFormat? { nil }
    public init(inputAudioFile: AVAudioFile, modules: [Any], finishAfterFile: Bool = false) async throws {}
    public init(modules: [Any]) {}
    public func prepareToAnalyze(in format: AVAudioFormat) async throws {}
    public func start<S>(inputSequence: S) async throws {}
    public func finalize(through: CMTime) async throws {}
    public func finalizeAndFinishThroughEndOfInput() async throws {}
    public func cancelAndFinishNow() async {}
}

public protocol SpeechModule {}

public struct AnalyzerInput {
    public init(buffer: AVAudioPCMBuffer) {}
}

public struct SpeechTranscriber: SpeechModule {
    public struct AttributeOptions: OptionSet {
        public let rawValue: Int
        public init(rawValue: Int) { self.rawValue = rawValue }
        public static let audioTimeRange = AttributeOptions(rawValue: 1)
        public static let transcriptionConfidence = AttributeOptions(rawValue: 2)
    }
    public struct ReportingOptions: OptionSet {
        public let rawValue: Int
        public init(rawValue: Int) { self.rawValue = rawValue }
        public static let volatileResults = ReportingOptions(rawValue: 1)
        public static let fastResults = ReportingOptions(rawValue: 2)
    }
    public init(locale: Locale, transcriptionOptions: [Any] = [], reportingOptions: ReportingOptions = [], attributeOptions: AttributeOptions = []) {}
    public static var isAvailable: Bool { false }
    public static var installedLocales: [Locale] { get async { [] } }
    public struct Result {
        public var text: AttributedString = AttributedString()
        public var isFinal: Bool = false
        public var range: CMTimeRange = .zero
    }
    public var results: AsyncThrowingStream<Result, Error> {
        AsyncThrowingStream { $0.finish() }
    }
}

public struct DictationTranscriber: SpeechModule {
    public struct AttributeOptions: OptionSet {
        public let rawValue: Int
        public init(rawValue: Int) { self.rawValue = rawValue }
        public static let audioTimeRange = AttributeOptions(rawValue: 1)
        public static let transcriptionConfidence = AttributeOptions(rawValue: 2)
    }
    public struct ReportingOptions: OptionSet {
        public let rawValue: Int
        public init(rawValue: Int) { self.rawValue = rawValue }
        public static let volatileResults = ReportingOptions(rawValue: 1)
        public static let frequentFinalization = ReportingOptions(rawValue: 2)
    }
    public struct ContentHints: OptionSet {
        public let rawValue: Int
        public init(rawValue: Int) { self.rawValue = rawValue }
        public static let farField = ContentHints(rawValue: 1)
    }
    public struct TranscriptionOptions: OptionSet {
        public let rawValue: Int
        public init(rawValue: Int) { self.rawValue = rawValue }
        public static let punctuation = TranscriptionOptions(rawValue: 1)
    }
    public init(locale: Locale, contentHints: ContentHints = [], transcriptionOptions: TranscriptionOptions = [], reportingOptions: ReportingOptions = [], attributeOptions: AttributeOptions = []) {}
    public static var installedLocales: [Locale] { get async { [] } }
    public struct Result {
        public var text: AttributedString = AttributedString()
        public var isFinal: Bool = false
        public var range: CMTimeRange = .zero
    }
    public var results: AsyncThrowingStream<Result, Error> {
        AsyncThrowingStream { $0.finish() }
    }
}

public struct AssetInventory {
    public enum Status {
        case installed
        case unsupported
        case other
    }
    public static func status(forModules: [Any]) async -> Status { .unsupported }
    public static func assetInstallationRequest(supporting: [Any]) async throws -> AssetInstallationRequest? { nil }
    public static var reservedLocales: [Locale] { get async { [] } }
    public static func release(reservedLocale: Locale) async -> Bool { false }
    public struct AssetInstallationRequest {
        public var progress: Progress = Progress()
        public func downloadAndInstall() async throws {}
    }
}

public struct TranslationSession {
    public init(installedSource: Locale.Language, target: Locale.Language) {}
    public func translate(_ text: String) async throws -> TranslationResponse { TranslationResponse() }
    public struct TranslationResponse {
        public var targetText: String = ""
    }
}

public struct LanguageAvailability {
    public init() {}
    public enum Status {
        case installed
        case supported
        case unsupported
    }
    public func status(from: Locale.Language, to: Locale.Language) async -> Status { .unsupported }
}


extension AttributedString.Runs.Run {
    public var transcriptionConfidence: Double? { nil }
    public var audioTimeRange: CMTimeRange? { nil }
}
#endif
