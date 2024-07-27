import fitz
import io
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfReader, PdfWriter


def process_form(data):
    initial = {"Reading", "Walking", "Music"}
    date = datetime.strptime("11-02-1994", "%d-%m-%Y")
    yield data["name"]
    yield date.strftime("%b")
    yield str(date.day)
    yield str(date.year)
    yield data["address"]

    # Checkboxes
    favorites = data["favorites"][0].split(",")
    yield "Yes" if "Reading" in favorites else "Off"
    yield "Yes" if "Walking" in favorites else "Off"
    yield "Yes" if "Music" in favorites else "Off"

    other = list(set(favorites) - initial)
    yield "Yes" if len(other) >= 1 else "Off"
    yield other[0] if len(other) else ""

    # Radios
    yield "1" if data["favorite"] == "Reading" else "Off"
    yield "1" if data["favorite"] == "Walking" else "Off"
    yield "1" if data["favorite"] == "Music" else "Off"
    yield (
        "Off"
        if data["favorite"] in initial
        else ("1" if len(data["favorite"]) >= 1 else "Off")
    )
    yield "" if data["favorite"] in initial else data["favorite"]

    # Buttons
    yield "1"
    yield "1"


def update_form(pdf_bytes,data):
    pdf_document = fitz.open(stream=io.BytesIO(pdf_bytes))
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        for field,field_val in zip(page.widgets(),process_form(data)):
            if(field.field_type != fitz.PDF_WIDGET_TYPE_BUTTON):
                # if "Button" not in field.field_name:
                if field_val != 'Off':
                    field.field_value = field_val
                    field.field_flags = fitz.PDF_FIELD_IS_READ_ONLY
                    field.update()
                    
    output_stream = io.BytesIO()
    
    # Set Read only Permission
    permission = fitz.PDF_PERM_ACCESSIBILITY
    permission |= fitz.PDF_PERM_MODIFY    
    
    # Save
    pdf_document.save(output_stream, permissions=permission)
    output_stream.seek(0)
    return output_stream