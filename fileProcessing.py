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
        # Word/PPT formatting only in one thread
        with convert_lock:

            # filename and extension
            fileName = fileNaming.fileNaming(path)[0]
            extension = fileNaming.fileNaming(path)[1]

            # input file path normalization
            filePath = os.path.normpath(path)

            # output PDF folder
            output_folder = r"C:\flask_upload\pdfConverted"
            os.makedirs(output_folder, exist_ok=True)

            # save path
            savePath = os.path.join(output_folder, fileName + ".pdf")

            print("Converting:", filePath)
            print("Saving to:", savePath)

            # ---------- about extension ----------
            if extension == '.pdf':
                # PDF
                shutil.copy(filePath, savePath)


            elif extension in ['.doc', '.docx']:
                word = comtypes.client.CreateObject("Word.Application")
                word.Visible = False

                doc = word.Documents.Open(filePath)
                doc.SaveAs(savePath, FileFormat=17)  # 17 = PDF
                doc.Close()
                word.Quit()


            elif extension in ['.ppt', '.pptx']:
                powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
                powerpoint.Visible = False

                ppt = powerpoint.Presentations.Open(filePath, WithWindow=False)
                ppt.SaveAs(savePath, FileFormat=32)  # 32 = PDF
                ppt.Close()
                powerpoint.Quit()


            else:
                print("Unsupported file type:", extension)
                return

            # wait...
            time.sleep(0.5)

            # -------- AI summary (Only PDF) --------
            doByAI.doSummarize(savePath)

    finally:
        pythoncom.CoUninitialize()

    return os.path.join(r"C:\flask_upload\summarizedCaption", f"{fileName}_Summary.pdf")




"""
    TextPage=[]
    i=-1

    for page in doc:
        i+=1
        texts = page.get_text()
        TextPage.append(texts)

    print(TextPage)
"""
