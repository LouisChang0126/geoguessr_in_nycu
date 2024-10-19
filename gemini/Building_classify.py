import PIL.Image
import google.generativeai as genai
import os
import numpy as np
import pandas as pd

def building_classify_fast(Input_image):

    input_image = PIL.Image.fromarray(Input_image)
    input_image = input_image.convert("RGB")
    input_image.save('input_img.jpg')

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")

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

    pd_images = pd.read_csv("uploaded_name.csv")

    #print(os.listdir('data'))

    image_list_1 = list()
    image_list_2 = list()
    image_list_3 = list()
    image_list_4 = list()
    image_list_5 = list()
    image_list_6 = list()
    image_list_7 = list()
    image_list_8 = list()
    image_list_9 = list()
    image_list_10 = list()

    for i in range(8):
        file = genai.get_file(name=pd_images['1'][i])
        image_list_1.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['2'][i])
        image_list_2.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['3'][i])
        image_list_3.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['4'][i])
        image_list_4.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['5'][i])
        image_list_5.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['6'][i])
        image_list_6.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['7'][i])
        image_list_7.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['8'][i])
        image_list_8.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['9'][i])
        image_list_9.append(file)
    for i in range(8):
        file = genai.get_file(name=pd_images['10'][i])
        image_list_10.append(file)


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

    prompt_main_2 = """
    請告訴我「使用者輸入照片」是來自於哪一棟建築物? 輸出回答格式為一個 json 格式，例如 : '{建築物名稱 : 科學一館}'
    """

    content = [prompt_1]
    content.extend(image_list_1)
    content.extend([prompt_2])
    content.extend(image_list_2)
    content.extend([prompt_3])
    content.extend(image_list_3)
    content.extend([prompt_4])
    content.extend(image_list_4)
    content.extend([prompt_5])
    content.extend(image_list_5)
    content.extend([prompt_6])
    content.extend(image_list_6)
    content.extend([prompt_7])
    content.extend(image_list_7)
    content.extend([prompt_8])
    content.extend(image_list_8)
    content.extend([prompt_9])
    content.extend(image_list_9)
    content.extend([prompt_10])
    content.extend(image_list_10)

    content.extend([prompt_main_1])
    content.extend([genai.upload_file(path='input_img.jpg', display_name='sc1_1')])
    content.extend([prompt_main_2])

    response = model.generate_content(content)

    print(response.text)

def building_classify_faster(Input_image):

    input_image = PIL.Image.fromarray(Input_image)
    input_image = input_image.convert("RGB")
    input_image.save('input_img.jpg')

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")

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

    pd_images = pd.read_csv("uploaded_name.csv")

    #print(os.listdir('data'))

    image_list_1 = list()
    image_list_2 = list()
    image_list_3 = list()
    image_list_4 = list()
    image_list_5 = list()
    image_list_6 = list()
    image_list_7 = list()
    image_list_8 = list()
    image_list_9 = list()
    image_list_10 = list()

    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['1'][i])
        image_list_1.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['2'][i])
        image_list_2.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['3'][i])
        image_list_3.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['4'][i])
        image_list_4.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['5'][i])
        image_list_5.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['6'][i])
        image_list_6.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['7'][i])
        image_list_7.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['8'][i])
        image_list_8.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['9'][i])
        image_list_9.append(file)
    for i in [1, 3, 5, 7]:
        file = genai.get_file(name=pd_images['10'][i])
        image_list_10.append(file)


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

    prompt_main_2 = """
    請告訴我「使用者輸入照片」是屬於前面十棟建築物中的哪一棟建築物? 只能從前面十個建築物中選擇。 輸出回答格式為一個 json 格式，例如 : '{建築物名稱 : 科學一館}'
    """

    content = [prompt_1]
    content.extend(image_list_1)
    content.extend([prompt_2])
    content.extend(image_list_2)
    content.extend([prompt_3])
    content.extend(image_list_3)
    content.extend([prompt_4])
    content.extend(image_list_4)
    content.extend([prompt_5])
    content.extend(image_list_5)
    content.extend([prompt_6])
    content.extend(image_list_6)
    content.extend([prompt_7])
    content.extend(image_list_7)
    content.extend([prompt_8])
    content.extend(image_list_8)
    content.extend([prompt_9])
    content.extend(image_list_9)
    content.extend([prompt_10])
    content.extend(image_list_10)

    content.extend([prompt_main_1])
    content.extend([genai.upload_file(path='input_img.jpg', display_name='sc1_1')])
    content.extend([prompt_main_2])

    response = model.generate_content(content)

    print(response.text)


