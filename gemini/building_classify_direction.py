import PIL
import google.generativeai as genai
import pandas as pd

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
        prompt = """接下來的八張照片是來自於建築物「工程三館」，分別代表不同的方位。"""
    elif(building_name == "2"):
        index = '2'
        building_name = "工程四館"
        prompt = """接下來的八張照片是來自於建築物「工程四館」，分別代表不同的方位。"""
    elif(building_name == "3"):
        index = '3'
        building_name = "工程五館"
        prompt = """接下來的八張照片是來自於建築物「工程五館」，分別代表不同的方位。"""
    elif(building_name == "4"):
        index = '4'
        building_name = "交映樓"
        prompt = """接下來的八張照片是來自於建築物「交映樓」，分別代表不同的方位。"""
    elif(building_name == "5"):
        index = '5'
        building_name = "科學一館"
        prompt = """接下來的七張照片是來自於建築物「科學一館」，分別代表不同的方位。"""
    elif(building_name == "6"):
        index = '6'
        building_name = "科學二館"
        prompt = """接下來的八張照片是來自於建築物「科學二館」，分別代表不同的方位。"""
    elif(building_name == "7"):
        index = '7'
        building_name = "竹湖"
        prompt = """接下來的八張照片是來自於建築物「竹湖」，分別代表不同的方位。"""
    elif(building_name == "8"):
        index = '8'
        building_name = "中正堂(大禮堂)"
        prompt = """接下來的八張照片是來自於建築物「中正堂(大禮堂)」，分別代表不同的方位。"""
    elif(building_name == "9"):
        index = '9'
        building_name = "體育館"
        prompt = """接下來的八張照片是來自於建築物「體育館」，分別代表不同的方位。"""
    elif(building_name == "10"):
        index = '10'
        building_name = "田家炳光電大樓"
        prompt = """接下來的八張照片是來自於建築物「田家炳光電大樓」，分別代表不同的方位。"""
        
    if index == '5':
        for i in range(7):
            file = genai.get_file(name=pd_images[index][i])
            image_list.append(file)
    else:
        for i in range(8):
            file = genai.get_file(name=pd_images[index][i])
            image_list.append(file)
    

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    content = [prompt]
    content.extend(image_list)

    prompt_main_1 = "接下來的一張照片，稱為「使用者輸入照片」是{}的照片.".format(building_name)
    content.extend([prompt_main_1])

    prompt_main_2 = "請告訴我「使用者輸入照片」和前面幾張參考照片中的哪一張最像? 只能從前面給的幾張參考照片中選擇，請注意，不包含「使用者輸入照片」。選出照片後請告訴我它在這些參考照片中是第幾張照片 輸出回答格式為一個 integer，例如 : 2"

    content.extend([genai.upload_file(path='input_img.jpg', display_name='sc1_1')])
    content.extend([prompt_main_2])

    response = model.generate_content(content)
    print(response.text)
    if response.text == '7' and index == '5':
        return '8'

    return response.text