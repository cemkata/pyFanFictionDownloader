import urllib.request  # import the library used to query a website
import os
import time
import jinja2
import hashlib
from io import BytesIO
import gzip

from static import *


class downloader:
    def __init__(self, controller):
        self.autor = ''
        self.storyName = ''
        self.chapterNumber = 1
        self.outdirectory = ''
        self.folder = ''
        self.tableOfContent = ''
        self.date = ''
        self.publisher = ''
        self.done = True
        self.firstChapter = True
        self.error = True
        #self.errorText = ''
        self.webSiteController = controller

    def downloadPage(self, url):
        hdr = { 'User-Agent' : HTTP_USER_AGENT, 'Accept-encoding':'gzip'} # HTTP_USER_AGENT is defined in static
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response
        return data

    def download(self):
        inLink = self.webSiteController.getStoryLink()
        self.publisher = link = self.webSiteController.getPublisher()  # get website
        # link will be changed to get the next chapter
        # on the first iteration of the while loop we need the oroginal inLink

        # Read the head for the HTML files, becasue we strip the original
        head = readTemplate('head.html')
        body = readTemplate('body.html')
        try:
            while True:
                # Query the website and return the html to the variable 'page'
                page = self.downloadPage(inLink)

                contens = self.webSiteController.getPageContent(
                    page)  # get only the html containing the text without menu and and other stuff

                if self.chapterNumber == 1:  # if this is the first chapter we create a folder for the html files
                    temp = self.webSiteController.getDetails(contens)  # get author and fiction name
                    self.autor = temp[0]
                    self.storyName = temp[1]
                    try:
                        self.tableOfContent = self.webSiteController.getChapterList(contens)
                    except AttributeError:
                        self.tableOfContent = [self.storyName]
                    self.date = time.strftime("%a, %d %b %Y %H:%M:%S",
                                              time.gmtime())  # get time stamp for unique folder name
                    # timestam is needed for the epub too
                    mHash = hashlib.md5()
                    mHash.update((self.date + self.autor + ' - ' + self.storyName).encode('utf-8'))
                    self.folder = mHash.hexdigest()
                    self.outdirectory = os.path.join(DOWNLOAD_DIR,
                                                     self.folder)  # prepaer the folder name for the html files
                    # Create the folder
                    if not os.path.exists(self.outdirectory):
                        os.makedirs(os.path.join(self.outdirectory, "OEBPS"))

                    # Create the Cover page
                    chaptername = "/OEBPS/Cover.html"  # Prepare the file name
                    with open(self.outdirectory + chaptername, "a") as outFile:
                        outFile.write(head.render(titel=self.storyName))  # We write the head
                        #############################################################################
                        # Formating the header
                        # Then we format the head changin the titel to Chapter X
                        # In the head.html check jinja2 rendering
                        #############################################################################
                        page = self.webSiteController.getCoverPage(contens)
                        coverPage = '''<div style="text-align: center;"><h1>{}</h1><h3><i>by {}</i></h3><div style="text-align: left;">{}</div></div>'''
                        pageConten = coverPage.format(self.storyName, self.autor, page)
                        outFile.write(body.render(body=pageConten))  # The rest of the contens

                    if self.firstChapter:  # flag if the fist chapter is done. Needed for the webinterface
                        self.firstChapter = False

                chaptername = "/OEBPS/Chapter{}.html".format(self.chapterNumber)  # Prepare the file name
                with open(self.outdirectory + chaptername, "a") as outFile:
                    outFile.write(head.render(titel=self.tableOfContent[self.chapterNumber - 1]))  # We write the head
                    #############################################################################
                    # Formating the header
                    # Then we format the head changin the titel to Chapter X
                    # In the head.html check jinja2 rendering
                    #############################################################################
                    page = self.webSiteController.parsePage(contens)
                    outFile.write(body.render(body=page))  # The rest of the contens

                nextLink = self.webSiteController.getNextLink(contens)
                if nextLink == "NULL":  # when the last link is null we end with the download
                    outFile.close()
                    break

                # Wait for 1.5 seconds to prevent any firewall rules regarding fludattacks
                time.sleep(1.5)
                self.chapterNumber += 1
                inLink = link + nextLink

            ##################
            ##Debuging##
            ## TODO to clean
            # if self.chapterNumber == 3:
            #  # a = 1/0
            #   outFile.close()
            #   break
        except Exception as e:
#        except ZeroDivisionError as e: #Debug to pass all exceptions and only stop x/0
            self.error = False
            self.firstChapter = False
            #self.errorText = "Error"
            print(str(e))
            print(inLink)

        self.done = False


def readTemplate(template_file):
    template_file = os.path.join(EPUB_TEMPLATES_DIR, template_file)
    with open(template_file, 'r') as inFile:
        template = inFile.read()
    template = jinja2.Template(template)
    return template
