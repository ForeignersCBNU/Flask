from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = r"C:\flask_upload\uploads"   #Authorized path!
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "Hello World! We are Kim and Tsoi."


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "File Not Found", 400

    f = request.files['file']
    if f.filename == '':
        return "Selected File Not Found", 400

    save_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(save_path)
    return f"{f.filename} uploaded Completely"

@app.route('/pdfConverted', methods=['POST'])
def convert_file():
    return 0

@app.route('/summarizedCaption', methods=['POST'])
def summarize_file():
    return 0

if __name__ == "__main__":
    app.run()

