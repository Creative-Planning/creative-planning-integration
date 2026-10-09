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

## Connecting a client company

Use the Production keys from the Intuit Developer portal. The client ID and secret stay in the
private credential store. The client ID is a placeholder below; do not put either value in this
repo.

1. In the portal, under the app's Production keys, register this exact redirect URI. Intuit
   compares it character for character, so no trailing slash and no case changes:

   ```
   https://creative-planning.github.io/creative-planning-integration/callback.html
   ```

2. Build the authorize URL. `state` is any random string; generate a new one per connection.

   ```
   https://appcenter.intuit.com/connect/oauth2
     ?client_id=<CLIENT_ID>
     &response_type=code
     &scope=com.intuit.quickbooks.accounting
     &redirect_uri=https%3A%2F%2Fcreative-planning.github.io%2Fcreative-planning-integration%2Fcallback.html
     &state=<RANDOM_STATE>
   ```

   `com.intuit.quickbooks.accounting` covers journal entries. Add
   `com.intuit.quickbooks.payment` only if the engagement needs it.

3. Open the URL in a browser. The client signs in to Intuit, picks the company, and authorizes.
   Intuit redirects to `callback.html`, which shows `code`, `state` and `realmId`. Check that
   `state` matches the value you sent.

4. Exchange the code within a few minutes. It works once. POST to
   `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` with HTTP Basic auth (client ID
   and client secret), `Content-Type: application/x-www-form-urlencoded`, and the body
   `grant_type=authorization_code&code=<CODE>&redirect_uri=<same redirect URI as step 2>`.

5. Store the access token, refresh token and `realmId` in the private tooling for that client.

If Intuit reports a redirect URI error, the URI in the request does not match the one registered
under the Production keys. Development keys are for sandbox companies only and have their own
redirect URI list.

## Editing

The HTML is generated. Edit `build.py`, then:

```sh
python3 build.py
```

The build fails if any page contains an em or en dash. Commit the regenerated HTML with the
`build.py` change. `assets/cp-logo.png` is the Creative Planning horizontal logo from the brand
kit; the build embeds it in each page.
