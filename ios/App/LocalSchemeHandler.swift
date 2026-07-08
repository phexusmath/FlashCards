import WebKit

/// Serves files from the app bundle's `www/` folder for `slovo://app/<file>` requests.
/// Responding with a real HTTPURLResponse (status 200 + Content-Type) makes the page
/// a proper same-origin context, so fetch('a1_combined.json') and localStorage both work.
final class LocalSchemeHandler: NSObject, WKURLSchemeHandler {
    private static let mimeTypes: [String: String] = [
        "html": "text/html",
        "js": "application/javascript",
        "css": "text/css",
        "json": "application/json",
        "png": "image/png",
        "jpg": "image/jpeg",
        "svg": "image/svg+xml",
        "woff2": "font/woff2",
    ]

    func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
        guard let url = urlSchemeTask.request.url else {
            urlSchemeTask.didFailWithError(URLError(.badURL))
            return
        }
        var path = url.path
        if path.isEmpty || path == "/" { path = "/index.html" }

        // Resolve inside the bundled www folder only; reject anything that escapes it.
        guard let wwwDir = Bundle.main.resourceURL?.appendingPathComponent("www", isDirectory: true) else {
            urlSchemeTask.didFailWithError(URLError(.fileDoesNotExist))
            return
        }
        let fileURL = wwwDir.appendingPathComponent(String(path.dropFirst())).standardizedFileURL
        guard fileURL.path.hasPrefix(wwwDir.standardizedFileURL.path),
              let data = try? Data(contentsOf: fileURL) else {
            let notFound = HTTPURLResponse(url: url, statusCode: 404, httpVersion: "HTTP/1.1",
                                           headerFields: ["Content-Type": "text/plain"])!
            urlSchemeTask.didReceive(notFound)
            urlSchemeTask.didReceive(Data("Not found".utf8))
            urlSchemeTask.didFinish()
            return
        }

        let ext = fileURL.pathExtension.lowercased()
        let mime = Self.mimeTypes[ext] ?? "application/octet-stream"
        let response = HTTPURLResponse(url: url, statusCode: 200, httpVersion: "HTTP/1.1", headerFields: [
            "Content-Type": mime + (mime.hasPrefix("text/") || mime == "application/javascript" ? "; charset=utf-8" : ""),
            "Content-Length": String(data.count),
            "Cache-Control": "no-cache",
        ])!
        urlSchemeTask.didReceive(response)
        urlSchemeTask.didReceive(data)
        urlSchemeTask.didFinish()
    }

    func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {
        // Responses are delivered synchronously above; nothing to cancel.
    }
}
