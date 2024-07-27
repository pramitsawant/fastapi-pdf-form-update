from typing import Annotated, List, Union
import json
from fastapi import Depends, Form, Response, FastAPI, File, UploadFile

from forms.UserForm import FormPayload
from utils.pdf import update_form

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/pdf")
async def create_upload_file(form_data: FormPayload = Depends()):
    pdf_bytes = await form_data.pdf.read()
    data = json.loads(form_data.model_dump_json(exclude={"pdf"}))
    output_stream = update_form(pdf_bytes,data)
    return Response(output_stream.read(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=new_pdf.pdf"})