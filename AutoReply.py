#!/usr/bin/python

import itchat, time, re, sys, urllib, urllib3, json
from itchat.content import *
from urllib import parse #quote,unquote,urlencode
import numpy as np

import requests
import argparse
import base64

API_ENDPOINT = 'http://www.tuling123.com/openapi/api'
API_KEY = 'a98151f5b12a43e88488f71895a195a7'

API_ENDPOINT_pic = 'https://vision.googleapis.com/v1/images:annotate'
API_KEY_pic = 'AIzaSyANGVE1gWK-_PKq7tnp4eKmF1aGkVyjpKk'

#print(itchat.search_chatrooms(name='树群'))

@itchat.msg_register([TEXT])
def textReply(msg):
	global index
	
	index = index + 1
	
	print(msg['Text'])
	
	match = re.search('新年', msg['Text']) or re.search('新春', msg['Text']) #.span()
	match2 = re.search('电话', msg['Text'])
	
	print(msg['FromUserName'])
	print(msg['ToUserName'])
	
	if match:
		itchat.send(('助手A：新年好啊!'), msg['FromUserName'])
		itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
		itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
	elif match2:
		itchat.send(('助手A：您好，请稍候。'))
		itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
		itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
		
	if index == 1:		
		itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])
		itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
		itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
			
	parameters = {
		'key': API_KEY,
		'info': msg['Text'],
		'loc': '波士顿',
		'userid': '0'
	}
		
	req = requests.post(url = API_ENDPOINT, data = parameters)
	try:
		replied_data = req.json()
		if replied_data['code'] == 100000:
			print(replied_data['code'])
			print(replied_data['text'])
			itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
			
		elif replied_data['code'] == 200000:
			print(replied_data['code'])
			print(replied_data['text'])
			print(replied_data['url'])
			itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
			itchat.send(('助手A: 请点击如下链接吧，\n' + replied_data['url']), msg['FromUserName'])
			
		elif replied_data['code'] == 302000: #news
			print(replied_data['code'])
			print(replied_data['text'])
			print(replied_data['list'])
			news = ''
			news_number = 10
			news_i = 0
			for news_i in range(np.array([len(replied_data['list']), news_number]).min()):
				news = news + replied_data['list'][news_i]['article'] + ', url: ' + replied_data['list'][news_i]['detailurl'] + ' --来自' + replied_data['list'][news_i]['source'] + '；' + '\n'
				news_i += 1
			itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
			itchat.send(('助手A: 请浏览如下内容并点击阅读详情啦，\n' + news), msg['FromUserName'])
			
		elif replied_data['code'] == 308000: #recipe
			print(replied_data['code'])
			print(replied_data['text'])
			print(replied_data['list'])
			recipes = ''
			recipes_number = 5
			recipes_i = 0
			
			for recipes_i in range(np.array([len(replied_data['list']), recipes_number]).min()):
				recipes = recipes + replied_data['list'][recipes_i]['name'] + ', url: ' + replied_data['list'][recipes_i]['info'] + ' --详情' + replied_data['list'][recipes_i]['detailurl'] + '；' + '\n'
				recipes_i += 1
			itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
			itchat.send(('助手A: 请参考如下内容并点击查看详情哦 ~ \n' + recipes), msg['FromUserName'])
			
		elif replied_data['code'] == 313000: #song
			print(replied_data['code'])
			print(replied_data['text'])
			print(replied_data['function'])
			itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
			itchat.send(('助手A: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['song'] + ' --来自' + replied_data['function']['singer']), msg['FromUserName'])
			
		elif replied_data['code'] == 314000: #poetry
			print(replied_data['code'])
			print(replied_data['text'])
			print(replied_data['function'])
			itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
			itchat.send(('助手A: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['name'] + ' --来自' + replied_data['function']['author']), msg['FromUserName'])
			
		else:
			print(replied_data['code'])
			print(replied_data['text'])
			itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
	except:
		pass
			
	m = parse.quote(msg['Text'].encode('utf8'))
	#m = msg['Text']
    #http://api.qingyunke.com/api.php?key=free&appid=0&msg=  
    #url = 'http://sandbox.api.simsimi.com/request.p?key=9470057a-909b-4e6c-a25d-19e0834d6667&lc=zh&ft=1.0&text='+m
	url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg='+m #tuling123, API: http://www.tuling123.com/openapi/api  APIkey: a98151f5b12a43e88488f71895a195a7
	print(url)
	raw = urllib.request.urlopen(url)
	try:
		data = json.loads(raw.read().decode('utf-8'))
		#print data['response']
		print(data['content'])
		itchat.send(('助手B: ' + data['content']), msg['FromUserName'])
		#print('助手B: ' + data['content'])
	except:
		pass

group_name_list = ['我家（My Family）','娘家人']
#group_list = np.array(['%s'%gname[0] for gname in group_name_list])
group_list = np.array([itchat.search_chatrooms(name='%s'%gname)[0]['UserName'] for gname in group_name_list])


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_text_reply(msg):
#	sender = msg['FromUserName']
#	nick = msg['FromUserName']
#	print(itchat.search_chatrooms(name='树群'))
#	print(itchat.search_chatrooms(name='我家（My Family）'))
	#print(itchat.search_chatrooms(name='树群')[0]['NickName'])
	#print(itchat.search_chatrooms(name='我家（My Family）')[0]['NickName'])
#	print(itchat.search_chatrooms(name='树群')[0]['UserName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['UserName'])
#	print(msg['FromUserName'])
#	print(msg['ToUserName'])
	
	if msg['ToUserName'] in [itchat.search_chatrooms(name='我家（My Family）')[0]['UserName']]: #itchat.search_chatrooms(name='树群')[0]['UserName'], 
		print(msg['Text'])
	
	if msg['FromUserName'] in [itchat.search_chatrooms(name='我家（My Family）')[0]['UserName']] or ('助手A' not in msg['Text'] and '助手A' not in msg['Text']  and 'Picture收到' not in msg['Text'] and '系统提示' not in msg['Text']): #itchat.search_chatrooms(name='树群')[0]['UserName'], 
		
		global freqs
		freqs = freqs + 1
		
		match3 = re.search('新年', msg['Text']) or re.search('新春', msg['Text']) #.span()
		match4 = re.search('电话', msg['Text'])
			
		if match3:
			itchat.send(('助手A：新年好啊!'), msg['FromUserName'])
			itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
			itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
		elif match4:
			itchat.send(('助手A：您好，请稍候。'))
			itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
			itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
			
		if index == 1:		
			itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])
			itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
			itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
				
		parameters = {
			'key': API_KEY,
			'info': msg['Text'],
			'loc': '',
			'userid': '0'
		}
			
		req = requests.post(url = API_ENDPOINT, data = parameters)
		try:
			replied_data = req.json()
			if replied_data['code'] == 100000:
				print(replied_data['code'])
				print(replied_data['text'])
				itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
				
			elif replied_data['code'] == 200000:
				print(replied_data['code'])
				print(replied_data['text'])
				print(replied_data['url'])
				itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
				itchat.send(('助手A: 请点击如下链接吧，\n' + replied_data['url']), msg['FromUserName'])
				
			elif replied_data['code'] == 302000: #news
				print(replied_data['code'])
				print(replied_data['text'])
				print(replied_data['list'])
				news = ''
				news_number = 10
				news_i = 0
				for news_i in range(np.array([len(replied_data['list']), news_number]).min()):
					news = news + replied_data['list'][news_i]['article'] + ', url: ' + replied_data['list'][news_i]['detailurl'] + ' --来自' + replied_data['list'][news_i]['source'] + '；' + '\n'
					news_i += 1
				itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
				itchat.send(('助手A: 请浏览如下内容并点击阅读详情啦，\n' + news), msg['FromUserName'])
				
			elif replied_data['code'] == 308000: #recipe
				print(replied_data['code'])
				print(replied_data['text'])
				print(replied_data['list'])
				recipes = ''
				recipes_number = 5
				recipes_i = 0
				
				for recipes_i in range(np.array([len(replied_data['list']), recipes_number]).min()):
					recipes = recipes + replied_data['list'][recipes_i]['name'] + ', url: ' + replied_data['list'][recipes_i]['info'] + ' --详情' + replied_data['list'][recipes_i]['detailurl'] + '；' + '\n'
					recipes_i += 1
				itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
				itchat.send(('助手A: 请参考如下内容并点击查看详情哦 ~ \n' + recipes), msg['FromUserName'])
				
			elif replied_data['code'] == 313000: #song
				print(replied_data['code'])
				print(replied_data['text'])
				print(replied_data['function'])
				itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
				itchat.send(('助手A: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['song'] + ' --来自' + replied_data['function']['singer']), msg['FromUserName'])
				
			elif replied_data['code'] == 314000: #poetry
				print(replied_data['code'])
				print(replied_data['text'])
				print(replied_data['function'])
				itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
				itchat.send(('助手A: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['name'] + ' --来自' + replied_data['function']['author']), msg['FromUserName'])
				
			else:
				print(replied_data['code'])
				print(replied_data['text'])
				itchat.send(('助手A: ' + replied_data['text']), msg['FromUserName'])
		except:
			pass
			
		m = parse.quote(msg['Text'].encode('utf8'))
		#m = msg['Text']
	    #http://api.qingyunke.com/api.php?key=free&appid=0&msg=  
	    #url = 'http://sandbox.api.simsimi.com/request.p?key=9470057a-909b-4e6c-a25d-19e0834d6667&lc=zh&ft=1.0&text='+m
		url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg='+m #tuling123, API: http://www.tuling123.com/openapi/api  APIkey: a98151f5b12a43e88488f71895a195a7
		print(url)
		raw = urllib.request.urlopen(url)
		try:
			data = json.loads(raw.read().decode('utf-8'))
			#print data['response']
			print(data['content'])
			itchat.send(('助手B: ' + data['content']), msg['FromUserName'])
		except:
			pass
				
	print(itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'])
	
@itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)
def group_text_reply(msg):
#	sender = msg['FromUserName']
#	nick = msg['FromUserName']
#	print(itchat.search_chatrooms(name='树群'))
#	print(itchat.search_chatrooms(name='我家（My Family）'))
	#print(itchat.search_chatrooms(name='树群')[0]['NickName'])
	#print(itchat.search_chatrooms(name='我家（My Family）')[0]['NickName'])
#	print(itchat.search_chatrooms(name='树群')[0]['UserName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['UserName'])
#	print(msg['FromUserName'])
#	print(msg['ToUserName'])助手A
	
	print('Content: ' + msg['FileName'] + '\n')
	print('FileName: ' + msg.fileName + '\n')
	print('MsgId: ' + msg['MsgId'] + '\n')
	print('Text: ' + msg.content + '\n')
	#print('Url: ' + msg.url + '\n')
	#print('Data: ' + msg.data + '\n')
#	print('CommentUrl: ' + msg.commenturl + '\n')
#	print('Imag: ' + msg.img + '\n')
#	print(f)
#	print(fd)
	#print(itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'])
	
	if msg['FromUserName'] in [itchat.search_chatrooms(name='我家（My Family）')[0]['UserName']] or msg['ToUserName'] in [itchat.search_chatrooms(name='我家（My Family）')[0]['UserName']]: #itchat.search_chatrooms(name='树群')[0]['UserName'], 
		
		global freqs2
		freqs2 = freqs2 + 1
			
		if freqs2 <= 1:
			itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])		
			itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
			itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
		
		msg.download(msg.fileName)
#		itchat.send('@%s@%s' % (
#			'img', msg['FileName']),
#			msg['FromUserName'])
#		with open(msg.fileName, 'wb') as f:
#			f.write(msg.fileName)
#		with open(msg.fileName, 'wb') as fd:
#			fd.write(msg.download(msg.fileName))
		itchat.send(('助手A：收到~'), msg['FromUserName'])
			
		image_filename = msg['FileName']
		image_filename_ne = image_filename.split('.')[0]
		parameters_pic_raw = {
			"requests": [
				{
					"image": {
						"content": base64.b64encode(open(image_filename,'rb').read()).decode('UTF-8')
					 },
					 "features": [
							{
								"type": "FACE_DETECTION",
								"maxResults": "10"
							},
							{
								"type": "LABEL_DETECTION",
								 "maxResults": "10"
							},
							{
								"type": "TEXT_DETECTION",
								"maxResults": "10"
							},
							{
								"type": "LANDMARK_DETECTION",
								"maxResults": "10"
							},
							{
								"type": "WEB_DETECTION",
								"maxResults": "10"
							}
					 ]
				 }
			]
		}
		output_filename = 'vision_%s.json'%image_filename_ne
		
		with open(output_filename, 'w') as output_file:
			json.dump(parameters_pic_raw, output_file, indent = 4)
		
		try:
			parameters_pic = open(output_filename,'rb').read()
			response_pic = requests.post(url = API_ENDPOINT_pic+'?key='+API_KEY_pic, data = parameters_pic)
		
			vision_results = response_pic.json()
		except:
			pass
			
		try:	
			itchat.send(('助手A：\n 图片文字：' + vision_results['responses'][0]['textAnnotations'][0]['description']), msg['FromUserName'])
		except:
			pass
		try:
			itchat.send(('助手A：\n 图片内容分析：' + str([vision_results['responses'][0]['labelAnnotations'][index]['description'] for index in range(len(vision_results['responses'][0]['labelAnnotations']))])[1:-1]), msg['FromUserName'])
		except:
			pass
		#vision_results['responses'][0]['webDetection']['bestGuessLabels'][0]['label']
		#itchat.send(('助手A：\n 相似图片：' + vision_results['responses'][0]['webDetection']['visuallySimilarImages'][0]['url']), msg['FromUserName'])
		try:
			itchat.send(('助手A：\n 相似图片：' + str([vision_results['responses'][0]['webDetection']['visuallySimilarImages'][ind]['url'] for ind in range(len(vision_results['responses'][0]['webDetection']['visuallySimilarImages']))])[1:-1]), msg['FromUserName'])
		except:
			pass
		try:
			vision_results_face_raw = vision_results['responses'][0]['faceAnnotations'][0]
			vision_results_face = dict(vision_results_face_raw)
			del vision_results_face['landmarks']
			itchat.send(('助手A：\n 人脸分析：' + str(vision_results_face)[1:-1]), msg['FromUserName'])
		except:
			pass
			
		try:
			vision_results_landmark = ('分析师A：\n 地标分析：' + str([(vision_results['responses'][0]['landmarkAnnotations'][index]['description'], vision_results['responses'][0]['landmarkAnnotations'][index]['locations']) for index in range(len(vision_results['responses'][0]['landmarkAnnotations']))])[1:-1])
			itchat.send(('助手A：\n 人脸分析：' + str(vision_results_landmark)), msg['FromUserName'])
			print(vision_results_landmark)
		except:
			pass
			
#		parameters_pic = open(output_filename,'rb').read()
#		response_pic = requests.post(url = API_ENDPOINT_pic+'?key='+API_KEY_pic, data = parameters_pic)
#		
#		vision_results = response_pic.json()
##		try:	
#		itchat.send(('助手A：\n 图片文字：' + vision_results['responses'][0]['textAnnotations'][0]['description']), msg['FromUserName'])
#		itchat.send(('助手A：\n 图片内容分析：' + str([vision_results['responses'][0]['labelAnnotations'][index]['description'] for index in range(len(vision_results['responses'][0]['labelAnnotations']))])[1:-1]), msg['FromUserName'])
#		#vision_results['responses'][0]['webDetection']['bestGuessLabels'][0]['label']
#		itchat.send(('助手A：\n 联想图片：' + str(vision_results['responses'][0]['webDetection']['bestGuessLabels'][0]['label'])+ ', ' + str([vision_results['responses'][0]['webDetection']['visuallySimilarImages'][ind]['url'] for ind in range(len(vision_results['responses'][0]['webDetection']['visuallySimilarImages']))])[1:-1]), msg['FromUserName'])
#		vision_results_face_raw = vision_results['responses'][0]['faceAnnotations'][0]
#		vision_results_face = dict(vision_results_face_raw)
#		del vision_results_face['landmarks']
#		itchat.send(('助手A：\n 人脸分析：' + str(vision_results_face)[1:-1]), msg['FromUserName'])
#		except:
#			pass
			
		#return '%s received' % msg['Type']
		
	
@itchat.msg_register(itchat.content.SHARING, isGroupChat=True)
def group_text_reply(msg):
#	sender = msg['FromUserName']
#	nick = msg['FromUserName']
#	print(itchat.search_chatrooms(name='树群'))
#	print(itchat.search_chatrooms(name='我家（My Family）'))
#	print(itchat.search_chatrooms(name='树群')[0]['NickName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['NickName'])
#	print(itchat.search_chatrooms(name='树群')[0]['UserName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['UserName'])
#	print(msg['FromUserName'])
#	print(msg['ToUserName'])
	
	if msg['FromUserName'] in [itchat.search_chatrooms(name='我家（My Family）')[0]['UserName']]: #itchat.search_chatrooms(name='树群')[0]['UserName'], 
		
		global freqs3
		freqs3 = freqs3 + 1
			
		if freqs3 <= 1:
			itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])
		itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
		itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
		itchat.send(('助手A：已接收~'), msg['FromUserName'])

	print(itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'])
	
@itchat.msg_register(itchat.content.VIDEO, isGroupChat=True)
def group_text_reply(msg):
#	sender = msg['FromUserName']
#	nick = msg['FromUserName']
#	print(itchat.search_chatrooms(name='树群'))
#	print(itchat.search_chatrooms(name='我家（My Family）'))
#	print(itchat.search_chatrooms(name='树群')[0]['NickName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['NickName'])
#	print(itchat.search_chatrooms(name='树群')[0]['UserName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['UserName'])
#	print(msg['FromUserName'])
#	print(msg['ToUserName'])
	
	if msg['FromUserName'] in [itchat.search_chatrooms(name='我家（My Family）')[0]['UserName']]: #itchat.search_chatrooms(name='树群')[0]['UserName'], 
		
		global freqs4
		freqs4 = freqs4 + 1
			
		if freqs4 <= 1:
			itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])		
		itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
		itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
		itchat.send(('助手A：%s收到啦~' % msg['Type']), msg['FromUserName'])

	print(itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'])
	
	
@itchat.msg_register(itchat.content.RECORDING, isGroupChat=True)
def group_text_reply(msg):
#	sender = msg['FromUserName']
#	nick = msg['FromUserName']
#	print(itchat.search_chatrooms(name='树群'))
#	print(itchat.search_chatrooms(name='我家（My Family）'))
#	print(itchat.search_chatrooms(name='树群')[0]['NickName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['NickName'])
#	print(itchat.search_chatrooms(name='树群')[0]['UserName'])
#	print(itchat.search_chatrooms(name='我家（My Family）')[0]['UserName'])
#	print(msg['FromUserName'])
#	print(msg['ToUserName'])
	
	if msg['FromUserName'] in [itchat.search_chatrooms(name='我家（My Family）')[0]['UserName']]: #itchat.search_chatrooms(name='树群')[0]['UserName'], 
		
		global freqs5
		freqs5 = freqs5 + 1
			
		if freqs5 <= 1:
			itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])	
		itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
		itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
		itchat.send(('助手A：%s已收到' % msg['Type']), msg['FromUserName'])

	print(itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'])
	

@itchat.msg_register([VIDEO])
def videoReply(msg):
	order = 0
	if order <=1:
		itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])
		itchat.send(('助手A：这不方便说话，文字比较好啦。'), msg['FromUserName'])
	itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
	itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
	itchat.send(('助手A：收到。'), msg['FromUserName'])

