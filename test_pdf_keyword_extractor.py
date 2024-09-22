import unittest
from unittest.mock import MagicMock, mock_open, patch
import PyPDF2
import io
from Create_new_PDF_only_containing_keywords import extract_pages_with_keywords

class TestExtractPagesWithKeywords(unittest.TestCase):
    def setUp(self):
        # Create a simple in-memory PDF file
        self.pdf_bytes = io.BytesIO()
        writer = PyPDF2.PdfWriter()

        # Create pages with content
        page1 = PyPDF2.pdf.PageObject.create_blank_page(None, 72, 72)
        page1_content = "This is a test page with keyword1."
        page1.insert_text(page1_content)
        writer.add_page(page1)

        page2 = PyPDF2.pdf.PageObject.create_blank_page(None, 72, 72)
        page2_content = "This page does not contain the keyword."
        page2.insert_text(page2_content)
        writer.add_page(page2)

        page3 = PyPDF2.pdf.PageObject.create_blank_page(None, 72, 72)
        page3_content = "Another test page with keyword2."
        page3.insert_text(page3_content)
        writer.add_page(page3)

        # Write the PDF to the in-memory bytes buffer
        writer.write(self.pdf_bytes)
        self.pdf_bytes.seek(0)

        # Define keywords
        self.keywords = ['keyword1', 'keyword2']

        # Mock output PDF path
        self.output_pdf_path = '/fake/path/output.pdf'

    @patch('builtins.open', new_callable=mock_open)
    @patch('PyPDF2.PdfReader')
    @patch('PyPDF2.PdfWriter')
    def test_extract_pages_with_keywords(self, mock_writer_class, mock_reader_class, mock_file):
        # Mock the PdfReader instance
        mock_reader = MagicMock()
        mock_reader.pages = []

        # Mock pages
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

        # Check that pages with keywords were added
        self.assertEqual(mock_writer.add_page.call_count, 2)
        mock_writer.add_page.assert_any_call(page1)
        mock_writer.add_page.assert_any_call(page3)

        # Check that the output PDF was written
        mock_writer.write.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('PyPDF2.PdfReader')
    @patch('PyPDF2.PdfWriter')
    def test_no_keywords_found(self, mock_writer_class, mock_reader_class, mock_file):
        # Mock the PdfReader instance
        mock_reader = MagicMock()
        mock_reader.pages = []

        # Mock pages without keywords
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

        # Check that no pages were added
        mock_writer.add_page.assert_not_called()

        # Check that write was not called since there are no pages
        mock_writer.write.assert_not_called()

if __name__ == '__main__':
    unittest.main()
