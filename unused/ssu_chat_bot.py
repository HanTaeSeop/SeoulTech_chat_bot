import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

project_id = "ssu-chat-bot-gvww"
session_id = "626733648328"
language_code = "kor"

session_client = dialogflow.SessionsClient()

session = session_client.session_path(project_id, session_id)
print("Session path:", session)

while True:
    user_input = input("사용자 입력: ")
    if user_input == "끝":
        break

    text_input = dialogflow.TextInput(text=user_input, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    except InvalidArgument:
        raise

    print("챗봇 응답:", response.query_result.fulfillment_text)