@itchat.msg_register([PICTURE])
def picReply(msg):
	order = 0
	if order <=1:
		itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])
	itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
	itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
	print(msg['FileName'])
	print(msg['MsgId'])
	#print(msg['Url'])
	
	msg.download(msg.fileName)
#	itchat.send('@%s@%s' % (
#		'img', msg['FileName']),
#		msg['FromUserName'])
#	with open(msg.fileName, 'wb') as f:
#		f.write(msg.download())
	itchat.send(('助手A：%s收到~' % msg['Type']), msg['FromUserName'])
		
	image_filename = msg['FileName']
	image_filename_ne = image_filename.split('.')[0]
	parameters_pic_raw = {
		"requests": [
			{
				"image": {
					"content": base64.b64encode(open(image_filename,'rb').read()).decode('UTF-8')
				 },
				 "features": [
						{
							"type": "FACE_DETECTION",
							"maxResults": "10"
						},
						{
							"type": "LABEL_DETECTION",
							 "maxResults": "10"
						},
						{
							"type": "TEXT_DETECTION",
							"maxResults": "10"
						},
						{
							"type": "LANDMARK_DETECTION",
							"maxResults": "10"
						},
						{
							"type": "WEB_DETECTION",
							"maxResults": "10"
						}
				 ]
			 }
		]
	}
	output_filename = 'vision_%s.json'%image_filename_ne
	
	with open(output_filename, 'w') as output_file:
		json.dump(parameters_pic_raw, output_file, indent = 4)
	
	try:
		parameters_pic = open(output_filename,'rb').read()
		response_pic = requests.post(url = API_ENDPOINT_pic+'?key='+API_KEY_pic, data = parameters_pic)
	
		vision_results = response_pic.json()
	except:
		pass
		
	try:	
		itchat.send(('助手A：\n 图片文字：' + vision_results['responses'][0]['textAnnotations'][0]['description']), msg['FromUserName'])
	except:
		pass
	try:
		itchat.send(('助手A：\n 图片内容分析：' + str([vision_results['responses'][0]['labelAnnotations'][index]['description'] for index in range(len(vision_results['responses'][0]['labelAnnotations']))])[1:-1]), msg['FromUserName'])
	except:
		pass
	#vision_results['responses'][0]['webDetection']['bestGuessLabels'][0]['label']
	#itchat.send(('助手A：\n 相似图片：' + vision_results['responses'][0]['webDetection']['visuallySimilarImages'][0]['url']), msg['FromUserName'])
	try:
		itchat.send(('助手A：\n 相似图片：' + str([vision_results['responses'][0]['webDetection']['visuallySimilarImages'][ind]['url'] for ind in range(len(vision_results['responses'][0]['webDetection']['visuallySimilarImages']))])[1:-1]), msg['FromUserName'])
	except:
		pass
	try:
		vision_results_face_raw = vision_results['responses'][0]['faceAnnotations'][0]
		vision_results_face = dict(vision_results_face_raw)
		del vision_results_face['landmarks']
		itchat.send(('助手A：\n 人脸分析：' + str(vision_results_face)[1:-1]), msg['FromUserName'])
	except:
		pass
	
	try:
		vision_results_landmark = ('分析师A：\n 地标分析：' + str([(vision_results['responses'][0]['landmarkAnnotations'][index]['description'], vision_results['responses'][0]['landmarkAnnotations'][index]['locations']) for index in range(len(vision_results['responses'][0]['landmarkAnnotations']))])[1:-1])
		print(vision_results_landmark)
	except:
		pass
