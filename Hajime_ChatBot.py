#coding: utf-8

import sys
import MeCab
import sqlite3
import random
import re

def getRandomText(text):
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
		#Talkにlistを対応させているだけなら後半部分だけでいいのでは
		return list[random.randint(0,len(list)-1)]
	'''else:
		return '''

if __name__ == '__main__':
	con = sqlite3.connect("Corpus.db")
	cur = con.cursor()
	sql = "create table if not exists Data(Log text)"
	con.execute(sql)

	while True:
		str = input("you: ")
		reply = getRandomText(str)
		if str == "さようなら":
			print("Hajime: またね。")
			print("- 対話が終了しました -")
			break

		sql = "insert into Data values('%s')" % (str)
		con.execute(sql)

		cur.execute("select * from Data")
		words = []
		for row in cur:
			words.append(row[0])
		if reply != None:
			print("Hajime:",reply+"がどうかした？")
		else:
			print("Hajime:",random.choice(words))


	con.commit()
	con.close()