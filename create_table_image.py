from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd


def create_table_image(table_data):

    #DataFrame으로 변환
    table_data = pd.DataFrame(table_data)

    # 테이블의 행과 열 개수 추출
    num_rows = len(table_data)
    num_cols = len(table_data.columns) if num_rows > 0 else 0

    # 셀의 너비와 높이 설정
    cell_width = 120
    cell_height = 40

    # 테이블 이미지의 너비와 높이 계산
    table_width = num_cols * cell_width
    table_height = (num_rows + 1) * cell_height + (len(table_data.columns) - 1) * cell_height  # 헤더 행 추가

    # 폰트 경로 설정
    font_path = r'C:\Users\Taeseop\Desktop\chat_bot\챗봇에사용된이미지\NanumGothic.ttf'

    # 테이블 이미지 생성
    table_image = Image.new('RGB', (table_width, table_height), color='white')
    draw = ImageDraw.Draw(table_image)

    # 폰트 설정
    font = ImageFont.truetype(font_path, size=10)

    # 테이블 데이터를 이미지에 그리기
    for i in range(num_rows + 1):  # 헤더 행 추가
        for j in range(num_cols):
            if i == 0:  # 헤더 행
                cell_text = str(table_data.columns[j])
            else:
                cell_info = table_data.iat[i - 1, j]
                if isinstance(cell_info, dict):
                    cell_text = str(cell_info.get('text', ''))
                else:
                    cell_text = str(cell_info)

            # 셀의 좌상단 좌표 계산
            x = j * cell_width
            y = i * cell_height

            # 셀의 경계선 그리기
            draw.rectangle([(x, y), (x + cell_width, y + cell_height)], outline='black')

            # 셀에 텍스트 그리기
            text_width, text_height = draw.textsize(cell_text, font=font)
            text_x = x + (cell_width - text_width) // 2
            text_y = y + (cell_height - text_height) // 2
            draw.text((text_x, text_y), cell_text, font=font, fill='black')

    merged_cells = set()  # 병합된 셀의 인덱스를 저장할 집합

    for i in range(num_rows):
        for j in range(num_cols):
            cell_info = table_data.iat[i, j]
            if isinstance(cell_info, dict):
                rowspan = int(cell_info.get('rowspan', 1))
                colspan = int(cell_info.get('colspan', 1))
            else:
                rowspan = 1
                colspan = 1
        
            # rowspan과 colspan이 1보다 큰 경우, 해당 셀을 병합합니다.
            if rowspan > 1 or colspan > 1:
               merged_cells.add((i, j))  # 병합된 셀의 인덱스를 저장합니다.

    # 병합된 셀을 처리하는 부분
    for i, j in merged_cells:
        cell_info = table_data.iat[i, j]

        if isinstance(cell_info, dict):
            cell_text = str(cell_info.get('text', ''))
        else:
            cell_text = str(cell_info)
            
        # 병합된 셀의 영역을 그리기 위해 좌상단 좌표와 우하단 좌표를 계산합니다.
        start_x = j * cell_width
        start_y = i * cell_height
        end_x = (j + colspan) * cell_width
        end_y = (i + rowspan) * cell_height
            
        # 병합된 셀 영역에 대한 직사각형을 그립니다.
        draw.rectangle([(start_x, start_y), (end_x, end_y)], fill='white', outline='black')
            
        # 병합된 셀에 텍스트를 가운데 정렬하여 그립니다.
        text_width, text_height = draw.textsize(cell_text, font=font)
        text_x = start_x + (end_x - start_x - text_width) // 2
        text_y = start_y + (end_y - start_y - text_height) // 2
        draw.text((text_x, text_y), cell_text, font=font, fill='black')


    return table_image

