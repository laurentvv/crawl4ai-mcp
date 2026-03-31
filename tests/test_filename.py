from unittest.mock import patch
from datetime import datetime

from crawl4ai_mcp import generate_filename_from_url

class TestGenerateFilenameFromUrl:
    @patch("crawl4ai_mcp.datetime")
    def test_standard_url(self, mock_datetime):
        # Configuration du mock pour datetime.now()
        mock_now = datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime.now.return_value = mock_now

        # Test avec une URL standard
        url = "https://example.com/some/path"
        result = generate_filename_from_url(url)

        # Le nom de domaine "example.com" devrait devenir "example_com"
        assert result == "crawl_example_com_20231027_143000.md"

    @patch("crawl4ai_mcp.datetime")
    def test_subdomain_url(self, mock_datetime):
        mock_now = datetime(2024, 1, 1, 0, 0, 0)
        mock_datetime.now.return_value = mock_now

        # Test avec des sous-domaines multiples
        url = "https://a.b.c.example.org/test"
        result = generate_filename_from_url(url)

        # Tous les points doivent être remplacés par des tirets bas
        assert result == "crawl_a_b_c_example_org_20240101_000000.md"

    @patch("crawl4ai_mcp.datetime")
    def test_url_with_port(self, mock_datetime):
        mock_now = datetime(2023, 12, 31, 23, 59, 59)
        mock_datetime.now.return_value = mock_now

        # Test avec un port dans l'URL
        url = "http://localhost:8080/api/data"
        result = generate_filename_from_url(url)

        # Le port fait partie du netloc, le deux-points est conservé (ou traité selon l'implémentation)
        # urllib.parse.urlparse("http://localhost:8080/api/data").netloc -> "localhost:8080"
        assert result == "crawl_localhost:8080_20231231_235959.md"

    @patch("crawl4ai_mcp.datetime")
    def test_no_scheme_url(self, mock_datetime):
        mock_now = datetime(2022, 5, 15, 8, 15, 30)
        mock_datetime.now.return_value = mock_now

        # Test avec une URL sans schéma (ex: juste un domaine)
        url = "example.com"
        result = generate_filename_from_url(url)

        # Pour "example.com" sans schéma, urlparse le considère souvent comme le "path" et non le "netloc".
        # Dans ce cas, netloc est vide.
        assert result == "crawl__20220515_081530.md"
