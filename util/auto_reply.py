# -*- coding: utf-8 -*-
import json
import requests
import traceback
import numpy as np


class TulingAutoReply:
    def __init__(self, tuling_key, tuling_url):
        self.key = tuling_key
        self.url = tuling_url

    def reply(self, unicode_str):
        body = {'key': self.key, 'info': unicode_str.encode('utf-8')}
        r = requests.post(self.url, data=body)
        r.encoding = 'utf-8'
        resp = r.text
        if resp is None or len(resp) == 0:
            return None
        try:
            # js = json.loads(resp)
            # if js['code'] == 100000:
            #     return js['text'].replace('<br>', '\n')
            # elif js['code'] == 200000:
            #     return js['url']
            
            # replied_data = req.json()
            replied_data = json.loads(resp)

            
            if replied_data['code'] == 100000:
                print(replied_data['code'])
                print(replied_data['text'])
                return ('Albert Mozart: ' + replied_data['text'].replace('<br>', '\n'))

            elif replied_data['code'] == 200000:
                print(replied_data['code'])
                print(replied_data['text'])
                print(replied_data['url'])
                return('Albert Mozart: ' + replied_data['text'] + '\n' + 'Albert Mozart: 请点击如下链接吧，\n' + replied_data['url'])
                # return('Albert Mozart: 请点击如下链接吧，\n' + replied_data['url'])

            elif replied_data['code'] == 302000:  # news
                print(replied_data['code'])
                print(replied_data['text'])
                print(replied_data['list'])
                news = ''
                news_number = 10
                news_i = 0
                for news_i in range(np.array([len(replied_data['list']), news_number]).min()):
                    news = news + replied_data['list'][news_i]['article'] + ', url: ' + replied_data['list'][news_i]['detailurl'] + ' --来自' + replied_data['list'][news_i]['source'] + '；' + '\n'
                # news_i += 1
                return('Albert Mozart: ' + replied_data['text'].replace('<br>', '\n') + '\n' + 'Albert Mozart: 请浏览如下内容并点击阅读详情啦，\n' + news)
                # return('Albert Mozart: 请浏览如下内容并点击阅读详情啦，\n' + news)

            elif replied_data['code'] == 308000:  # recipe
                print(replied_data['code'])
                print(replied_data['text'])
                print(replied_data['list'])
                recipes = ''
                recipes_number = 5
                recipes_i = 0
    
                for recipes_i in range(np.array([len(replied_data['list']), recipes_number]).min()):
                    recipes = recipes + replied_data['list'][recipes_i]['name'] + ', url: ' + replied_data['list'][recipes_i]['info'] + ' --详情' + replied_data['list'][recipes_i]['detailurl'] + '；' + '\n'
                # recipes_i += 1
                return('Albert Mozart: ' + replied_data['text'].replace('<br>', '\n') + '\n' + 'Albert Mozart: 请参考如下内容并点击查看详情哦 ~ \n' + recipes)
                # return('Albert Mozart: 请参考如下内容并点击查看详情哦 ~ \n' + recipes)

            elif replied_data['code'] == 313000:  # song
                print(replied_data['code'])
                print(replied_data['text'])
                print(replied_data['function'])
                return('Albert Mozart: ' + replied_data['text'].replace('<br>', '\n') + '\n' + 'Albert Mozart: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['song'] + ' --来自' + replied_data['function']['singer'])
                # return('Albert Mozart: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['song'] + ' --来自' + replied_data['function']['singer'])

            elif replied_data['code'] == 314000:  # poetry
                print(replied_data['code'])
                print(replied_data['text'])
                print(replied_data['function'])
                return('Albert Mozart: ' + replied_data['text'].replace('<br>', '\n') + '\n' + 'Albert Mozart: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['name'] + ' --来自' + replied_data['function']['author'])
                # return('Albert Mozart: 请欣赏如下内容并点击仔细品味吧，\n' + replied_data['function']['name'] + ' --来自' + replied_data['function']['author'])

            else:
                print(replied_data['code'])
                print(replied_data['text'])
                return('Albert Mozart: ' + replied_data['text'].replace('<br>', '\n'))
            else:
                return None
        
        except Exception:
            traceback.print_exc()
            return None

class GoogleVision_AutoReply:
    def __init__(self, google_vis_key, google_vis_url):
        self.key = google_vis_key
        self.url = google_vis_url
        
    def analyse(self, picture_url, picture_mediaID, picture_msgID, picture_createtime):
        parameters_pic_raw = {
            "requests":[
                {
                    "image":{
                        "source":{
                            "imageUri":
                                '%s'%picture_url
                        }
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

        output_filename = 'vision_parameters.json' #%picture_mediaID
        with open(output_filename, 'w') as output_file:
            json.dump(parameters_pic_raw, output_file, indent = 4)
        
        print ('Pmid: ' + picture_msgID)
        print ('Pct: ' + picture_createtime)
        print (output_filename)
        print (parameters_pic_raw)
        
        parameters_pic = open(output_filename,'rb').read()
        #print ('parameters_pic: ' + parameters_pic)
        print('google key: '+self.key)
        print('google url: '+self.url)
        response_pic = requests.post(url = self.url + '?key=' + self.key, data = parameters_pic)
        print ('response_pic_info: ' + str(np.info(response_pic)))
        
        vision_results = response_pic.json()
        print ('vision_results: ' + str(vision_results))
        return vision_results


class DefaultAutoReply:
    def __init__(self):
        pass

    def reply(self, unicode_str):
        return None
