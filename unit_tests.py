import unittest
from unittest.mock import MagicMock, mock_open, patch
from Create_new_PDF_only_containing_keywords import extract_pages_with_keywords

class TestExtractPagesWithKeywords(unittest.TestCase):
    def setUp(self):
        # Define keywords
        self.keywords = ['keyword1', 'keyword2']
        # Mock output PDF path
        self.output_pdf_path = '/fake/path/output.pdf'

    @patch('PyPDF2.PdfWriter')
    @patch('PyPDF2.PdfReader')
    @patch('builtins.open', new_callable=mock_open)
    def test_extract_pages_with_keywords(self, mock_file, mock_reader_class, mock_writer_class):
        # Mock the PdfReader instance
        mock_reader = MagicMock()
        mock_reader.pages = []

        # Create mock pages with text
        page1 = MagicMock()
        page1.extract_text.return_value = "This is a test page with keyword1."
        page2 = MagicMock()
        page2.extract_text.return_value = "This page does not contain the keyword."
        page3 = MagicMock()
        page3.extract_text.return_value = "Another test page with keyword2."
        mock_reader.pages = [page1, page2, page3]

        mock_reader_class.return_value = mock_reader

        # Mock the PdfWriter instance
        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        # Call the function under test
        extract_pages_with_keywords('/fake/path/input.pdf', self.keywords, self.output_pdf_path)

        # Assert that pages with keywords were added
        self.assertEqual(mock_writer.add_page.call_count, 2)
        mock_writer.add_page.assert_any_call(page1)
        mock_writer.add_page.assert_any_call(page3)

        # Assert that the output PDF was written
        mock_writer.write.assert_called_once()

    @patch('PyPDF2.PdfWriter')
    @patch('PyPDF2.PdfReader')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_keywords_found(self, mock_file, mock_reader_class, mock_writer_class):
        # Mock the PdfReader instance
        mock_reader = MagicMock()
        mock_reader.pages = []

        # Create mock pages without keywords
        page1 = MagicMock()
        page1.extract_text.return_value = "This is a test page with no keywords."
        page2 = MagicMock()
        page2.extract_text.return_value = "Another page without any keywords."
        mock_reader.pages = [page1, page2]

        mock_reader_class.return_value = mock_reader

        # Mock the PdfWriter instance
        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        # Call the function under test
        extract_pages_with_keywords('/fake/path/input.pdf', self.keywords, self.output_pdf_path)

        # Assert that no pages were added
        mock_writer.add_page.assert_not_called()

        # Assert that write was not called since there are no pages
        mock_writer.write.assert_not_called()

if __name__ == '__main__':
    unittest.main()
