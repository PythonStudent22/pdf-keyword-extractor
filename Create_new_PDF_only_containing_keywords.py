import PyPDF2

def extract_pages_with_keywords(pdf_path, keywords, output_pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        writer = PyPDF2.PdfWriter()
        pages_added = set()

        # Convert keywords to lowercase
        keywords_lower = [keyword.lower() for keyword in keywords]

        # Iterate through all pages
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()

            # Check if any keyword is present on the page
            if text:
                text_lower = text.lower()
                for keyword in keywords_lower:
                    if keyword in text_lower:
                        # Prevent adding duplicate pages
                        if page_num not in pages_added:
                            writer.add_page(page)
                            pages_added.add(page_num)
                        break  # Exit loop if a keyword is found

        # Check if any pages were added
        if pages_added:
            # Save the extracted pages to a new PDF
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)
            print(f"The pages with the keywords have been saved to {output_pdf_path}.")
        else:
            print("No pages with the specified keywords were found.")

# Add this block at the end of your script
if __name__ == '__main__':
    # Example input path, change this to the path of your PDF file
    pdf_path = '/path/to/your/input.pdf'

    # Example keywords, change this to the keywords you want to search for
    keywords = [
        'example_keyword_1',
        'example_keyword_2',
        'example_keyword_3',
        'example_keyword_4'
    ]

    # Example output path, change this to the path where you want to save the extracted pages
    output_pdf_path = '/path/to/your/output.pdf'

    extract_pages_with_keywords(pdf_path, keywords, output_pdf_path)
