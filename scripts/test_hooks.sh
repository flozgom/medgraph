#!/usr/bin/env bash
# Self-test for the guardrail hooks: each case feeds a fake tool call on stdin
# and checks the exit code (0 = allowed, 2 = blocked).
set -u
cd "$(dirname "$0")/.."
export CLAUDE_PROJECT_DIR="$PWD"
fail=0

expect() {  # expect <exit-code> <hook> <json> <label>
  echo "$3" | python3 ".claude/hooks/$2" 2>/dev/null
  got=$?
  if [ "$got" -eq "$1" ]; then echo "ok   $4"; else echo "FAIL $4 (got $got, want $1)"; fail=1; fi
}
edit() { echo "{\"tool_input\":{\"file_path\":\"$PWD/$1\"}}"; }
bash_cmd() { echo "{\"tool_input\":{\"command\":\"$1\"}}"; }

expect 0 protect_paths.py "$(edit medgraph/ingest/fhir.py)" "package edit allowed"
expect 2 protect_paths.py "$(edit .github/workflows/ci.yml)" "CI workflow protected"
expect 2 protect_paths.py "$(edit .claude/hooks/git_gate.py)" "hooks protected"
expect 2 protect_paths.py "$(edit data/snomed/terms.csv)" "SNOMED release protected"
expect 2 protect_paths.py "$(edit evals/tasks/001-x.yaml)" "agent eval tasks protected"
expect 2 protect_paths.py "$(edit benchmarks/dev-baseline.json)" "eval baseline protected"
expect 0 protect_paths.py "$(edit medgraph/gold/oracle.py)" "oracle editable before gold-lock"
expect 0 protect_paths.py "$(edit tests/test_schema.py)" "tests editable normally"
touch .claude/gold-lock .claude/fix-mode
expect 2 protect_paths.py "$(edit medgraph/gold/oracle.py)" "oracle locked by gold-lock"
expect 2 protect_paths.py "$(edit data/gold/gaps.jsonl)" "gold labels locked by gold-lock"
expect 2 protect_paths.py "$(edit tests/test_schema.py)" "tests locked in fix-mode"
rm -f .claude/gold-lock .claude/fix-mode

expect 0 no_secrets.py '{"tool_input":{"content":"SNOMED_CKD = \"709044004\""}}' "concept IDs allowed"
expect 2 no_secrets.py '{"tool_input":{"content":"key = \"sk-ant-api03-abcdefghijklmnopqrstuv\""}}' "Anthropic key blocked"
expect 2 no_secrets.py '{"tool_input":{"new_string":"api_key = \"supersecretvalue123\""}}' "secret assignment blocked"
expect 2 no_secrets.py '{"tool_input":{"file_path":"/r/tests/fixtures/x.tsv","content":"id\teffectiveTime\tactive\tmoduleId\tconceptId"}}' "RF2 content blocked in repo"
expect 0 no_secrets.py '{"tool_input":{"file_path":"/r/data/snomed/x.tsv","content":"id\teffectiveTime\tactive\tmoduleId\tconceptId"}}' "RF2 content allowed under data/"

expect 0 git_gate.py "$(bash_cmd 'git push origin flozgom/feature')" "feature push allowed"
expect 2 git_gate.py "$(bash_cmd 'git push origin main')" "push to main blocked"
expect 2 git_gate.py "$(bash_cmd 'git push --force origin x')" "force push blocked"
expect 2 git_gate.py "$(bash_cmd 'git add -f data/snomed/terms.csv')" "force add blocked"
expect 2 git_gate.py "$(bash_cmd 'git add data/gold/gaps.jsonl')" "staging data/ blocked"
expect 0 git_gate.py "$(bash_cmd 'git add medgraph/config.py')" "normal add allowed"

exit $fail
