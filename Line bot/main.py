from chatBotConfig import channel_secret, channel_access_token
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent,
    TextSendMessage,
    MessageEvent,
    TextMessage,
    PostbackEvent,
    ButtonsTemplate,
    TemplateSendMessage,
    PostbackTemplateAction,
    CarouselTemplate,
    CarouselColumn,
    ConfirmTemplate,
    FlexSendMessage
)
from datetime import datetime, timedelta
#firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)

def is_sign_in(lineId):
    # 是否有登入
    query = db.collection("user").where("lineId", "==", lineId).limit(1)
    docs = query.get()
    if len(docs) > 0 and docs[0].exists:
        return True
    return False

def sign_in(name, lineId):
    #登入
    account=db.collection("user").document(name).get()
    if account.exists and account.to_dict()['lineId']=='':
        lib={"lineId":lineId,
            "alarm_type":[False, False, True, False, False, False]}
        db.collection("user").document(name).set(lib, merge=True)
        return True
    return False


# (0) Messages
welcomeMessage = TextSendMessage(text='歡迎加入青崇服事系統')
loginMessage = TextSendMessage(text='請先輸入你的名字登入(2個字)\n格式範例:阿光')
errorMessage = TextSendMessage(text='哦，這超出我的能力範圍......')
def alarmMessage():
    from week_alarm import alarm
    return FlexSendMessage(alt_text='提醒設定', contents= alarm)
def menuMessage():
    from week_alarm import menu
    return FlexSendMessage(alt_text='目錄', contents= menu)

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
    replyMessages = [welcomeMessage, loginMessage]
    line_bot_api.reply_message(event.reply_token, replyMessages)

# (3) Message Event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    lineId = event.source.user_id
    command = event.message.text
    if is_sign_in(lineId):
        if (command in ['總班表','全部班表']):
            replyMessages = wholeChart(lineId)
            
        elif (command in ['換班', '調班']):#選調班日、種類
            replyMessages = TemplateSendMessage(alt_text='調班選單', template=CarouselTemplate(shift_0(lineId, 'S')))
        
        elif (command in ['贈予', '贈送', '贈與']):
            replyMessages = TemplateSendMessage(alt_text='調班選單', template=CarouselTemplate(shift_0(lineId, 'G')))
        
        elif (command in ['設定提醒', '提醒設定', '設定']):
            replyMessages = alarmMessage()
        
        elif (command in ['目錄', 'Menu', 'menu', '主選單', '選單']):
            replyMessages = menuMessage()
            
        elif (command[0:5] == "管理員模式"):#強制調班
            replyMessages = manager_mode(command)
                
        else:
            return
    else:
        if (len(command) == 2):
            if sign_in(command, lineId):
                replyMessages = [TextSendMessage(text = "登入成功"),TextSendMessage(text = "手機請\"點按功能主選單\"\n平板請傳送「目錄」呼叫選單")]
            else:
                replyMessages = TextSendMessage(text = "登入失敗")

        else:
            replyMessages = [errorMessage, loginMessage]
                                                                                        
    line_bot_api.reply_message(event.reply_token, replyMessages)

# (4) Postback Event
@handler.add(PostbackEvent)
def handle_postback(event):
    print(event)
    lineId = event.source.user_id
    command = event.postback.data
    
    if (command[0:2] == 'A*'):#選調班日
        replyMessages = shift_Z(command[2:].split("+"), lineId)
    
    elif (command[0:2] == 'A&'):#選被調班日、被調班人
        replyMessages = shift_A(command[2:].split("+"))
        
    elif (command[0:2] == 'B&'):#跟調班人-確認申請
        replyMessages = shift_B(command, "S")
        
    elif (command[0:2] == 'B#'):#該服事有兩人的處理
        replyMessages = shift_B_twoUser(command[2:].split("+"))
        
                                                                                                                                                                     
    line_bot_api.reply_message(event.reply_token, replyMessages)