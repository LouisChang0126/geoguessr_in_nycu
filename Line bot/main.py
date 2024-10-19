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

def link_and_building(num):
    link = 'https://drive.google.com/uc?export=view&id='
    name = None
    if num == 1:
        link += '1cp6tBT7Qu2hXCEU6qCSm2vW3MTRDo_Sg'
        name = '工程三館'
    elif num == 2:
        link += '1Qz5K3MAPtQB4rHR9QYoqFpMJMPEFgFru'
        name = '工程四館'
    elif num == 3:
        link += '104smxuN5q_L_rliTRomrX7uICm2k0sEQ'
        name = '工程五館'
    elif num == 4:
        link += '1E73OAwrh4lNuOX6xpE9ua4bNBwFqgYDG'
        name = '交映樓'
    elif num == 5:
        link += '1QKbHl3e279j16kQoZvSUq0gNEFHSL0ds'
        name = '科學一館'
    elif num == 6:
        link += '1m5y65XOZYgXxC2UIkTS6QKlXsw8yM_SE'
        name = '科學二館'
    elif num == 7:
        link += '12LqA_0YQJsnkz7WERXqk1jVSmOX4KopY'
        name = '竹湖'
    elif num == 8:
        link += '1eqoMJ4FQqX6k1vNt_GNDcV2Qvkl1tlnu'
        name = '中正堂(大禮堂)'
    elif num == 9:
        link += '1GhUxrqJrZpCprTNAqsvA9aW9wJ66wv6q'
        name = '體育館'
    elif num == 10:
        link += '1E1nZFLg2jvUoOCIiw_E8h4GgI0gzFvgb'
        name = '田家炳光電大樓'

    return [TextSendMessage(text=name), ImageSendMessage(original_content_url=link,
                    preview_image_url=link)]

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
        #msg = "Upload success"
        msgID = event.message.id 
        message_content = line_bot_api.get_message_content(msgID)
        image = Image.open(BytesIO(message_content.content))
        image_array = np.array(image)

        msg = building_classify_fast_thread_int_return(image_array)

        replyMessages = link_and_building(msg)
        
        replyMessages.append(TemplateSendMessage(alt_text='請選擇一個',
                            template=ButtonsTemplate(
                            title='要開啟Google map還是選擇想要前往的目的地?',
                            text='<3',
                            actions=[
                                PostbackTemplateAction(
                                    label='開啟Google map',
                                    text='開啟Google map',
                                    data=msg
                                ),
                                PostbackTemplateAction(
                                    label='選擇目的地',
                                    text='選擇目的地',
                                    data=msg
                                )
                            ]
                        )
                    )
        )
        
        #replyMessages.append(TextSendMessage(text = msg))
        #replyMessages = TextSendMessage(text = msg)
        

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
