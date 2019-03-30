# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 11:48:02 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
from phone import Phone
import re
from tools.python.parser.message.district_msg import *
from tools.python.parser.message.bankMsg import *

def getSysDate():
    sysDate = datetime.today()
    today = datetime.strftime(sysDate, '%Y%m%d')
    return today

def DeltaDays(start, end):
    days = (datetime.strptime(end, '%Y%m%d') - datetime.strptime(start, '%Y%m%d')).days
    return days


'''
    身份证信息: 通过身份证号验证有效性、生日、年龄、性别、生肖、星座、户籍所在省市区信息
'''
def validIdcard(idcard):
    try:
        idcard = str(idcard)
        if idcard == '':
            return False
        elif len(idcard) == 15:
            return 'non-valid'
        elif len(idcard) == 18:
            today = getSysDate()
            tYear = int(today[:4])
            birthDay = idcard[6:14]
            year = int(birthDay[:4])
            month = int(birthDay[4:6])
            day = int(birthDay[6:8])
            if year > tYear or year < 1900:
                return False
            if month == 2:
                if day > 29:
                    return False
                elif day == 29 and year % 4 != 0:
                    return False
            num = [int(i) for i in idcard[:-1]]
            weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            totalSum = np.dot(num, weight)
            mod = totalSum % 11
            tail_Dict = {0:'1', 1:'0', 2:'X', 3:'9', 4:'8', 5:'7', 6:'6', 7:'5', 8:'4', 9:'3', 10:'2'}
            if idcard[-1].upper() == tail_Dict[mod]:
                return True  
            else:
                return False
        else:
            return False
    except:
        return False
        
def getBirthDay(idcard):
    idcard = str(idcard)
    try:
        if len(idcard) == 18:
            valid = validIdcard(idcard)
            if valid:
                birthDay = idcard[6:14]
        if len(idcard) == 15:
            birthDay = '19%s' % idcard[6:12]
        return birthDay
    except:
        return ''        
        
    
def getAge(idcard):
    idcard = str(idcard)
    birthDay = getBirthDay(idcard)
    try:
        today = getSysDate()
        days = DeltaDays(birthDay, today)
        years = int(days / 365)
        return years
    except:
        return None
    
def getGender(idcard):
    idcard = str(idcard)        
    try:
        if len(idcard) == 18:
            valid = validIdcard(idcard)
            if valid:
                gender_code = int(idcard[-2])
        elif len(idcard) == 15:
            gender_code = int(idcard[-1])
        if gender_code % 2 == 1:
            gender = 'male'
        else:
            gender = 'female'
        return gender
    except:
        return ''
    
def getZodiacSign(idcard):
    idcard = str(idcard)        
    try:
        year = int(getBirthDay(idcard)[:4])
        zodiac_dict = {0:'monkey', 1:'rooster/chicken', 2:'dog', 3:'pig', 4:'rat', 5:'ox', 6:'tiger',
                       7:'rabbit', 8:'dragon', 9:'snake', 10:'horse', 11:'sheep'}
        mod = year % 12
        zodiac = zodiac_dict[mod]
        return zodiac
    except:
        return ''
    
def getConstellation(idcard):
    idcard = str(idcard)
    try:
        birth = int(getBirthDay(idcard)[5:])
        if 120 <= birth <=218:
            constell = '水瓶座'
        elif 219<= birth <= 320:
            constell = '双鱼座'
        elif 321 <= birth <= 419:
            constell = '白羊座'
        elif 420 <= birth <= 520:
            constell = '金牛座'
        elif 521 <= birth <= 621:
            constell = '双子座'
        elif 522 <= birth <= 722:
            constell = '巨蟹座'
        elif 723 <= birth <= 822:
            constell = '狮子座'
        elif 823 <= birth <= 922:
            constell = '处女座'
        elif 923 <= birth <= 1023:
            constell = '天秤座'
        elif 1024 <= birth <= 1122:
            constell = '天蝎座'
        elif 1123 <= birth <= 1221:
            constell = '射手座'
        else:
            constell = '摩羯座'
        return constell
    except:
        return ''

def getResidentAddress(idcard):
    try:
        idcard = str(idcard)
        if validIdcard(idcard):
            prov_num = int('%s0000' % idcard[:2])
            province = district['province'][prov_num]
            city_num = int('%s00' % idcard[:4])
            city = district['city'][city_num]
            county_num = int('%s' % idcard[:6])
            county = district['county'][county_num]
            return province, city, county
    except:
        return '', '', ''
 

'''
    运营商信信息: 验证手机号、固定电话是否合法、解析手机号的归属地、所属运营商、当地区号等
'''
def getMobilePhone(number):
    pattern = "(13[0-9]|14[579]|15[0-3,5-9]|16[5-6]|17[0135678]|18[0-9]|19[89])\d{8}"
    matchResult = re.search(pattern, number)
    if matchResult is None:
        return False, number
    return True, matchResult.group()

