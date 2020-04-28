import sqlite3

class Database():

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, date_time text, website text, title text NOT NULL , link text NOT NULL)')
        self.conn.commit()

    def readAll(self):
        self.cur.execute('SELECT * from articles')
        rows = self.cur.fetchall()
        return rows

    def readUniqueTimes(self):
        "reports a list of unique times from the table"
        self.cur.execute('SELECT DISTINCT date_time FROM articles ORDER BY date_time DESC')
        rows = self.cur.fetchall()
        # extract values from the output tuples
        out = [elem[0] for elem in rows]
        return out

    def readByTime(self, inp_date_time):
        "Returns all rows with given date"
        self.cur.execute('SELECT * FROM articles WHERE date_time=? ORDER BY id',(inp_date_time,))
        rows = self.cur.fetchall()
        return rows
    

    def insert(self,date_time,website,title,link):
        self.cur.execute('INSERT INTO articles VALUES (NULL,?,?,?,?)', (date_time,website,title,link))
        #
        self.conn.commit()

    def removeByTime(self, inp_date_time):
        self.cur.execute('DELETE FROM articles WHERE date_time=?',(inp_date_time,))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute('DELETE FROM articles WHERE id=?',(id,))
        self.conn.commit()

    def removeAll(self):
        self.cur.execute('DELETE FROM articles')
        self.conn.commit()

    def __del__(self):
        self.conn.close()