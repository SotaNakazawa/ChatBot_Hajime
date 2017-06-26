#coding: UTF-8

import http.server

#http://localhost:8000/cgi-bin/Hajime_ChatBot.py
http.server.test(HandlerClass=http.server.CGIHTTPRequestHandler)