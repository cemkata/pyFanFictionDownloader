#!/usr/bin/python3
from gevent import monkey;
monkey.patch_all()

import time, threading
import shutil
import os
from bottle import route, static_file, request, abort, redirect, Bottle as createBottleAppObject
import json

from captcha import getCaptha, checkCaptha
from downloader import downloader
from ebookLib import eBookCreater
from controller import getControler
from static import *  # all static and and changeble content

webAppFicDownloader = application = app= createBottleAppObject()  # Bottle()


@webAppFicDownloader.route('/download', method='POST')
def downloadFic():
    inLink = request.forms.get('ficURL')
    fileFormat = int(request.forms.get('ficFormat'))

    if inLink.count('.') < 1:  #
       abort(400, "")          # check that the link doesn't point to local path
    if inLink.startswith('/'): # beter safe than sory
       abort(400, "")          #

    c = getControler(inLink)  # find and create the controlle that will extract
                              #only the fiction text (with out any header, foote rand etc) from the site

    d = downloader(c)  # downloder that will down load each chapter it uses the controler from above to clear the text
    e = eBookCreater(d, fileFormat)  # creates the ebook

    threading.Timer(0.01, getFanFic, (d, e)).start()  # timer to start the download and conversion
                                                      # it is a thread to alow providing a status of the
                                                      # download to the browser

    # give the downloader few seconds to get the details
    while d.firstChapter:  # Wait until this fist page is ready
        time.sleep(0.1) # do not use pass becasue the cpu is clocked and the flag for fist chapter is never changed
                        # with wait it works

    yield d.storyName + " - " + d.autor + ";;;"
    maxChapter = len(d.tableOfContent)
    yield str(maxChapter) + ";;;"

    while d.done:  # Wait untill the book is downloaded and give the status of the downloaded chapters
        yield str(d.chapterNumber) + ";;;"
        time.sleep(1)  # wait 1 second just not to spam the client

    if not d.error:  # In case there is an error
        abort(400, "")

    while e.done:  # Wait until the book is created same as above
        yield "Creating e-book file;;;-1;;;"
        time.sleep(1)

    if not e.error:
        abort(400, "")

    threading.Timer(600, cleanUP, (d.folder, 0)).start()  # create a time do delete the e-book file
                                                          # after 10 minutes (600 seconds)

    yield str(d.folder)  # return the id for downloading the file


def getFanFic(*arg):  # threading.Timer(0.01, getFanFic, (d, e)).start()
    arg[0].download()
    if arg[0].error:
       arg[1].getTheBook()


def cleanUP(*arg):  # threading.Timer(600, cleanUP, (d.folder, 0)).start()
    outputPad = os.path.join(OUT_PUT_DIR, arg[0])
    shutil.rmtree(outputPad)  # Clean up


@webAppFicDownloader.route('/getFile', method='GET')
def getFile():
    fileID = request.query.fileID or 0
    if fileID == 0:
        redirect("/")
    else:
      try:
        folder = os.path.join(OUT_PUT_DIR, fileID)  # get the folder where the generated file is stored
        file = os.listdir(folder)[0]  # get the file name
        # the folder should contain only one file this is ensured by the eBookLib method __cleanUP
        return static_file(file, root=folder, download=file)
      except Exception as e:
        redirect("/")
        print(str(e))

#######################
# Static files
# some working around to serve the all static content from one folder and subfolders
# Begin block
#######################

@webAppFicDownloader.route('/js/<path:path>')
def getJS(path):
    return staticFile('js/' + path)


@webAppFicDownloader.route('/css/<path:path>')
def getCSS(path):
    return staticFile('css/' + path)

@webAppFicDownloader.route('/imgs/<path:path>')
def getImgs(path):
    return staticFile('imgs/' + path)

def staticFile(path):
    if CAPTCHAENABLED == False:
       if path.startswith('css') or path.startswith('js'):
           path = path.replace('.', '_nocaptcha.')
    return static_file(path, root=STATIC_FILES_DIR)

#######################
# Static files
# End block
#######################

@webAppFicDownloader.route('/download')
def goHomeCheater():
    redirect("/")

#######################
# Captha
# Begin block
#######################

@webAppFicDownloader.route('/checkCaptha', method='POST')
def capthaCheck():
    idText = request.forms.get('sesionID')
    captchatext = request.forms.get('userText')
    captchaCheckResult = checkCaptha(captchatext, idText)
    return str(captchaCheckResult)

@webAppFicDownloader.route('/getCaptchImg')
def getCaptchImg():
    imgText, text = getCaptha()
    return json.dumps({"img": imgText, "id": text})

#######################
# Captha
# End block
#######################

@webAppFicDownloader.route('/')
def home():
    # for now the page is static in future this may be will be changed with template
    return static_file('form.html', root=HTML_TEMPLATES_DIR)

def clean(folder):
  try:
   for the_file in os.listdir(folder):
       file_path = os.path.join(folder, the_file)
       try:
           if os.path.isfile(file_path):
               os.unlink(file_path)
           elif os.path.isdir(file_path):
               shutil.rmtree(file_path)
       except Exception as e:
           print(e)
  except FileNotFoundError as e:
    os.makedirs(folder)

if __name__ == '__main__':
    # run the bottle server
    clean(OUT_PUT_DIR)
    clean(DOWNLOAD_DIR)

    webAppFicDownloader.run(host=IP_ADRR, port=PORT, server='gevent')
