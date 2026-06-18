from pypdf import PdfReader

PDF_PATH = "data/bns/BNS_2023.pdf"


def extract_pdf_text():

    reader = PdfReader(PDF_PATH)

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text


def chunk_text(text, chunk_size=1000):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks


if __name__ == "__main__":

    text = extract_pdf_text()

    chunks = chunk_text(text)

    print(f"\nTOTAL CHARACTERS: {len(text)}")

    print(f"\nTOTAL CHUNKS: {len(chunks)}")

    print("\nFIRST CHUNK:\n")

    print(chunks[0])