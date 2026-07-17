---
name: supply-chain-security
description: Before installing or recommending any package (npm, PyPI, MCP server), run checks to catch supply chain attacks, malicious versions, and postinstall script exploits.
scope: portable
globs: ["**/package.json", "**/package-lock.json", "**/node_modules/**", "**/requirements*.txt", "**/pyproject.toml", "**/setup.py", "**/Pipfile", "**/.mcp.json", "**/mcp.json", "**/claude_desktop_config.json"]
depends_on: []
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - DEPENDENCIES.md
---

## Supply-chain security check

Before installing or recommending any package, run these checks. `npm audit` and `pip-audit` only catch known CVEs. Supply chain attacks like the axios compromise (March 2026) and the Shai-Hulud campaigns (May 2026) had no CVE when the malicious versions were live.

### 1. Check for recent compromise reports

Before recommending a package, search for: `[package-name] npm malware` or `[package-name] npm compromised`. The axios attack (March 31, 2026) showed that even the most downloaded JavaScript library can be hijacked briefly. Brief is enough.

### 2. Verify the exact version before install

```bash
npm view <package> time --json         # check published timestamps for each version
npm view <package>@<version> dist-tags # check dist-tag assignments
```

Suspicious signal: a version published at an unusual hour, with an unexpected version jump, or with a new transitive dependency that wasn't in the prior version.

### 3. Inspect postinstall scripts before install

```bash
npm pack <package>@<version> --dry-run  # see what ships in the tarball
cat node_modules/<package>/package.json | jq '.scripts'
```

Red flag: a postinstall or install script in a package that has no legitimate reason to run code at install time (e.g., a utility library, an HTTP client). Also check transitive dependencies added in the same version bump.

### 4. Run audit after install

```bash
npm audit
npm audit --audit-level=high
```

This catches known CVEs. It does not catch zero-day supply chain attacks. Treat a clean audit as necessary but not sufficient.

### 5. Verify with Socket.dev (for high-trust packages)

socket.dev/npm/[package-name] does supply chain analysis beyond CVE databases. Useful before adding a new package to a production app.

### Reference case: axios March 2026

Malicious versions: axios@1.14.1 and axios@0.30.4
Live window: March 31, 2026, 00:21 to 03:15 UTC (about 2 hours)
Vector: injected fake dependency plain-crypto-js@4.2.1 with a RAT-dropping postinstall script targeting macOS, Windows, and Linux. Malware then self-deleted to evade forensic detection.
Attribution: Sapphire Sleet, a North Korean state actor (also tracked as UNC1069 by Google)
Safe versions: 1.14.0 and 0.30.3

If axios was installed during that window: rotate all secrets and credentials immediately.

### Apply when

- User runs or plans to run `npm install`
- User asks for package recommendations
- User upgrades a package to a new minor or major version
- Reviewing a `package.json` diff that adds new dependencies
- User shares a lockfile showing new packages

### PyPI: Python package checks

Apply when working in Django/Python projects (Atlas, Search) or adding Python dependencies.

#### 1. Check for recent compromise reports

Search for: `[package-name] pypi malware` or `[package-name] pypi compromised`. The Shai-Hulud campaigns (May 2026) hit PyPI alongside npm, compromising packages like Mistral AI and TanStack simultaneously across ecosystems.

#### 2. Run pip-audit before and after install

```bash
pip-audit                          # scan current environment
pip-audit -r requirements.txt      # scan requirements file
pip-audit --desc                   # include vulnerability descriptions
```

#### 3. Inspect before installing unfamiliar packages

```bash
pip download --no-deps <package>   # download without installing
pip show <package>                 # check installed package metadata
```

Red flag: a setup.py with network calls, subprocess execution, or obfuscated code. Legitimate packages do not need to phone home at install time.

#### 4. Verify with safety or Socket.dev

```bash
safety check                       # check against known malicious packages
```

socket.dev/pypi/[package-name] for supply chain analysis beyond CVE databases.

### MCP servers: the unmonitored attack surface

MCP servers run with your credentials and file system access. They are package-equivalent execution surfaces but are rarely audited. The Nx Console VS Code extension compromise (May 18, 2026) showed that editor/agent tooling is a real attack vector.

#### Before adding a new MCP server

