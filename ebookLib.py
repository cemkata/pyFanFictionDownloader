import os
import shutil
import zipfile
import time
import string
import random
import subprocess
import jinja2 # template engine extenal lib needs to be installed
from bs4 import BeautifulSoup # library to work with HTML extenal lib needs to be installed
from weasyprint import HTML # library to create PDF extenal lib needs to be installed (this libry needs few others)
from static import *


class eBookCreater:

 def __init__(self, book, format):
     self.book = book # this should b an instance of downloader.py
     self.done = True
     self.error = True
     #self.errorText = ''
     # self.__worker is change to point diffrent method depending on the file format
     if format == 1:
       self.__worker = self.__createEpub
       self.FileExtension = '.epub'
       # epub
     elif format == 2:
       self.__worker = self.__epub2mobi
       self.FileExtension = '.mobi'
       # mobi
     elif format == 3:
       self.__worker = self.__createTXT
       self.FileExtension = '.txt'
       # txt
     elif format == 4:
       self.__worker = self.__createHTML
       self.FileExtension = '.html'
       # html
     elif format == 5:
       self.__worker = self.__createPDF
       self.FileExtension = '.pdf'
       # pdf
     elif format == 6:
       self.__worker = self.__getAll
       self.FileExtension = '.zip'
       # all(zip)

 def getTheBook(self):
     self.__setConversionFoler() #get the folder where the out put files should be stored
     try:
        self.__worker() # create the ebook in the needed format
     except Exception as e:
        self.error = False
        #self.errorText = "Error"
        print(str(e))

     self.__cleanUP() # delete all unneeded file except the requested formt in some case there is nothing to delete
     self.done = False # set the flag that the creation is complete needed fow the webinterface framework

 def __setConversionFoler(self):
    self.outPutPath = os.path.join(OUT_PUT_DIR, self.book.folder) # get the out put folder according to static.py
    if not os.path.exists(self.outPutPath):
        os.makedirs(self.outPutPath) # create the output folder
    self.outFile = os.path.join(self.outPutPath, self.book.storyName.translate(str.maketrans(FORBIDDENCHARACTERS)) + \
                                  ' - ' + self.book.autor.translate(str.maketrans(FORBIDDENCHARACTERS)))
    #Clear the forbiden chars from the file name (name format: "FicName - Autor")

 def __getAll(self): # generate all files and zip them
     #self.__createEpub()
     self.__epub2mobi() # mobi is conversion from epub!! it calls epub generation method
     self.__createTXT()
     self.__createHTML()
     self.__createPDF()
     # zipf is zipfile handle
     zipName = self.outFile +'.zip'
     zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
     # the next few lines will crate a zip with relative path
     abs_src = os.path.abspath(self.outPutPath)
     for file in os.listdir(self.outPutPath):
         if not file.endswith(".zip"):
             absname = os.path.abspath(os.path.join(self.outPutPath, file))
             arcname = absname[len(abs_src) + 1:]
             zipf.write(absname, arcname)
     zipf.close()

 def __cleanUP(self):
    try:
      for file in os.listdir(self.outPutPath):
         if not file.endswith(self.FileExtension):
             os.remove(os.path.join(self.outPutPath, file)) # delete all files except the requested format
      shutil.rmtree(self.book.outdirectory) # Clean up download folder with the chaptes.
    except OSError:
         pass # from time to time there is an error that a file is not delete pops

 def __createEpub(self):
    createMetadata(self.book) #create the static epub content
    self.__packEpub() # creat the .epub file

 def __packEpub(self):
     # zipf is zipfile handle
     zipName = self.outFile +'.epub'
     zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
     abs_src = os.path.abspath(self.book.outdirectory)
     # the next few lines will crate a zip with relative path
     for root, dirs, files in os.walk(self.book.outdirectory):
         for file in files:
             absname = os.path.abspath(os.path.join(root, file))
             arcname = absname[len(abs_src) + 1:]
             zipf.write(absname, arcname)
     zipf.close()

 # generate a single html file as a string
 def __mergeEpubChapters(self):
   htmlPath = os.path.join(self.book.outdirectory, 'OEBPS')
   if os.path.exists(htmlPath):
     body = "<!DOCTYPE html><html>"
     first = True
     for file in sorted(os.listdir(htmlPath)):
       if file.endswith(".html"):
         htmlFile = os.path.join(htmlPath, file)
         with open(htmlFile, 'r') as inFile:
              page = inFile.read()
         soup = BeautifulSoup(page, features="html5lib")
         if first:
            # load and render the templates
            # templateText = readTemplate('css.html')
            templateText = readTemplate('head.html')
            renderedTemplate = templateText.render(titel = self.book.storyName + " - " + self.book.autor, html = True)
            body = body + renderedTemplate
            body = body + "<body>"
            first = False
         body = body + str(soup.findAll('body')[0])
     body = body + "</body></html>"
     return body

 # clear the html tags and save the txt file
 def __createTXT(self):
   html = self.__mergeEpubChapters()
   soup = BeautifulSoup(html, features="html5lib")
   soup = soup.findAll('p')
   text = ''
   with open(self.outFile+'.txt', "a") as outFile:
     for i in soup:
        outFile.write(i.get_text() + '\n')

 # first generate the html and the export to PDF
 def __createPDF(self):
   self.__createHTML()
   HTML(self.outFile+'.html').write_pdf(self.outFile+'.pdf')

 def __epub2mobi(self):
   self.__createEpub()
   subprocess.run(["ebook-convert", str(self.outFile+'.epub'), str(self.outFile+'.mobi')])

 # save the html file
 def __createHTML(self):
   html = self.__mergeEpubChapters()
   with open(self.outFile+'.html', "a") as outFile:
        outFile.write(html)

