from datetime import date
import unittest

from albo_monitor.scraper import parse_listing_html, parse_date, page_url


HTML = """
<table>
  <thead>
    <tr><th>Repertorio</th><th>Titolo</th><th>Tipologia</th><th>Richiedente</th><th>Inizio</th><th>Fine</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>2026000500</td>
      <td><a href="/atto/500">Impegno di spesa per servizio</a></td>
      <td>Determina</td>
      <td>Area Tecnica</td>
      <td>29/06/2026</td>
      <td>14/07/2026</td>
    </tr>
  </tbody>
</table>
"""


class ParserTest(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("29/06/2026"), date(2026, 6, 29))
        self.assertEqual(parse_date("2026-06-29"), date(2026, 6, 29))
        self.assertIsNone(parse_date(""))

    def test_page_url(self):
        self.assertEqual(
            page_url("https://example.com/albo", 2),
            "https://example.com/albo?page=2",
        )

    def test_parse_listing_html(self):
        acts = parse_listing_html(HTML, "https://example.com/albo-pretorio?page=1")
        self.assertEqual(len(acts), 1)
        self.assertEqual(acts[0].repertorio, "2026000500")
        self.assertEqual(acts[0].typology, "Determina")
        self.assertEqual(acts[0].start_date, date(2026, 6, 29))
        self.assertEqual(acts[0].detail_url, "https://example.com/atto/500")


if __name__ == "__main__":
    unittest.main()
