import unittest
import os
import sys
import io
from contextlib import redirect_stdout
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logx import parse_level, cmd_tail, cmd_filter, cmd_count, cmd_stats


class TestParseLevel(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(parse_level("INFO starting"), "info")
        self.assertEqual(parse_level("ERROR failed"), "error")
        self.assertEqual(parse_level("WARN retrying"), "warn")
        self.assertEqual(parse_level("DEBUG details"), "debug")
        self.assertIsNone(parse_level("no level here"))


class TestTail(unittest.TestCase):
    def test_tail(self):
        p = os.path.join(os.path.dirname(__file__), "t.log")
        with open(p, "w") as f:
            f.write("line1\nline2\nline3\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_tail(type("A", (), {"file": p, "lines": 2})())
        lines = buf.getvalue().strip().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[-1], "line3")
        os.unlink(p)


class TestFilter(unittest.TestCase):
    def test_filter(self):
        p = os.path.join(os.path.dirname(__file__), "t2.log")
        with open(p, "w") as f:
            f.write("INFO msg1\nERROR msg2\nDEBUG msg3\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_filter(type("A", (), {"file": p, "level": "error"})())
        self.assertIn("ERROR msg2", buf.getvalue())
        self.assertNotIn("INFO msg1", buf.getvalue())
        os.unlink(p)


class TestCount(unittest.TestCase):
    def test_count(self):
        p = os.path.join(os.path.dirname(__file__), "t3.log")
        with open(p, "w") as f:
            f.write("INFO a\nERROR b\nINFO c\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_count(type("A", (), {"file": p})())
        out = buf.getvalue()
        self.assertIn("info: 2", out)
        self.assertIn("error: 1", out)
        os.unlink(p)


class TestStats(unittest.TestCase):
    def test_stats(self):
        p = os.path.join(os.path.dirname(__file__), "t4.log")
        with open(p, "w") as f:
            f.write("INFO a\nERROR b\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_stats(type("A", (), {"file": p})())
        out = buf.getvalue()
        self.assertIn("total lines: 2", out)
        os.unlink(p)


if __name__ == "__main__":
    unittest.main()
