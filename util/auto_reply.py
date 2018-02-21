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
            js = json.loads(resp)
            if js['code'] == 100000:
                return js['text'].replace('<br>', '\n')
            elif js['code'] == 200000:
                return js['url']
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