#	except:
#		pass
	#return '%s received' % msg['Type']


#@itchat.msg_register([PICTURE])
#def download_files(msg):
#	msg.download(msg.fileName)
#	itchat.send('@%s@%s' % (
#		'img', msg['FileName']),
#		msg['FromUserName'])
##	with open(msg.fileName, 'wb') as f:
##		f.write(msg.download())
#	itchat.send(('%s received' % msg['Type']), msg['FromUserName'])
#		
#	image_filename = msg['FileName']
#	image_filename_ne = image_filename.split('.')[0]
#	parameters_pic_raw = {
#		"requests": [
#			{
#				"image": {
#					"content": base64.b64encode(open(image_filename,'rb').read()).decode('UTF-8')
#				 },
#				 "features": [
#						{
#							"type": "FACE_DETECTION",
#							"maxResults": "10"
#						},
#						{
#							"type": "LABEL_DETECTION",
#							 "maxResults": "10"
#						},
#						{
#							"type": "TEXT_DETECTION",
#							"maxResults": "10"
#						},
#						{
#							"type": "LANDMARK_DETECTION",
#							"maxResults": "10"
#						},
#						{
#							"type": "WEB_DETECTION",
#							"maxResults": "10"
#						}
#				 ]
#			 }
#		]
#	}
#	output_filename = 'vision_%s.json'%image_filename_ne
#	
#	with open(output_filename, 'w') as output_file:
#		json.dump(parameters_pic_raw, output_file, indent = 4)
#		
#	parameters_pic = open(output_filename,'rb').read()
#	response_pic = requests.post(url = API_ENDPOINT_pic+'?key='+API_KEY_pic, data = parameters_pic)
#	
#	vision_results = response_pic.json()
#	itchat.send(('助手A：\n 图片文字：' + vision_results['responses'][0]['textAnnotations'][0]['description']), msg['FromUserName'])
#	itchat.send(('助手A：\n 图片内容分析：' + str([vision_results['responses'][0]['labelAnnotations'][index]['description'] for index in range(len(vision_results['responses'][0]['labelAnnotations']))])[1:-1]), msg['FromUserName'])
#	#vision_results['responses'][0]['webDetection']['bestGuessLabels'][0]['label']
#	itchat.send(('助手A：\n 相似图片：' + vision_results['responses'][0]['webDetection']['visuallySimilarImages'][0]['url']), msg['FromUserName'])
#	#return '%s received' % msg['Type']
	