1. Check the package name against recent advisories. Search: `[package-name] npm malware` (most MCP servers install via `npx`) or `[package-name] pypi malware` (for `uvx` servers).
2. The `npx -y <pkg>` pattern executes arbitrary code at invocation time with no install-time gate. Treat every `npx -y` in an MCP config as equivalent to `npm install --global`. When you control the invocation, pin the exact version (`pkg@1.4.8`, not `pkg@latest`) so a hijacked latest tag cannot run on your machine. This is worth doing even for a package you install yourself: pin the version in the config rather than trusting a `latest` tag.
3. Check the server's source repo: is it maintained? Does it have more than one contributor? When was the last commit?
4. Environment values in MCP configs often contain API keys and credentials. Never log, commit, or share MCP config files without redacting env blocks.
5. Provision least privilege. Give a new integration its own scoped credential, not your full-access one: a read-only token, a single-folder write scope, a separate service account. An agent with a tool inherits that tool's reach, so scope the reach down to exactly the job before connecting it (a pattern seen in chief-of-staff-style agent designs: scope each new integration's credential to exactly the job before connecting it).

#### Enable versus trust: a two-phase gate for executable extensions

Separate "content loaded" from "code allowed to run." They are different risk levels and deserve different gates.

- Passive content (a skill, a prompt template, an agent definition, a rule) may auto-load when enabled. It cannot execute on its own; the worst case is a bad instruction you can read.
- Executable surfaces (an MCP server, a hook, an LSP server, anything invoked via `npx`/`uvx`) stay inert until an explicit, logged trust decision, even after the extension is enabled. Enabling is not trusting.

Concretely: enabling a plugin or extension should load its skills and prompts but must not activate its hooks or MCP servers until you have reviewed the source and explicitly trusted it. Repo-local executable config (a project `.mcp.json`, a project hook) requires a folder-trust step before it can run, so cloning a hostile repo cannot silently wire up a server with your credentials. This enable-versus-trust split (passive parts load on enable, executable surfaces need an explicit trust step) is the cleaner default for the Meridian Inventory + approval gate in `ai-security-standards.md`: pair the two-phase gate with version-pinning (point 2 above) so a trusted server is also a pinned one.

#### Periodic audit

Run `bumblebee scan --profile baseline --ecosystem mcp` to inventory all configured MCP servers. Compare against your expected list. Flag any server you do not recognize.

### Cross-ecosystem principle: read before execute

Prefer reading metadata over executing package managers when you just need to inspect:
- npm: `npm pack --dry-run` (reads) over `npm ls` (can execute postinstall)
- PyPI: `pip download --no-deps` (downloads) over `pip install` (executes setup.py)
- MCP: read the config JSON directly before running `npx -y`

### Reference cases

#### axios March 2026 (npm)

Malicious versions: axios@1.14.1 and axios@0.30.4
Live window: March 31, 2026, 00:21 to 03:15 UTC (about 2 hours)
Vector: injected fake dependency plain-crypto-js@4.2.1 with a RAT-dropping postinstall script targeting macOS, Windows, and Linux. Malware then self-deleted to evade forensic detection.
Attribution: Sapphire Sleet, a North Korean state actor (also tracked as UNC1069 by Google)
Safe versions: 1.14.0 and 0.30.3

#### Shai-Hulud May 2026 (npm, PyPI, Composer, RubyGems, Go)

Scale: 324+ packages, 643+ versions across 5 ecosystems simultaneously
Targets: TanStack, Mistral AI, OpenSearch, AntV, Laravel Lang, and others
Key lesson: supply-chain security is not an npm problem or a Python problem. It is a cross-ecosystem problem.

If any compromised version was installed during the attack window: rotate all secrets and credentials immediately.

### Apply when

- User runs or plans to run `npm install`, `pip install`, or adds a new MCP server
- User asks for package recommendations (any ecosystem)
- User upgrades a package to a new minor or major version
- Reviewing a `package.json`, `requirements.txt`, or MCP config diff that adds new dependencies
- User shares a lockfile showing new packages

### Do NOT apply when

- cargo, gem, go get (not yet covered, separate security tooling)
- This repo has no package dependencies

The test: did I verify the package (any ecosystem) before recommending or installing it?
