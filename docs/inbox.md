# Inbox

- It would be nice to have rqmd-docs have a skill to check for dead links:
    - First check for local links being broken (lightning fast)
    - Then check for external links being broken (slower, do asyncronously)
    - Script that did this in a different project:

```
python3 - << 'PYEOF'
import re, os
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')

# Directories to skip
SKIP_DIRS = {'node_modules', '.venv', '.venv3.12', 'build', 'dist', '.git', 'cassettes'}

md_files = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if f.endswith('.md'):
            md_files.append(os.path.join(root, f))

broken_internal = []
all_external = {}  # url -> [(src, text)]

for md_file in sorted(md_files):
    with open(md_file, 'r', encoding='utf-8', errors='replace') as fh:
        content = fh.read()
    base_dir = os.path.dirname(md_file)
    for match in LINK_RE.finditer(content):
        text, url = match.group(1), match.group(2)
        url_no_frag = url.split('#')[0]
        if url.startswith('http://') or url.startswith('https://'):
            if url_no_frag:
                all_external.setdefault(url_no_frag, []).append((md_file, text, url))
        elif not url.startswith('mailto:') and url_no_frag:
            target = os.path.normpath(os.path.join(base_dir, url_no_frag))
            if not os.path.exists(target):
                broken_internal.append((md_file, text, url, target))

print("=== BROKEN INTERNAL LINKS ===")
if broken_internal:
    for src, text, url, target in broken_internal:
        print(f"  {src}: [{text}]({url})")
else:
    print("  (none)")

print(f"\nChecking {len(all_external)} unique external URLs...")

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
        with urllib.request.urlopen(req, timeout=6) as resp:
            return url, resp.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception as e:
        return url, str(e)

results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(check_url, u): u for u in all_external}
    for fut in as_completed(futs):
        url, status = fut.result()
        results[url] = status

print("\n=== EXTERNAL 4XX ===")
found_4xx = False
for url, status in sorted(results.items(), key=lambda x: str(x[1])):
    if isinstance(status, int) and 400 <= status < 500:
        found_4xx = True
        for src, text, orig_url in all_external[url]:
            print(f"  HTTP {status}  {src}: [{text}]({orig_url})")
if not found_4xx:
    print("  (none)")

print("\n=== OTHER ERRORS (5xx / connection failures) ===")
found_other = False
for url, status in sorted(results.items(), key=lambda x: str(x[1])):
    if not isinstance(status, int) or status >= 500:
        found_other = True
        for src, text, orig_url in all_external[url]:
            print(f"  {status}  {src}: [{text}]({orig_url})")
if not found_other:
    print("  (none)")

print("\n=== ALL EXTERNAL STATUSES ===")
for url, status in sorted(results.items()):
    print(f"  {status}  {url}")
PYEOF
```

-  I have a full telemetry server set up that we haven't even used yet to ingest feedback from! 
- When providing a list of instructions, often times it is possible to embed a 'start page' hyperlink if the instructions start with "login here" or "go to this page" or "open this page" -- we can hyperlink the page in the instruction text. That way, when a user follows the instructions, the first instruction will have an actionable link that will get them started in the rigth place instead of having to figure out "where are the GitHub Actions for this repo..?"
- Is the fact that inbox.md is only temporarially holding items mean that it is gonna be an issue on multiuser repos where lots of ppl might churn through the inbox? As long as each item is a line item, git is quite good at merging line-item churn, so maybe not? Maybe we just need to make sure to keep items small and atomic so that they can be easily merged if multiple people are adding items at the same time?
-  "Agent Context File" is a term maybe??
- Brainstorm.md, inbox.md, and any other md files we depend on should have some basic boilerplate/discussion of purpose at the top and instructison on hwo to use it as if it were just a MD doc (but also still nudge them towards using it as an agent context file)... 
- When upgrading the rqmd VS Code extension, VS Code should try to install the newest version of rqmd CLI tool at the same time! OBVIOUS! Hopefully vscode extension marketplace supports this kind of paired release.
- Get rid of `reqmd` entirely -- we shouldn't have an extra name for our tool, just `rqmd`!
- rqmd should not do a  `git push --force` without explicit acknowledgement from teh user. This is a risky operation!
- Add a custom icon for the rqmd VS Code extension (`package.json` top-level `icon` field, 128×128 PNG). Currently shows as generic in the chat mode picker. Agent/Ask/Plan icons are VS Code built-ins — track whether `chatAgents` gains per-agent icon support in future API.
- UX pain: After updating/reinstalling the rqmd extension, VS Code silently deselects "rqmd" mode and falls back to "Agent" — the user doesn't notice and starts chatting without rqmd context. Need a way to detect this and/or persist mode selection across extension updates. Could be: (1) extension activation checks if rqmd was the last mode and re-selects it, (2) a visual cue when running in non-rqmd mode in an rqmd workspace, or (3) VS Code API for sticky mode selection.
- [tech-debt] RQMD-EXT-087 refinement: when `/tech-debt` encounters "implemented-but-unreferenced" reqs, recommend "annotate tests/source with `# RQMD-*` xref comments" as a batch action instead of "consider deprecating." Depends on RQMD-CORE-056 adding `"reason": "xref_gap"` to `--staleness --json`.