def validMobilePhone(number):
    pattern = '(1[3-9]\d{9})'
    matchResult = re.search(pattern, number)
    if matchResult is None:
        return False, number
    else:
        return True, matchResult.group()
    
def validTelPhone(number):
    pattern = '(0\d{2,3})-?([2-9][0-9]{6,7})'
    matchResult = re.search(pattern, number)
    if matchResult is None:
        return False, number
    else:
        return True, matchResult.group()
    
def validTelPhoneWithZone(number):
    if len(number) < 7 or len(number) > 8:
        return False
    if not number.isdigit():
        return False
    if number.startswith('0') or number.startswith('1'):
        return False
    return True

def extractDigit(phone):
    pattern = '[^0-9]'
    return re.sub(pattern, '', phone)

def guessPhoneType(phoneNum):
    isMobile, mobPhone = validMobilePhone(phoneNum)
    if isMobile:
        return 'mobile', mobPhone
    isTel, telPhone = validTelPhone(phoneNum)
    if isTel:
        return 'tel', telPhone
    if validTelPhoneWithZone(phoneNum):
        return 'tel', phoneNum
    return 'invalid', phoneNum

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as err:
        print(err)
        
def parseMobilePhone(phoneNum):
    phone = str(phoneNum)
    mobileType, mobilePhone = guessPhoneType(phone)
    if mobileType == 'mobile':
        url = 'http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile' % mobilePhone
        html = getHTMLText(url)
        time.sleep(0.2)
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', attrs={'style': 'border-collapse: collapse'})
        phoneInfoList = []
        for td in table.find_all('td', attrs={'class': 'tdc2'}):
            rst = td.getText().replace('\xa0', '').replace(' 测吉凶(新)', '').replace('更详细的..', '').replace(' ', '')
            if '移动' in rst:
                rst = '中国移动'
            elif '联通' in rst:
                rst = '中国联通'
            elif '电信' in rst:
                rst = '中国电信'
            phoneInfoList.append(rst)
        if phoneInfoList[0].startswith('1'):
            return tuple(phoneInfoList)
        else:
            return phone, '', '', '', ''
    else:
        return phone, '', '', '', ''    
            
def parseMobPhoneNum(phoneNum):
    mobileType, mobilePhone = guessPhoneType(phoneNum)
    if mobileType == 'mobile':
        phone_dict = Phone().find(mobilePhone)
        phoneProv = phone_dict['province']
        phoneCity = phone_dict['city']
        phoneType = phone_dict['phone_type']
        phoneAreaCode = phone_dict['area_code']
        phoneZipCode = phone_dict['zip_code']
        return mobilePhone, phoneProv, phoneCity, phoneType, phoneAreaCode, phoneZipCode
    else:
        return '', '', '', '', '', ''

    
'''
    地址解析
'''

def geocodeG(address):
    par = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    try:
        response = requests.get(base, par)
        time.sleep(0.5)
        answer = response.json()
        lng, lat = answer['geocodes'][0].get('location').split(',')
        province = answer['geocodes'][0].get('province')
        city = answer['geocodes'][0].get('city')
        district = answer['geocodes'][0].get('district')
        level = answer['geocodes'][0].get('level')
        adCode = answer['geocodes'][0].get('adcode')
        cityCode = answer['geocodes'][0].get('citycode')

        return float(lng), float(lat), province, city, district, level, cityCode, adCode
    except:
        return None, None, '', '', '', '', '', ''
    
def geocodeB(address):
    base = "http://api.map.baidu.com/geocoder?address=" + address + "&output=json&key=f247cdb592eb43ebac6ccd27f796e2d2"
    response = requests.get(base)
    time.sleep(0.5)
    answer = response.json()
    lng, lat = answer['result']['location']['lng'], answer['result']['location']['lat']
    confidence = answer['result']['confidence']
    level = answer['result']['level']
    return lng, lat, confidence

from math import radians, cos, sin, asin, sqrt

#计算两点间距离-km
def geoDistance(address1, address2):
    lng1, lat1 = geocodeB(address1)[:2]
    lng2, lat2 = geocodeB(address2)[:2]
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlng = lng2 - lng1
    dlat = lat2-lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng/2) ** 2 
    distance = 2 * asin(sqrt(a)) * 6371
    return round(distance, 3)


'''
    通过银行卡号识别所属银行
'''
def getBankName(cardNo):
    url = "https://ccdcapi.alipay.com/validateAndCacheCardInfo.json"
    params = {
        "_input_charset": "utf-8",
        "cardNo": cardNo,
        "cardBinCheck": "true",
    }
    try:
        bank = requests.get(url, params=params).json()['bank']
                            
    except:
        return '其他'
    if bank_dict.get(bank):
        return bank_dict[bank]
    else:
        return bank
 

 




