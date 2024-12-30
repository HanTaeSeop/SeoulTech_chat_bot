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

app = Flask(__name__)

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    #
    req = request.get_json(silent=True, force = True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
    
    
    #날씨
    if query_result.get('action') == 'ask-weather.ask-weather-yes':

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

        fulfillmentText = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3)) + "\n" + ''.join((ful_text4)) + "\n" +''.join((ful_text5)) + "\n" +''.join((ful_text6)) + "\n" +''.join((ful_text7)) + "\n" +''.join((ful_text8)) + "\n" 

        return{
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
        }
    
    # 식단
    if query_result.get('action') == 'ask-school_food.ask-school_food-custom':
        if query_result.get('parameters') == {"school_food_building": "학생 제2식당"}:
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
                fulfillmentText = ''.join((ful_text1)) + "\n" + ''.join((ful_text2))+ "\n" + ''.join((ful_text3))+ "\n" + ''.join((ful_text4))+ "\n" + ''.join((ful_text5))
            else :
                ful_text1 = '등록된 식단이 없습니다.'
                
                    
        if query_result.get('parameters') == {"school_food_building": "테크노파크"}:
            now = datetime.now()
            nowDate = now.strftime('%Y년 %m월 %d일')
            
            ful_text1 = nowDate
            ful_text2 = '테크노파크(STP) 식단은 테크노파크사정으로 제공되지 않습니다.'
            ful_text3 = 'http://www.seoultp.or.kr/user/nd70791.do'
            fulfillmentText = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3))
        
        if query_result.get('parameters') == {"school_food_building": "KB학사"}:
            today = datetime.today().strftime('%A')
            url = 'https://domi.seoultech.ac.kr/support/food/?foodtype=kb'
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
            fulfillmentText = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3))
            
        if query_result.get('parameters') == {"school_food_building": "성림학사"}:
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
            fulfillmentText = f"{ful_text1}\n{ful_text2}\n{ful_text3}"

        if query_result.get('parameters') == {"school_food_building": "수림학사"}:
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
            fulfillmentText = ''.join((ful_text1)) + "\n" + ''.join((ful_text2)) + "\n" + ''.join((ful_text3))



        return{
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
            }
        
    
    #건물
    if query_result.get('action') == 'SeoultechBuilding.SeoultechBuilding-yes':
        if 'building' in query_result.get('parameters'):
            building_name = query_result.get('parameters')['building']        
            
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
            fulfillmentText = ''.join((ful_text1))
        return{
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
            }
    #학과
    if query_result.get('action') == 'ask_major.ask_major-yes':           
        major = query_result.get('outputContexts')[0]["parameters"]["university_major"][0]
                
        with open('major_info.json', 'r', encoding='utf-8') as b:
            major_info = json.load(b)
        if major in major_info:
            university_info = major_info[major]
            university_name = university_info['name']
            university_description = university_info['description']
            university_link = university_info['os:image']
            university_curriculum = university_info.get('curriculum',"")

            ful_text1= f'{major}에 대한 정보는 다음과 같다. \n {university_description}\n 교육과정은 다음과 같다. \n {university_curriculum} \n 홈페이지링크: {university_link}'
                                   
        else:
            ful_text1 = f'{major}에 대한 정보를 찾을 수 없습니다.'
        
        fulfillmentText = ''.join((ful_text1))
        
        return{
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
            }    
        
@app.route("/kakao",methods=['POST'])
def kakao():
    
    project_id = "ssu-chat-bot-gvww"
    session_id = "626733648328"
    language_code = "kor"

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    

    while True:
        user_input = request.json['userRequest']['utterance']

        if user_input == "끝":
            break

        text_input = dialogflow.TextInput(text=user_input, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        try:
            response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        except InvalidArgument:
            raise

        answer = response.query_result.fulfillment_text
    # 답변 텍스트 설정
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

    # 답변 전송
        return jsonify(res)






#플라스크 실행 시키기  
if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')