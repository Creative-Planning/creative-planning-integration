#!/usr/bin/env python3
"""Build the public GitHub Pages site the Intuit Developer portal needs.

Pages (all static, CP letterhead styling, no client data, no personal names):
  index.html         launch URL / app description
  eula.html          end-user license agreement
  connect.html       connect / reconnect request URL
  disconnected.html  disconnect URL
  callback.html      OAuth redirect URI: shows code / state / realmId for copy-paste
  privacy.html       forwards to Creative Planning's privacy policy
  404.html

Output: this directory. Run:  python3 build.py
"""
from __future__ import annotations

import base64
import pathlib
import sys

SITE = pathlib.Path(__file__).resolve().parent
APP = "Creative Planning Integration"
BASE_URL = "https://creative-planning.github.io/creative-planning-integration"
PRIVACY_URL = "https://creativeplanning.com/privacy-policy/"
EFFECTIVE = "September 29, 2026"

# CP palette. Literal hex, same values as the applying-cp-brand skill.
BLUE = "#165D7D"
NIGHT = "#1C5266"
MIST = "#87A0A8"
LEISURE = "#C3AC80"
SLATE = "#363739"

# Embedded rather than linked so 404.html, which GitHub serves at any missing path,
# still finds it.
LOGO = "data:image/png;base64," + base64.b64encode(
    (SITE / "assets/cp-logo.png").read_bytes()
).decode()

CSS = f"""
<style>
body {{
  margin:0; background:#FFFFFF; color:{SLATE};
  font-family:"Atten New","Trebuchet MS",Tahoma,sans-serif;
  font-size:11.5pt; line-height:1.55;
}}
.sheet {{ max-width:7.5in; margin:0 auto; padding:0.5in 0.4in 0.6in; }}
h1,h2,h3 {{ font-family:"Mencken Headline",Georgia,"Times New Roman",serif; font-weight:bold; }}
h1 {{ font-size:24pt; line-height:1.15; color:{BLUE}; margin:0 0 4pt; }}
h2 {{ font-size:14pt; color:{BLUE}; margin:22pt 0 2pt; }}
h3 {{ font-size:11.5pt; color:{NIGHT}; margin:14pt 0 2pt; }}
p {{ margin:7pt 0; }}
a {{ color:{BLUE}; }}

.logo {{ width:2.25in; height:0.75in; display:block; }}
.division {{
  font-size:7.5pt; letter-spacing:0.14em; text-transform:uppercase;
  color:{MIST}; font-weight:bold; margin:6pt 0 10pt;
}}
.rule {{ border-top:2px solid {LEISURE}; height:0; margin:0 0 4pt; }}
.eyebrow {{
  font-size:7.5pt; letter-spacing:0.14em; text-transform:uppercase;
  color:{LEISURE}; font-weight:bold; margin:20pt 0 8pt;
}}
.lede {{ font-size:12pt; margin:16pt 0 0; }}
.note {{ color:#5C6468; font-size:10.5pt; }}

ul {{ margin:7pt 0; padding-left:0.24in; }}
li {{ margin:4pt 0; }}
ul.diamond {{ list-style:none; padding-left:0.24in; }}
ul.diamond li {{ text-indent:-0.16in; }}
ul.diamond li:before {{ content:"\\25C6  "; color:{LEISURE}; font-size:8pt; }}
ol {{ margin:7pt 0; padding-left:0.3in; }}
ol li {{ margin:5pt 0; }}
ol li::marker {{ color:{BLUE}; font-weight:bold; }}

.nav a {{ color:{BLUE}; text-decoration:none; margin-right:14pt; font-size:10pt; }}
.nav a:hover {{ text-decoration:underline; }}
.box {{ border:1px solid {LEISURE}; padding:10pt 12pt; margin:12pt 0; background:#FBF9F4; }}
code, .mono {{ font-family:Menlo,Consolas,monospace; font-size:10.5pt; }}
.field {{ margin:8pt 0; }}
.field label {{ display:block; font-size:9pt; color:{NIGHT}; text-transform:uppercase; letter-spacing:1px; }}
.field input {{ width:100%; box-sizing:border-box; font-family:Menlo,Consolas,monospace; font-size:11pt; padding:6pt; border:1px solid #ccc; }}
button.copy {{ background:{BLUE}; color:#fff; border:0; padding:6pt 12pt; font-size:10.5pt; cursor:pointer; margin-top:6pt; }}
.warn {{ color:#8A2B2B; }}

.footer {{ margin-top:28pt; border-top:2px solid {LEISURE}; padding-top:9pt; text-align:center; }}
.footer .contact {{
  font-size:8pt; letter-spacing:0.1em; text-transform:uppercase;
  font-weight:bold; color:{BLUE}; margin:0 0 3pt;
}}
.footer p.fine {{ font-size:8.5pt; color:#7E888C; margin:0; }}

@media print {{ .sheet {{ padding:0; }} h2 {{ page-break-after:avoid; }} }}

@media (prefers-color-scheme:dark) {{
  body {{ background:#101A1F; color:#E6EDEF; }}
  h1, h2, .footer .contact, .nav a, a {{ color:#7FB4CC; }}
  h3, .field label {{ color:#9CC6D6; }}
  .note {{ color:#AFBDC2; }}
  .box {{ background:#16242B; border-color:#2A3F49; }}
  .field input {{ background:#101A1F; color:#E6EDEF; border-color:#2A3F49; }}
  .warn {{ color:#E59A9A; }}
  .footer p.fine {{ color:#8B9BA1; }}
}}
</style>
"""

