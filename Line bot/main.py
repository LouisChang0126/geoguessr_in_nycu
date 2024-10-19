from chatBotConfig import channel_secret, channel_access_token
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent,
    TextSendMessage,
    MessageEvent,
    TextMessage,
    ImageMessage,
    PostbackEvent,
    ImageSendMessage,
    ButtonsTemplate,
    TemplateSendMessage,
    PostbackTemplateAction,
    CarouselTemplate,
    CarouselColumn,
    ConfirmTemplate,
    FlexSendMessage
)
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
import numpy as np
from Building_classify import building_classify_fast_thread_int_return

#firestore
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# cred = credentials.Certificate('serviceAccount.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)

# (0) Messages
welcomeMessage = TextSendMessage(text='歡迎加入陽交大校園地圖小幫手')
errorMessage = TextSendMessage(text='哦，這超出我的能力範圍......')


# (1) Webhook
def lineWebhook(request):
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')
    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print(e)

    return '200 OK'

# (2) Follow Event
@handler.add(FollowEvent)
def handle_follow(event):
    replyMessages = [welcomeMessage]
    line_bot_api.reply_message(event.reply_token, replyMessages)

# (3) Message Event
@handler.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_message(event):
    #lineId = event.source.user_id
    types = event.message.type
    
    if types == 'image':
        msg = "Upload success"
        msgID = event.message.id 
        message_content = line_bot_api.get_message_content(msgID)
        #replyMessages = [TextSendMessage(text = msg),
                        #ImageSendMessage(original_content_url="https://github.com/LouisChang0126/geoguessr_in_nycu/blob/main/data/10_1.png",
                    #preview_image_url="https://github.com/LouisChang0126/geoguessr_in_nycu/blob/main/data/10_1.png")]
        image = Image.open(BytesIO(message_content.content))
        image_array = np.array(image)

        msg = str(building_classify_fast_thread_int_return(image_array))
        replyMessages = TextSendMessage(text = msg)
        

    elif types == 'text':
        msg = event.message.text
        replyMessages = TextSendMessage(text = msg)

    else:
        replyMessages = [errorMessage]
                                                                                        
    line_bot_api.reply_message(event.reply_token, replyMessages)

# (4) Postback Event
# @handler.add(PostbackEvent)
# def handle_postback(event):
#     print(event)
#     lineId = event.source.user_id
#     command = event.postback.data
    
    # if (command[0:2] == 'A*'):#選調班日
    #     replyMessages = shift_Z(command[2:].split("+"), lineId)
    
    # elif (command[0:2] == 'A&'):#選被調班日、被調班人
    #     replyMessages = shift_A(command[2:].split("+"))
        
    # elif (command[0:2] == 'B&'):#跟調班人-確認申請
    #     replyMessages = shift_B(command, "S")
        
    # elif (command[0:2] == 'B#'):#該服事有兩人的處理
    #     replyMessages = shift_B_twoUser(command[2:].split("+"))
        
                                                                                                                                                                     
    # line_bot_api.reply_message(event.reply_token, replyMessages)
