import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from reusable_data_tools import DatabaseSettings, convert_delimited, read_header, transaction, clean_cell


class CoreTests(unittest.TestCase):
    def test_clean_cell(self):
        self.assertEqual(clean_cell(" hi\r\nthere\x00 "), "hi there")

    def test_delimited_round_trip(self):
        with TemporaryDirectory() as tmp:
            source, dest = Path(tmp) / "input.csv", Path(tmp) / "output.tsv"
            source.write_text('first,second\n"a,b",c\n', encoding="utf-8")
            self.assertEqual(convert_delimited(source, dest), 2)
            self.assertEqual(read_header(dest), ["first", "second"])
            self.assertIn("a,b\tc", dest.read_text())

    def test_sqlite_transaction(self):
        with TemporaryDirectory() as tmp:
            settings = DatabaseSettings("sqlite", "", str(Path(tmp) / "test.db"))
            with transaction(settings) as conn:
                conn.execute("CREATE TABLE item (id INTEGER)")
                conn.execute("INSERT INTO item VALUES (1)")
            with sqlite3.connect(settings.database) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM item").fetchone()[0], 1)

    def test_required_setting(self):
        from reusable_data_tools.config import required_env
        with self.assertRaisesRegex(RuntimeError, "MISSING_TEST_KEY"):
            required_env("MISSING_TEST_KEY")


if __name__ == "__main__":
    unittest.main()