NAV = f"""
  <p class="nav">
    <a href="{BASE_URL}/">Overview</a>
    <a href="{BASE_URL}/eula.html">License Agreement</a>
    <a href="{PRIVACY_URL}">Privacy Policy</a>
    <a href="{BASE_URL}/connect.html">Connect</a>
  </p>
"""

EYEBROW = f"Creative Planning &middot; {APP}"


def shell(title: str, h1: str, body: str, eyebrow: str = EYEBROW) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{CSS}
</head>
<body>
<div class="sheet">
  <img class="logo" src="{LOGO}" alt="Creative Planning">
  <p class="division">Technology &middot; Data and Automation</p>
  <div class="rule"></div>
{NAV}
  <p class="eyebrow">{eyebrow}</p>
  <h1>{h1}</h1>
{body}
  <div class="footer">
    <p class="contact">866-CREATIVE &nbsp;|&nbsp; CreativePlanning.com</p>
    <p class="fine">{APP} is an application built by Creative Planning Technology for
    companies Creative Planning works with. It is not listed on the Intuit App Store.</p>
  </div>
</div>
</body>
</html>
"""


INDEX = shell(
    APP,
    APP,
    f"""
  <p class="lede">A connector Creative Planning Technology uses to link a client's
  QuickBooks Online or Intuit Enterprise Suite company to the reporting and automation we
  build for that client.</p>

  <h2>Why It Exists</h2>
  <p>Any software that reads from or writes to QuickBooks Online has to be registered with
  Intuit as an app, and each company has to authorize that app before it can connect.
  Rather than register a separate app for every engagement, Creative Planning maintains this
  one. Each client company authorizes it separately, and each authorization reaches only
  that client's own company.</p>

  <h2>What It Does</h2>
  <ul class="diamond">
    <li>Reads accounting lists such as the chart of accounts, classes, customers, and vendors
    to validate and reconcile data.</li>
    <li>Creates the transactions an engagement calls for, most often journal entries, for
    example a weekly payroll summary posted from a payroll system.</li>
    <li>Uses only Intuit's accounting permission. It does not request access to Intuit
    payments or payroll.</li>
  </ul>
  <p>What a given connection reads and writes is agreed with that client before the
  connection is made.</p>

  <h2>Who Can Use It</h2>
  <p>Companies Creative Planning works with, connected by Creative Planning Technology staff
  with the company's authorization. The app is not listed on the Intuit App Store and cannot
  be installed by the public.</p>

  <h2>Documents</h2>
  <ul class="diamond">
    <li><a href="{BASE_URL}/eula.html">End-User License Agreement</a></li>
    <li><a href="{PRIVACY_URL}">Privacy Policy</a> (Creative Planning)</li>
  </ul>

  <h2>Support</h2>
  <p>Contact Creative Planning Technology through your Creative Planning advisor, or via
  <a href="https://creativeplanning.com">creativeplanning.com</a>.</p>