def building_classify(Input_image):

    input_image = PIL.Image.fromarray(Input_image)
    input_image = input_image.convert("RGB")
    input_image.save('input_img.jpg')

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")


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

    image_list_1 = list()
    image_list_2 = list()
    image_list_3 = list()
    image_list_4 = list()
    image_list_5 = list()
    image_list_6 = list()
    image_list_7 = list()
    image_list_8 = list()
    image_list_9 = list()
    image_list_10 = list()

    for file_name in os.listdir('data'):
        if file_name[0:2] == '10':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_10.append(the_uploaded_file)
            #file = genai.get_file(name=the_uploaded_file.name)
            #print(the_uploaded_file.name)
            #print(f"Retrieved file '{file.display_name}' as: {the_uploaded_file.uri}")
            #print("upload 10 :", file_name)
            pass
        elif file_name[0] == '1':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_1.append(the_uploaded_file)
            print("upload 1 :", file_name)
            pass
        elif file_name[0] == '2':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_2.append(the_uploaded_file)
            print("upload 2 :", file_name)
            pass
        elif file_name[0] == '3':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_3.append(the_uploaded_file)
            print("upload 3 :", file_name)
            pass
        elif file_name[0] == '4':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_4.append(the_uploaded_file)
            print("upload 4 :", file_name)
            pass
        elif file_name[0] == '5':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_5.append(the_uploaded_file)
            print("upload 5 :", file_name)
            pass
        elif file_name[0] == '6':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_6.append(the_uploaded_file)
            print("upload 6 :", file_name)
            pass
        elif file_name[0] == '7':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_7.append(the_uploaded_file)
            print("upload 7 :", file_name)
            pass
        elif file_name[0] == '8':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_8.append(the_uploaded_file)
            print("upload 8 :", file_name)
            pass
        elif file_name[0] == '9':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_9.append(the_uploaded_file)
            print("upload 9 :", file_name)
            pass


    """
    sc1_1 = genai.upload_file(path=r'.\images\1_1.png', display_name='sc1_1')
    sc1_2 = genai.upload_file(path=r'.\images\1_2.png', display_name='sc1_2')
    sc1_3 = genai.upload_file(path=r'.\images\1_3.png', display_name='sc1_3')
    sc1_4 = genai.upload_file(path=r'.\images\1_4.png', display_name='sc1_4')
    print("sc1 upload!")

    lib_1 = genai.upload_file(path=r'.\images\2_1.png', display_name='lib_1')
    lib_2 = genai.upload_file(path=r'.\images\2_2.png', display_name='lib_2')
    lib_3 = genai.upload_file(path=r'.\images\2_3.png', display_name='lib_3')
    lib_4 = genai.upload_file(path=r'.\images\2_4.png', display_name='lib_4')
    print("lib upload!")

    res2_1 = genai.upload_file(path=r'.\images\3_1.png', display_name='res2_1')
    res2_2 = genai.upload_file(path=r'.\images\3_2.png', display_name='res2_2')
    res2_3 = genai.upload_file(path=r'.\images\3_3.png', display_name='res2_3')
    res2_4 = genai.upload_file(path=r'.\images\3_4.png', display_name='res2_4')
    print("res2 upload!")
    """


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

    prompt_main_2 = """
    請告訴我「使用者輸入照片」是來自於哪一棟建築物? 輸出回答格式為一個 json 格式，例如 : '{建築物名稱 : 科學一館}'
    """

    """
    content = [prompt_SC1, 
            sc1_1, 
            sc1_2, 
            sc1_3, 
            prompt_lib,
            lib_1, 
            lib_2,
            lib_3,
            prompt_2_res,
            res2_1,
            res2_2,
            res2_3,
            prompt2, 
            lib_4, 
            prompt3]
    """

    content = [prompt_1]
    content.extend(image_list_1)
    content.extend([prompt_2])
    content.extend(image_list_2)
    content.extend([prompt_3])
    content.extend(image_list_3)
    content.extend([prompt_4])
    content.extend(image_list_4)
    content.extend([prompt_5])
    content.extend(image_list_5)
    content.extend([prompt_6])
    content.extend(image_list_6)
    content.extend([prompt_7])
    content.extend(image_list_7)
    content.extend([prompt_8])
    content.extend(image_list_8)
    content.extend([prompt_9])
    content.extend(image_list_9)
    content.extend([prompt_10])
    content.extend(image_list_10)

    content.extend([prompt_main_1])
    content.extend([genai.upload_file(path='input_img.jpg', display_name='sc1_1')])
    content.extend([prompt_main_2])

    response = model.generate_content(content)

    print(response.text)


