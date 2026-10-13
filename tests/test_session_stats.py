import importlib.util
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "fixtures", "session.jsonl")

spec = importlib.util.spec_from_file_location(
    "session_stats", os.path.join(HERE, "..", "token-coach", "scripts", "session_stats.py"))
ss = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ss)


class SessionStatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = ss.analyse(FIXTURE)

    def test_only_user_prompts_are_counted(self):
        # typed x3 + suggestion_accepted x1; isMeta and promptSource "system" are excluded
        self.assertEqual(self.out["user_prompts"], 4)

    def test_older_transcripts_without_prompt_source(self):
        entry = {"type": "user", "message": {"role": "user", "content": "hello"}}
        self.assertEqual(ss.real_prompt(entry), "hello")
        entry["isMeta"] = True
        self.assertIsNone(ss.real_prompt(entry))

    def test_corrections_use_typed_text_not_pasted_blocks(self):
        self.assertEqual(self.out["prompt_stats"]["correction_style_prompts"], 1)
        self.assertTrue(ss.is_correction("no, I meant the other file"))
        self.assertFalse(ss.is_correction("log:\n```\nno wrong again\n```"))

    def test_subagent_tokens_read_from_subagents_folder(self):
        # streamed duplicates of one message count once, at the largest value
        self.assertEqual(self.out["subagent_output_tokens"], 500)

    def test_test_run_detection(self):
        run = lambda cmd: ss.diy_category({"name": "Bash", "cmd": cmd, "size": 0})
        self.assertEqual(run("mvn test"), "running_tests")
        self.assertEqual(run("mvn -q clean test"), "running_tests")
        self.assertIsNone(run("mvn test-compile"))
        self.assertEqual(run("git status"), "git_commands")

    def test_chained_commands_must_all_be_simple(self):
        run = lambda cmd: ss.diy_category({"name": "Bash", "cmd": cmd, "size": 0})
        self.assertEqual(run("git log --oneline | head -5"), "git_commands")
        self.assertEqual(run("cd repo && git add -A && git commit -F - <<'EOF'\nmsg\nEOF"),
                         "git_commands")
        self.assertIsNone(run("git status && mvn package"))
        self.assertIsNone(run("for f in *; do git add $f; done"))

    def test_tool_result_totals_group_by_tool(self):
        totals = {t["tool"]: t for t in self.out["tool_result_totals"]}
        self.assertEqual(totals["Bash"]["calls"], 1)
        self.assertEqual(totals["mcp:jira"]["calls"], 2)
        self.assertEqual(totals["mcp:jira"]["est_tokens"], 200)

    def test_output_is_json_serialisable_with_range_text(self):
        json.dumps(self.out)
        self.assertIn("combined_pct_text", self.out["estimated_savings"])


if __name__ == "__main__":
    unittest.main()