""",
    eyebrow="Creative Planning &middot; QuickBooks Online and Intuit Enterprise Suite Integration",
)

EULA = shell(
    f"End-User License Agreement | {APP}",
    "End-User License Agreement",
    f"""
  <p class="note">Effective {EFFECTIVE}</p>

  <p>This End-User License Agreement (the "Agreement") is between <b>Creative Planning, LLC</b>
  and its affiliates ("Creative Planning," "we") and the organization that authorizes the
  Application to connect to its Intuit company ("Licensee," "you"). It governs use of the
  {APP} application (the "Application"), which connects to your Intuit Enterprise
  Suite or QuickBooks Online company through Intuit's application programming interfaces.</p>

  <h2>1. License</h2>
  <p>Creative Planning grants you a non-exclusive, non-transferable, revocable license to use the
  Application solely with your own Intuit company files, for your internal business purposes. You
  may not sublicense, resell, or make the Application available to any other company.</p>

  <h2>2. What the Application Does</h2>
  <p>The Application reads list data (such as accounts, classes, customers, and vendors) from
  your Intuit company and creates the transactions, such as journal entries, that you direct it
  to create under your engagement with Creative Planning. It does not request access to Intuit
  payments or payroll services.</p>

  <h2>3. Your Data</h2>
  <p>Your Intuit data stays in your Intuit company. The Application holds only the OAuth access
  and refresh tokens Intuit issues when you authorize it, and those are stored on systems you or
  Creative Planning control on your behalf. Creative Planning does not sell your data or share it
  with third parties except as needed to operate the Application or as required by law. Our
  handling of personal information is described in the
  <a href="{PRIVACY_URL}">Creative Planning Privacy Policy</a>.</p>

  <h2>4. Intuit</h2>
  <p>Your use of Intuit Enterprise Suite and QuickBooks Online is governed by your agreement with
  Intuit Inc. Intuit is not a party to this Agreement and has no obligation to you regarding the
  Application.</p>

  <h2>5. Termination</h2>
  <p>You may end this license at any time by disconnecting the Application from your Intuit
  company (Settings, Apps, Disconnect) and notifying Creative Planning. Creative Planning may
  suspend the Application if it is misused or if Intuit's terms require it. On termination, the
  Application's tokens are revoked and no further access occurs.</p>

  <h2>6. No Warranty</h2>
  <p>The Application is provided "as is." Creative Planning disclaims all warranties, express or
  implied, including fitness for a particular purpose. You are responsible for reviewing
  transactions the Application creates before relying on them for financial reporting or tax
  purposes.</p>

  <h2>7. Limitation of Liability</h2>
  <p>To the extent permitted by law, Creative Planning's total liability arising from the
  Application will not exceed the fees you paid Creative Planning for the Application in the
  twelve months before the claim. Creative Planning is not liable for indirect, incidental, or
  consequential damages.</p>

  <h2>8. Governing Law</h2>
  <p>This Agreement is governed by the laws of the State of Kansas, without regard to its
  conflict-of-law rules.</p>

  <h2>9. Changes</h2>
  <p>Creative Planning may update this Agreement by posting a new version at this address with a
  new effective date. Continued use after that date is acceptance of the change.</p>

  <p class="note">Questions about this Agreement go to Creative Planning Technology through your
  Creative Planning advisor.</p>
""",
)

CONNECT = shell(
    f"Connect | {APP}",
    f"Connecting {APP}",
    f"""
  <p class="lede">This page is shown when someone starts a connection to the Application from
  Intuit. Connections are set up by Creative Planning Technology for each client, not from
  this page.</p>

  <h2>How A Connection Is Made</h2>
  <ol>
    <li>Creative Planning starts the authorization from its tooling.</li>
    <li>Intuit asks you to sign in and pick the company to connect.</li>
    <li>Intuit returns you to our <a href="{BASE_URL}/callback.html">callback page</a>, which
    shows the one-time authorization code.</li>
    <li>The code is exchanged for tokens. Nothing is stored on this website.</li>
  </ol>

  <p>If you reached this page unexpectedly, no connection was made. Close the tab or return to
  <a href="https://qbo.intuit.com">QuickBooks</a>.</p>
