# pyFanFictionDownloader
You need python 3.6
- Libraryes list
- bottle -Web framework
- gevent -Web server for asynchronus_web
- beautifulsoup -HTML parser
- Jinja2 -HTML templates
- WeasyPrint -HTML to PDF
- claptcha -Library for capcha
- Pillow -Needed for claptcha. search for PIL

Install this libraries using pip:
- pip install bottle
- pip install gevent
- pip install beautifulsoup
- pip install Jinja2
- pip install WeasyPrint
- pip install claptcha
- pip install Pillow

Install calibre for convertion to mobi and usage of convert to all file types.
Test the calibre instalation just run ebook-convert

Configuration:
Edit static.py. And read the coments

RAM drive. Why it is good idea. During the download and creation of the epub file. Alot of smal files are created. This can reduce the live of a SSD drive.
To prevent this use a RAM drive. A RAM drive uses part of the free RAM as a hard disk.
How to create RAM drive check in google. The steps are diffrent for linux/windows/macOS
After you have created a RAM drive chnage the WORKING_DIR to the RAM drive path. 
Important in the RAM drive create folders output and download.

To start the application run python3 rootApp.py

For few ideas you can check simpleStartApp.sh and simpleStartAppRamDrive.sh

Unfinished additional ideas to create linux service. In serviceTest you can find my progress.

How to add additinal sites check __HowTheApplicationWorks.txt

Licences
I am including the libraries. The files are not modifed! For more information regarding the licences of each librarie check the librarie it self.

Regarding my application - it is distributed under GNU GENERAL PUBLIC LICENSE
