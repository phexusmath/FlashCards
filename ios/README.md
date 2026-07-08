# Слово for iOS

A native iOS wrapper around the Слово Russian trainer, targeting **iOS 16.1+** (tested config: 16.1.1). The web app lives in `www/` (a self-contained iOS-tuned copy of the main `index.html` plus the word decks) and is hosted in a full-screen WKWebView. Local assets are served through a custom `slovo://` URL scheme so `fetch()` and `localStorage` behave exactly like on the web.

## Get the IPA (no Mac needed)

Every push touching `ios/` runs the **Build iOS IPA** GitHub Actions workflow (also runnable manually from the Actions tab). It compiles the app on a macOS runner and uploads **`Slovo-unsigned.ipa`** as a build artifact — download it from the workflow run page.

## Install on an iPhone (iOS 16.1.1)

iOS refuses unsigned apps, so the IPA must be signed with *your* Apple ID during install. Both options below do that automatically and run on Windows:

- **[Sideloadly](https://sideloadly.io)** — plug the iPhone into the PC, drag `Slovo-unsigned.ipa` in, log in with any (free) Apple ID, Start.
- **[AltStore](https://altstore.io)** — install AltServer on the PC, then open the IPA through AltStore on the phone.

With a free Apple ID the signature lasts 7 days (re-sideload to renew, progress is kept — it lives in the app's localStorage). A paid developer account signs for a year.

After installing, trust the certificate on the phone: Settings → General → VPN & Device Management.

## Build locally (Mac only)

```sh
brew install xcodegen
cd ios
xcodegen generate      # produces Slovo.xcodeproj from project.yml
open Slovo.xcodeproj   # set your signing team, then run on a device
```

## Layout

- `project.yml` — [XcodeGen](https://github.com/yonas/XcodeGen) spec; the `.xcodeproj` is generated, never committed
- `App/` — Swift sources (WKWebView shell + `slovo://` scheme handler), `Info.plist`, asset catalog (icon, launch color)
- `www/` — iOS-adapted copy of the web app. It intentionally diverges from the root `index.html`: safe-area padding for the notch, no pinch/double-tap zoom, no text-selection callouts, `-webkit-backdrop-filter`, and no service worker (the bundle *is* the offline cache). The JSON decks are byte-for-byte copies of the root ones — re-copy them if the root data changes.
