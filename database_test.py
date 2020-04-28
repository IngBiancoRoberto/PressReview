import unittest
import database
import sqlite3
import os



class TestDatabase(unittest.TestCase):

   def setUp(self):
      self.db = database.Database('test.db')


   def test_DatabaseOpen(self):
      # execute
      #db = database.Database('test.db')
      # assert
      self.db.cur.execute('SELECT name FROM sqlite_master WHERE type= "table"')
      table_list = self.db.cur.fetchall()
      self.assertEqual(table_list,[('articles',)],'Should contain only one table articles')

   def test_DatabaseInsert(self):
      #setup
      #db = database.Database('test.db')
      # execute
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      # assert
      self.db.cur.execute('SELECT * FROM articles')
      rows = self.db.cur.fetchall()
      self.assertEqual(len(rows),1,'Should be one row')
      self.assertEqual(len(rows[0]), 5, 'Five elements')

   def test_DatabaseReadAll(self):
      # setup
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      # execute
      rows = self.db.readAll()
      # assert
      self.assertEqual(len(rows),3,'3 rows')

   def test_DatabaseReadUniqueTimes(self):
      # setup
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-18 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-18 12:00:00','Repubblica','Title','Link')
      # execute
      rows = self.db.readUniqueTimes()
      # assert
      self.assertEqual(rows,['2020-04-17 12:00:00','2020-04-18 12:00:00'],'unique times')

   def test_DatabaseReadByTime(self):
      # setup
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-18 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-18 12:00:00','Repubblica','Title','Link')
      # execute
      rows = self.db.readByTime('2020-04-17 12:00:00')
      # assert
      self.assertEqual(len(rows),2)
      self.assertEqual(len(rows[0]),5)

   def test_DatabaseRemoveByTime(self):
      # setup
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-18 12:00:00','Repubblica','Title','Link')
      # execute
      self.db.removeByTime('2020-04-17 12:00:00')
      # assert
      rows = self.db.readAll()
      self.assertEqual(len(rows),1)
      self.assertEqual(len(rows[0]),5)


   def test_DatabaseRemoveAll(self):
      # setup
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      self.db.insert('2020-04-17 12:00:00','Repubblica','Title','Link')
      # execute
      self.db.removeAll()
      # assert
      self.db.cur.execute('SELECT * FROM articles')
      rows = self.db.cur.fetchall()
      self.assertEqual(rows,[],'table should be empty')


   def tearDown(self):
      del(self.db)
      os.remove('test.db')




if __name__ == '__main__':
    unittest.main()