def save_csv():

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")


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

    image_list_1 = list()
    image_list_2 = list()
    image_list_3 = list()
    image_list_4 = list()
    image_list_5 = list()
    image_list_6 = list()
    image_list_7 = list()
    image_list_8 = list()
    image_list_9 = list()
    image_list_10 = list()

    for file_name in os.listdir('data'):
        if file_name[0:2] == '10':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_10.append(the_uploaded_file.name)
            #file = genai.get_file(name=the_uploaded_file.name)
            #print(the_uploaded_file.name)
            #print(f"Retrieved file '{file.display_name}' as: {the_uploaded_file.uri}")
            print("upload 10 :", file_name)
            pass
        elif file_name[0] == '1':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_1.append(the_uploaded_file.name)
            print("upload 1 :", file_name)
            pass
        elif file_name[0] == '2':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_2.append(the_uploaded_file.name)
            print("upload 2 :", file_name)
            pass
        elif file_name[0] == '3':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_3.append(the_uploaded_file.name)
            print("upload 3 :", file_name)
            pass
        elif file_name[0] == '4':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_4.append(the_uploaded_file.name)
            print("upload 4 :", file_name)
            pass
        elif file_name[0] == '5':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_5.append(the_uploaded_file.name)
            print("upload 5 :", file_name)
            pass
        elif file_name[0] == '6':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_6.append(the_uploaded_file.name)
            print("upload 6 :", file_name)
            pass
        elif file_name[0] == '7':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_7.append(the_uploaded_file.name)
            print("upload 7 :", file_name)
            pass
        elif file_name[0] == '8':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_8.append(the_uploaded_file.name)
            print("upload 8 :", file_name)
            pass
        elif file_name[0] == '9':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_9.append(the_uploaded_file.name)
            print("upload 9 :", file_name)
            pass
    
    the_dict = {'1':image_list_1,
                '2':image_list_2,
                '3':image_list_3,
                '4':image_list_4,
                '5':image_list_5,
                '6':image_list_6,
                '7':image_list_7,
                '8':image_list_8,
                '9':image_list_9,
                '10':image_list_10}
    temp = pd.DataFrame(the_dict)
    print(temp)
    temp.to_csv('uploaded_name.csv', encoding='utf-8', index=False)

def save_csv_():

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")


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

    image_list_1 = list()
    image_list_2 = list()
    image_list_3 = list()
    image_list_4 = list()
    image_list_5 = list()
    image_list_6 = list()
    image_list_7 = list()
    image_list_8 = list()
    image_list_9 = list()
    image_list_10 = list()

    for file_name in os.listdir('data'):
        if file_name[0:2] == '10':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_10.append(the_uploaded_file.name)
            #file = genai.get_file(name=the_uploaded_file.name)
            #print(the_uploaded_file.name)
            #print(f"Retrieved file '{file.display_name}' as: {the_uploaded_file.uri}")
            print("upload 10 :", file_name)
            pass
        elif file_name[0] == '1':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_1.append(the_uploaded_file.name)
            print("upload 1 :", file_name)
            pass
        elif file_name[0] == '2':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_2.append(the_uploaded_file.name)
            print("upload 2 :", file_name)
            pass
        elif file_name[0] == '3':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_3.append(the_uploaded_file.name)
            print("upload 3 :", file_name)
            pass
        elif file_name[0] == '4':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_4.append(the_uploaded_file.name)
            print("upload 4 :", file_name)
            pass
        elif file_name[0] == '5':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_5.append(the_uploaded_file.name)
            print("upload 5 :", file_name)
            pass
        elif file_name[0] == '6':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_6.append(the_uploaded_file.name)
            print("upload 6 :", file_name)
            pass
        elif file_name[0] == '7':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_7.append(the_uploaded_file.name)
            print("upload 7 :", file_name)
            pass
        elif file_name[0] == '8':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_8.append(the_uploaded_file.name)
            print("upload 8 :", file_name)
            pass
        elif file_name[0] == '9':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_9.append(the_uploaded_file.name)
            print("upload 9 :", file_name)
            pass
    
    the_dict = {'1':image_list_1,
                '2':image_list_2,
                '3':image_list_3,
                '4':image_list_4,
                '5':image_list_5,
                '6':image_list_6,
                '7':image_list_7,
                '8':image_list_8,
                '9':image_list_9,
                '10':image_list_10}
    temp = pd.DataFrame(the_dict)
    print(temp)
    temp.to_csv('uploaded_name_.csv', encoding='utf-8', index=False)


