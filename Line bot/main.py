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
from instruction import Instructor

inst = Instructor()

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
errorMessage = TextSendMessage(text='ㄜ...看不懂ㄛ...')
courseMessage = TextSendMessage('課程增加方式：\n輸入"課程名稱/建築物"\n\n範例：微積分/科學一館\n------------------------------------\n課程地圖使用：\n在課程名稱前輸入"課程#"\n\n範例：課程#微積分')   

building_name = (
    '工程三館', '工程四館', '工程五館', '交映樓', '科學一館',
    '科學二館', '竹湖', '中正堂(大禮堂)', '體育館', '田家炳光電大樓'
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

def sign_in(lineId):
    #登入
    account=db.collection("user").document(lineId).get()
    if account.exists:
        return account.to_dict()
    else:
        db.collection("user").document(lineId).set({})
        return {}

def building_name_carousel(mode, building):
    columns=[]
    action_S=[]
    tmp = building_name + ['', '']
    for i in range(12):
        action_S.append(PostbackTemplateAction(
            label=tmp[i],
            text=tmp[i],
            data=f"{'A&' if mode==1 else 'B&'}{i+1}%{building}")
        )
        if len(action_S)%3 == 0:
            columns.append(CarouselColumn(
                title='目的地',
                text='選擇一個目的地',
                actions=action_S
            ))
            action_S=[]
    return columns

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

    return [TextSendMessage(text=building_name[num]), ImageSendMessage(original_content_url=link+link2[num],
                    preview_image_url=link+link2[num])]

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
    lineId = event.source.user_id
    types = event.message.type
        
    if types == 'image':
        #msg = "Upload success"
        msgID = event.message.id 
        message_content = line_bot_api.get_message_content(msgID)
        image = Image.open(BytesIO(message_content.content))
        image_array = np.array(image)

        msg = building_classify_fast_thread_int_return(image_array)
        if type(msg) == str:
            line_bot_api.reply_message(event.reply_token, [errorMessage])

        replyMessages = link_and_building(msg)
        
        replyMessages.append(TemplateSendMessage(alt_text='請選擇一個',
                            template=ButtonsTemplate(
                            title='要開啟Google Map或是選擇想要前往的目的地嗎?',
                            text='',
                            actions=[
                                URITemplateAction(
                                    label='開啟Google map',
                                    uri=map_link[msg]
                                ),
                                PostbackTemplateAction(
                                    label='選擇目的地',
                                    text='選擇目的地',
                                    data=f'choose_destination%{msg}'
                                )
                            ]
                        )
                    )
        )
        
    elif types == 'text':
        account = sign_in(lineId)
        
        msg = event.message.text
        if ('/' in msg):
            if(msg.split('/')[1] in building_name):
                account[msg.split('/')[0]] = msg.split('/')[1]
                db.collection("user").document(lineId).set(account)
                replyMessages = TextSendMessage(text=f'新增 {msg.split("/")[0]} 成功')
            else:
                replyMessages = TextSendMessage(text='目前不支援這棟建築ㄛ')
        elif (msg[:3] == '課程#'):
            if(msg.split('#')[1] in account):
                name = f'{account[msg.split("#")[1]]}'
                index = building_name.index(name)
                replyMessages = [TextSendMessage(text=name)]
                replyMessages.append(TemplateSendMessage(alt_text='請選擇一個',
                            template=ButtonsTemplate(
                            title='要開啟Google Map或是開啟文字敘述導航?',
                            text='',
                            actions=[
                                URITemplateAction(
                                    label='開啟Google map',
                                    uri=map_link[index]
                                ),
                                PostbackTemplateAction(
                                    label='文字導航',
                                    text='文字導航',
                                    data=f'choose_start%{index}'
                                )
                            ]
                        )
                    )
            )
            else:
                replyMessages = TextSendMessage(text='你目前沒有新增這門課程ㄛ')
        else:
            replyMessages = [errorMessage, courseMessage]

    else:
        replyMessages = errorMessage
                                                                                        
    line_bot_api.reply_message(event.reply_token, replyMessages)

# (4) Postback Event
@handler.add(PostbackEvent)
def handle_postback(event):
    print(event)
    lineId = event.source.user_id
    command = event.postback.data
    
    if (command == 'template_classes'): #傳送課程的範例
        replyMessages = courseMessage
    elif ('choose_destination' in command): #選擇目的地
        replyMessages = TemplateSendMessage(alt_text='選擇目的地', template=CarouselTemplate(building_name_carousel(1, command.split('%')[1])))
    elif ('choose_start' in command): #選擇目的地
        replyMessages = TemplateSendMessage(alt_text='選擇現在位置', template=CarouselTemplate(building_name_carousel(2, command.split('%')[1])))
    elif (command[:2] == "A&"): #文字地圖
        replyMessages = inst.navigotor(command[2:].split('%')[1], command[2:].split('%')[0])
    elif (command[:2] == "B&"): #文字地圖
        replyMessages = inst.navigotor(command[2:].split('%')[0], command[2:].split('%')[1])

    if replyMessages is not None:
        line_bot_api.reply_message(event.reply_token, replyMessages)
