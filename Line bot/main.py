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
    FlexSendMessage,
    URITemplateAction
)
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
import numpy as np
from Building_classify import building_classify_fast_thread_int_return

#firestore
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)

# (0) Messages
welcomeMessage = TextSendMessage(text='歡迎加入陽交大校園地圖小幫手')
errorMessage = TextSendMessage(text='哦，這超出我的能力範圍......')

def link_and_building(num):
    link = 'https://drive.google.com/uc?export=view&id='
    link2 = (
        '1cp6tBT7Qu2hXCEU6qCSm2vW3MTRDo_Sg',
        '1Qz5K3MAPtQB4rHR9QYoqFpMJMPEFgFru',
        '104smxuN5q_L_rliTRomrX7uICm2k0sEQ',
        '1E73OAwrh4lNuOX6xpE9ua4bNBwFqgYDG',
        '1QKbHl3e279j16kQoZvSUq0gNEFHSL0ds',
        '1m5y65XOZYgXxC2UIkTS6QKlXsw8yM_SE',
        '12LqA_0YQJsnkz7WERXqk1jVSmOX4KopY',
        '1eqoMJ4FQqX6k1vNt_GNDcV2Qvkl1tlnu',
        '1GhUxrqJrZpCprTNAqsvA9aW9wJ66wv6q',
        '1E1nZFLg2jvUoOCIiw_E8h4GgI0gzFvgb'
    )
    map_link = (
        'https://maps.app.goo.gl/UAedZmCRucFeJCxKA',
        'https://maps.app.goo.gl/6xo22gbxfCoHVGi1A',
        'https://maps.app.goo.gl/iQkXEZCTQGqS8F5UA',
        'https://maps.app.goo.gl/dJZmhwrVB8qoRCWd8',
        'https://maps.app.goo.gl/UKSS5y4U4sGzMJkR7',
        'https://maps.app.goo.gl/jyLjyYkw5NCEYfoy6',
        'https://maps.app.goo.gl/6i1qVfAAPPPoULUv5',
        'https://maps.app.goo.gl/AxUsGuoEKQjfcvbA6',
        'https://maps.app.goo.gl/iJHVtsTi8LS2wtFc6',
        'https://maps.app.goo.gl/QtU5YUmCEmzkqcx49'
    )
    name = (
        '工程三館', '工程四館', '工程五館', '交映樓', '科學一館',
        '科學二館', '竹湖', '中正堂(大禮堂)', '體育館', '田家炳光電大樓'
    )

    return [TextSendMessage(text=name[num]), ImageSendMessage(original_content_url=link+link2[num],
                    preview_image_url=link+link2[num])], map_link[num]

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

        replyMessages, map_link = link_and_building(msg)
        
        replyMessages.append(TemplateSendMessage(alt_text='請選擇一個',
                            template=ButtonsTemplate(
                            title='要開啟Google map還是選擇想要前往的目的地?',
                            text='<3',
                            actions=[
                                URITemplateAction(
                                    label='開啟Google map',
                                    uri=map_link
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
@handler.add(PostbackEvent)
def handle_postback(event):
    print(event)
    lineId = event.source.user_id
    command = event.postback.data
    
    if (command == 'template_classes'): #傳送課程的範例
        replyMessages = TextSendMessage('課程增加方式：\n輸入"課程名稱/建築物"\n\n範例：微積分/科學一館\n---------\n\n課程地圖使用：\n在課程名稱前輸入"課程#"\n\n範例：課程#微積分')   
    
    if replyMessages is not None:
        line_bot_api.reply_message(event.reply_token, replyMessages)
