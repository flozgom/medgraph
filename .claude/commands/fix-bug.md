---
description: Fix a bug test-first, with tests locked while fixing
argument-hint: <short bug description>
---

Bug: $ARGUMENTS

1. Write ONE failing test in `tests/` that reproduces the bug. Run `make test` and confirm it fails
   for the right reason. Show me the failure.
2. Stop and ask me to commit the test and enable fix-mode (`touch .claude/fix-mode`). While fix-mode
   is on, the `protect_paths` hook makes `tests/` read-only.
3. After I confirm, change only files under `medgraph/` until `make check` passes.
4. Summarise the root cause in one sentence, and suggest whether it deserves a line under
   Corrections in CLAUDE.md.
