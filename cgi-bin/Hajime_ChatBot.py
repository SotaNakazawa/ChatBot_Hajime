#!/usr/bin/python
#coding: UTF-8

import sys
import sqlite3
import random
import datetime
import cgi
#import MeCab

#HTMLの中身
html_body = """
	<html>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<head>
		<title>人工無能「はじめ」</title>
	</head>
	<body>

	    <center>%s<br>

	    <form method="POST" action="/cgi-bin/Hajime_ChatBot.py">
	        <input type="text" name="word">
	        <input type="submit" />
	    </form></center>
	</body>
	</html>"""

"""
def getRandomText(text):
	#入力文を形態素解析して名詞を抽出，一旦ポア
	tagger = MeCab.Tagger("-Ochasen")
	#parseToNode()に渡すのが解析してほしい文
	node = tagger.parseToNode(text)
	list =[]

	while node:
		if node.feature.split(",")[0] == "名詞":
			list.append(node.surface)
			#featureに品詞情報、surfaceに単語が格納されている
		node = node.next

	if 0 < len(list):
		return list[random.randint(0,len(list)-1)]
"""

def firstMessage():
	#最初の一言
	cur.execute("select initial from Greet")
	words = []
	for row in cur:
		words.append(row[0])
	return random.choice(words)

def greeting(hour):
	#時間に応じたあいさつ
	if hour in range(4,10+1):
		cur.execute("select morning from Greet")
		greets = []
		for row in cur:
			if len(row[0]) > 0:
				greets.append(row[0])
			else:
				break
		return random.choice(greets)
	elif hour in range(11,17+1):
		cur.execute("select evening from Greet")
		greets = []
		for row in cur:
			if len(row[0]) > 0:
				greets.append(row[0])
			else:
				break
		return random.choice(greets)
	elif hour in range(16,24):
		cur.execute("select night from Greet")
		greets = []
		for row in cur:
			if len(row[0]) > 0:
				greets.append(row[0])
			else:
				break
		return random.choice(greets)
	elif hour in range(1,3+1):
		cur.execute("select midnight from Greet")
		greets = []
		for row in cur:
			if len(row[0]) > 0:
				greets.append(row[0])
			else:
				break
		return random.choice(greets)
	else:
		cur.execute("select other from Greet")
		greets = []
		for row in cur:
			if len(row[0]) > 0:
				greets.append(row[0])
			else:
				break
		return random.choice(greets)

def insertLog(who,txt):
	#Corpus.dbに発言者、内容、時間のログを保存
	if txt:
		today = datetime.datetime.today()
		now = today.strftime("%Y/%m/%d %H:%M:%S")
		con.execute("insert into Log values('%s', '%s', '%s')" % (who, txt, now))

def chatLog():
	context = ""
	log_user = []
	log_word = []
	log = []
	cur.execute("select who from Log order by time desc limit 10")
	for i in cur:
		log_user.append(i[0])
	cur.execute("select word from Log order by time desc limit 10")
	for j in cur:
		log_word.append(j[0])
	
	for k in range(10):
		log.append(log_user[k] + ":" + log_word[k] + "<br>")
	log.reverse()
	
	for i in log:
		context += i

	return context

form = cgi.FieldStorage()
you_say = form.getfirst("word","")

con = sqlite3.connect("Corpus.db")
cur = con.cursor()
sql = "create table if not exists Log(who text, word text, time text)"
con.execute(sql)
print("Content-type: text/html; charset=utf-8\n")


if not you_say:
	hajime_say = greeting(datetime.datetime.now().hour) + firstMessage()
	insertLog("Hajime",hajime_say)
	con.commit()
	log_print = chatLog()
	print(html_body % log_print.encode("utf-8"))

elif you_say:
	cur.execute("select * from Data")
	words = []
	for row in cur:
		words.append(row[0])
	hajime_say = random.choice(words).encode("utf-8")
	insertLog("Hajime",hajime_say)
	insertLog("you",you_say)
	con.commit()
	log_print = chatLog()
	print(html_body % log_print.encode("utf-8"))
	
else:
	print(html_body % ("・・・",""))


"""
reply = getRandomText(str)
cur.execute("select * from Data")
words = []
for row in cur:
	words.append(row[0])
if reply != None:
	print("Hajime:",reply+"がどうかした？")
else:
	print("Hajime:",random.choice(words))

"""

#迷子
con.close()