# Example project (Atlas)

This folder is a stand-in for a real software project. In the fabricated example this repo uses throughout, it represents Atlas, a web platform, and it is the one folder that would carry its own language, framework, and build tooling once you replace it with actual code.

Nothing here is meant to run. It exists so the two glob-scoped rules in `.claude/rules/atlas-production-standards.md` and `.claude/rules/atlas-production-examples.md` have a real path to attach to (`Work/example-project/**`), and so `GETTING_STARTED.md` has a concrete folder to point at during setup.

## What to do with this folder

Delete everything in it and put your real project here, or point the two `atlas-production-*` rule globs at wherever your real code actually lives. Either works. The rules themselves describe security and code quality patterns (parameterized SQL, escaped user input, no secrets in logs) that apply to any Django or similar backend, not anything specific to this placeholder.

See [GETTING_STARTED.md](../../GETTING_STARTED.md) for the full one-time setup pass.