#End of the class


#Methods needed for the epub creation
def readTemplate(template_file): #load the templates
        template_file = os.path.join(EPUB_TEMPLATES_DIR, template_file)
        with open(template_file, 'r') as inFile:
                template = inFile.read()
        template = jinja2.Environment(loader=jinja2.FileSystemLoader(EPUB_TEMPLATES_DIR)).from_string(template)
        #template = jinja2.Template(template)
        return template

def saveTemplates(otputFolder,templateList):
      opfTemplate="/OEBPS/book.opf"
      with open(otputFolder + opfTemplate, "a") as outFile:
           outFile.write(templateList[0])

      ncxTemplate="/OEBPS/book.ncx"
      with open(otputFolder + ncxTemplate, "a") as outFile:
           outFile.write(templateList[2])

      tocTemplate="/OEBPS/toc.xhtml"
      with open(otputFolder + tocTemplate, "a") as outFile:
           outFile.write(templateList[1])

def copyStatic(destinationFolder): #files without any chages, but needed for the epub format
        minetype_template = os.path.join(EPUB_TEMPLATES_DIR, 'mimetype.txt')
        shutil.copy(minetype_template, os.path.join(destinationFolder, 'mimetype'))
        #Add the meta information
        directoryMetaINF = os.path.join(destinationFolder, "META-INF")
        if not os.path.exists(directoryMetaINF):
             os.makedirs(directoryMetaINF)
        container_template = os.path.join(EPUB_TEMPLATES_DIR, 'container.xml')
        shutil.copy(container_template, os.path.join(directoryMetaINF, 'container.xml'))
        #Add css stile sheet
        css_style = os.path.join(EPUB_TEMPLATES_DIR, 'epub.css')
        shutil.copy(css_style, os.path.join(destinationFolder, 'OEBPS/epub.css'))

def renderTemplates(inData):
        idList = range(len(inData.tableOfContent)) #create the IDs
        playOrderList = [n + 1 for n in idList]
        titleList = [c for c in inData.tableOfContent]
        linkList = ["Chapter{}.html".format(n + 1) for n in idList]
        chapters = []
        #prepare the chaptes to be rendert in the template
        for i,p,t,l in zip(idList, playOrderList, titleList, linkList):
            chapter = {'id': i,
                       'play_order': p,
                       'title': t,
                       'link': l}
            chapters.append(chapter)

        uid = genUID() #book id needed for the epub

        # load and render the templates
        templateText = readTemplate('toc_ncx.xml')
        renderedNcxTemplate = templateText.render(chapters = chapters, uid = uid, titel = inData.storyName
                                                  , author = inData.autor)

        templateText = readTemplate('toc.html')
        renderedTocTemplate = templateText.render(chapters = chapters)

        templateText = readTemplate('opf.xml')
        renderedOpfTemplate = templateText.render(chapters = chapters, titel = inData.storyName,
                                                  creator = inData.autor, language = 'EN',
                                                  rights = "fanfic", publisher = inData.publisher,
                                                  uid = uid, date = inData.date)

        return (renderedOpfTemplate, renderedTocTemplate, renderedNcxTemplate)

def genUID(length = 20):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

def createMetadata(data):
    copyStatic(data.outdirectory)
    templates = renderTemplates(data)
    saveTemplates(data.outdirectory, templates)
