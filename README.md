# pyFanFictionDownloader
Discontinued. Downloads from FanFiction.net result in 403 Forbidden. I dont have intention to debug or try to bypass the bot protection.

You need python 3.6
- Libraries list
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

Install calibre for conversion to mobi.
Test the calibre installation just run ebook-convert

Configuration:
Edit static.py. And read the comments

RAM drive. Why it is a good idea. During the download and creation of the epub file. Alot of smal files are created. This can reduce the life of a SSD drive.
To prevent this use a RAM drive. A RAM drive uses part of the free RAM as a hard disk.
How to create RAM drive check in google. The steps are different for linux/windows/macOS
After you have created a RAM drive change the WORKING_DIR to the RAM drive path. 
Important in the RAM drive create folders output and download.

To start the application run python3 rootApp.py

For few ideas you can check simpleStartApp.sh and simpleStartAppRamDrive.sh

Unfinished additional ideas to create linux service. In serviceTest, you can find my progress. I am stopping the development of this for the time being.

How to add additional sites check __HowTheApplicationWorks.txt

Licenses
I am including the libraries. The libraries archives are not modified! For more information regarding the licenses of each library check the library itself.

Regarding my application - it is distributed under GNU GENERAL PUBLIC LICENSE
