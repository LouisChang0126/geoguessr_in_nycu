def get_prompt_from_file(file_path):
    f = open(file_path, "r")
    prompt = f.read()
    f.close()
    return prompt


def get_static_shots(n=5):#"training data" must fix
    few_shots = [
        {   'country': 'Brazil', 'path': '../dataset/train/h0/bra/-35.55282434676715_-5.142338177092807_h0_p0_f90.jpg'}, 
        {   'country': 'Australia', 'path': '../dataset/train/h0/aus/145.9034775926887_-35.57502509281566_h0_p0_f90.jpg'},
        {   'country': 'China','path': '../dataset/train/h90/chn/104.895851_26.53953_h90_p0_f90.jpg'},
        {   'country': 'United States', 'path': '../dataset/train/h90/usa/-94.32801821093504_46.41032019311709_h90_p0_f90.jpg'},
        {   'country': 'Russia', 'path': '../dataset/train/h0/rus/38.47268937998618_56.49643063880474_h0_p0_f90.jpg'}]
    
    return few_shots[:n]


def get_prompt():
    basic_prompt = 'You are an expert in geography, terrain, landscapes, flora, fauna, and more. Using expert reasoning and thinking skills, please predict which country this photo was taken. Your answer should be in a JSON format, for example: {"country": your_answer}. If you are not sure, please try your best to guess one country and only return {"country": "unknown"} if there is nothing.'
    must_prompt = 'You are an expert in geography, terrain, landscapes, flora, fauna, and more. Using expert reasoning and thinking skills, please predict which country this photo was taken. Your answer should be in a JSON format, for example: {"country": your_answer}. Please try your best to guess one country. You must provide a country name.'
    must_NYCU_prompt = 'You are a navigation and geography expert at Yangming Jiaotong University. Please use your professional reasoning and thinking skills to predict which building at National Yang-Ming Chiao Tung University this photo is taken of, and provide satellite coordinates. Your answer should be in JSON format, for example: {"building": your_answer, "direction": direction_of_camera}. Please try your best to guess a building and a direction. You must provide the building name and direction of the shot.'
    return {
        "must_NYCU_prompt": must_NYCU_prompt,
        "basic_prompt": basic_prompt,
        "must_prompt": must_prompt,
    }
