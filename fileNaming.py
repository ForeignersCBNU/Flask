def fileNaming(pathText):
    for startPoint in range(len(pathText)-1, 0, -1):
        if pathText[startPoint]=='\\':
            startPoint += 1
            break
    for endPoint in range(startPoint, len(pathText)):
        if pathText[endPoint]=='.':
            break
        
    fileName=f'{pathText[startPoint:endPoint]}'         #if path is a/b/c/d.docx -> fileName == d
    fileExtension = f'{pathText[endPoint:]}'         #if path is a/b/c/d.docx -> fileExtension == .docx
    newFilePath = f'{pathText[:endPoint]}.pdf'          #if path is a/b/c/d.docx -> newFilePath == a/b/c/d.pdf


    return fileName, fileExtension
