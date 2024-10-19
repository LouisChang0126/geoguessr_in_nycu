import PIL
import google.generativeai as genai
import pandas as pd
import numpy as np

def direction_classify(Input_image, building_name):
    input_image = PIL.Image.fromarray(Input_image)
    input_image = input_image.convert("RGB")
    input_image.save('input_img.jpg')

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")

    pd_images = pd.read_csv("uploaded_name_direction.csv")

    image_list = []
    index = None
    prompt = None

    if(building_name == "1"):
        index = '1'
        building_name = "工程三館"

    elif(building_name == "2"):
        index = '2'
        building_name = "工程四館"

    elif(building_name == "3"):
        index = '3'
        building_name = "工程五館"

    elif(building_name == "4"):
        index = '4'
        building_name = "交映樓"

    elif(building_name == "5"):
        index = '5'
        building_name = "科學一館"

    elif(building_name == "6"):
        index = '6'
        building_name = "科學二館"

    elif(building_name == "7"):
        index = '7'
        building_name = "竹湖"

    elif(building_name == "8"):
        index = '8'
        building_name = "中正堂(大禮堂)"

    elif(building_name == "9"):
        index = '9'
        building_name = "體育館"

    elif(building_name == "10"):
        index = '10'
        building_name = "田家炳光電大樓"
        
    for i in range(8):
      file = genai.get_file(name=pd_images[index][i])
      image_list.append(file)
    

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt_main = "你將會接收到 8 張圖片作為參考樣本，分別標記為 1 到 8。接著，我會給你一張查詢圖片，請比較這張查詢圖片與所有參考樣本的相似度。 請回傳與查詢圖片最相似的圖片的索引，並將索引範圍設為 1～8（即第一張圖片的索引為 1，第二張圖片的索引為 2，依此類推）。 回應格式：<index>（例：3）"
    content = [prompt_main]
    content.extend(image_list)

    content.extend([genai.upload_file(path='input_img.jpg', display_name='sc1_1')])
    response = model.generate_content(content)
    

    return response.text
