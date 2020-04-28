#
#import requests
#import sys
import webread
import unittest

class TestWebread(unittest.TestCase):

    def test_GenericReadFailed(self):
        page = webread.generic_read(website_url='http://xxx')
        # assert
        self.assertEqual(page,[])

    def test_RepubblicaRead(self):
        media = 2
        no_media = 1
        websites,titles,links = webread.repubblica_read(media=media,no_media=no_media)
        self.assertEqual(len(websites),media+no_media)
        self.assertEqual(websites[0],'Repubblica')
        self.assertEqual(len(titles),media+no_media)
        self.assertEqual(len(links),media+no_media)

    def test_RepubblicaManyRead(self):
        media = 100
        no_media = 0
        websites,titles,links = webread.repubblica_read(media=media,no_media=no_media)
        self.assertEqual(len(websites)>0,True)
        self.assertEqual(websites[0],'Repubblica')
        self.assertEqual(len(titles)>0,True)
        self.assertEqual(len(links)>0,True)


    def test_RepubblicaFailedRead(self):
        websites, titles, links= webread.repubblica_read(website_url='http://xxx')
        #
        self.assertEqual(websites,[],'websites should be empty')
        self.assertEqual(titles,[],'Titles should be empty')
        self.assertEqual(links,[],'Links should be empty')
    
    def test_CorriereRead(self):
        websites, titles,links = webread.corriere_read(xmedium=2,medium=2)
        self.assertEqual(len(websites),4)
        self.assertEqual(websites[0],'Corriere')
        self.assertEqual(len(titles),4)
        self.assertEqual(len(links),4)

    def test_CorriereManyRead(self):
        # to test extreme values for article numbers
        websites, titles,links = webread.corriere_read(xmedium=100,medium=0)
        self.assertEqual(len(websites)>0,True)
        self.assertEqual(websites[0],'Corriere')
        self.assertEqual(len(titles)>0,True)
        self.assertEqual(len(links)>0,True)

    def test_CorriereFailedRead(self):
        websites, titles, links= webread.corriere_read(website_url='http://xxx')
        #assert
        self.assertEqual(websites,[],'websites should be empty')
        self.assertEqual(titles,[],'Titles should be empty')
        self.assertEqual(links,[],'Links should be empty')

    def test_BBCNewsRead(self):
        websites, titles,links = webread.bbcnews_read()
        self.assertEqual(len(websites),2)
        self.assertEqual(websites[0],'BBC News')
        self.assertEqual(len(titles),2)
        self.assertEqual(len(links),2)

    def test_BBCNewsFailedRead(self):
        websites, titles, links= webread.bbcnews_read(website_url='http://xxx')
        #assert
        self.assertEqual(websites,[],'websites should be empty')
        self.assertEqual(titles,[],'Titles should be empty')
        self.assertEqual(links,[],'Links should be empty')

    def test_Sole24OreRead(self):
        websites, titles,links = webread.sole24ore_read(narts=2)
        self.assertEqual(len(websites),2)
        self.assertEqual(websites[0],'Sole 24 Ore')
        self.assertEqual(len(titles),2)
        self.assertEqual(len(links),2)

    def test_Sole24OreManyRead(self):
        websites, titles,links = webread.sole24ore_read(narts=100)
        self.assertEqual(len(websites)>0,True)
        self.assertEqual(websites[0],'Sole 24 Ore')
        self.assertEqual(len(titles)>0,True)
        self.assertEqual(len(links)>0,True)

    def test_Sole24OreFailedRead(self):
        websites, titles, links= webread.sole24ore_read(website_url='http://xxx')
        #assert
        self.assertEqual(websites,[],'websites should be empty')
        self.assertEqual(titles,[],'Titles should be empty')
        self.assertEqual(links,[],'Links should be empty')

    def test_NYTimesRead(self):
        websites, titles,links = webread.nytimes_read(narts=2)
        self.assertEqual(len(websites),2)
        self.assertEqual(websites[0],'NY Times')
        self.assertEqual(len(titles),2)
        self.assertEqual(len(links),2)

    def test_NYTimesFailedRead(self):
        websites, titles, links= webread.nytimes_read(website_url='http://xxx')
        #assert
        self.assertEqual(websites,[],'websites should be empty')
        self.assertEqual(titles,[],'Titles should be empty')
        self.assertEqual(links,[],'Links should be empty')


if __name__ == '__main__':
    unittest.main()