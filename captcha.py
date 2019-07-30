import random
import string
import os
import datetime

import random
import string
from PIL import Image
from claptcha import Claptcha
import base64

from static import *
from vigenereCipher import *

def genClapchaImgStr(capthaText):
    c = Claptcha(capthaText, FONT, (500, 150), resample=Image.BICUBIC, noise=0.5)
    #c.size = (250, 200)
    c.margin = (5, 5)
    _, img = c.bytes
    prefix = f'data:image/png;base64,'
    imgStr = prefix + base64.b64encode(img.read()).decode('utf-8')
    return imgStr

def randomString():
    rndLetters = (random.choice(string.ascii_uppercase) for _ in range(MAX_CAPTCHA_LENGTH))
    return "".join(rndLetters)

def getCaptha():

   capthaText = randomString()
   imgStr = genClapchaImgStr(capthaText)
   idStr = encrypt(capthaText, SECRET)

   n = 3
   rslStr = [idStr[i:i+n] for i in range(0, len(idStr), n)]
   now = datetime.datetime.now()

   #day1 = math.floor(now.day/10)
   #day2 = now.day - day1 * 10

   #This should be faster because there is no division, multiplication and calling floor
   if now.day < 10:
       day1 = 4
       day2 = now.day
   elif now.day < 20:
       day1 = 2
       day2 = now.day - 10
   elif now.day < 30:
       day1 = 9
       day2 = now.day - 20
   else:
       day1 = 6
       day2 = now.day - 30

   if now.month < 10:
       month1 = 5
       month2 = now.month
   else:
       month1 = 7
       month2 = now.month - 10

   if now.hour < 10:
      hour1 = 9
      hour2 = now.hour
   elif now.hour < 20:
      hour1 = 7
      hour2 = now.hour - 10
   else:
      hour1 = 6
      hour2 = now.hour - 20

   hours = hour1 * 10 + hour2

   if now.minute < 10:
       minutes = 90 + now.minute
   else:
       minutes = now.minute
   
   rslStr[0] = str(month2) + rslStr[0] + str(day1)
   rslStr[1] = str(day2) + rslStr[1] + str(month1)
   rslStr[2] = str(hours) + rslStr[2] + str(minutes)

   idStr = rslStr[0] + '-' + rslStr[1] + '-' + rslStr[2]

   return (imgStr, idStr)
   
   
   
def checkCaptha(capthaInText, idStr):

   if not len(idStr) == 19:
      return -1
   
   idStr = idStr.split('-')
   
   try:
     month2 = int(idStr[0][0])
     day1 = int(idStr[0][-1])
   
     month1 = int(idStr[1][-1])
     day2 = int(idStr[1][0])
   
     hour1 = int(idStr[2][0])
     hour2 = int(idStr[2][1])

     minute1 = int(idStr[2][-2])
     minute2 = int(idStr[2][-1])
   
   except ValueError:
      return -1

   idStr = idStr[0] + idStr[1] + idStr[2]
   idStr = ''.join([i for i in idStr if not i.isdigit()])

   now = datetime.datetime.now()

   if month1 == 5:
      month1 = 0
   else:
      month1=1

   month = month1 * 10 + month2
   if now.month != month:
      return -1

   if day1 == 4:
      day1 = 0
   elif day1 == 2:
      day1 = 1
   elif day1 == 9:
      day1 = 2
   else:
      day1=3

   day = day1 * 10 + day2
   if now.day != day:
      return -1

   if hour1 == 9:
      hour1 = 0
   elif hour1 == 7:
      hour1 = 1
   else:
      hour1=2

   hour = hour1 * 10 + hour2
   if now.hour > hour + 2:
      return -1
   elif now.hour == hour + 2:
         if minute1 == 9:
             minute1 = 0

         minute = minute1 * 10 + minute2
         if now.minute > minute:
            return -1

   capthaOutText = decrypt(idStr, SECRET)
   
   capthaInText = capthaInText.upper()
   capthaInText = capthaInText.replace("0", "O")

   if not capthaOutText == capthaInText:
      return -1
   
   return 1
