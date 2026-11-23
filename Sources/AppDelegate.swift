import UIKit
import WebKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?

    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let window = UIWindow(frame: UIScreen.main.bounds)
        window.rootViewController = WebViewController()
        window.makeKeyAndVisible()
        self.window = window
        return true
    }
}

final class WebViewController: UIViewController {
    private let webView = WKWebView(frame: .zero)

    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = UIColor(red: 0.027, green: 0.039, blue: 0.063, alpha: 1)

        webView.translatesAutoresizingMaskIntoConstraints = false
        if #available(iOS 11.0, *) {
            // The HTML uses viewport-fit=cover and env(safe-area-inset-*) itself.
            webView.automaticallyAdjustsContentInsets = false
            webView.scrollView.contentInsetAdjustmentBehavior = .never
        }
        webView.scrollView.bounces = false
        view.addSubview(webView)
        NSLayoutConstraint.activate([
            webView.topAnchor.constraint(equalTo: view.topAnchor),
            webView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            webView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])

        let url = Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "www")
            ?? Bundle.main.url(forResource: "index", withExtension: "html")

        if let url = url {
            webView.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
        } else {
            let label = UILabel(frame: view.bounds)
            label.text = "index.html not found"
            label.textColor = .white
            label.textAlignment = .center
            view.addSubview(label)
        }
    }

    override var prefersStatusBarHidden: Bool { false }
    override var preferredStatusBarStyle: UIStatusBarStyle { .lightContent }
}
