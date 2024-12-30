import requests
from flask import Flask, request, jsonify
import json
import datetime
from datetime import date, datetime, timedelta
import urllib
import urllib.request 
import ssl
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.parse
import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from create_table_image import create_table_image
import pandas as pd
from table_to_2d import table_to_2d
from PIL import Image, ImageDraw, ImageFont
import random
app = Flask(__name__)

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    req = request.get_json(silent=True, force = True)
    user_result = req.get('userRequest')
    action = req.get('action')   
    contexts = req.get('contexts')
    user_input = request.json['userRequest']['utterance']
    print(user_input)       
    
    # 생활관 시설현황_인원현황 블록      
    if user_result.get('block')['name'] == '생활관 시설현황_인원현황':
        # 웹 페이지 가져오기
        url = 'https://domi.seoultech.ac.kr/site/dormitory/popup/info.jsp'
        response = requests.get(url)
        html_lol = response.content
        soup = BeautifulSoup(html_lol, 'html.parser')
        table = soup.select("table")
        df = pd.read_html(str(table))[1]

        # 테이블 데이터 확인

        # 표 이미지 생성
        table_image = create_table_image(df)
       

        # 이미지를 파일로 저장
        image_path = r'/root/static/images/table_image.png'
        table_image.save(image_path, "png")
        
        # 이미지 파일의 URL 생성
        # https://tohttps.hanmesoft.com/ 참고 
        image_url = 'https://tohttps.hanmesoft.com/forward.php?url=http%3A%2F%2F101.101.208.100%3A5000%2Fstatic%2Fimages%2Ftable_image.png'  
        

        # 이미지를 카카오톡 응답에 첨부
        res = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'simpleImage': {
                            'imageUrl': image_url,
                            'altText': '테이블 시각화'
                        }
                    }
                ]
            }
        }
        
        return jsonify(res)
    # 생활관 성과평가 블록    
    if user_result.get('block')['name'] == '생활관 성과평가':
        # 웹 페이지 가져오기
        url = 'https://domi.seoultech.ac.kr/site/dormitory/popup/info.jsp'
        response = requests.get(url)
        html_lol = response.content
        soup = BeautifulSoup(html_lol, 'html.parser')
        table = soup.select("table")

        res = {
            'version': '2.0',
            'template': {
                'outputs': []
            }
        }
    
        # 빈 리스트 생성
        images_list = []

        
        for i in range (6,10):
            df = pd.read_html(str(table))[i]

            # 테이블 데이터 확인
            

            # 표 이미지 생성
            table_image = create_table_image(df)

            # 이미지에 표 이름 추가
            if i == 6:
                table_name = "2021년 1분기 (성림학사) 성과평가 결과"
            elif i == 7:
                table_name = "2021년 2분기 (성림학사) 성과평가 결과"
            elif i == 8:
                table_name = "2021년 3분기 (성림학사) 성과평가 결과"
            elif i == 9:
                table_name = "2021년 4분기 (성림학사) 성과평가 결과"
            


            # 폰트 경로 설정
            font_path = r'/root/NanumGothic.ttf'
    
            # 텍스트를 이미지 위에 추가
            draw = ImageDraw.Draw(table_image)
            font = ImageFont.truetype(font_path, 25)  # 원하는 폰트와 크기로 설정
            text_width, text_height = draw.textsize(table_name, font=font)
            text_x = (table_image.width - text_width) // 2
            text_y = table_image.height - text_height - 10  # 텍스트를 이미지 하단에 추가하려면 조정
            draw.text((text_x, text_y), table_name, fill="black", font=font)  # 원하는 위치에 텍스트 추가
               

            # 이미지를 파일로 저장
            image_path = rf'/root/static/images/table_image_{i}.png'
            table_image.save(image_path, "png")
            

            image_url = f'https://tohttps.hanmesoft.com/forward.php?url=http%3A%2F%2F101.101.208.100%3A5000%2Fstatic%2Fimages%2Ftable_image_{i}.png'  



            # 이미지를 카카오톡 응답에 첨부
            images_list.append({
                'simpleImage': {    
                    'imageUrl': image_url,
                    'altText': f'테이블 시각화 {i}'
                }
            })

        for i in range (11,15):
            df = pd.read_html(str(table))[i]

            # 테이블 데이터 확인
            

            # 표 이미지 생성
            table_image = create_table_image(df)

            # 이미지에 표 이름 추가
            if i == 11:
                table_name = "2021년 1분기 (수림학사,누리학사) 성과평가 결과"
            elif i == 12:
                table_name = "2021년 2분기 (수림학사,누리학사) 성과평가 결과"
            elif i == 13:
                table_name = "2021년 3분기 (수림학사,누리학사) 성과평가 결과"
            elif i == 14:
                table_name = "2021년 4분기 (수림학사,누리학사) 성과평가 결과"

            # 폰트 경로 설정
            font_path = r'/root/NanumGothic.ttf'

            

            # 텍스트를 이미지 위에 추가
            draw = ImageDraw.Draw(table_image)
            font = ImageFont.truetype(font_path, 25)  # 원하는 폰트와 크기로 설정
            text_width, text_height = draw.textsize(table_name, font=font)
            text_x = (table_image.width - text_width) // 2
            text_y = table_image.height - text_height - 10  # 텍스트를 이미지 하단에 추가하려면 조정
            draw.text((text_x, text_y), table_name, fill="black", font=font)  # 원하는 위치에 텍스트 추가
               

            # 이미지를 파일로 저장
            image_path = rf'/root/static/images/table_image_{i}.png'
            table_image.save(image_path, "png")
        
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #
            image_url = f'https://tohttps.hanmesoft.com/forward.php?url=http%3A%2F%2F101.101.208.100%3A5000%2Fstatic%2Fimages%2Ftable_image_{i}.png'  
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #

            # 이미지를 카카오톡 응답에 첨부
            images_list.append({
                'simpleImage': {    
                    'imageUrl': image_url,
                    'altText': f'테이블 시각화 {i}'
                }
            })
    
        # 반복문이 모든 표를 처리한 후에 이미지 리스트를 응답에 추가
        res['template']['outputs'] = images_list
    
        return jsonify(res)       
    # 날씨    
    if user_result.get('block')['name'] == '날씨-예':
        now = datetime.now()
        nowDate = now.strftime('%Y년 %m월 %d일 %H시 %M분 입니다.')

        ful_text1 = nowDate
        ful_text2 = '오늘의 날씨 정보입니다.\n'

        # 네이버 날씨 크롤링
        context = ssl._create_unverified_context()
        webpage = urllib.request.urlopen('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B3%B5%EB%A6%89%EB%8F%99+%EB%82%A0%EC%94%A8&oquery=%EA%B3%B5%EB%A6%89&tqi=itC8cwp0YihssT1HIpwssssstWK-291962',context=context)
        soup = BeautifulSoup(webpage, 'html.parser')
        temps = soup.find('div', 'temperature_text')
        summary = soup.find('p', 'summary')
        ful_text3 = "공릉동 " + temps.text.strip()
        ful_text4 = summary.text.strip()

        html = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EA%B3%B5%EB%A6%89%EB%8F%99+%EB%82%A0%EC%94%A8')
        #pprint(html.text)

        soup = BeautifulSoup(html.text,'html.parser')

        data1 = soup.find('div',{'class':'report_card_wrap'})
        #pprint(data1)

        data2 = data1.findAll('li')
        #pprint(data2)

        fine_dust = data2[0].find('span',{'class':'txt'}).text
        ful_text5 = "미세먼지 농도:", fine_dust

        ultra_fine_dust = data2[1].find('span',{'class':'txt'}).text
        ful_text6 ="초미세먼지 농도:", ultra_fine_dust

        UV_rays = data2[2].find('span',{'class':'txt'}).text
        ful_text7 = "자외선:", UV_rays 

        sunset = data2[3].find('span',{'class':'txt'}).text
        ful_text8 = "일몰:", sunset 

        answer = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3)) + "\n" + ''.join((ful_text4)) + "\n" +''.join((ful_text5)) + "\n" +''.join((ful_text6)) + "\n" +''.join((ful_text7)) + "\n" +''.join((ful_text8)) + "\n" 
        
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }

        return jsonify(res)
    # 식단
    if user_result.get('block')['name'] == '학식제공':
        params = None
        if len(contexts) > 0:
            params = contexts[0].get('params')
        
        if action.get('clientExtra') == {'건물': '학생제2식당'} or (params and params.get('건물이름_번호_2', {}).get('resolvedValue') == '제2학생회관'):
            now = datetime.now()
            nowDate = now.strftime('%Y년 %m월 %d일')
            url = 'https://www.seoultech.ac.kr/life/student/food2/'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')            
            divSoup = soup.find('div', {'class': 'dts_design'})
            message_div = divSoup.find_all('table')
            if message_div:
                launch = message_div[0]
                dinner = message_div[1]
                menu_items = []
                menu_items1 = []

                for row in launch.find_all('tr')[1:]:  # 첫 번째 행은 헤더이므로 제외
                    columns = row.find_all('td')
                    menu = columns[0].text.strip()
                    menu_name = columns[2].get_text(strip=True).replace(" ", "")  # 띄어쓰기 제거
                    price = columns[1].text.strip()  
                    menu_items.append(f"{menu} : {menu_name} {price}")

                for row1 in dinner.find_all('tr')[1:]:  # 첫 번째 행은 헤더이므로 제외
                    columns1 = row1.find_all('td')
                    menu1 = columns1[0].text.strip()
                    menu_name1 = columns1[2].get_text(strip=True).replace(" ", "")  # 띄어쓰기 제거
                    price1 = columns1[1].text.strip() 
                    menu_items1.append(f"{menu1} : {menu_name1} {price1}")

                message = "\n".join(menu_items)
                message1 = "\n".join(menu_items1)
                ful_text1 = nowDate
                ful_text2 = '점심'
                ful_text3 = message
                ful_text4 = '저녁'
                ful_text5 = message1
                answer = ''.join((ful_text1)) + "\n" + ''.join((ful_text2))+ "\n" + ''.join((ful_text3))+ "\n" + ''.join((ful_text4))+ "\n" + ''.join((ful_text5))
            else :
                answer = '등록된 식단이 없습니다.'
        if action.get('clientExtra') == {'건물': '테크노파크'} or (params and params.get('건물이름_번호_2', {}).get('resolvedValue') == '서울테크노파크'):
            now = datetime.now()
            nowDate = now.strftime('%Y년 %m월 %d일')
            
            ful_text1 = nowDate
            ful_text2 = '테크노파크(STP) 식단은 테크노파크사정으로 제공되지 않습니다.'
            ful_text3 = 'http://www.seoultp.or.kr/user/nd70791.do'
            answer = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3))
        if action.get('clientExtra') == {'건물': 'KB학사'} or (params and params.get('건물이름_번호_2', {}).get('resolvedValue') == 'KB학사'):
            today = datetime.today().strftime('%A')
            url = 'https://domi.seoultech.ac.kr/support/food/?foodtype=kb'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            divSoup = soup.find('div',{'class': 't4'})

            if divSoup:
                message_div = divSoup.find('table',{'class':'chang'})
                row = message_div.find_all('tr')
                if today == 'Monday':
                    ful_text1 = '오늘은 월요일 입니다' 
                    columns = row[0].find('td')
                    if len(columns) > 0:
                        ful_text2 = columns.text.strip()
                elif  today == 'Tuesday':
                    ful_text1 = '오늘은 화요일 입니다' 
                    columns = row[1].find('td')
                    if len(columns) > 0:
                        ful_text2 = columns.text.strip()
                elif today == 'Wednesday':
                    ful_text1 = '오늘은 수요일 입니다' 
                    columns = row[2].find('td')
                    if len(columns) > 0:
                        ful_text2 = columns.text.strip()
                elif today == 'Thursday':
                    ful_text1 = '오늘은 목요일 입니다' 
                    columns = row[3].find('td')
                    if len(columns) > 0:
                        ful_text2 = columns.text.strip()
                elif today == 'Friday':
                    ful_text1 = '오늘은 금요일 입니다' 
                    columns = row[4].find('td')
                    if len(columns) > 0:
                        ful_text2 = columns.text.strip()
                elif today == 'Saturday':
                    ful_text1 = '오늘은 토요일 입니다' 
                    columns = row[5].find('td')
                    if len(columns) > 0:
                        ful_text2 = columns.text.strip()
                elif today == 'Sunday':
                    ful_text1 = '오늘은 일요일 입니다' 
                    columns = row[6].find('td')
                    if len(columns) > 0:
                        ful_text2 = columns.text.strip()
            else: 
                ful_text1 = 'KB학사 식당 미운영'
                ful_text2 =''
            ful_text3 = url
            answer = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3))
        if action.get('clientExtra') == {'건물': '성림학사'} or (params and params.get('건물이름_번호_2', {}).get('resolvedValue') == '성림학사'):
            today = datetime.today().strftime('%A')
            url = 'https://domi.seoultech.ac.kr/support/food/?foodtype=sung'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            divSoup = soup.find('div',{'class': 't4'})
            message_div = divSoup.find('table',{'class':'chang'})
            row = message_div.find_all('tr')
            if today == 'Monday':
                ful_text1 = '오늘은 월요일 입니다' 
                columns = row[0].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif  today == 'Tuesday':
                ful_text1 = '오늘은 화요일 입니다' 
                columns = row[1].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Wednesday':
                ful_text1 = '오늘은 수요일 입니다' 
                columns = row[2].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Thursday':
                ful_text1 = '오늘은 목요일 입니다' 
                columns = row[3].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Friday':
                ful_text1 = '오늘은 금요일 입니다' 
                columns = row[4].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Saturday':
                ful_text1 = '오늘은 토요일 입니다' 
                columns = row[5].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Sunday':
                ful_text1 = '오늘은 일요일 입니다' 
                columns = row[6].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            
            ful_text3 = url
            answer = f"{ful_text1}\n{ful_text2}\n{ful_text3}"
        if action.get('clientExtra') == {'건물': '수림학사'} or (params and params.get('건물이름_번호_2', {}).get('resolvedValue') == '수림학사'):
            today = datetime.today().strftime('%A')
            url = 'https://domi.seoultech.ac.kr/support/food/?foodtype=surim'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            divSoup = soup.find('div',{'class': 't4'})
            message_div = divSoup.find('table',{'class':'chang'})
            row = message_div.find_all('tr')
            if today == 'Monday':
                ful_text1 = '오늘은 월요일 입니다' 
                columns = row[0].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif  today == 'Tuesday':
                ful_text1 = '오늘은 화요일 입니다' 
                columns = row[1].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Wednesday':
                ful_text1 = '오늘은 수요일 입니다' 
                columns = row[2].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Thursday':
                ful_text1 = '오늘은 목요일 입니다' 
                columns = row[3].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Friday':
                ful_text1 = '오늘은 금요일 입니다' 
                columns = row[4].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Saturday':
                ful_text1 = '오늘은 토요일 입니다' 
                columns = row[5].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            elif today == 'Sunday':
                ful_text1 = '오늘은 일요일 입니다' 
                columns = row[6].find('td')
                if len(columns) > 0:
                    ful_text2 = columns.text.strip()
            
            ful_text3 = url
            answer = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3))
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }

        return jsonify(res)
    # 건물
    if user_result.get('block')['name'] == '건물위치':
        
        if '건물이름_번호' in action.get('params'):
            building_name = action.get('params')['건물이름_번호']        
            
            with open('buildings.json', 'r', encoding='utf-8') as b:
                buildings = json.load(b)
            
            if building_name in buildings:
                building_info = buildings[building_name]
                building_number = building_info['번호']
                building_location = building_info['위치']
                building_addinfo = building_info.get('추가정보', "")
                building_map = building_info.get('카카오맵', None)
                
                school_site_link = 'https://www.seoultech.ac.kr/intro/map/'

                if building_map:
                    parsed_url = urllib.parse.urlparse(building_map)
                    query_dict = urllib.parse.parse_qs(parsed_url.query)
                    query_dict['og:image'] = [building_info['og:image']]
                    new_query = urllib.parse.urlencode(query_dict, doseq=True)
                    building_map = urllib.parse.urlunparse(parsed_url._replace(query=new_query))
                ful_text1 = f'\n 건물 번호{building_number}. {building_name}\n\n - 카카오지도 : "{building_map}"\n\n{building_addinfo}\n\n - 캠퍼스지도 : "{school_site_link}"\n\n - 강의실, 관련업무등 자세한 사항은 "캠퍼스지도"를 참고해주세요.'
            else:
                ful_text1 = f'{building_name}에 대한 정보를 찾을 수 없습니다.'
            answer = ''.join((ful_text1))
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }

        return jsonify(res)
    if user_result.get('block')['name'] == '건물위치2':
        params = None
        if len(contexts) > 0:
            params = contexts[0].get('params')

        building_name = params.get('건물이름_번호_2', {}).get('resolvedValue')        
            
        with open('buildings.json', 'r', encoding='utf-8') as b:
            buildings = json.load(b)
            
        if building_name in buildings:
            building_info = buildings[building_name]
            building_number = building_info['번호']
            building_location = building_info['위치']
            building_addinfo = building_info.get('추가정보', "")
            building_map = building_info.get('카카오맵', None)
                
            school_site_link = 'https://www.seoultech.ac.kr/intro/map/'

            if building_map:
                parsed_url = urllib.parse.urlparse(building_map)
                query_dict = urllib.parse.parse_qs(parsed_url.query)
                query_dict['og:image'] = [building_info['og:image']]
                new_query = urllib.parse.urlencode(query_dict, doseq=True)
                building_map = urllib.parse.urlunparse(parsed_url._replace(query=new_query))
            ful_text1 = f'\n 건물 번호{building_number}. {building_name}\n\n - 카카오지도 : "{building_map}"\n\n{building_addinfo}\n\n - 캠퍼스지도 : "{school_site_link}"\n\n - 강의실, 관련업무등 자세한 사항은 "캠퍼스지도"를 참고해주세요.'
        else:
            ful_text1 = f'{building_name}에 대한 정보를 찾을 수 없습니다.'
        answer = ''.join((ful_text1))
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }

        return jsonify(res)
    # 장학
    if user_result.get('block')['name'] == '장학-시작':
        res={
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "궁금한 내용을 선택해 주세요."
                        },
                        "items": [
                            {
                            "title": "Q. 장학금에 대해 알고 싶어요.",
                            "action": "message",
                            "messageText": "Q. 장학금에 대해 알고 싶어요.",
                            "action": "block",
                            "blockId":"646875066ce345751ec251e3",
                            "extra": {
                                "발화": "1"
                            }
                            },
                            {
                            "title": "Q. 장학금 중 교내성적 추가 장학금은 없나요?",
                            "action": "message",
                            "messageText": "Q. 장학금 중 교내성적 추가 장학금은 없나요?",
                            "action": "block",
                            "blockId":"646875066ce345751ec251e3",
                            "extra": {
                                "발화": "2"
                            }
                            },
                            {
                            "title": "Q. 장학금 중복으로 못 받나요?",
                            "action": "message",
                            "messageText": "Q. 장학금 중복으로 못 받나요?",
                            "action": "block",
                            "blockId":"646875066ce345751ec251e3",
                            "extra": {
                                "발화": "3"
                            }
                            },
                            {
                            "title": "Q. 장학금 포기에 대해 알고 싶어요.",
                            "action": "message",
                            "messageText": "Q. 장학금 포기에 대해 알고 싶어요.",
                            "action": "block",
                            "blockId":"646875066ce345751ec251e3",
                            "extra": {
                                "발화": "4"
                            }
                            },
                            {
                            "title": "Q. 장학금 기준이 어떻게 되나요?",
                            "action": "message",
                            "messageText": "Q. 장학금 기준이 어떻게 되나요?",
                            "action": "block",
                            "blockId":"646875066ce345751ec251e3",
                            "extra": {
                                "발화": "5"
                            }
                            },
                        ]
                    }
                }]
            }
        }
        return jsonify(res)
    if user_result.get('block')['name'] == '장학-1':
        if action.get('clientExtra') == {'발화': '1'}:
            res={
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "원하는 버튼을 클릭하세요."
                        },
                        "items": [
                            {
                            "title": "국가장학금",
                            "action": "message",
                            "messageText": "국가장학금",
                            "action": "block",
                            "blockId":"64689a6f03afae55d1059e4c",
                            "extra": {
                                "발화": "국장"
                            }
                            },
                            {
                            "title": "교내장학금",
                            "action": "message",
                            "messageText": "교내장학금",
                            "action": "block",
                            "blockId":"64689a6f03afae55d1059e4c",
                            "extra": {
                                "발화": "교장"
                            }
                            },
                            {
                            "title": "대학원장학금",
                            "action": "message",
                            "messageText": "대학원장학금",
                            "action": "block",
                            "blockId":"64d4c312c800862a5416f70a",
                            },
                            {
                            "title": "맞춤형 장학조회",
                            "link": {
                                "web": "https://www.seoultech.ac.kr/life/scholarship/lookup/"
                            }
                            },                       
                        ]
                    }
                }]
            }
            }
            return jsonify(res)
            
        if action.get('clientExtra') == {'발화': '2'}:
            res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "교내성적추가 장학금은 없습니다."
                        }
                    }
                ]
            }
            }

            return jsonify(res)

        if action.get('clientExtra') == {'발화': '3'}:
            res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "교내 학비감면 장학금은 원칙적으로 중복수혜가 불가합니다. 단, 중복된 학비감면 장학금 중 학생이 본인에게 유리한 장학금을 선택할 수 있습니다. 기타 교내 장학금은 장학금별 기준이 상이하니 '서울과학기술대학교 장학금 관리 지침'을 참고하시기 바랍니다."
                        }
                    }
                ]
            }
            }

            return jsonify(res)

        if action.get('clientExtra') == {'발화': '4'}:
            res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "교내장학금 포기를 원하는 경우 장학복지팀(02-970-6054~5)번으로 유선연락 바랍니다."
                        }
                    }
                ]
            }
            }

            return jsonify(res)

        if action.get('clientExtra') == {'발화': '5'}:
            res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "교내장학제도 수혜기준은 '서울과학기술대학교 장학금 관리 지침'을 참고하시기 바랍니다."
                        }
                    }
                ]
            }
            }

            return jsonify(res)
    if user_result.get('block')['name'] == '장학-2':
        if action.get('clientExtra') == {'발화': '국장'} or action.get('params') == {'서비스장학2':'국가장학금'}:
            res={
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "원하는 버튼을 클릭하세요."
                        },
                        "items": [
                            {
                            "title": "소득연계형 국가장학금",
                            "action": "message",
                            "messageText": "소득연계형 국가장학금",
                            "action": "block",
                            "blockId":"6468a9432ecb0e7d2bec3fd9",
                            "extra": {
                                "발화": "소득연계형 국가장학금"
                            }
                            },
                            {
                            "title": "국가근로장학금",
                            "action": "message",
                            "messageText": "국가근로장학금",
                            "action": "block",
                            "blockId":"6468a9432ecb0e7d2bec3fd9",
                            "extra": {
                                "발화": "국가근로장학금"
                            }
                            },
                            {
                            "title": "국가우수장학금",
                            "action": "message",
                            "messageText": "국가우수장학금",
                            "action": "block",
                            "blockId":"6468a9432ecb0e7d2bec3fd9",
                            "extra": {
                                "발화": "국가우수장학금"
                            }
                            },
                            {
                            "title": "중소기업취업연계장학금(희망사다리)",
                            "action": "message",
                            "messageText": "중소기업취업연계장학금(희망사다리)",
                            "action": "block",
                            "blockId":"6468a9432ecb0e7d2bec3fd9",
                            "extra": {
                                "발화": "중소기업취업연계장학금(희망사다리)"
                            }
                            },
                            {
                            "title": "기부장학금",
                            "action": "message",
                            "messageText": "기부장학금",
                            "action": "block",
                            "blockId":"6468a9432ecb0e7d2bec3fd9",
                            "extra": {
                                "발화": "기부장학금"
                            }
                            },                       
                        ]
                    }
                }]
            }
            }
            return jsonify(res)
        if action.get('clientExtra') == {'발화': '교장'} or action.get('params') == {'서비스장학2':'교내장학금'}:
            res={
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "원하는 버튼을 클릭하세요."
                        },
                        "items": [
                            {
                            "title": "장학제도 안내",
                            "action": "message",
                            "messageText": "장학제도 안내",
                            "action": "block",
                            "blockId":"64d4c1cbc800862a5416f704",
                            "extra": {
                                "발화": "장학제도 안내"
                            }
                            },
                            {
                            "title": "감면 장학금",
                            "action": "message",
                            "messageText": "감면 장학금",
                            "action": "block",
                            "blockId":"64d4c319c800862a5416f70c",
                            "extra": {
                                "발화": "감면 장학금"
                            }
                            },
                            {
                            "title": "현금 장학금",
                            "action": "message",
                            "messageText": "현금 장학금",
                            "action": "block",
                            "blockId":"64d4c31e7ad92a7e8643ffc0",
                            "extra": {
                                "발화": "현금 장학금"
                            }
                            },
                            {
                            "title": "기타 장학금",
                            "action": "message",
                            "messageText": "기타 장학금",
                            "action": "block",
                            "blockId":"64d4c323399c092c9229d66e",
                            "extra": {
                                "발화": "기타 장학금"
                            }
                            },                       
                        ]
                    }
                }]
            }
            }
            return jsonify(res)                                 
    if user_result.get('block')['name'] == '장학-3':
        if action.get('clientExtra') == {'발화': '소득연계형 국가장학금'}:
            res={
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "원하는 버튼을 클릭하세요."
                        },
                        "items": [
                            {
                            "title": "국가장학금 I유형 (학생직접지원형)",
                            "action": "message",
                            "messageText": "국가장학금 I유형",
                            "action": "block",
                            "blockId":"6468a94c2ecb0e7d2bec3fdb",
                            "extra": {
                                "발화": "국가장학금 I유형"
                            }
                            },
                            {
                            "title": "국가장학금 II유형 (학생직접지원형)",
                            "action": "message",
                            "messageText": "국가장학금 II유형",
                            "action": "block",
                            "blockId":"6468a94c2ecb0e7d2bec3fdb",
                            "extra": {
                                "발화": "국가장학금 II유형"
                            }
                            },
                            {
                            "title": "다자녀 국가장학금",
                            "action": "message",
                            "messageText": "다자녀 국가장학금",
                            "action": "block",
                            "blockId":"6468a94c2ecb0e7d2bec3fdb",
                            "extra": {
                                "발화": "다자녀 국가장학금"
                            }
                            },
                            {
                            "title": "지역인재장학금",
                            "action": "message",
                            "messageText": "지역인재장학금",
                            "action": "block",
                            "blockId":"6468a94c2ecb0e7d2bec3fdb",
                            "extra": {
                                "발화": "지역인재장학금"
                            }
                            },
                            {
                            "title": "입학금 지원 장학금",
                            "action": "message",
                            "messageText": "입학금 지원 장학금",
                            "action": "block",
                            "blockId":"6468a94c2ecb0e7d2bec3fdb",
                            "extra": {
                                "발화": "입학금 지원 장학금"
                            }
                            },                       
                        ]
                    }
                }]
            }
            }
            return jsonify(res)

        if action.get('clientExtra') == {'발화': '국가근로장학금'}:
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가근로장학금\n안정적인 학업여건 조성과 취업역량 제고를 위한 장학금\n\n<방학 집중근로 프로그램>\n\n운영목적: 국가근로장학생에게 방학기간 중 양질의 근로지를 발굴·제공하여 다양한 근로체험 및 계속적 자기역량 계발의 기회 제공\n\n운영기간: 하계방학: 7월 ~ 8월, 동계방학: 1월 ~ 2월\n\n희망근로장학기관 신청기간: 하계방학: 5월 중, 동계방학: 11월 중\n\n※ 희망근로장학기관 신청기간은 매 학기 상이하므로, 자세한 사항은 공지사항에서 확인하여 주시기 바랍니다.\n\n국가근로장학금에 대해서 알고 싶으신 항목을 선택해주세요."
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "지원대상",
                            "action": "block",
                            "label": "지원대상",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원대상",
                                "key1":"국가근로"
                            }
                        },
                        {
                            "messageText": "선발기준",
                            "action": "block",
                            "label": "선발기준",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"성적기준",
                                "key1":"국가근로"
                            }
                        },
                        {
                            "messageText": "지원절차",
                            "action": "block",
                            "label": "지원절차",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원절차",
                                "key1":"국가근로"
                            }
                        },
                        {
                            "messageText": "제출서류",
                            "action": "block",
                            "label": "제출서류",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"제출서류",
                                "key1":"국가근로"
                            }
                        },
                        {
                            "messageText": "지원금액",
                            "action": "block",
                            "label": "지원금액",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원금액",
                                "key1":"국가근로"
                            }
                        },
                        {
                            "messageText": "부정근로안내",
                            "action": "block",
                            "label": "부정근로안내",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"부정근로안내",
                                "key1":"국가근로"
                            }
                        },
                        {
                            "messageText": "안전사고 발생시",
                            "action": "block",
                            "label": "안전사고 발생시",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"안전사고 발생시",
                                "key1":"국가근로"
                            }
                        },
                        {
                            "messageText": "FAQ 바로가기",
                            "action": "block",
                            "label": "FAQ 바로가기",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"FAQ 바로가기",
                                "key1":"국가근로"
                            }
                        }
                    ]

                }
            }
            return jsonify(res)

        if action.get('clientExtra') == {'발화': '국가우수장학금'}:
            res={
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "carousel":{
                        "type": "listCard",
                        "items": [
                            {
                            "header": {
                                "title": "원하는 버튼을 클릭하세요."
                            },
                            "items": [
                                {
                                "title": "대통령과학장학금",
                                "action": "message",
                                "messageText": "대통령과학장학금",
                                "action": "block",
                                "blockId":"6468a94c2ecb0e7d2bec3fdb",
                                "extra": {
                                    "발화": "대통령과학장학금"
                                }
                                },
                                {
                                "title": "국가우수장학금(이공계)",
                                "action": "message",
                                "messageText": "국가우수장학금(이공계)",
                                "action": "block",
                                "blockId":"6468a94c2ecb0e7d2bec3fdb",
                                "extra": {
                                    "발화": "국가우수장학금(이공계)"
                                }
                                },
                                {
                                "title": "인문100년장학금",
                                "action": "message",
                                "messageText": "인문100년장학금",
                                "action": "block",
                                "blockId":"6468a94c2ecb0e7d2bec3fdb",
                                "extra": {
                                    "발화": "인문100년장학금"
                                }
                                },
                                {
                                "title": "예술체육비전장학금",
                                "action": "message",
                                "messageText": "예술체육비전장학금",
                                "action": "block",
                                "blockId":"6468a94c2ecb0e7d2bec3fdb",
                                "extra": {
                                    "발화": "예술체육비전장학금"
                                }
                                },
                                {
                                "title": "우수고등학생해외유학장학금(드림장학금)",
                                "action": "message",
                                "messageText": "드림장학금",
                                "action": "block",
                                "blockId":"6468a94c2ecb0e7d2bec3fdb",
                                "extra": {
                                    "발화": "드림장학금"
                                }
                                },                      
                            ]
                            },
                            {
                            "header": {
                                "title": "원하는 버튼을 클릭하세요."
                            },
                            "items":[
                                {
                                "title": "대학원생지원장학금",
                                "action": "message",
                                "messageText": "대학원생지원장학금",
                                "action": "block",
                                "blockId":"6468a94c2ecb0e7d2bec3fdb",
                                "extra": {
                                    "발화": "대학원생지원장학금"
                                }
                                }
                            ]
                            }
                        ]
                }}]
            }
            }
            return jsonify(res)

        if action.get('clientExtra') == {'발화': '중소기업취업연계장학금(희망사다리)'}:
            res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "교내장학제도 수혜기준은 '서울과학기술대학교 장학금 관리 지침'을 참고하시기 바랍니다."
                        }
                    }
                ]
            }
            }

            return jsonify(res)

        if action.get('clientExtra') == {'발화': '기부장학금'}:
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                            "header": {
                                "title": "원하는 버튼을 클릭하세요."
                            },
                            "items": [
                                {
                                "title": "기부장학금",
                                "description": "푸른등대 기부장학금  \n푸른등대 기부자의 의도를 반영하여 다양한 분야의 저소득층 우수 학생을 지원하는 장학금 (기부금 조성 상황에 따라 매년 사업규모가 변동됨)  \n기부처별 신청자격을 고려하여 1개만 신청  \n(동일 학기에 1개 기부처 장학금만 수혜 가능)  \n신규장학생 선발 시 동일학기 푸른등대 기부장학금, 푸른등대 삼성SOS장학금 간 중복수혜 불가(계속장학생 포함)  \n전공대, 대학원대, 방송통신대, 원격대, 사이버대, 기능대, 평생교육원은 제외  \n푸른등대 기부장학금 계속 지원의 경우 별도 신청절차 없이 성적요건이 충족될 시 계속 지원  \n장학생 선발기준 등 세부사항에 대해서는 반드시 공지사항 및 사업계획 확인  \n※ 소득구간, 학사정보, 학적상태 등에 대한 심사는 1차 심사 시작일 기준 확인된 정보로 심사진행"
                                }                               
                            ],
                            "buttons": [
                                {
                                "label": "[기부처별 푸른등대 장학금 정보 확인 바로가기]",
                                "action": "webLink",
                                "webLinkUrl" : "https://www.kosaf.go.kr/ko/scholar.do?pg=scholarship05_11_01"
                                },
                                {
                                "label": "[다른 국가 장학금 정보]",
                                "action": "block",
                                "blockId" : "64689a6f03afae55d1059e4c",
                                "extra":{"발화": "국장"}
                                }
                            ] 
                            }
                        }
                    ]
                }
            }

                            
            return jsonify(res)
    if user_result.get('block')['name'] == '장학-4':
        if action.get('clientExtra') == {'발화': '국가장학금 I유형'}:

            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅰ유형(학생직접지원형)\n\n 소득수준에 연계하여 경제적으로 어려운 학생들에게 보다 많은 혜택이 주어지도록 설계된 장학금"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "지원대상",
                            "action": "block",
                            "label": "지원대상",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원대상",
                                "key1":"1유형"
                            }
                        },
                        {
                            "messageText": "성적기준",
                            "action": "block",
                            "label": "성적기준",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"성적기준",
                                "key1":"1유형"
                            }
                        },
                        {
                            "messageText": "지원금액",
                            "action": "block",
                            "label": "지원금액",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원금액",
                                "key1":"1유형"
                            }
                        },
                        {
                            "messageText": "지원절차",
                            "action": "block",
                            "label": "지원절차",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원절차",
                                "key1":"1유형"
                            }
                        },
                        {
                            "messageText": "제출서류",
                            "action": "block",
                            "label": "제출서류",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"제출서류",
                                "key1":"1유형"
                            }
                        },
                        {
                            "messageText": "유의사항",
                            "action": "block",
                            "label": "유의사항",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"유의사항",
                                "key1":"1유형"
                            }
                        },
                        {
                            "messageText": "심사기준",
                            "action": "block",
                            "label": "심사기준",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"심사기준",
                                "key1":"1유형"
                            }
                        }
                    ]

                }
            }
            return jsonify(res)
        if action.get('clientExtra') == {'발화': '국가장학금 II유형'}:

            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅱ유형(대학연계지원형)\n\n 대학의 적극적인 등록금 부담완화 참여를 도모하기 위해 대학 자체노력과 연계하여 지원하는 장학금"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "지원대상",
                            "action": "block",
                            "label": "지원대상",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원대상",
                                "key1":"2유형"
                            }
                        },
                        {
                            "messageText": "지원금액",
                            "action": "block",
                            "label": "지원금액",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원금액",
                                "key1":"2유형"
                            }
                        },
                        {
                            "messageText": "지원절차",
                            "action": "block",
                            "label": "지원절차",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원절차",
                                "key1":"2유형"
                            }
                        },
                        {
                            "messageText": "제출서류",
                            "action": "block",
                            "label": "제출서류",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"제출서류",
                                "key1":"2유형"
                            }
                        },
                        {
                            "messageText": "유의사항",
                            "action": "block",
                            "label": "유의사항",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"유의사항",
                                "key1":"2유형"
                            }
                        }
                    ]

                }
            }
            return jsonify(res)
        if action.get('clientExtra') == {'발화': '다자녀 국가장학금'}:
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "다자녀 국가장학금\n\n 다자녀 가구의 등록금 부담 경감을 위해 지원되는 장학금"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "지원대상",
                            "action": "block",
                            "label": "지원대상",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원대상",
                                "key1":"다자녀"
                            }
                        },
                        {
                            "messageText": "성적기준",
                            "action": "block",
                            "label": "성적기준",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"성적기준",
                                "key1":"다자녀"
                            }
                        },
                        {
                            "messageText": "지원금액",
                            "action": "block",
                            "label": "지원금액",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원금액",
                                "key1":"다자녀"
                            }
                        },
                        {
                            "messageText": "지원절차",
                            "action": "block",
                            "label": "지원절차",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원절차",
                                "key1":"다자녀"
                            }
                        },
                        {
                            "messageText": "제출서류",
                            "action": "block",
                            "label": "제출서류",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"제출서류",
                                "key1":"다자녀"
                            }
                        },
                        {
                            "messageText": "유의사항",
                            "action": "block",
                            "label": "유의사항",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"유의사항",
                                "key1":"다자녀"
                            }
                        }
                    ]

                }
            }
            return jsonify(res)
        if action.get('clientExtra') == {'발화': '지역인재장학금'}:
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "지역인재장학금\n\n 지역대학의 우수 인재 유치 및 미래인재 양성을 위해 지원되는 장학금"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "지원대상",
                            "action": "block",
                            "label": "지원대상",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원대상",
                                "key1":"지역인재"
                            }
                        },
                        {
                            "messageText": "성적기준",
                            "action": "block",
                            "label": "성적기준",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"성적기준",
                                "key1":"지역인재"
                            }
                        },
                        {
                            "messageText": "지원금액",
                            "action": "block",
                            "label": "지원금액",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원금액",
                                "key1":"지역인재"
                            }
                        },
                        {
                            "messageText": "지원절차",
                            "action": "block",
                            "label": "지원절차",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원절차",
                                "key1":"지역인재"
                            }
                        },
                        {
                            "messageText": "제출서류",
                            "action": "block",
                            "label": "제출서류",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"제출서류",
                                "key1":"지역인재"
                            }
                        },
                        {
                            "messageText": "유의사항",
                            "action": "block",
                            "label": "유의사항",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"유의사항",
                                "key1":"지역인재"
                            }
                        }
                    ]

                }
            }
            return jsonify(res)
        if action.get('clientExtra') == {'발화': '입학금 지원 장학금'}:
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "입학금 지원 장학금(입학금 감축 대응지원)\n 입학금 감축계획을 이행한 대학의 당해 연도 신,편입, 재입학생에게 입학금의 일부를 지원\n\n<신청방법>\n입학금 감축계획을 이행한 대학의 당해 연도 신입, 편입, 재입학생\n※ 선발 시 성적 및 소득기준 미적용\n※ 국공립대는 2018년 입학금 전액 폐지에 따라 미지원\n\n<지원금액>\n입학금 폐지 합의에 따라 2017년 입학금의 20%(전문대는 33%) 수준으로 지원\n등록금 내 필수경비(수업료+입학금) 한도 내에서 지원\n단, 입학금 감축 규모 초과이행 등의 사유로 입학금 감축 대응지원액이 입학금을 초과한 경우, 수업료 항목 지원 인정"
                            }
                        }
                    ]
                }
            }

            return jsonify(res)
        if action.get('clientExtra') == {'발화': '대통령과학장학금'}:

            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금\n창의적이고 잠재력이 풍부한 과학기술분야의 최우수학생을 발굴·육성 지원함으로써 세계적 수준의 핵심 과학자군 양성을 위한 장학금\n\n대통령과학장학금에 대해서 알고 싶으신 항목을 선택해주세요."
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "지원자격",
                            "action": "block",
                            "label": "지원자격",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원대상",
                                "key1":"대통령"
                            }
                        },
                        {
                            "messageText": "지원금액",
                            "action": "block",
                            "label": "지원금액",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원금액",
                                "key1":"대통령"
                            }
                        },
                        {
                            "messageText": "지원절차",
                            "action": "block",
                            "label": "지원절차",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원절차",
                                "key1":"대통령"
                            }
                        },
                        {
                            "messageText": "제출서류",
                            "action": "block",
                            "label": "제출서류",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"제출서류",
                                "key1":"대통령"
                            }
                        }
                    ]

                }
            }
            return jsonify(res)
        if action.get('clientExtra') == {'발화': '국가우수장학금(이공계)'}:
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가우수장학금(이공계)\n우수 인재를 이공계로 적극 유도하여 국가 핵심 인재군으로 육성하고 과학기술분야 국가 경쟁력 우위를 확보하기 위하여 지원하는 사업\n\n국가우수장학금에 대해서 알고 싶으신 항목을 선택해주세요."
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "지원자격",
                            "action": "block",
                            "label": "지원자격",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원대상",
                                "key1":"이공계"
                            }
                        },
                        {
                            "messageText": "지원금액",
                            "action": "block",
                            "label": "지원금액",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원금액",
                                "key1":"이공계"
                            }
                        },
                        {
                            "messageText": "지원절차",
                            "action": "block",
                            "label": "지원절차",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"지원절차",
                                "key1":"이공계"
                            }
                        },
                        {
                            "messageText": "제출서류",
                            "action": "block",
                            "label": "제출서류",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"제출서류",
                                "key1":"이공계"
                            }
                        },
                        {
                            "messageText": "이공계환수제도",
                            "action": "block",
                            "label": "이공계환수제도",
                            "blockId": "6468a9532ecb0e7d2bec3fdd",
                            "extra":{
                                "발화":"이공계환수제도",
                                "key1":"이공계"
                            }
                        }
                    ]

                }
            }
            return jsonify(res)
    if user_result.get('block')['name'] == '장학-5':
        if action.get('clientExtra',{}).get('발화') == '지원대상':
            if action.get('clientExtra',{}).get('key1') == '1유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅰ유형(학생직접지원형)\n지원대상\n국가장학금Ⅰ유형(학생직접지원형)의 지원자격은 대한민국 국적으로 국내 대학에 재학 중인 소득 8구간(분위) 이하 대학생 중 성적기준 충족자로 해당학기 국가장학금 신청절차(가구원 동의, 서류제출)를 완료하여 소득수준이 파악된 학생입니다. \n\n국가장학금Ⅰ유형(학생직접지원형)\n대상대학\n국내대학(외국대학 제외)\n다만, 2020년 재정지원제한 유형 Ⅱ등급 대학 신입 및 편입생 지원 제외(최초 지정 후 등급 변화가 없으면 계속하여 지원 제한)\n\n※ 국가장학금 대상대학의 목록은 [한국장학재단 > 장학금 > 국가장학금Ⅰ유형(학생직접지원형) > 지원대상]에서 '2020년 국가장학금 Ⅰ유형(학생직접지원형) 지원가능대학 확인'을 통해 조회하실 수 있습니다."
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '2유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅱ유형(대학연계지원형) 지원대상\n대한민국 국적으로 국가장학금 Ⅱ유형(대학연계지원형) 참여대학에 재학 중인 대학생 중 해당 학기 국가장학금 신청절차(가구원동의, 서류제출)를 완료하여 소득수준이 파악된 학생입니다. \n\n<우대지원 권고사항>\n\n  - 장애인, 대학생 자녀가 2명 이상인 가구 또는 자녀가 3명 이상인 가구의 학생\n  - 긴급 경제사정 곤란자\n  - 선취업-후진학 학생\n\n국가장학금Ⅱ유형(대학연계지원형) 지원대상\n- 당해 년도 국가장학금 Ⅱ유형(대학연계지원형) 지원가능대학 중 Ⅱ유형(대학연계지원형) 참여 대학\n- 학자금지원제도 심의위원회 심의 결과(’18.9.)에 따른 제한 대상은 지원 제한"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '다자녀':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "다자녀 국가장학금 지원대상\n<지원자격>\n\n  - 대한민국 국적을 소지한 국내대학의 소득 8구간 이하, 다자녀 가정의 가구원인 대학생(미혼에 한함, 연령 무관)\n\n    * 다자녀 가구(자녀3명 이상)의 모든 자녀에게 지원\n    * 단, 사망 자녀는 자녀 수 합산에 불가하나, 신청일 기준 만 1년 이내 사망한 경우에는 추가 증빙서류(사망일자가 확인되는 사망신고서 등) 확인 후 자녀 수로 합산가능\n  - 해당학기 국가장학금 신청절차(가구원동의, 서류제출)를 완료하여 소득수준이 파악된 학생\n\n<소득기준>\n  - 소득 8구간(분위) 이하\n    * 사회보장정보시스템을 통해 확인한 가구원 소득, 재산, 금융자산, 부채 등을 반영하여 소득인정액을 산정하여 결정"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '지역인재':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "지역인재장학금 지원대상\n\n<지원자격>\n비수도권 고교를 졸업하고, ’19학년도 비수도권 대학에 입학한 소득 8구간(분위) 이하 신입생 중 국가장학금 신청절차(가구원동의, 서류제출)를 완료하여 소득수준이 파악된 학생\n\n※ 단, ’19학년도 지역인재장학금 참여대학 소속 학생에 한함\n\n<대상대학>\n고등교육법 제2조 1호 내지 제4호에 해당하는 학교 중 비수도권 소재대학\n※ 한국과학기술원, 광주과학기술원, 대구경북과학기술원, 울산과학기술원, 한국전통문화대학교, 한국농수산대학도 대상 포함"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가근로장학금 지원자격\n- 국내 대학의 재학생(입학예정자 포함)\n- 소득 8구간(분위) 이하\n- 직전학기 70점(100점 만점) 이상인 학생\n\n(우선선발) 장애인, 다자녀가구(3자녀이상), 다문화·탈북 가구, 국가유공자, 국가보훈자, 부모 중 한 분이 장애인·중증환자, 학업·육아 병행학생, 파란사다리 및 글로벌 현장실습 장학생\n\n(소득구간(분위) 적용 배제) 긴급한 가계곤란 학생 및 취업연계유형(취업연계 중점대학, 권역별 취업연계 활성화), 봉사유형(장애대학생·외국인유학생), 농·산·어촌 근로 시에는 소득구간(분위)적용 배제 가능\n\n※ 직전학기 미선발자가 당해 학기에 60%이상 선발되도록 권장함(단, 장애대학생 봉사유형, 취업연계유형, 대학생 청소년교육지원사업은 예외로 함)"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '대통령':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금 지원자격\n대한민국 국적을 소지한 자\n\n - 주민등록상 해외이주 신고자, 영주권자 제외\n\n당해연도 국내 고등학교 졸업(예정)자 또는 ｢초･중등교육법｣ 상 고교 졸업자와 동등한 학력을 인정받은 자\n(이하 ‘동등학력자’)로서 국내 및 해외 4년제 대학의 자연과학 및 공학계열 학과(부)에 입학예정(확정)인 자"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "고등학교 졸업자(학업성적 보유자) 신청자격",
                            "action": "block",
                            "label": "고등학교 졸업자(학업성적 보유자) 신청자격",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"고등학교 졸업자"
                            }
                        },
                        {
                            "messageText": "동등학력자(학업성적 미보유자) 신청자격",
                            "action": "block",
                            "label": "동등학력자(학업성적 미보유자) 신청자격",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"동등학력자"
                            }
                        },
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '성적기준':
            if action.get('clientExtra',{}).get('key1') == '1유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅰ유형(학생직접지원형) 성적기준\n<신입생>\n\n  - 성적 및 이수학점 기준 미 적용(첫 학기)\n\n<재학생>\n\n  - 직전학기 12학점, 백분위 80점(2.75/4.5) 이상\n\n  - 기초~차상위 C학점(백분위 70점(1.88/4.5)) 이상\n\n  - 1~3분위는 백분위 70점~80점 미만인 경우 2회까지 수혜\n\n ※ 한국장학재단 학사원장의 졸업학기가 “Y”인 경우 직전학기 이수학점 심사 X\n\n ※ 직전학기를 P/N과목만 이수한 경우 전전학기 성적으로 심사"}

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '다자녀':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "다자녀 국가장학금 성적기준\n<신입생>\n\n  - 성적 및 이수학점 기준 미 적용(첫 학기)\n\n<재학생>\n\n  - 직전학기 12학점, 백분위 80점(2.75/4.5) 이상\n\n  - 기초~차상위 C학점(백분위 70점(1.88/4.5)) 이상\n\n  - 1~3분위는 백분위 70점~80점 미만인 경우 2회까지 수혜\n\n ※ 한국장학재단 학사원장의 졸업학기가 “Y”인 경우 직전학기 이수학점 심사 X\n\n ※ 직전학기를 P/N과목만 이수한 경우 전전학기 성적으로 심사"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '지역인재':
                image_Url = "https://ifh.cc/g/CdGk6m.png"
                #만료 : 2024-04-16

                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleImage": {
                                "imageUrl": image_Url, 
                                "altText": "이미지 저장기간 만료."
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가근로장학금 선발기준\n(기본사항) 학적 및 성적, 소득요건을 만족한 자에 대해서는 우선선발 기준을 고려하여 대학자체기준을 수립하고, 대학생을 심사하여, 대학별 배정예산 내에서 선발\n\n우선선발기준\n  - 1순위: 소득 4구간(분위) 이하\n  - 2순위: 소득 5구간(분위) 이상 ~ 6구간(분위) 이하\n  - 3순위: 소득 7구간(분위) 이상 ~ 8구간(분위) 이하\n\n(권장사항) 장애인, 다자녀가구(3자녀이상), 다문화·탈북 가구, 국가유공자, 국가보훈자, 부모 중 한 분이 장애인·중증환자, 학업·육아 병행학생, 파란사다리 및 글로벌 현장실습 장학생\n\n(예외사항) 긴급한 가계곤란 학생 및 취업연계유형(취업연계 중점대학, 권역별 취업연계 활성화), 봉사유형(장애대학생·외국인유학생), 농·산·어촌 근로 시에는 소득구간(분위)적용 배제 가능\n\n(대체선발) 선발 인원의 학적변동 또는 중도 포기 등의 사유로 부득이하게 활동이 중단되는 경우, 대학은 가용예산의 범위 내에서 대체 인원 선발\n\n(중복참여 금지) 국가근로장학 세부사업*간 중복 참여 불가\n* 국가근로장학사업, 다문화·탈북학생멘토링, 대학생 청소년교육지원 사업.\n※ 기존 참여 사업 근로 종료 처리 후, 타 사업 참여 가능"
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '지원금액':
            if action.get('clientExtra',{}).get('key1') == '1유형':
                image_Url = "https://ifh.cc/g/SOwBn2.jpg"
                #만료 : 2024-04-16

                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleImage": {
                                "imageUrl": image_Url, 
                                "altText": "이미지 저장기간 만료."
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '2유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅱ유형(대학연계지원형) 지원금액\n대학 자체기준에 따라 등록금 필수경비(입학금, 수업료) 범위 내에서 지원금액 결정\n\n※ 과소지급 방지를 위해 최소 10만원 이상 지급을 원칙으로 함"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '다자녀':
                image_Url = "https://ifh.cc/g/swrOMr.png"
                #만료 : 2024-04-16

                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleImage": {
                                "imageUrl": image_Url, 
                                "altText": "이미지 저장기간 만료."
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '지역인재':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "지역인재장학금 지원금액\n<지원금액>\n\n지원기간 내 등록금 필수경비(입학금, 수업료) 전액지원\n\n<지원기간>\n\n1. 신규선발\n\n  - (기초~기준중위소득 100%*) 전 학기 지원**\n  - (기준중위소득 100% 초과~소득 8구간) 1년 지원(2학기)\n  * ’19년 소득구간 확정에 따라 중위소득 100%에 해당하는 소득구간 적용(Ⅰ유형과 동일)\n  ** 학제 및 전공별 정규학기를 기준으로 수혜횟수 확정(예시: 4년제 → 8회)\n  ※ 편입 등으로 학교가 변경되어도 장학금 수혜횟수는 누적관리(동일대학 재입학 포함)\n\n2. 일시선발 : 선발학기 1회 지원\n\n3. 이전 계속 지원(최초 선발학기를 포함)\n\n  - '16년까지 선발자 : 최대 2년(4학기) 지원\n  - '17년 선발자 : 최대 1년(2학기) 지원\n  - '18년 선발자 : 소득구간(분위)에 따라 최대 전 학기 지원 또는 1년(2학기) 지원"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가근로장학금 지원금액\n<지원범위>\n(시급단가) 교내근로: 9,000원, 교외근로 11,150원\n(최대근로시간) 1일 8시간, 주당 학기중 20시간(방학중 40시간), 학기당 520시간\n※ 시급단가는 최저임금 기준이며, 매년초에 새로 책정됨.\n야간대, 원격대학 학생, 취업연계형 학생에 한해 학기중 주당 40시간까지 활동가능\n단, 장애인, 다자녀가구(3자녀이상), 다문화 및 북한이탈주민 가구, 국가유공자, 국가보훈자, 부모 중 한분이 장애인·중증환자, 학업·육아 병행 학생, 장애대학생 봉사유형, 취업연계유형은 학기당 520시간 이상 근로 가능"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '대통령':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금 지원금액\n신규장학생 147명 내외, 계속장학생 375명 내외 지원\n\n궁금하신 항목을 선택하여 주세요."
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "국내장학생 지원금액",
                            "action": "block",
                            "label": "국내장학생 지원금액",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"국내장학생 지원금액"
                            }
                        },
                        {
                            "messageText": "해외장학생 지원금액",
                            "action": "block",
                            "label": "해외장학생 지원금액",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"해외장학생 지원금액"
                            }
                        },
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '지원절차':
            if action.get('clientExtra',{}).get('key1') == '1유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅰ유형(학생직접지원형) 지원절차\n온라인 신청 및 서류 제출 -> 소득정보 확인 -> 심사 -> 선발 -> 장학금 지급\n※ 상세 절차 내용은 한국장학재단 홈페이지 참조"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '2유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅱ유형(대학연계지원형) 지원절차\n온라인 신청 및 서류 제출 -> 소득정보 확인 -> 심사 -> 선발 -> 장학금 지급\n\n* 상세 절차 내용은 한국장학재단 홈페이지 참조"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '다자녀':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "다자녀 국가장학금 지원절차\n온라인 신청 및 서류 제출 -> 소득정보 확인 -> 심사 -> 선발 -> 장학금 지급\n\n* 상세 절차 내용은 한국장학재단 홈페이지 참조"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '지역인재':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "지역인재장학금 지원절차\n온라인 신청 및 서류 제출 -> 소득정보 확인 -> 심사 -> 선발 -> 장학금 지급\n\n* 상세 절차 내용은 한국장학재단 홈페이지 참조"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                image_Url = "https://ifh.cc/g/0oPPal.png"
                #만료 : 2024-04-16

                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleImage": {
                                "imageUrl": image_Url, 
                                "altText": "이미지 저장기간 만료."
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '대통령':    
                image_Url = "https://ifh.cc/g/AqCXbP.png"
                #만료 : 2024-04-21

                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleImage": {
                                "imageUrl": image_Url, 
                                "altText": "이미지 저장기간 만료."
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        }
                    ]
                }
            }
            return jsonify(res)       
        if action.get('clientExtra',{}).get('발화') == '제출서류':
            if action.get('clientExtra',{}).get('key1') == '1유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "○ 서류제출대상자 확인\n○ 홈페이지 서류제출 : [장학금]-[장학금신청]-[서류제출현황]-우측 하단 “서류제출” 클릭 후 해당 서류 파일 업로드\n○ 형제/자매(자녀) 정보 증빙 서류(제출대상자 서류 제출)\n\n- 미혼의 경우 신청자 본인 포함 형제·자매가 3명 이상(부 또는 모 명의 가족관계증명서 제출)\n\n- 기혼의 경우 본인의 자녀가 3명 이상(본인 명의 가족관계증명서 제출)"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '2유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "○ 서류제출대상자 확인\n○ 홈페이지 서류제출 : [장학금]-[장학금신청]-[서류제출현황]-우측 하단 “서류제출” 클릭 후 해당 서류 파일 업로드\n○ 형제/자매(자녀) 정보 증빙 서류(제출대상자 서류 제출)\n\n- 미혼의 경우 신청자 본인 포함 형제·자매가 3명 이상(부 또는 모 명의 가족관계증명서 제출)\n\n- 기혼의 경우 본인의 자녀가 3명 이상(본인 명의 가족관계증명서 제출)"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '다자녀':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                               "text": "다자녀국가장학금 제출서류\n서류제출 생략이 가능한지 여부를 먼저 확인하세요!\n\n신청 후 1일~3일(휴일 제외) 뒤에 [장학금] > [장학금신청] > [서류제출현황]에서 제출대상여부 확인 가능"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '지역인재':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                               "text": "지역인재장학금 제출서류\n서류제출 생략이 가능한지 여부를 먼저 확인하세요!\n\n신청 후 1일~3일(휴일 제외) 뒤에 [장학금] > [장학금신청] > [서류제출현황]에서 제출대상여부 확인 가능"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                               "text": "국가근로장학금 제출서류\n서류제출 생략이 가능한지 여부를 먼저 확인하세요!\n\n신청 후 1일~3일(휴일 제외) 뒤에 [장학금] > [장학금신청] > [서류제출현황]에서 제출대상여부 확인 가능"
                            }

                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '대통령':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금 제출서류\n\n<공통 제출서류>\n1. 과학활동실적서\n2. 학업계획서\n3. 전인적 인재 성장 계획서\n4. 기타 증빙서류\n\n	<고교졸업자>\n1. 학교장 또는 교육감 추천서\n2. 학교생활기록부\n\n<동등학력 인정자>\n1. 검정고시 출신자\n2. 해외고등학교 졸업(예정)자\n3. 기타(북한이탈주민 등)"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        },
                        {
                            "messageText": "제출서류 작성요령",
                            "action": "block",
                            "label": "제출서류 작성요령",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"제출서류 작성요령",
                            }
                        }
                    ]
                }
            }

            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '유의사항':
            if action.get('clientExtra',{}).get('key1') == '1유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금Ⅰ유형(학생직접지원형) 유의사항\n<자퇴, 휴학 시 국가장학금 반환>\n  - 자퇴, 제적 등으로 학적이 소멸하거나 휴학 등으로 등록금을 환불받는 경우\n\n<중복지원 발생 시 학자금 반환>\n  - 해당학기 등록금을 초과하여 학자금을 지원받은 학생\n  ※ 단, 과거학기 중복지원으로 해당학기 국가장학금이 거절된 경우 해당학기 심사기간 내 등록금 초과 수혜금액을 반환하여 중복지원을 해소하면 국가장학금 재심사 가능\n\n<기타 유의사항>\n  - 사회적 물의를 야기하는 등 국가장학금 수혜자로서 적절하지 않다고 판단되는 경우 국가장학금 지원제한 가능\n  - 과거학기 국가장학금을 전액 반환하여도 수혜횟수 누적(학적변동, 중복지원 발생 시 제외)"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '2유형':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "국가장학금ⅠI유형(대학연계지원형) 유의사항\n<자퇴, 휴학 시 국가장학금 반환>\n  - 자퇴, 제적 등으로 학적이 소멸하거나 휴학 등으로 등록금을 환불받는 경우\n\n<중복지원 발생 시 학자금 반환>\n  - 해당학기 등록금을 초과하여 학자금을 지원받은 학생\n  ※ 단, 과거학기 중복지원으로 해당학기 국가장학금이 거절된 경우 해당학기 심사기간 내 등록금 초과 수혜금액을 반환하여 중복지원을 해소하면 국가장학금 재심사 가능\n\n<기타 유의사항>\n  - 사회적 물의를 야기하는 등 국가장학금 수혜자로서 적절하지 않다고 판단되는 경우 국가장학금 지원제한 가능\n  - 과거학기 국가장학금을 전액 반환하여도 수혜횟수 누적(학적변동, 중복지원 발생 시 제외)"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '다자녀':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "다자녀국가장학금 유의사항\n\n서류 미제출 등으로 다자녀 여부가 확인되지 않을 경우 국가장학금I 유형 으로 심사 및 지급\n\n<자퇴, 휴학 시 국가장학금 반환>\n  - 자퇴, 제적 등으로 학적이 소멸하거나 휴학 등으로 등록금을 환불받는 경우\n\n<중복지원 발생 시 학자금 반환>\n  - 해당학기 등록금을 초과하여 학자금을 지원받은 학생\n  ※ 단, 과거학기 중복지원으로 해당학기 국가장학금이 거절된 경우 해당학기 심사기간 내 등록금 초과 수혜금액을 반환하여 중복지원을 해소하면 국가장학금 재심사 가능\n\n<기타 유의사항>\n  - 사회적 물의를 야기하는 등 국가장학금 수혜자로서 적절하지 않다고 판단되는 경우 국가장학금 지원제한 가능\n  - 과거학기 국가장학금을 전액 반환하여도 수혜횟수 누적(학적변동, 중복지원 발생 시 제외)"
                            }
                        }
                    ]
                }
            }
            if action.get('clientExtra',{}).get('key1') == '지역인재':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "지역인재장학금 유의사항\n\n대학에서 선발되었더라도 해당학기 국가장학금을 미신청하거나 소득구간(분위) 산정이 완료되지 않을 경우 지역인재장학금 지원 불가. 세부선발기준은 대학에 따라 상이할 수 있음.\n\n계속지원을 위한 성적 유지 노력 필요\n▷ 성적기준 미충족으로 탈락할 경우 계속지원 영구 탈락\n   단, ’19년부터 전 학기 장학생의 경우 1회에 한하여 C학점 경고제 적용(지원대상 참고)\n\n타 장학금 수혜 등으로 계속장학생 자격을 상실하지 않도록 유의\n▷ 타장학금 수혜로 지역인재장학금을 포기한 경우 추후 타장학금 수혜 취소 또는 포기를 하더라도 해당학기 종료 이후 지역인재장학금 소급지원 불가\n\n<자퇴, 휴학 시 국가장학금 반환>\n  - 자퇴, 제적 등으로 학적이 소멸하거나 휴학 등으로 등록금을 환불받는 경우\n\n<중복지원 발생 시 학자금 반환>\n  - 해당학기 등록금을 초과하여 학자금을 지원받은 학생\n  ※ 단, 과거학기 중복지원으로 해당학기 국가장학금이 거절된 경우 해당학기 심사기간 내 등록금 초과 수혜금액을 반환하여 중복지원을 해소하면 국가장학금 재심사 가능\n\n<기타 유의사항>\n  - 사회적 물의를 야기하는 등 국가장학금 수혜자로서 적절하지 않다고 판단되는 경우 국가장학금 지원제한 가능\n  - 과거학기 국가장학금을 전액 반환하여도 수혜횟수 누적(학적변동, 중복지원 발생 시 제외)"
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '심사기준':
            if action.get('clientExtra',{}).get('key1') == '1유형':
                image_Url = "https://ifh.cc/g/WHO8Lp.jpg"
                #만료 : 2024-04-16

                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleImage": {
                                "imageUrl": image_Url, 
                                "altText": "이미지 저장기간 만료."
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '부정근로안내':
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                               "text": "국가근로장학금 부당근로 안내\n<부정근로 유형>\n\n부정근로로 인한 근로장학금 부정수급은 범죄입니다\n\n허위근로: 근로를 하지 않았음에도 불구하고 근로한 것처럼 출근부를 작성 및 입력한 경우\n(예시 1) 1시간 근로 후 2시간 이상 출근부를 작성한 경우\n(예시 2) 일시적인 휴강 시간에 근로한 경우(일시적인 휴강 등으로 인하여 발생한 시간에 이루어진 활동은 해당 시간이 학업시간표과 중복되어 근로활동으로 인정되지 않음)\n\n대리근로: 선발된 근로장학생 본인이 아닌 타인이 근로를 대신한 경우\n(예시) 근로장학생 본인의 부득이한 사정에 의해 친구에게 근로를 대신 요청하여 근로를 진행한 경우\n\n대체근로: 실질적으로 근로한 시간과 출근부상 작성 및 입력한 시간이 상이한 경우\n(예시) 10:00 ~ 11:00(1시간) 근로를 실시하였으나, 13:00 ~ 14:00 근로한 것으로 작성한 경우\n※ 주의사항: 출근부는 반드시 장학생 본인이 근로 후 즉시(최대 5일 이내) 직접 입력해야 하며, 타인이 입력하여 문제가 발생한 경우 그에 따른 책임은 근로장학생 본인에게 있음\n\n<부정근로에 대한 조치사항>\n허위근로: 장학금 환수 및 확정일로부터 해당학기를 포함하여 4개 학기 사업 참여 제한\n대리근로: 장학금 환수 및 확정일로부터 해당학기를 포함하여 2개 학기 사업 참여 제한(대리근로자도 2개 학기 사업 참여 제한)\n대체근로: 확정일로부터 해당학기를 포함하여 2개 학기 사업 참여 제한"
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '안전사고 발생시':
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                               "text": "국가근로장학 안전사고 처리절차\n1. 사고발생 : 근로중 안전사고 발생\n2. 초기대응\n  - 사고의 심각성에 따라 119에 연락\n3. 재단에 연락\n  - 한국장학재단 안전사고 긴급전화(1599-4920)로 연락하여 사고 경위 설명 및 상해보험(해당 시) 처리절차 확인\n4. 사고처리\n  - 재단 및 보험사가 안내한 절차에 따라 보험서류 처리\n5. 후속조치\n  - 상해보험 접수 및 지급 안내, 부상의 정도에 따라 업무조정 요청 또는 근로종료\n\nQ. 안전사고가 발생하면 어떻게 해야 하나요?\nA. 안전사고 발생 시, 한국장학재단 안전사고 긴급전화(1599-4920)를 통해 상해보험 처리절차를 확인하고 진행합니다.\n(본인부담금이 발생할 수 있음)"
                            }
                        }
                    ]
                }
            }
            return jsonify(res)        
        if action.get('clientExtra',{}).get('발화') == 'FAQ 바로가기':
            if action.get('clientExtra',{}).get('key1') == '국가근로':
                res={
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "원하는 버튼을 클릭하세요."
                        },
                        "items": [
                            {
                            "title": "FAQ 바로가기",
                            "action": "message",
                            "messageText": "FAQ 바로가기",
                            }                                                   
                        ],
                        "buttons": [
                                {
                                "label": "[홈페이지]",
                                "action": "webLink",
                                "webLinkUrl" : "https://www.kosaf.go.kr/ko/faq.do?searchType=s&searchStr=&ctgrId1=NODE0000001472&ctgrId2=&nodenm=%EA%B5%AD%EA%B0%80%EA%B7%BC%EB%A1%9C%EC%9E%A5%ED%95%99%EA%B8%88&ttab1=4&ttab2=tabitemlst4"
                                }
                        ]
                    }
                }]
            }
            }
            return jsonify(res)  
    if user_result.get('block')['name'] == '장학-6':
        if action.get('clientExtra',{}).get('발화') == '고등학교 졸업자':
            image_Url = "https://ifh.cc/g/BF89wX.png"
                #만료 : 2024-04-16

            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleImage": {
                                "imageUrl": image_Url, 
                                "altText": "이미지 저장기간 만료."
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "동등학력자(학업성적 미보유자) 신청자격",
                            "action": "block",
                            "label": "동등학력자(학업성적 미보유자) 신청자격",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"동등학력자",
                            }
                        },
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금"
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '동등학력자':
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금 지원자격\n동등학력자(학업성적 미보유자) 신청자격\n\n「초･중등교육법」상 고교 졸업자와 동등한 학력을 인정받은 자로 고교 내신성적이 없어 성적산정이 불가능한 경우에 한하여 지원 가능\n\n① 검정고시 출신자: '18년 고등학교 졸업 학력 검정고시에 합격한 자\n\n② 해외고등학교 졸업(예정)자: '19년 해외고등학교 졸업(예정)자를 기준으로 함.\n 다만, '18년 졸업자 중 '19년 대학 입학(예정)인 자로서 출신 고교 소재 국가의 학제 상 졸업일정과 대학 입학시기의 연속성 등 지원자격을 종합적으로 판단하여, 고교졸업과 대학입학 시기가 연속적인 자만 지원 가능\n\n③ 기타: '18년 학력심의위원회 심의(북한 이탈주민 등)를 거쳐 고등학교 학력 인정을 받은 자 등"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "고등학교 졸업자(학업성적 보유자) 신청자격",
                            "action": "block",
                            "label": "고등학교 졸업자(학업성적 보유자) 신청자격",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"고등학교 졸업자",
                            }
                        },
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '국내장학생 지원금액':
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금 지원금액(국내장학생)\n매학기별 등록금 전액지원\n등록금 : \n계속지원기준 충족 시 매학기별 대학 등록금(입학금, 수업료) 전액 지원\n\n학업장려비 :\n 계속지원기준 충족 시 학기당 250만 원 추가 지원\n\n생활비 :\n계속지원기준을 충족하는 기초생활수급자*는 학기당 250만원 추가 지원\n\n* 생계급여 일반수급자, 생계급여 조건부 수급자, 의료급여 수급자, 보장시설 수급자"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "해외장학생 지원금액",
                            "action": "block",
                            "label": "해외장학생 지원금액",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"해외장학생 지원금액"
                            }
                        },
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        }
                    ]
                }
            }
            return jsonify(res)  
        if action.get('clientExtra',{}).get('발화') == '해외장학생 지원금액':
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금 지원금액\n실비학비, 체제비 등 연간 최대 미화 5만달러\n\n실비학비 인정범위 :\n수업료, 등록비, 보험료 (기타 징수금은 제외)\n\n체제비 :\n연간 최대 2만$까지 정액 지급(국가, 도시에 따른 차등지급)\n※ 연간 학비 우선 지원 후 지원가능 범위 내에서 체재비 지원\n\n출국항공료 :\n신규장학생에 한하여 별도 1회 실비 지원(이코노미, 편도 기준)"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "국내장학생 지원금액",
                            "action": "block",
                            "label": "국내장학생 지원금액",
                            "blockId": "64db5c7195c8f07cdf6b176a",
                            "extra":{
                                "발화":"국내장학생 지원금액"
                            }
                        },
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        if action.get('clientExtra',{}).get('발화') == '제출서류 작성요령':
            res={
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "대통령과학장학금 제출서류 작성요령\n<과학활동실적서 작성 요령>\n1.주요 과학활동 실적 작성 요령\n - 고등학교 재학 기간 동안의 특기할만한 수학·과학 활동 실적 중 신청자가 판단하여 가장 중요한 실적 2건 이내로 기재하여, 실적의 내용 요약·본인의 역할·실적의 중요성 기재\n※ 주요실적으로 본인이 제출하더라도 심사위원 판단에 따라 실적에서 제외할 수 있음\n2.주요 실적 예시\n - 국내 및 국제의 수학 및 과학 분야 경시·경연대회(올림피아드 대회, 토너먼트대회 등)\n - 과학관련 특별활동 참가 등\n - 다만, 주요 과학활동실적은 반드시 증빙자료 제출 시에만 인정\n3.기타 과학 활동 실적 작성 요령\n - 고등학교 재학 기간 동안의 특기할만한 과학활동실적 중 신청자가 판단하여 중요도 순으로 5개 이내로 기재\n\n<학업계획서 작성요령>\n신청자의 성장 과정 및 가치관, 대학에서의 학업계획, 과학자로서의 진로 및 비전에 대해 자유롭게 작성함(총 2장 이내)"
                            }
                        }
                    ],
                    "quickReplies":[
                        {
                            "messageText": "장학금 다른 정보 보기",
                            "action": "block",
                            "label": "장학금 다른 정보 보기",
                            "blockId": "6468a94c2ecb0e7d2bec3fdb",
                            "extra":{
                                "발화":"대통령과학장학금",
                            }
                        }
                    ]
                }
            }
            return jsonify(res)

        # 웹 페이지 가져오기
        url = 'https://domi.seoultech.ac.kr/site/dormitory/popup/info.jsp'
        response = requests.get(url)
        html_lol = response.content
        soup = BeautifulSoup(html_lol, 'html.parser')
        table = soup.select("table")

        res = {
            'version': '2.0',
            'template': {
                'outputs': []
            }
        }
    
        # 빈 리스트 생성
        images_list = []

        
        for i in range (6,10):
            df = pd.read_html(str(table))[i]

            # 테이블 데이터 확인
            print(df)

            # 표 이미지 생성
            table_image = create_table_image(df)

            # 이미지에 표 이름 추가
            if i == 6:
                table_name = "2021년 1분기 (성림학사) 성과평가 결과"
            elif i == 7:
                table_name = "2021년 2분기 (성림학사) 성과평가 결과"
            elif i == 8:
                table_name = "2021년 3분기 (성림학사) 성과평가 결과"
            elif i == 9:
                table_name = "2021년 4분기 (성림학사) 성과평가 결과"
            


            # 폰트 경로 설정
            font_path = r'C:\Users\Taeseop\Desktop\chat_bot\챗봇에사용된이미지\NanumGothic.ttf'
    
            # 텍스트를 이미지 위에 추가
            draw = ImageDraw.Draw(table_image)
            font = ImageFont.truetype(font_path, 25)  # 원하는 폰트와 크기로 설정
            text_width, text_height = draw.textsize(table_name, font=font)
            text_x = (table_image.width - text_width) // 2
            text_y = table_image.height - text_height - 10  # 텍스트를 이미지 하단에 추가하려면 조정
            draw.text((text_x, text_y), table_name, fill="black", font=font)  # 원하는 위치에 텍스트 추가
               

            # 이미지를 파일로 저장
            image_path = rf'C:\Users\Taeseop\Desktop\chat_bot\static\images\table_image_{i}.png'
            table_image.save(image_path, "png")
            
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #
            image_url = f'https://40a6-218-235-238-232.ngrok-free.app/static/images/table_image_{i}.png'  
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #


            # 이미지를 카카오톡 응답에 첨부
            images_list.append({
                'simpleImage': {    
                    'imageUrl': image_url,
                    'altText': f'테이블 시각화 {i}'
                }
            })

        for i in range (11,15):
            df = pd.read_html(str(table))[i]

            # 테이블 데이터 확인
            print(df)

            # 표 이미지 생성
            table_image = create_table_image(df)

            # 이미지에 표 이름 추가
            if i == 11:
                table_name = "2021년 1분기 (수림학사,누리학사) 성과평가 결과"
            elif i == 12:
                table_name = "2021년 2분기 (수림학사,누리학사) 성과평가 결과"
            elif i == 13:
                table_name = "2021년 3분기 (수림학사,누리학사) 성과평가 결과"
            elif i == 14:
                table_name = "2021년 4분기 (수림학사,누리학사) 성과평가 결과"

            # 폰트 경로 설정
            font_path = r'C:\Users\Taeseop\Desktop\chat_bot\챗봇에사용된이미지\NanumGothic.ttf'

            

            # 텍스트를 이미지 위에 추가
            draw = ImageDraw.Draw(table_image)
            font = ImageFont.truetype(font_path, 25)  # 원하는 폰트와 크기로 설정
            text_width, text_height = draw.textsize(table_name, font=font)
            text_x = (table_image.width - text_width) // 2
            text_y = table_image.height - text_height - 10  # 텍스트를 이미지 하단에 추가하려면 조정
            draw.text((text_x, text_y), table_name, fill="black", font=font)  # 원하는 위치에 텍스트 추가
               

            # 이미지를 파일로 저장
            image_path = rf'C:\Users\Taeseop\Desktop\chat_bot\static\images\table_image_{i}.png'
            table_image.save(image_path, "png")
        
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #
            image_url = f'https://40a6-218-235-238-232.ngrok-free.app/static/images/table_image_{i}.png'  
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #

            # 이미지를 카카오톡 응답에 첨부
            images_list.append({
                'simpleImage': {    
                    'imageUrl': image_url,
                    'altText': f'테이블 시각화 {i}'
                }
            })
    
        # 반복문이 모든 표를 처리한 후에 이미지 리스트를 응답에 추가
        res['template']['outputs'] = images_list
    
        return jsonify(res)       
    # 전공_정보 블록
    if user_result.get('block')['name'] == '전공_정보':
        user_params = req['action']['params']
        university_major1 = user_params.get('전공_1')
        
        thumbnail_url = "https://imgur.com/1xhrXaU"
        
        print(req)


        with open('major_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            major_info = data.get('major_info')

        if university_major1 in major_info:
            university_info = major_info[university_major1]
            university_name = university_info['name']
            university_description = university_info['description']
            university_link = university_info.get('os:image', "")
            university_curriculum = university_info.get('curriculum', "")

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": f"{university_name}",
                                "description": f"{university_description}",
                                "thumbnail": {"imageUrl": thumbnail_url + ".jpg"},
                                "buttons": [
                                            {
                                                "action": "webLink",
                                                "label": "홈페이지 링크",
                                                "webLinkUrl": f"{university_link}"
                                            },
                                            {
                                                # 차후 커리큘럼 메세지가 아니라 홈페이지의 각 학과 커리큘럼 링크로 대체할것
                                                "action": "message",
                                                "label": "커리큘럼",
                                                "messageText": f"{university_curriculum}"
                                            }
                                            ]
                                }
                            }
                    ]
               }
           }

            return jsonify(res)

        else:
            # 조건을 만족하지 않는 경우에 대한 처리
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": "하단 리스트에서 원하시는 정보를 찾아주세요!"
                                    },
                                "items": [
                                    {
                                        "title": "전공 정보",
                                        "description": "전공관련 정보입니다",
                                        "action": "block",
                                        "blockId": "6458b76c28eb02106c03f010"
                                    },
                                    {
                                        "title": "과기대 전공 종류(목록)",
                                        "description": "서울과기대의 전공 목록들입니다",
                                        "action": "block",
                                        "blockId": "6458bd2a64533008d7f94b8e"
                                    },
                                    {
                                        "title": "학과 홈페이지",
                                        "description": "해당전공의 학과 홈페이지입니다",
                                        "action": "block",
                                        "blockId": "6458e6e964533008d7f94cbf"
                                    },
                                    {
                                        "title": "전공 커리큘럼",
                                        "description": "전공의 커리큘럼 예시들입니다",
                                        "action": "block",
                                        "blockId": "6458eaf98dc11c3fea80d763"
                                    }  
                                    
                                ]
                            
                            }
                        }
                    ]
                }
            }
        
            return jsonify(res)
    # 전공_커리큘럼 블록
    if user_result.get('block')['name'] == '전공_커리큘럼':
        user_params = req['action']['params']
        university_major1 = user_params.get('전공_이름')
        
        thumbnail_url = "https://imgur.com/1xhrXaU"

        with open('major_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            major_info = data.get('major_info')

        if university_major1 in major_info:
            university_info = major_info[university_major1]
            university_name = university_info['name']
            university_description = university_info['description']
            university_link = university_info.get('os:image', "")
            university_curriculum = university_info.get('curriculum', "")

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": f"{university_name}",
                                "description": f"{university_description}",
                                "thumbnail": {"imageUrl": thumbnail_url + ".jpg"},
                                "buttons": [
                                            {
                                                "action": "webLink",
                                                "label": "홈페이지 링크",
                                                "webLinkUrl": f"{university_link}"
                                            },
                                            {
                                                # 차후 커리큘럼 메세지가 아니라 홈페이지의 각 학과 커리큘럼 링크로 대체할것
                                                "action": "message",
                                                "label": "커리큘럼",
                                                "messageText": f"{university_curriculum}"
                                            }
                                            ]
                                }
                            }
                    ]
               }
           }

            return jsonify(res)

        else:
            # 조건을 만족하지 않는 경우에 대한 처리
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": "하단 리스트에서 원하시는 정보를 찾아주세요!"
                                    },
                                "items": [
                                    {
                                        "title": "전공 정보",
                                        "description": "전공관련 정보입니다",
                                        "action": "block",
                                        "blockId": "6458b76c28eb02106c03f010"
                                    },
                                    {
                                        "title": "과기대 전공 종류(목록)",
                                        "description": "서울과기대의 전공 목록들입니다",
                                        "action": "block",
                                        "blockId": "6458bd2a64533008d7f94b8e"
                                    },
                                    {
                                        "title": "학과 홈페이지",
                                        "description": "해당전공의 학과 홈페이지입니다",
                                        "action": "block",
                                        "blockId": "6458e6e964533008d7f94cbf"
                                    },
                                    {
                                        "title": "전공 커리큘럼",
                                        "description": "전공의 커리큘럼 예시들입니다",
                                        "action": "block",
                                        "blockId": "6458eaf98dc11c3fea80d763"
                                    }  
                                    
                                ]
                            
                            }
                        }
                    ]
                }
            }
        
            return jsonify(res)
    # 전공_홈페이지 블록
    if user_result.get('block')['name'] == '전공_홈페이지':
        user_params = req['action']['params']
        university_major1 = user_params.get('전공_name')
        
        thumbnail_url = "https://imgur.com/1xhrXaU"

        

        with open('major_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            major_info = data.get('major_info')

        if university_major1 in major_info:
            university_info = major_info[university_major1]
            university_name = university_info['name']
            university_description = university_info['description']
            university_link = university_info.get('os:image', "")
            university_curriculum = university_info.get('curriculum', "")

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": f"{university_name}",
                                "description": f"{university_description}",
                                "thumbnail": {"imageUrl": thumbnail_url + ".jpg"},
                                "buttons": [
                                            {
                                                "action": "webLink",
                                                "label": "홈페이지 링크",
                                                "webLinkUrl": f"{university_link}"
                                            },
                                            {
                                                # 차후 커리큘럼 메세지가 아니라 홈페이지의 각 학과 커리큘럼 링크로 대체할것
                                                "action": "message",
                                                "label": "커리큘럼",
                                                "messageText": f"{university_curriculum}"
                                            }
                                            ]
                                }
                            }
                    ]
               }
           }

            return jsonify(res)

        else:
            # 조건을 만족하지 않는 경우에 대한 처리
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": "하단 리스트에서 원하시는 정보를 찾아주세요!"
                                    },
                                "items": [
                                    {
                                        "title": "전공 정보",
                                        "description": "전공관련 정보입니다",
                                        "action": "block",
                                        "blockId": "6458b76c28eb02106c03f010"
                                    },
                                    {
                                        "title": "과기대 전공 종류(목록)",
                                        "description": "서울과기대의 전공 목록들입니다",
                                        "action": "block",
                                        "blockId": "6458bd2a64533008d7f94b8e"
                                    },
                                    {
                                        "title": "학과 홈페이지",
                                        "description": "해당전공의 학과 홈페이지입니다",
                                        "action": "block",
                                        "blockId": "6458e6e964533008d7f94cbf"
                                    },
                                    {
                                        "title": "전공 커리큘럼",
                                        "description": "전공의 커리큘럼 예시들입니다",
                                        "action": "block",
                                        "blockId": "6458eaf98dc11c3fea80d763"
                                    }  
                                    
                                ]
                            
                            }
                        }
                    ]
                }
            }
        
            return jsonify(res)
    # 연락처 블록_부서
    if user_result.get('block')['name'] == '연락처_부서':
        user_params = req['action']['params']
        major_name = user_params.get('전공_1')
        department_name = user_params.get('대학_부서')

        with open('연락처.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            contact = data.get('contact')

        if major_name in data['contact'] and not department_name:
            contact_info = data['contact'][major_name]
            contact_name = contact_info['name']
            contact_number = contact_info['number']
            
            

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText" : {
                                    "text" : f"{contact_name}의 연락처입니다.\n{contact_name} : {contact_number}"
                                }
                            }
                    ]
               }
           }

            return jsonify(res)

        elif department_name in data['contact'] and not major_name:
            contact_info = data['contact'][department_name]
            contact_name = contact_info['name']
            contact_number = contact_info['number']

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText" : {
                                    "text" : f"{contact_name}의 연락처입니다.\n\n{contact_name} : {contact_number}"
                                }
                            }
                    ]
               }
           }

            return jsonify(res)
    # 연락처 블록_학과
    if user_result.get('block')['name'] == '연락처_학과':
        user_params = req['action']['params']
        major_name = user_params.get('전공_1')
        
        print(req)
        with open('연락처.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            contact = data.get('contact')

        if major_name in data['contact']:
            contact_info = data['contact'][major_name]
            contact_name = contact_info['name']
            contact_number = contact_info['number']
            
            

            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText" : {
                                    "text" : f"{contact_name}의 연락처입니다.\n{contact_name} : {contact_number}"
                                }
                            }
                    ]
               }
           }
            
            return jsonify(res)

    
               
    # 랜덤 리스트 출력 
    if user_result.get('block')['name'] == '인사' or user_result.get('block')['name'] == '웰컴 블록':

        
        block_id_연락처 = ['65215e1c4a2aa96a2977f465', '연락처 정보']
        blodk_id_학교주변 = ['652a4ac4da81f579ccd366fa', '학교주변 정보']
        block_id_생활관 = ['65055e22ed24787e55b1b274', '생활관 정보']
        block_id_학식 = ['64621e1b95f0716a5582bb8d', '학식 정보']
        block_id_와이파이 = ['646246e1954e43077f05bc8d', '와이파이 정보']
        block_id_웹메일 = ['64688d40a2844e2dbe389f58', '웹메일 정보']
        block_id_장학 = ['646873426a1cf7451400dc60', '장학 정보']
        block_id_휴학 = ['644f856c82e69401205aacc0', '휴학 정보']
        block_id_복학 = ['644fbffdbc002146b56d36ec', '복학 정보']
        block_id_수강신청 = ['64bcd160d3906927d1ddc6bd', '수강신청 정보']
        block_id_전과 = ['65057258443c4c44dc7fc372', '전과 정보']
        block_id_졸업 = ['65100433e1d39518fa282c77', '졸업 정보']
        block_id_학사일정 = ['652a4086648eee21606e220d', '학사일정']
        block_id_학교정보 = ['652a54707a5bab3eee316c96', '학교정보']
        
        block_ids = [
            
            block_id_연락처,
            blodk_id_학교주변,
            block_id_생활관,
            block_id_학식,
            block_id_와이파이,
            block_id_웹메일,
            block_id_장학,
            block_id_휴학,
            block_id_복학,
            block_id_수강신청, 
            block_id_전과,
            block_id_졸업,
            block_id_학사일정,
            block_id_학교정보
            
            ]
        
        selected_block_ids = random.sample(block_ids, 5)
            
        block_0 = selected_block_ids[0][0]
        block_0_title = selected_block_ids[0][1]
        
        block_1 = selected_block_ids[1][0]
        block_1_title = selected_block_ids[1][1]
        
        block_2 = selected_block_ids[2][0]
        block_2_title = selected_block_ids[2][1]
        
        block_3 = selected_block_ids[3][0]
        block_3_title = selected_block_ids[3][1]
        
        block_4 = selected_block_ids[4][0]
        block_4_title = selected_block_ids[4][1]




        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {                        
                        "listCard": {
                            "header": {
                                "title": "안녕하세요! 서울과학기술대학교 챗봇입니다!"
                                },
                            "items": [
                                {
                                    "title": block_0_title,
                                    "description": "",
                                    "action": "block",
                                    "blockId": block_0
                                },
                                {
                                    "title": block_1_title,
                                    "description": "",
                                    "action": "block",
                                    "blockId": block_1
                                },
                                {
                                    "title": block_2_title,
                                    "description": "",
                                    "action": "block",
                                    "blockId": block_2
                                },
                                {
                                    "title": block_3_title,
                                    "description": "",
                                    "action": "block",
                                    "blockId": block_3
                                },
                                {
                                    "title": block_4_title,
                                    "description": "",
                                    "action": "block",
                                    "blockId": block_4
                                }   
                            ]
                        }

                    }
                ]
            }
        }
        
        
        return jsonify(res)
    

        

#플라스크 실행 시키기  
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')