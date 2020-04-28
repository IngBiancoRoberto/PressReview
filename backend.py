import webread
import database
from datetime import datetime
import os

class Backend:

    def __init__(self,dbname=[]):
        # change dbname for testing purposes

        # standard database
        if dbname == []:
            dbname = os.path.dirname(__file__) + '\\articles.db'

        #db initialise
        self.db = database.Database(dbname)
        # cursor properties
        self.websites = []
        self.titles = []
        self.links = []

    def reset_cursors(self):
        self.websites = []
        self.titles = []
        self.links = []

    def attach(self, *args):
        "aux func, updates cursor properties"
        ls = list(args[0])
        self.websites = self.websites+ls[0]
        self.titles = self.titles +ls[1]
        self.links = self.links +ls[2]

    def collect_press(self):
        "Method to gather data from websites. Update this when new websites are added"
    
        
        #initialise cursors empty
        self.reset_cursors()
        
        # repubblica
        self.attach(webread.repubblica_read())
        # corriere
        self.attach(webread.corriere_read())
        # sole 24
        self.attach(webread.sole24ore_read())
        # bbc news
        self.attach(webread.bbcnews_read())
        # ny times
        self.attach(webread.nytimes_read())
        

    def update_db(self):
        "Collects data from websites and updates the db content"

        # gather web data
        self.collect_press()
        if len(self.websites)==0:
            return 'no_data'

        # fix time
        now_string = datetime.strftime(datetime.now(),"%Y.%m.%d %H:%M:%S, %a")

        # find last date
        all_dates = self.db.readUniqueTimes()
        if len(all_dates)==0:
            updateFlag=True
        else:
            last_date = all_dates[0]
            # collect data from db with last date point
            last_rows = self.db.readByTime(last_date)
            updateFlag = self.checkUpdateFlag(last_rows)

        # populate database
        if updateFlag:
            for website, title, link in zip(self.websites,self.titles,self.links):
                self.db.insert(now_string, website,title,link)
            return 'data_updated'
        else:
            return 'same_data'

    def checkUpdateFlag(self, last_rows):
        # last rows is the output of readByTime
        updateFlag = False
        # compare last rows with new data
        if len(last_rows) == len(self.links): 
            for k in range(len(self.links)):
                if last_rows[k][4] != self.links[k]:
                    updateFlag = True
                    break
        else: # if different length, update
            updateFlag=True
        
        return updateFlag
        
   