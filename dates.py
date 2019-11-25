# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 02:29:35 2019

@author: niran
"""

## Importing Libraries
from flask import Flask
from flask import request
from flask_restful import Resource
from flask_restful import Api

import base64
import PIL.Image
import cv2
import numpy as np
import pytesseract
import re
import io


app = Flask(__name__)
api = Api(app)

def iserror(func, int, **kw):
        try:
            func(int, **kw)
            return False
        except Exception:
            return True


@app.route('/', methods=['POST'])

class Image(Resource):
    def post(self, name):
        dict_gt = []
        request_data=raw_b64_imagedata=raw_data = None
        request_data = request.get_json()
        raw_b64_imagedata = request_data['img_data']

        raw_data = {
            'img_data': raw_b64_imagedata,
            'name': name
        }
        
        ####################################
        ###################################
        
        bytes1 = bytes(raw_data["img_data"][1:], 'utf-8')
        imgdata_dict = base64.b64decode(bytes1)
        zxc = PIL.Image.open(io.BytesIO(imgdata_dict))
        qqq = np.array(zxc)
        gray = cv2.cvtColor(qqq, cv2.COLOR_BGR2GRAY)
        
        for i in range(120, 201):
            gray_thresh=text_gray_thresh=matches=dates = None
            thresh_val = i
            ret, gray_thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
            text_gray_thresh = pytesseract.image_to_string(gray_thresh)
            pattern = re.compile(r'\w{1,3}[-./*]\w{1,3}[-./*]\d{2,4}')
            matches = pattern.finditer(text_gray_thresh)

            for match in matches:
                dates = text_gray_thresh[match.start() : match.end()]
                dict_gt.append(dates)
            
            
        if dict_gt == []: 

            return('Date: NIL')

        else:

            count_gt = [None] * len(dict_gt)
            for d in range (0,len(dict_gt)):
                count_gt[d] = dict_gt.count(dict_gt[d])

            pos=date=date_gt = None
            pos = count_gt.index(max(count_gt))
            date_gt = dict_gt[pos]       
            date = date_gt

            temp= [] 
            matches = None
            patt = re.compile(r'[\ \-\.\/\*]')
            matches = patt.finditer(date)                    

            for match in matches:
                temp.append(match.start())
             
            temp_1=temp_2=temp_3 = None    
            temp_1 = date[0:temp[0]]
            temp_2 = date[temp[0]+1:temp[1]]
            temp_3 = date[temp[1]+1:]

            date_yr = temp_3
            if temp_1.lower() in ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'):
                date_m = temp_1
                date_d = temp_2

            elif temp_2.lower() in ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'):
                date_m = temp_2
                date_d = temp_1
            
            elif iserror(int, temp_1) == True or iserror(int, temp_2) == True or iserror(int, temp_3) == True:
                date_yr = 'N'
                date_m = 'I'
                date_d = 'L'

            elif temp_1 in ('0','00','000') or temp_2 in ('0','00','000') or temp_3 in ('0','00','000'):
                date_yr = 'N'
                date_m = 'I'
                date_d = 'L'
            
            elif int(temp_1) >= 12 and int(temp_2) <= 12:
                date_m = temp_2
                date_d = temp_1

            elif int(temp_2) >= 12 and int(temp_1) <= 12:
                date_m = temp_1
                date_d = temp_2

            else:
                date_m = temp_2
                date_d = temp_1


            return('Date: ' + date_yr + '-' + date_m + '-' + date_d)
        
        #####################################
        #########################################
        
        
        #return('working')
        #return raw_data['img_data'][1:]
        
api.add_resource(Image, '/<string:name>')

app.run(port=5000)