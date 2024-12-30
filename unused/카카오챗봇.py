import webbrowser
from flask import Flask, request, jsonify, url_for
import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from create_table_image import create_table_image
import pandas as pd
from table_to_2d import table_to_2d
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/sample_1', methods=['POST'])
def sample_a():
    req = request.get_json()
    user_result = req.get('userRequest')


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
        print(df)

        # 표 이미지 생성
        table_image = create_table_image(df)
       

        # 이미지를 파일로 저장
        image_path = r'C:\Users\tjrrb\source\repos\카카오챗봇\카카오챗봇\static\images\table_image.png'
        table_image.save(image_path, "png")
        
        # 이미지 파일의 URL 생성
        # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #
        image_url = 'https://d74f-61-74-227-240.ngrok.io/static/images/table_image.png'  
        # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #

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
            font_path = r'C:\Users\tjrrb\source\repos\카카오챗봇\카카오챗봇\nanum-all\나눔 글꼴\나눔고딕\NanumGothic.ttf'
    
            # 텍스트를 이미지 위에 추가
            draw = ImageDraw.Draw(table_image)
            font = ImageFont.truetype(font_path, 25)  # 원하는 폰트와 크기로 설정
            text_width, text_height = draw.textsize(table_name, font=font)
            text_x = (table_image.width - text_width) // 2
            text_y = table_image.height - text_height - 10  # 텍스트를 이미지 하단에 추가하려면 조정
            draw.text((text_x, text_y), table_name, fill="black", font=font)  # 원하는 위치에 텍스트 추가
               

            # 이미지를 파일로 저장
            image_path = rf'C:\Users\tjrrb\source\repos\카카오챗봇\카카오챗봇\static\images\table_image_{i}.png'
            table_image.save(image_path, "png")
        
            # 이미지 파일의 URL 생성
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #
            image_url = f'https://d74f-61-74-227-240.ngrok.io/static/images/table_image_{i}.png'  
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
            font_path = r'C:\Users\tjrrb\source\repos\카카오챗봇\카카오챗봇\nanum-all\나눔 글꼴\나눔고딕\NanumGothic.ttf'
    
            # 텍스트를 이미지 위에 추가
            draw = ImageDraw.Draw(table_image)
            font = ImageFont.truetype(font_path, 25)  # 원하는 폰트와 크기로 설정
            text_width, text_height = draw.textsize(table_name, font=font)
            text_x = (table_image.width - text_width) // 2
            text_y = table_image.height - text_height - 10  # 텍스트를 이미지 하단에 추가하려면 조정
            draw.text((text_x, text_y), table_name, fill="black", font=font)  # 원하는 위치에 텍스트 추가
               

            # 이미지를 파일로 저장
            image_path = rf'C:\Users\tjrrb\source\repos\카카오챗봇\카카오챗봇\static\images\table_image_{i}.png'
            table_image.save(image_path, "png")
        
            # 이미지 파일의 URL 생성
            # -------------- ngrok 킬 때마다 url 수정 필요 ----------------- #
            image_url = f'https://d74f-61-74-227-240.ngrok.io/static/images/table_image_{i}.png'  
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

        print(university_major1)
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
                            "simpleText": {
                                "text": "조건에 해당하는 정보를 찾지 못했습니다."
                            }
                        }
                    ]
                }
            }
        
            return jsonify(res)
    # 전공_커리큘럼 블록
    if user_result.get('block')['name'] == '전공_커리큘럼':
        user_params = req['action']['params']
        university_major1 = user_params.get('전공_1')
        
        thumbnail_url = "https://imgur.com/1xhrXaU"

        print(university_major1)
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
                            "simpleText": {
                                "text": "조건에 해당하는 정보를 찾지 못했습니다."
                            }
                        }
                    ]
                }
            }
        
            return jsonify(res)
    # 전공_홈페이지 블록
    if user_result.get('block')['name'] == '전공_홈페이지':
        user_params = req['action']['params']
        university_major1 = user_params.get('전공_1')
        
        thumbnail_url = "https://imgur.com/1xhrXaU"

        print(university_major1)
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
                            "simpleText": {
                                "text": "조건에 해당하는 정보를 찾지 못했습니다."
                            }
                        }
                    ]
                }
            }
        
            return jsonify(res)
    # 연락처 블록
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

        else:
            
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "죄송합니다. 원하시는 정보가 없습니다. 상담원과의 연락(추가예정)을 원하시면 버튼(추가예정)을 눌러주세요"
                            }
                        }
                    ]
                }
            }

            return jsonify(res)



    #


if __name__ == '__main__':
    app.run(port=5000)

