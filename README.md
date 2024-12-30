# SeoulTech_chat_bot
이 레포지토리는 [Kakao 오픈빌더](https://chatbot.kakao.com/)용 웹훅(Webhook) 예시 구현을 담고 있습니다. KakaoTalk 환경에서 동작하는 챗봇이 사용자 메시지를 전달받고 응답을 생성할 수 있도록 하는 핵심 코드 예시를 제공합니다. 이를 통해 텍스트, 버튼, 리치 미디어 등 카카오톡의 다양한 메시지 유형을 효과적으로 처리할 수 있습니다.

# Project Gantt Chart
![image](https://github.com/user-attachments/assets/00f453c3-ddab-445f-a7c5-b8319380b1cb)<br>
2023.03.01 ~ 2023.11.10

# How It Works
![image](https://github.com/user-attachments/assets/7168a386-a067-4cef-92ab-f6eeb16feaff)<br>
-사용자 입력<br>
사용자가 카카오톡 챗봇에게 메시지를 전송하면, 카카오 서버가 해당 요청을 설정된 웹훅 URL로 전달합니다.

-웹훅 처리<br>
웹훅 서버는 사용자 메시지와 함께 전달된 JSON 데이터를 수신하고, 해당 정보를 바탕으로 비즈니스 로직을 수행합니다(사용자 의도 분석, 데이터베이스 조회, API 호출 등).

-응답 반환<br>
웹훅 서버는 처리 결과를 JSON 형태로 카카오 서버에 다시 전송합니다. 카카오 서버는 이를 사용자에게 최종 메시지로 보여줍니다.

# vs [ChatMe](https://itc.seoultech.ac.kr/service/chatme/)
![image](https://github.com/user-attachments/assets/8c5ec2a5-61f5-46aa-b459-f2eda62ad31d)<br>
![image](https://github.com/user-attachments/assets/e884d847-d7fe-4d0a-95ce-fc2db48b6b20)<br>
![image](https://github.com/user-attachments/assets/e81049f4-0f0f-49e7-8e0a-e77f5906b1d1)<br>
![image](https://github.com/user-attachments/assets/e827feec-b45f-42da-b004-8d822818e586)

# Demo Result
![image](https://github.com/user-attachments/assets/a22ea2e6-47ba-497b-b11b-599d1047bd44)<br>
 https://github.com/HanTaeSeop/SeoulTech_chat_bot/blob/main/docs/kakao%20open%20builder%EC%9D%98%20%EC%9E%90%EC%97%B0%EC%96%B4%20%EC%B2%98%EB%A6%AC%20%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98%20%EA%B8%B0%EB%B0%98%20%EC%B1%97%EB%B4%87.pdf


