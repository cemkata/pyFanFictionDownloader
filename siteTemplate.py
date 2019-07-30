from bs4 import BeautifulSoup #import the Beautiful soup functions to parse the data returned from the website

class 'Sitename'Controler:
      def __init__(self):
         pass

      def getDetails(self, page):
         #Parse the html in the 'page' variable, and store it in Beautiful Soup format
         autor = #findAutor in html page
         storyName = #findStoryName in html page
         return (autor,storyName)

      def parsePage(self, page):
            #Parse the html in the 'page' variable, and store it in Beautiful Soup format
            soup = BeautifulSoup(page, features="html.parser")
            contens = soup.find() #get the page before additional cleaning
            return self.__getPage(contens)

      def __getPage(self, page):
         #clear all unneeded tags. We want only the text of the story.
         resultingPage = ""
         return resultingPage

      def getNextLink(self, page):
         # find the link for the next chapter
         for l in links:
             if l.contents[0] == : # find the link for the next chapter
                return l.get('href')
         return "NULL"

      def getChapterList(self, page):
         chapterList = # find the table of contents if possible
         chapters = []
         for chap in chapterList:
             chapters.append(chap.contents[0])
         return chapters
