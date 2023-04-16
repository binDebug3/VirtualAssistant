import PyPDF2
import nbformat
from nbconvert import PDFExporter


def merge_pdfs(file_path1, file_path2):
    """
    Merge two PDFs into one
    :param file_path1: (string) path to the first PDF
    :param file_path2: (string) path to the second PDF
    :return:
        True if the merge was successful, False otherwise
    """
    try:
        # Open the two PDF files in binary mode
        pdf1_file = open(file_path1, 'rb')
        pdf2_file = open(file_path2, 'rb')

        # Create a PDF reader object for each file
        pdf1_reader = PyPDF2.PdfFileReader(pdf1_file)
        pdf2_reader = PyPDF2.PdfFileReader(pdf2_file)

        # Create a PDF writer object to which the merged PDFs will be written
        pdf_writer = PyPDF2.PdfFileWriter()

        # Add the pages of the first PDF to the writer object
        for page_num in range(pdf1_reader.getNumPages()):
            page = pdf1_reader.getPage(page_num)
            pdf_writer.addPage(page)

        # Add the pages of the second PDF to the writer object
        for page_num in range(pdf2_reader.getNumPages()):
            page = pdf2_reader.getPage(page_num)
            pdf_writer.addPage(page)

        # Write the merged PDF to a new file
        new_file = file_path1[:-4] + '_merged.pdf'
        output_file = open(new_file, 'wb')
        pdf_writer.write(output_file)

        # Close the input and output files
        pdf1_file.close()
        pdf2_file.close()
        output_file.close()

        return True, new_file.split('/')[-1]

    except Exception as e:
        print(e)
        return False, None


def convert_notebook(notebook_path):
    """
    Convert a Jupyter notebook to a PDF file
    :param notebook_path: (string) path to the notebook file
    :return: True if the conversion was successful, False otherwise
    """
    try:
        # Load the notebook file
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)

        # Configure the PDF exporter
        pdf_exporter = PDFExporter()
        pdf_exporter.exclude_input = True  # Exclude input cells from the PDF

        # Export the notebook as a PDF
        new_name = notebook_path[:-6] + '.pdf'
        (body, resources) = pdf_exporter.from_notebook_node(nb)
        with open(new_name, 'wb') as f:
            f.write(body)

        return True, new_name.split('/')[-1]

    except Exception as e:
        print(e)
        return False, None


def extract_text(pdf_path):
    """
    Extract text from a PDF file
    :param pdf_path: (string) path to the PDF file
    :return: The text from the PDF file
    """
    try:
        # Open the PDF file and read its contents
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_text = ''
        for page in range(pdf_reader.numPages):
            pdf_text += pdf_reader.getPage(page).extractText()

        # Create a new text file and add the PDF text to it
        name = pdf_path[:-4] + '.txt'
        with open(name, 'w') as txt_file:
            txt_file.write(pdf_text)

        return True, name.split('/')[-1]

    except Exception as e:
        print(e)
        return False, None