#@itchat.msg_register([RECORDING, ATTACHMENT, VIDEO])
#def download_files(msg):
#	f = open(msg.fileName, 'wb')
#	print(f)
	
@itchat.msg_register([RECORDING])
def recordReply(msg):
	order = 0
	if order <=1:
		itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])
	itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
	itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
	itchat.send(('助手A：%s收到啦' % msg['Type']), msg['FromUserName'])

@itchat.msg_register([SHARING])
def sharingReply(msg):
	order = 0
	if order <=1:
		itchat.send(('系统提示：内容若涉及国家机密，请您遵守所在国家及地区法律。'), msg['FromUserName'])
	itchat.send(('助手A：TA不在，发送文本消息，我可以陪您畅所欲言，衣食住行，天文地理，有问必答哦~'), msg['FromUserName'])
	itchat.send(('助手A：发送图片，我还可以为您做图片分析呢。'), msg['FromUserName'])
	itchat.send(('助手A：%s已接收' % msg['Type']), msg['FromUserName'])
#		pass

#@itchat.msg_register([PICTURE])
#def download_files(msg):
#	msg.download(msg.fileName)
#	itchat.send('@%s@%s' % (
#		'img', msg['FileName']),
#		msg['FromUserName'])
#	return '%s received' % msg['Type']

