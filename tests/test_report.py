from datetime import date
import unittest

from albo_monitor.models import Act
from albo_monitor.report import redact_sensitive, render_telegram
from albo_monitor.telegram import split_message


class ReportTest(unittest.TestCase):
    def test_redact_sensitive(self):
        acts = [
            Act(repertorio="1", title="Determina lavori", typology="Determina"),
            Act(repertorio="2", title="Pubblicazione di matrimonio", typology="Stato civile"),
        ]
        safe, redacted = redact_sensitive(acts)
        self.assertEqual(len(safe), 1)
        self.assertEqual(redacted, 1)

    def test_render_telegram(self):
        acts = [Act(repertorio="1", title="Determina lavori", typology="Determina", start_date=date(2026, 6, 29))]
        text = render_telegram(acts, date(2026, 6, 22))
        self.assertIn("📋 Albo Pretorio", text)
        self.assertIn("🔹 1. Repertorio", text)

    def test_split_message(self):
        chunks = split_message("a\n" * 5000, limit=1000)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 1000 for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
