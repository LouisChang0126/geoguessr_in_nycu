import PIL.Image
import google.generativeai as genai
import os
import numpy as np
import pandas as pd
import threading

def building_classify_fast_thread(Input_image):

    input_image = PIL.Image.fromarray(Input_image)
    input_image = input_image.convert("RGB")
    input_image.save('input_img.jpg')

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")

    image_list_ = [[], [], [], [], [], [], [], [], [], []]


    def return_image_list(num):
        pd_images = pd.read_csv("uploaded_name.csv")
        return_list = list()

        for i in range(8):
            file = genai.get_file(name=pd_images[str(num + 1)][i])
            return_list.append(file)

        image_list_[num] = return_list

    """
    10個建築物ver2
    1. 工程三館 EC
    2. 工程四館 ED
    3. 工程五館 EE
    4. 交映樓 CY
    5. 科學一館 SA
    6. 科學二館 SB
    7. 竹湖 lake
    8. 中正堂(大禮堂) AD
    9. 體育館 PH
    10. 田家炳光電大樓 EO
    """

    #print(os.listdir('data'))
    threads = list()
    for i in range(10):
        threads.append(threading.Thread(target = return_image_list, args = (i,)))
        threads[i].start()

    for i in range(10):
        threads[i].join()

    #print(image_list_)

    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt_1 = """
    接下來的八張照片是來自於建築物「工程三館」。
    """

    prompt_2 = """
    接下來的八張照片是來自於建築物「工程四館」。
    """

    prompt_3 = """
    接下來的八張照片是來自於建築物「工程五館」。
    """

    prompt_4 = """
    接下來的八張照片是來自於建築物「交映樓」。
    """

    prompt_5 = """
    接下來的八張照片是來自於建築物「科學一館」。
    """

    prompt_6 = """
    接下來的八張照片是來自於建築物「科學二館」。
    """

    prompt_7 = """
    接下來的八張照片是來自於建築物「竹湖」。
    """

    prompt_8 = """
    接下來的八張照片是來自於建築物「中正堂(大禮堂)」。
    """

    prompt_9 = """
    接下來的八張照片是來自於建築物「體育館」。
    """

    prompt_10 = """
    接下來的八張照片是來自於建築物「田家炳光電大樓」。
    """

    prompt_main_1 = """
    接下來的一張照片，稱為「使用者輸入照片」是一張建築物的照片.
    """

    #prompt_main_2 = """
    #請告訴我「使用者輸入照片」屬於上述十棟建築物的哪一棟建築物? 你的回答只能從上述十棟建築物挑選一個最相似的。 輸出回答格式為一個 json 格式，例如 : '{建築物名稱 : 科學一館}'
    #"""
    prompt_main_2 = """
    請告訴我「使用者輸入照片」屬於上述十棟建築物的哪一棟建築物? 你的回答只能從上述十棟建築物挑選一個最相似的。 例如 : 科學一館
    """

    content = [prompt_1]
    content.extend(image_list_[0])
    content.extend([prompt_2])
    content.extend(image_list_[1])
    content.extend([prompt_3])
    content.extend(image_list_[2])
    content.extend([prompt_4])
    content.extend(image_list_[3])
    content.extend([prompt_5])
    content.extend(image_list_[4])
    content.extend([prompt_6])
    content.extend(image_list_[5])
    content.extend([prompt_7])
    content.extend(image_list_[6])
    content.extend([prompt_8])
    content.extend(image_list_[7])
    content.extend([prompt_9])
    content.extend(image_list_[8])
    content.extend([prompt_10])
    content.extend(image_list_[9])

    content.extend([prompt_main_1])
    content.extend([genai.upload_file(path='input_img.jpg', display_name='input image')])
    content.extend([prompt_main_2])

    response = model.generate_content(content)

    print(response.text)
    return response.text

def building_classify_fast_thread_int_return(Input_image):

    input_image = PIL.Image.fromarray(Input_image)
    input_image = input_image.convert("RGB")
    input_image.save('input_img.jpg')

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")

    image_list_ = [[], [], [], [], [], [], [], [], [], []]


    def return_image_list(num):
        pd_images = pd.read_csv("uploaded_name.csv")
        return_list = list()

        for i in range(8):
            file = genai.get_file(name=pd_images[str(num + 1)][i])
            return_list.append(file)

        image_list_[num] = return_list

    """
    10個建築物ver2
    1. 工程三館 EC
    2. 工程四館 ED
    3. 工程五館 EE
    4. 交映樓 CY
    5. 科學一館 SA
    6. 科學二館 SB
    7. 竹湖 lake
    8. 中正堂(大禮堂) AD
    9. 體育館 PH
    10. 田家炳光電大樓 EO
    """

    #print(os.listdir('data'))
    threads = list()
    for i in range(10):
        threads.append(threading.Thread(target = return_image_list, args = (i,)))
        threads[i].start()

    for i in range(10):
        threads[i].join()

    #print(image_list_)

    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt_1 = """
    接下來的八張照片是來自於建築物「1」。
    """

    prompt_2 = """
    接下來的八張照片是來自於建築物「2」。
    """

    prompt_3 = """
    接下來的八張照片是來自於建築物「3」。
    """

    prompt_4 = """
    接下來的八張照片是來自於建築物「4」。
    """

    prompt_5 = """
    接下來的八張照片是來自於建築物「5」。
    """

    prompt_6 = """
    接下來的八張照片是來自於建築物「6」。
    """

    prompt_7 = """
    接下來的八張照片是來自於建築物「7」。
    """

    prompt_8 = """
    接下來的八張照片是來自於建築物「8」。
    """

    prompt_9 = """
    接下來的八張照片是來自於建築物「9」。
    """

    prompt_10 = """
    接下來的八張照片是來自於建築物「10」。
    """

    prompt_main_1 = """
    接下來的一張照片，稱為「使用者輸入照片」是一張建築物的照片.
    """

    #prompt_main_2 = """
    #請告訴我「使用者輸入照片」屬於上述十棟建築物的哪一棟建築物? 你的回答只能從上述十棟建築物挑選一個最相似的。 輸出回答格式為一個 json 格式，例如 : '{建築物名稱 : 科學一館}'
    #"""
    prompt_main_2 = """
    請告訴我「使用者輸入照片」屬於上述十棟建築物的哪一棟建築物? 你的回答只能從上述十棟建築物挑選一個最相似的。 例如 : '3'
    """

    content = [prompt_1]
    content.extend(image_list_[0])
    content.extend([prompt_2])
    content.extend(image_list_[1])
    content.extend([prompt_3])
    content.extend(image_list_[2])
    content.extend([prompt_4])
    content.extend(image_list_[3])
    content.extend([prompt_5])
    content.extend(image_list_[4])
    content.extend([prompt_6])
    content.extend(image_list_[5])
    content.extend([prompt_7])
    content.extend(image_list_[6])
    content.extend([prompt_8])
    content.extend(image_list_[7])
    content.extend([prompt_9])
    content.extend(image_list_[8])
    content.extend([prompt_10])
    content.extend(image_list_[9])

    content.extend([prompt_main_1])
    content.extend([genai.upload_file(path='input_img.jpg', display_name='input image')])
    content.extend([prompt_main_2])

    response = model.generate_content(content)

    print(response.text)
    return response.text



if __name__ == '__main__':

    for i in range(11):
        if i == 0:
            continue
        the_input_image = PIL.Image.open(f'test_data/{i}.jfif')
        the_input_image_np = np.array(the_input_image)

        building_classify_fast_thread_int_return(the_input_image_np)