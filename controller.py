from bs4 import BeautifulSoup  # import the Beautiful soup functions to parse the data returned from the website


def getControler(siteLink):
    if 'adult-fanfiction.org' in siteLink:
        c = adlFanFicControler(siteLink)
        return c
    if 'fanfiction.net' in siteLink or 'fictionpress.com' in siteLink:
        c = fanFictionNetControler(siteLink)
        return c
    else:
        pass
        # c = SitenameControler(siteLink)
        # return c


class adlFanFicControler:
    def __init__(self, link):
        self.inLink = link

    def getDetails(self, page):
        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        rows = page.findAll('a')
        autor = rows[1].contents[0]
        storyName = page.find('h2')  # the html document looks <h2><a>Test</a></h2>
        storyName = storyName.a.contents[0]  # this will get the text of the link for the exsample above "Test"
        return (autor, storyName)

    def getPageContent(self, page):
        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        soup = BeautifulSoup(page, features="html.parser")
        contens = soup.find("div", {"id": "contentdata"})  # get the page before additional cleaning
        return contens

    def getCoverPage(self, page):
        ##TODO
        #return "CoverText"
        rows = page.findAll('a')
        Cover1 = rows[2].contents[0]
        Cover2 = rows[3].contents[0]
        finalCover = '''<b><i>Category: {} > {}</b></i>'''.format(Cover1, Cover2)
        return finalCover

    def parsePage(self, page):
        page = page.findAll('tr')
        resultingPage = ""
        # for part in page[5].find('td').contents:
        for part in page[5].find('td'):
            # get the table contenet after the 5-th <tr> tag
            try:
                for match in part.findAll('span'):
                    match.unwrap()  # this clears the <span tags that cause problems with the epub>
            except:  # the last part usualy is empty and raises an exception this solves the problem
                pass
            resultingPage += str(part)
        return resultingPage

    def getNextLink(self, page):
        pagination = page.find("div", {"class": "pagination"})
        links = pagination.findAll('a')
        for l in links:
            if l.contents[0] == ">":
                return l.get('href')
        return "NULL"

    def getChapterList(self, page):
        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        tableOfContent = page.find("div", {"class": "dropdown-content"})
        chapterList = tableOfContent.findAll('a')
        chapters = []
        for chap in chapterList:
            chapters.append(chap.contents[0])
        return chapters

    def getStoryLink(self):
        return self.inLink.split('&chapter')[0]  # remove &chapter from the initial link

    def getPublisher(self):
        return self.inLink.split('story.php')[0]  # remove story.php from the initial link


class fanFictionNetControler:
    def __init__(self, link):
        self.inLink = link

    def getDetails(self, page):
        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        autor = page.findAll("a", {"class": "xcontrast_txt"})  # the html document looks <h2><a>Test</a></h2>
        autor = autor[2].text  # this will get the text of the link for the exsample above "Test"
        storyName = page.findAll("b", {"class": "xcontrast_txt"})  # the html document looks <h2><a>Test</a></h2>
        storyName = storyName[0].text  # this will get the text of the link for the exsample above "Test"
        return (autor, storyName)

    def getPageContent(self, page):
        # Parse the html in the 'page' variable, and store it in Beautiful Soup format
        soup = BeautifulSoup(page, features="html.parser")
        contens = soup.find("body")  # get the page before additional cleaning
        return contens

    def getCoverPage(self, page):
        coverTopRow = page.findAll("div", {"class": "xcontrast_txt"})
        coverBottomRow = page.findAll("span", {"class": "xgray xcontrast_txt"})
        Cover1 = coverTopRow[0].get_text()
        Cover2 = coverBottomRow[0].get_text()
        finalCover = Cover1 + '<br>' + Cover2
        return finalCover

    def parsePage(self, page):
        page = page.findAll("div", {"id": "storytext"})
        resultingPage = ""
        for match in page[0].contents:
            if '<br' in str(match):
                newMatch = str(match).replace("<br", '')
            resultingPage += str(match)
        return resultingPage

    def getNextLink(self, page):
        buttons = page.findAll("button", {"class": "btn"})
        for btn in buttons:
            if "Next" in btn.contents[0]:
                link = btn.attrs['onclick']
                link = link.split("'")
                return link[1]
        return "NULL"

    def getChapterList(self, page):
        tableOfContent = page.find("select", {"id": "chap_select"})
        chapterList = tableOfContent.findAll('option')
        chapters = []
        for chap in chapterList:
            chapters.append(chap.contents[0])
        return chapters

    def getStoryLink(self):
        tmpStr = self.inLink.split('/s/')
        tmpStr[1].split('/')
        stotyID = tmpStr[1].split('/')
        finalLink = tmpStr[0] + '/s/' + stotyID[0] + '/'
        return finalLink

    def getPublisher(self):
        return self.inLink.split('/s/')[0]  # remove story.php from the initial link

''' #######################################################
    #Template for the functions needed for the controller!#
    #######################################################

   class SitenameControler:
      def __init__(self, link):
         self.inLink = link

      def getDetails(self, page):
         #Parse the html in the 'page' variable, and store it in Beautiful Soup format
         autor = #findAutor in html page
         storyName = #findStoryName in html page
         return (autor,storyName)

    def getCoverPage(self, page):
        ##TODO
        #return "CoverText"

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
		 
      def getStoryLink(self):
         tmpStr = self.inLink.split('/s/')
         tmpStr[1].split('/')
         stotyID = tmpStr[1].split('/')
         finalLink = tmpStr[0] + '/s/' + stotyID[0] + '/'
         return finalLink

      def getPublisher(self):
         return self.inLink.split('/s/')[0]  # remove story.php from the initial link
'''

class SitenameControler:
    def __init__(self, link):
        self.inLink = link

    def getDetails(self, page):
        #Parse the html in the 'page' variable, and store it in Beautiful Soup format
        autor = "#findAutor in html page"
        storyName = "#findStoryName in html page"
        return (autor,storyName)

    def parsePage(self, page):
        #Parse the html in the 'page' variable, and store it in Beautiful Soup format
        #soup = BeautifulSoup(page, features="html.parser")
        return self.__getPage(contens)

    def __getPage(self, page):
        #clear all unneeded tags. We want only the text of the story.
        resultingPage = "Cleaned text only the text of the fanfic no header/footer/tableofcontence/etc. "
        return resultingPage

    def getNextLink(self, page):
        # find the link for the next chapter
        #for l in links:
        #    if l.contents[0] == : # find the link for the next chapter
        #       return l.get('href')
        return "NULL"

    def getChapterList(self, page):
        chapterList = ['Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4']# find the table of contents if possible
        chapters = []
        for chap in chapterList:
            chapters.append(chap.contents[0])
        return chapters

    def getStoryLink(self):
        finalLink = 'link to go to the given chapter chapter'
        return finalLink

    def getPublisher(self):
        publisher = "http://site"
        return publisher
        
