from openai import OpenAI
from PIL import Image
import io
import fitz
from fpdf import FPDF
import fileNaming
import time
import os
import base64
import warnings
import json
from datetime import datetime


warnings.filterwarnings("ignore", category=UserWarning)  # FPDF 경고 숨김


def pil_to_base64_url(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    base64_data = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{base64_data}"


def doSummarize(path):

    # PDF 읽기
    doc = fitz.open(path)
    TextPage = []
    ImagePage = []

    for page in doc:
        TextPage.append(page.get_text())

        for img_info in page.get_images(full=True):
            xref = img_info[0]
            base = doc.extract_image(xref)
            image_bytes = base["image"]
            image = Image.open(io.BytesIO(image_bytes))
            ImagePage.append(image)

    # OpenAI 클라이언트
    client = OpenAI(api_key="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")

    # --- 텍스트 전체 문자열 ---
    fullText = "\n".join(TextPage)

    # --- 텍스트 요약 ---
    responseText = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Summarize this text in Korean."},
                    {"type": "input_text", "text": fullText}
                ]
            }
        ]
    )

    text_summary = responseText.output_text

    # --- 이미지 설명 ---
    responseImage = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Explain these images in Korean."},
                    *[
                        {
                            "type": "input_image",
                            "image_url": pil_to_base64_url(img)
                        }
                        for img in ImagePage
                    ]
                ]
            }
        ]
    )

    image_summary = responseImage.output_text

    # --- 파일명 ---
    fileName = fileNaming.fileNaming(path)[0]

    # --- PDF 저장 폴더 ---
    out_dir = r"C:\flask_upload\summarizedCaption"
    os.makedirs(out_dir, exist_ok=True)

    font_path = r"C:\flask_upload\fonts\malgun.ttf"

    # -------------------------------------------------------
    #   📌 하나의 PDF 안에 텍스트 요약 + 이미지 설명 넣기
    # -------------------------------------------------------
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('malgun', '', font_path, uni=True)
    pdf.set_font('malgun', '', 12)

    # 텍스트 요약
    pdf.multi_cell(0, 10, text_summary)

    pdf.ln(10)  # 줄바꿈

    # 구분선
    pdf.set_font('malgun', '', 12)
    pdf.multi_cell(0, 10, "----------------------------------------")
    pdf.ln(5)

    # 이미지 요약
    pdf.multi_cell(0, 10, image_summary)

    # PDF로 저장
    pdf.output(os.path.join(out_dir, f"{fileName}_Summary.pdf"))



    # -------------------------------------------------------
    #   📌 JSON 파일로도 저장
    # -------------------------------------------------------
    json_data = {
        "fileName": fileName,
        "text_summary": text_summary,
        "image_summary": image_summary,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    json_path = os.path.join(out_dir, f"{fileName}_Summary.json")

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)




    time.sleep(1)
