# Creative Planning Integration (public pages)

Static pages for **Creative Planning Integration**, the Intuit app that Creative Planning
Technology uses to connect a client's QuickBooks Online or Intuit Enterprise Suite company to
the reporting and automation we build for that client.

## Why this exists

Intuit requires any software that calls the QuickBooks Online API to be registered as an app in
the Intuit Developer portal. A production app has to supply public URLs for a launch page, an
end-user license agreement, a privacy policy, connect and disconnect pages, and an HTTPS OAuth
redirect URI. Intuit checks those URLs, and the client's browser is sent to the redirect URI
during authorization, so they have to be reachable without a login.

We register one app for all Creative Planning clients instead of one per engagement. Each
client company authorizes it separately, and each authorization reaches only that company. This
repo hosts the pages that app needs, through GitHub Pages.

The app was first built for a single client's payroll journal entry automation. Nothing in these
pages is specific to that client, and the same app is used for any company we work with that is
on QuickBooks Online or Intuit Enterprise Suite.

## Why this repo is public, and why that is safe

GitHub Pages serves this site from a public repo. Intuit and the client's browser must reach the
pages anonymously, so the site cannot sit behind a GitHub or Creative Planning login.

Nothing secret is in this repo, and nothing secret is ever sent to it:

| Concern | Where it actually lives |
|---|---|
| Intuit client ID and client secret | Private Creative Planning tooling and its credential store, never here |
| OAuth access and refresh tokens | Private tooling, per client, never here |
| Client names, realm IDs, financial data | Private engagement repos, never here |
| Server-side code | There is none. GitHub Pages serves static HTML only. |

The one page that handles live data is `callback.html`, the OAuth redirect URI. It reads `code`,
`state`, and `realmId` from its own address, shows them so the operator can paste them into the
Creative Planning tool that started the connection, and then removes them from the browser
history. It makes no network requests. An authorization code on its own is not useful to anyone
else: it expires within minutes, works once, and can only be exchanged for tokens with the
client secret.

Keep it that way. Do not commit client names, company IDs, credentials, tokens, logs, or personal
contact details to this repo.

## Pages

| Page | Intuit Developer portal field |
|---|---|
| `index.html` | Launch URL, host domain landing page |
| `eula.html` | End-user license agreement URL |
| `privacy.html` | Privacy policy URL (forwards to Creative Planning's privacy policy) |
| `connect.html` | Connect / reconnect request URL |
| `disconnected.html` | Disconnect URL |
| `callback.html` | Production OAuth redirect URI |
| `404.html` | GitHub Pages not-found page |

Published at `https://creative-planning.github.io/creative-planning-integration/`.

If the repo is renamed, the GitHub Pages URL changes and GitHub does not redirect the old one.
Every URL above has to be updated in the Intuit Developer portal, and the redirect URI has to be
updated in any tooling that starts a connection, before the old URLs stop working for clients.

## Editing

The HTML is generated. Edit `build.py`, then:

```sh
python3 build.py
```

The build fails if any page contains an em or en dash. Commit the regenerated HTML with the
`build.py` change. `assets/cp-logo.png` is the Creative Planning horizontal logo from the brand
kit; the build embeds it in each page.
