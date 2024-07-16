from app.model.data_reader.pdf_reader import PDFReader



def test_pdf_reader():
    pdf_reader = PDFReader()
    documents = pdf_reader.extract_data("tests/utils/fake_context_files/MSc.pdf")
    assert documents[0].metadata["page"] == 1
    