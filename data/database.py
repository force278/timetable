import sqlite3 as sql
import asyncio
from datetime import date, timedelta

class Database:
	def __init__(self):
		connection = sql.connect("students.sqlite", check_same_thread=False)
		q = connection.cursor()
		q.execute('''CREATE TABLE IF NOT EXISTS students
		(
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		UserID Varchar(20),
		University Varchar(50),
		GroupName Varchar(20),
		GroupID INTEGER,
		Subgroup INTEGER
		)
		''')
		connection.commit()
		connection.close()
	async def add(self, UserID):
		connection = sql.connect("students.sqlite", check_same_thread=False)
		q = connection.cursor()
		q.execute("SELECT * FROM students WHERE UserID = '%s'" % (UserID))
		result = q.fetchall()
		if len(result) == 0:
			q.execute(
			"INSERT INTO students (UserID, University, GroupName, GroupID, Subgroup) VALUES ('%s', '%s', '%s', '%s', '%s')" % (UserID, None, None, 0, 0))
		connection.commit()
		connection.close()
	async def update(self, UserID, University=None, GroupName=None, GroupID=None, Subgroup=None):
		connection = sql.connect("students.sqlite", check_same_thread=False)
		q = connection.cursor()
		q.execute("SELECT * FROM students WHERE UserID = '%s'" % (UserID))
		result = q.fetchall()
		if University:
			q.execute("UPDATE students SET University = '%s' WHERE UserID = '%s'" % (University, UserID))
		if GroupName:
			q.execute("UPDATE students SET GroupName = '%s' WHERE UserID = '%s'" % (GroupName, UserID))
		if GroupID:
			q.execute("UPDATE students SET GroupID = '%s' WHERE UserID = '%s'" % (GroupID, UserID))
		if Subgroup:
			q.execute("UPDATE students SET Subgroup = '%s' WHERE UserID = '%s'" % (Subgroup, UserID))
		connection.commit()
		connection.close()
	async def get(self, UserID):
		connection = sql.connect("students.sqlite", check_same_thread=False)
		q = connection.cursor()
		q.execute("SELECT * FROM students WHERE UserID = '%s'" % (UserID))
		result = q.fetchall()
		connection.commit()
		connection.close()
		return result
	async def info(self):
		result = []
		connection = sql.connect("students.sqlite", check_same_thread=False)
		q = connection.cursor()
		q.execute("SELECT * FROM students")
		result.append(len(q.fetchall()))
		q.execute("SELECT * FROM students WHERE (University = 'ЧГУ' OR University = 'None')")
		result.append(len(q.fetchall()))
		q.execute("SELECT * FROM students WHERE University = '%s'" % ('ЧГАУ'))
		result.append(len(q.fetchall()))
		connection.commit()
		connection.close()
		return result
	async def get_all(self):
		connection = sql.connect("students.sqlite", check_same_thread=False)
		q = connection.cursor()
		q.execute("SELECT * FROM students")
		result = q.fetchall()
		connection.commit()
		connection.close()
		return result
	async def get_all_usersid(self):
		connection = sql.connect("students.sqlite", check_same_thread=False)
		q = connection.cursor()
		q.execute("SELECT UserID FROM students")
		result = q.fetchall()
		connection.commit()
		connection.close()
		return result



class CountRequests:
	def __init__(self):
		self.today = date.today()
		self.count = 0
		self.chuvsu_count = 0
		self.chgau_count = 0
	async def augment(self):
		if date.today() != self.today:
			self.today = date.today()
			self.count = 0
			self.chuvsu_count = 0
			self.chgau_count = 0
		self.count = self.count + 1
	async def chgau_augment(self):
		if date.today() != self.today:
			self.today = date.today()
			self.count = 0
			self.chgau_count = 0
			self.chuvsu_count = 0
		self.count = self.count + 1
		self.chgau_count = self.chgau_count + 1
	async def chuvsu_augment(self):
		if date.today() != self.today:
			self.today = date.today()
			self.count = 0
			self.chuvsu_count = 0
			self.chgau_count = 0
		self.count = self.count + 1
		self.chuvsu_count = self.chuvsu_count + 1
	async def get_info(self):
		string = f'🔂 Всего запросов за день: {str(self.count)}\nИз них\n🔵ЧГУ: <code>{str(self.chuvsu_count)}</code>\n🟢ЧГАУ: <code>{str(self.chgau_count)}</code>'
		return string