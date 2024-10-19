import json
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import RichMenu
from chatBotConfig import channel_access_token,channel_secret

# 初始化 LineBotApi
line_bot_api = LineBotApi(channel_access_token)

# 讀取 Rich Menu 設定的 JSON 檔案，使用 utf-8 編碼
with open("menuChatBot-tmp.json", "r", encoding="utf-8") as json_file:
    rich_menu_settings = json.load(json_file)

# 建立 Rich Menu
rich_menu_to_create = RichMenu.new_from_json_dict(rich_menu_settings)

try:
    # 建立 Rich Menu，並取得 Rich Menu ID
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print("\n\n\nRich Menu created with ID:", rich_menu_id, "\n\n\n")

    # 上傳 Rich Menu 的圖片
    with open("rich11.png", "rb") as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

    # 設定預設 Rich Menu
    line_bot_api.set_default_rich_menu(rich_menu_id)
    print("Default Rich Menu set successfully!")
except LineBotApiError as e:
    print("Error creating Rich Menu:", e)
