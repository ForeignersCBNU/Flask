from flask import Flask, request, jsonify
import os
import fileProcessing

app = Flask(__name__)

UPLOAD_FOLDER = r"C:\flask_upload\uploads"   #Authorized path!
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "Hello World! We are Kim and Tsoi."


@app.route('/upload', methods=['POST'])

def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    f = request.files['file']

    if f.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # 1️⃣ 파일 저장
    save_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(save_path)

    # 2️⃣ 요약 PDF 생성
    try:
        summary_pdf_path = fileProcessing.fileProcessing(save_path)
    except Exception as e:
        return jsonify({"message": f"Processing error: {str(e)}"}), 500

    # 3️⃣ URL로 변환 (Android에서 접근 가능하도록)
    file_name = os.path.basename(summary_pdf_path)
    pdf_url = f"https://changlit.com/summarizedCaption/{file_name}"

    # 4️⃣ JSON 응답
    return jsonify({
        "message": "File processed successfully",
        "text_pdf_url": pdf_url
    }), 200


"""
    save_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(save_path)
    return f"{f.filename} uploaded Completely"
"""

@app.route('/pdfConverted', methods=['POST'])
def convert_file():
    return 0

@app.route('/summarizedCaption', methods=['POST'])
def summarize_file():
    return 0

if __name__ == "__main__":
    app.run()