if __name__ == '__main__':
		index = 0
		freqs = 0
		freqs2 = 0
		freqs3 = 0
		freqs4 = 0
		freqs5 = 0
		itchat.auto_login(enableCmdQR=False,hotReload=False)
		itchat.run()


#data = open('request.json', 'rb').read()


# 李TA @@3a3683f0a1f883491e0e9f0d3d7787a0ccac8517cad1c2a47924395933229462
# 李TA（Victor）@07be37eb8d53d09e8b6a1d83110ab507a9dfa9a35ea338ba778da235d58d2bdd
# 树群 @@1304c51149762594d5ce4e7256d5771315262722996a68019cb8cd6964354fc4
# 我家（My Family） @@20e51126fe77612b69daa7f7b45a500f214697b1b7a2fb3cd49cf04d55f755cd

#@itchat.msg_register([TEXT])
#def text_reply(msg):
#	match = re.search('年', msg['Text']).span()
#	if match:
#		itchat.send(('新年快乐啊！'), msg['FromUserName'])
#	else:
#		itchat.send(('系统错误：内容涉及涉及国家机密。'))
#
#@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
#
#def other_reply(msg):
#	itchat.send(('系统错误：内容涉及涉及国家机密。'))
#
#@itchat.msg_register([VIDEO])
#def videoReply(msg):
#	itchat.send(('2333!Got it!'), msg['FromUserName'])
#
#@itchat.msg_register([PICTURE])
#def picReply(msg):
#	itchat.send(('系统错误：内容涉及涉及国家机密。'))
#
#@itchat.msg_register([RECORDING])
#def recordReply(msg):
#	itchat.send(('系统错误：内容涉及涉及国家机密。'))
#
#@itchat.msg_register([SHARING])
#def sharingReply(msg):
#	itchat.send(('系统错误：内容涉及涉及国家机密。'))
#
#if __name__ == '__main__':
#	
#	itchat.auto_login(enableCmdQR=False,hotReload=False)
#	itchat.run()

#itchat.auto_login(True)
#itchat.run()


#def other_reply(msg):
#	itchat.send(('系统错误：内容涉及涉及国家机密。'))

	
#itchat.auto_login(enableCmdQR=True, hotReload=True)
#itchat.run()