from flask import Flask, request, jsonify
import os
import fileProcessing

app = Flask(__name__)

UPLOAD_FOLDER = r"C:\flask_upload\uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({"message": "No selected file"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(save_path)

    try:
        result = fileProcessing.fileProcessing(save_path)
    except Exception as e:
        return jsonify({"message": f"Processing error: {str(e)}"}), 500

    # result must contain summary_pdf_path
    pdf_name = os.path.basename(result["summary_pdf_path"])
    pdf_path = f"https://changlit.com/summarizedCaption/{pdf_name}"

    return jsonify({
    "message": "File processed successfully",
    "summary_text": result["summary_text"],
    "summary_image": result["summary_image"],
    "text_pdf_url": f"https://changlit.com/summarizedCaption/{os.path.basename(result['pdf_path'])}"
})