def save_csv_240():

    genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")


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

    image_list_1 = list()
    image_list_2 = list()
    image_list_3 = list()
    image_list_4 = list()
    image_list_5 = list()
    image_list_6 = list()
    image_list_7 = list()
    image_list_8 = list()
    image_list_9 = list()
    image_list_10 = list()

    for file_name in os.listdir('data_240'):
        if file_name[0:2] == '10':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_10.append(the_uploaded_file.name)
            #file = genai.get_file(name=the_uploaded_file.name)
            #print(the_uploaded_file.name)
            #print(f"Retrieved file '{file.display_name}' as: {the_uploaded_file.uri}")
            print("upload 10 :", file_name)
            pass
        elif file_name[0] == '1':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_1.append(the_uploaded_file.name)
            print("upload 1 :", file_name)
            pass
        elif file_name[0] == '2':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_2.append(the_uploaded_file.name)
            print("upload 2 :", file_name)
            pass
        elif file_name[0] == '3':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_3.append(the_uploaded_file.name)
            print("upload 3 :", file_name)
            pass
        elif file_name[0] == '4':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_4.append(the_uploaded_file.name)
            print("upload 4 :", file_name)
            pass
        elif file_name[0] == '5':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_5.append(the_uploaded_file.name)
            print("upload 5 :", file_name)
            pass
        elif file_name[0] == '6':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_6.append(the_uploaded_file.name)
            print("upload 6 :", file_name)
            pass
        elif file_name[0] == '7':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_7.append(the_uploaded_file.name)
            print("upload 7 :", file_name)
            pass
        elif file_name[0] == '8':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_8.append(the_uploaded_file.name)
            print("upload 8 :", file_name)
            pass
        elif file_name[0] == '9':
            the_uploaded_file = genai.upload_file(path=os.path.join('data', file_name), display_name=file_name)
            image_list_9.append(the_uploaded_file.name)
            print("upload 9 :", file_name)
            pass
    
    the_dict = {'1':image_list_1,
                '2':image_list_2,
                '3':image_list_3,
                '4':image_list_4,
                '5':image_list_5,
                '6':image_list_6,
                '7':image_list_7,
                '8':image_list_8,
                '9':image_list_9,
                '10':image_list_10}
    temp = pd.DataFrame(the_dict)
    print(temp)
    temp.to_csv('uploaded_name_240.csv', encoding='utf-8', index=False)




if __name__ == '__main__':

    for i in range(11):
        if i == 0:
            continue
        the_input_image = PIL.Image.open(f'test_data/{i}.jfif')
        the_input_image_np = np.array(the_input_image)
    #building_classify(the_input_image_np)
    #save_csv()
    #genai.configure(api_key="AIzaSyDYf9O2CzW1HVxb4mkFq13YLx0qNo8oc2g")
    
    #file = genai.get_file(name='files/jhugt7go4he2')
    #model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    #response = model.generate_content([file, "Please describe the picture"])
    #print(response.text)

    #print(f"Retrieved file '{file.display_name}' as: {0}")
    #A = pd.read_csv("uploaded_name.csv")
    #print(A['10'][0])

        building_classify_faster(the_input_image_np)
