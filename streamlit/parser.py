import os
import re

import fitz  # PyMuPDF
from newspaper import Article


def pdf_to_txt(pdf_path, output_txt_path):
    """
    Converts a PDF file to a text file, separating regular text and LaTeX symbols,
    and removes unnecessary newline characters.

    :param pdf_path: Path to the input PDF file.
    :param output_txt_path: Path where the output text file will be saved.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"The file '{pdf_path}' does not exist.")

    latex_pattern = r"(\$.*?\$|\$\$.*?\$\$|\\\[.*?\\\])"  # Regex for inline and block LaTeX

    with fitz.open(pdf_path) as pdf:
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                text = page.get_text("text")

                # Remove unnecessary newlines within text
                text = re.sub(r'\n{2,}', '\n', text).strip()

                # Split text based on LaTeX pattern
                segments = re.split(latex_pattern, text)

                # Write each segment, tagging LaTeX separately
                txt_file.write(f"--- Page {page_num + 1} ---\n")
                for segment in segments:
                    if re.match(latex_pattern, segment):
                        txt_file.write(f"[LaTeX]: {segment}\n")
                    else:
                        # Clean multiple internal newlines
                        segment_cleaned = re.sub(r'\n+', ' ', segment).strip()
                        txt_file.write(segment_cleaned + " ")
                txt_file.write("\n\n")
    with open(output_txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def url_to_txt(url, output_txt_path):
    """
    Extracts article content from a URL and saves it as a text file.

    :param url: The URL of the article.
    :param output_txt_path: Path where the output text file will be saved.
    """
    article = Article(url)
    article.download()
    article.parse()  # Parses the article content

    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(article.title + "\n\n")  # Add title
        txt_file.write(article.text)  # Add main content

    print(f"Article content saved to '{output_txt_path}'.")
    with open(output_txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content