""",
)

DISCONNECTED = shell(
    f"Disconnected | {APP}",
    f"{APP} Has Been Disconnected",
    """
  <p class="lede">The Application no longer has access to the Intuit company it was connected
  to. Its access and refresh tokens are now invalid.</p>

  <h2>What Happens Next</h2>
  <ul class="diamond">
    <li>No further transactions will be posted and no lists will be read.</li>
    <li>Transactions already created remain in your company; nothing is deleted on disconnect.</li>
    <li>To reconnect, contact Creative Planning Technology through your advisor.</li>
  </ul>
""",
)

CALLBACK = shell(
    f"Authorization Callback | {APP}",
    "Authorization Received",
    """
  <p class="lede">Intuit has returned an authorization code. Copy the values below into the
  Creative Planning tool that started the connection. Nothing on this page is sent anywhere;
  it runs entirely in your browser.</p>

  <div class="box" id="ok" hidden>
    <div class="field"><label>Authorization code</label><input id="code" readonly></div>
    <div class="field"><label>State</label><input id="state" readonly></div>
    <div class="field"><label>Realm ID (company id)</label><input id="realm" readonly></div>
    <button class="copy" id="copyAll">Copy all three as one line</button>
    <span id="copied" class="note" hidden>&nbsp;Copied.</span>
  </div>

  <div class="box" id="err" hidden>
    <p class="warn"><b>Intuit returned an error:</b> <span id="errText"></span></p>
  </div>

  <div class="box" id="none" hidden>
    <p>No authorization code is present in this page's address. If you were expecting one, start
    the connection again from the Creative Planning tool.</p>
  </div>

  <p class="note">The authorization code expires within minutes and can be used only once.
  Close this tab after you have pasted it.</p>

  <script>
  (function () {
    var q = new URLSearchParams(window.location.search);
    var code = q.get('code'), state = q.get('state'), realm = q.get('realmId'), err = q.get('error');
    if (err) {
      document.getElementById('err').hidden = false;
      document.getElementById('errText').textContent = err + (q.get('error_description') ? ': ' + q.get('error_description') : '');
      return;
    }
    if (!code) { document.getElementById('none').hidden = false; return; }
    document.getElementById('ok').hidden = false;
    document.getElementById('code').value = code;
    document.getElementById('state').value = state || '';
    document.getElementById('realm').value = realm || '';
    document.getElementById('copyAll').onclick = function () {
      var line = 'code=' + code + ' state=' + (state || '') + ' realmId=' + (realm || '');
      navigator.clipboard.writeText(line).then(function () {
        document.getElementById('copied').hidden = false;
      });
    };
    if (window.history && window.history.replaceState) {
      // keep the code out of browser history once displayed
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  })();
  </script>
""",
)

PRIVACY = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={PRIVACY_URL}">
<title>Privacy Policy | {APP}</title>
</head><body>
<p>Redirecting to the <a href="{PRIVACY_URL}">Creative Planning Privacy Policy</a>.</p>
</body></html>
"""

NOT_FOUND = shell(
    f"Not Found | {APP}",
    "Page Not Found",
    f"""
  <p>That address does not exist on this site. Try the <a href="{BASE_URL}/">overview</a> or the
  <a href="{BASE_URL}/eula.html">license agreement</a>.</p>
""",
)

FILES = {
    "index.html": INDEX,
    "eula.html": EULA,
    "connect.html": CONNECT,
    "disconnected.html": DISCONNECTED,
    "callback.html": CALLBACK,
    "privacy.html": PRIVACY,
    "404.html": NOT_FOUND,
    ".nojekyll": "",
}


def main() -> None:
    bad = []
    for name, html in FILES.items():
        for ch in ("—", "–"):
            # the base64 logo never contains these, so any hit is real copy
            if ch in html.replace(LOGO, ""):
                bad.append((name, ch))
        (SITE / name).write_text(html)
        print(f"wrote {name}: {len(html):,} bytes")
    if bad:
        sys.exit(f"dash characters found: {bad}")
    print(f"site -> {SITE}")


if __name__ == "__main__":
    main()
