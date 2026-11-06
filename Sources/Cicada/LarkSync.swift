import AppKit
import Foundation

/// Bridge to Lark / Feishu Tasks via lark-cli.
enum LarkSync {
    private static func findLarkCLI() -> String? {
        let envPath = ProcessInfo.processInfo.environment["PATH"] ?? ""
        var candidates = envPath.split(separator: ":").map { "\($0)/lark-cli" }
        let home = FileManager.default.homeDirectoryForCurrentUser.path
        candidates.append("\(home)/.npm-global/bin/lark-cli")
        candidates.append("/opt/homebrew/bin/lark-cli")
        candidates.append("/usr/local/bin/lark-cli")
        return candidates.first { FileManager.default.isExecutableFile(atPath: $0) }
    }

    private static func prepareProcess(cli: String, args: [String]) -> Process {
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: cli)
        proc.arguments = args
        var env = ProcessInfo.processInfo.environment
        let home = FileManager.default.homeDirectoryForCurrentUser.path
        let extraPaths = [
            "\(home)/.npm-global/bin",
            "/usr/local/bin",
            "/opt/homebrew/bin",
            "/opt/homebrew/sbin"
        ]
        let currentPath = env["PATH"] ?? "/usr/bin:/bin:/usr/sbin:/sbin"
        env["PATH"] = extraPaths.joined(separator: ":") + ":" + currentPath
        proc.environment = env
        return proc
    }

    static func extractLarkURL(from text: String) -> URL? {
        let prefixes = [
            "https://applink.larksuite.com/client/todo/task_list?guid=",
            "https://applink.larksuite.com/client/todo/detail?guid=",
            "https://applink.feishu.cn/client/todo/task_list?guid=",
            "https://applink.feishu.cn/client/todo/detail?guid="
        ]
        for p in prefixes {
            if let r = text.range(of: p) {
                let tail = text[r.lowerBound...]
                let endChars = CharacterSet(charactersIn: "\"'\n\r\t ()")
                if let endRange = tail.rangeOfCharacter(from: endChars) {
                    let urlStr = String(tail[..<endRange.lowerBound])
                    if let u = URL(string: urlStr) { return u }
                } else if let u = URL(string: String(tail)) {
                    return u
                }
            }
        }
        return nil
    }

    /// Push all meeting action items to Lark Tasks as a new tasklist.
    static func pushAllToLark(title: String, todos: [NoteItem], conclusions: [NoteItem] = [], completion: ((Bool, String?) -> Void)? = nil) {
        guard let cli = findLarkCLI() else {
            completion?(false, L("未检测到 lark-cli，请先安装: npm i -g @larksuite/cli"))
            return
        }
        guard !todos.isEmpty else {
            completion?(false, L("当前会议暂无待办事项"))
            return
        }

        let tasklistName = L("【会议待办】\(title)")
        var tasks: [[String: String]] = []
        for todo in todos {
            var desc = L("来源会议：\(title)\n")
            if let owner = todo.owner { desc += L("发言人：\(owner)\n") }
            if !conclusions.isEmpty {
                desc += L("会议结论参考：\n")
                for c in conclusions.prefix(3) {
                    desc += "- \(c.text)\n"
                }
            }
            tasks.append([
                "summary": todo.text,
                "description": desc
            ])
        }

        guard let payload = try? JSONSerialization.data(withJSONObject: tasks),
              let jsonStr = String(data: payload, encoding: .utf8) else {
            completion?(false, L("待办数据格式化失败"))
            return
        }

        DispatchQueue.global(qos: .userInitiated).async {
            let proc = prepareProcess(cli: cli, args: ["task", "+tasklist-create", "--name", tasklistName, "--data", jsonStr])
            let pipe = Pipe()
            proc.standardOutput = pipe
            proc.standardError = pipe

            do {
                try proc.run()
                proc.waitUntilExit()
                let output = String(data: pipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8) ?? ""
                let ok = proc.terminationStatus == 0
                DispatchQueue.main.async {
                    completion?(ok, output)
                }
            } catch {
                DispatchQueue.main.async {
                    completion?(false, error.localizedDescription)
                }
            }
        }
    }

    /// Push a single action item to Lark as a personal task.
    static func pushSingleTodo(title: String, todo: NoteItem, conclusions: [NoteItem] = [], completion: ((Bool, String?) -> Void)? = nil) {
        guard let cli = findLarkCLI() else {
            completion?(false, L("未检测到 lark-cli，请先安装: npm i -g @larksuite/cli"))
            return
        }

        var desc = L("来源会议：\(title)\n")
        if let owner = todo.owner { desc += L("发言人：\(owner)\n") }
        if !conclusions.isEmpty {
            desc += L("相关结论参考：\n")
            for c in conclusions.prefix(2) {
                desc += "- \(c.text)\n"
            }
        }

        DispatchQueue.global(qos: .userInitiated).async {
            let proc = prepareProcess(cli: cli, args: [
                "task", "+create",
                "--summary", todo.text,
                "--description", desc
            ])
            let pipe = Pipe()
            proc.standardOutput = pipe
            proc.standardError = pipe

            do {
                try proc.run()
                proc.waitUntilExit()
                let output = String(data: pipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8) ?? ""
                let ok = proc.terminationStatus == 0
                DispatchQueue.main.async {
                    completion?(ok, output)
                }
            } catch {
                DispatchQueue.main.async {
                    completion?(false, error.localizedDescription)
                }
            }
        }
    }
}
