import os

IP_ADRR = '0.0.0.0' # Server address where the app will listen
PORT = 8080 # Port where the app will listen

BASE_DIR = '.' # Folder with all templates js, css and images. This includes all files needed for creation of epub files
WORKING_DIR = '.' # folder where each chapter will be downloaded and where the ebook will be generated.
RAM_DRIVE = False  #Used onlu in the shell script that starts the app do not remove
EPUB_TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates/epub/') # templates for the epub generation
HTML_TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates/html/') # for the webpages
STATIC_FILES_DIR = os.path.join(BASE_DIR, 'templates/html/staticfiles/') # folder for js, css and all static content
OUT_PUT_DIR = os.path.join(WORKING_DIR, 'output/') # file for the generated ebook (epub, mobi, pdf and etc)
DOWNLOAD_DIR = os.path.join(WORKING_DIR, 'download/') # temp folder for the chapters each as html page and other needed files

FORBIDDENCHARACTERS={'<': '',  '>': '', ':': '', '"': '',
                     '/': '', '\\': '', '|': '', '?': '',
                     '*': '', '\'': '',}                 # dictionary to clear the illigal chars
                                                         # becasus we will create a file and send it
                                                         # The are some forbiden chars in file name

HTTP_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' # When requesting a web page the server will see the
                                                             # the requst as coming from the Mozzilla. Can be changed
                                                             # to chrome or other browser

FONT = os.path.join(BASE_DIR, 'font/FreeMono.ttf') # For the captch
MAX_CAPTCHA_LENGTH = 9 # should be divadble by 3!!
SECRET = 'Asd'
CAPTCHAENABLED = True
