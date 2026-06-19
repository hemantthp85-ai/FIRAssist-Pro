import re

from app.rag.ingest_bns import extract_pdf_text


def extract_sections():

    text = extract_pdf_text()

    pattern = r"\n(\d+)\."

    matches = list(
        re.finditer(
            pattern,
            text
        )
    )

    sections = []

    for i in range(len(matches)):

        start = matches[i].start()

        if i < len(matches) - 1:

            end = matches[i + 1].start()

        else:

            end = len(text)

        section_text = text[start:end]

        section_number = matches[i].group(1)

        sections.append({
            "section": section_number,
            "text": section_text
        })

    return sections


if __name__ == "__main__":

    sections = extract_sections()

    print(f"\nTOTAL SECTIONS: {len(sections)}")

    print("\nFIRST SECTION:\n")

    print(
        sections[0]["text"][:1500]
    )