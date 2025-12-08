import fileNaming
import doByAI
import fitz
import os
import comtypes.client
import time
import shutil
import pythoncom
import threading

# Word/PPT formatting must be in single threads
convert_lock = threading.Lock()

def fileProcessing(path):
    pythoncom.CoInitialize()
    try:
        with convert_lock:

            # filename and extension
            fileName, extension = fileNaming.fileNaming(path)

            # input file path normalization
            filePath = os.path.normpath(path)

            # output PDF folder
            output_folder = r"C:\flask_upload\pdfConverted"
            os.makedirs(output_folder, exist_ok=True)

            # save path
            savePath = os.path.join(output_folder, fileName + ".pdf")

            print("Converting:", filePath)
            print("Saving to:", savePath)

            # ---------- convert section ----------
            if extension == '.pdf':
                shutil.copy(filePath, savePath)

            elif extension in ['.doc', '.docx']:
                word = comtypes.client.CreateObject("Word.Application")
                word.Visible = False
                doc = word.Documents.Open(filePath)
                doc.SaveAs(savePath, FileFormat=17)
                doc.Close()
                word.Quit()

            elif extension in ['.ppt', '.pptx']:
                powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
                powerpoint.Visible = False
                ppt = powerpoint.Presentations.Open(filePath, WithWindow=False)
                ppt.SaveAs(savePath, FileFormat=32)
                ppt.Close()
                powerpoint.Quit()

            else:
                print("Unsupported file type:", extension)
                return None
            

            # wait for file write
            time.sleep(0.5)

            # -------- AI summary (Only PDF) --------
            result = doByAI.doSummarize(savePath)

            # -----result must include these three-----

            # result["text_summary"]
            # result["image_summary"]
            # result["summary_pdf_path"]

            return result

    finally:
        pythoncom.CoUninitialize()
