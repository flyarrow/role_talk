import sys
from start_api import start_api
from config import ROLE_A, ROLE_B, ROLE_A_CONFIG, ROLE_B_CONFIG, TXT_FOLDER, WAV_FOLDER, TEST_MODE

# 确保API已启动
try:
    start_api()
except SystemExit:
    print("API启动失败，程序退出。")
    sys.exit(1)

import requests
import json
import os
import time

# API服务地址
API_URL = "http://127.0.0.1:9880"

def set_sovits_model(weights_path):
    response = requests.get(f"{API_URL}/set_sovits_weights?weights_path={weights_path}")
    if response.status_code == 200:
        print("SoVITS模型设置成功")
    else:
        print(f"SoVITS模型设置失败: {response.text}")

def set_gpt_model(weights_path):
    response = requests.get(f"{API_URL}/set_gpt_weights?weights_path={weights_path}")
    if response.status_code == 200:
        print("GPT模型设置成功")
    else:
        print(f"GPT模型设置失败: {response.text}")

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def text_to_speech(text, reference_audio, reference_text):
    payload = {
        "text": text,
        "text_lang": "zh",  # 假设输入文本是中文
        "ref_audio_path": reference_audio,
        "prompt_text": reference_text,
        "prompt_lang": "zh",  # 假设提示文本也是中文
        "top_k": 5,
        "top_p": 1,
        "temperature": 1,
        "text_split_method": "cut5",
        "batch_size": 1,
        "batch_threshold": 0.75,
        "split_bucket": True,
        "speed_factor": 1.0,
        "streaming_mode": False,
        "seed": -1,
        "parallel_infer": True,
        "repetition_penalty": 1.35
    }
    
    while True:
        response = requests.post(f"{API_URL}/tts", json=payload)
        if response.status_code == 200:
            return response.content
        else:
            print(f"语音转换失败: {response.text}")
            print("重试中...")
            continue

def save_audio_file(audio_data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as file:
        file.write(audio_data)
    print(f"音频文件已保存: {output_path}")

def set_role(role_config):
    set_sovits_model(role_config["sovits_weights"])
    set_gpt_model(role_config["gpt_weights"])
    return role_config["reference_audio"], role_config["reference_text"]

def process_files(test_mode=False):
    txt_folder = TXT_FOLDER
    wav_folder = WAV_FOLDER
    processed_roles = set()
    
    for file_name in os.listdir(txt_folder):
        if file_name.endswith(".txt"):
            role = file_name.split('-')[1][0]  # 获取角色标识
            
            # 如果是测试模式且已处理过该角色,则跳过
            if test_mode and role in processed_roles:
                continue
            
            if role == 'A':
                reference_audio, reference_text = set_role(ROLE_A_CONFIG)
            elif role == 'B':
                reference_audio, reference_text = set_role(ROLE_B_CONFIG)
            else:
                print(f"未知角色: {role}")
                continue

            # 读取文本内容
            input_text = read_text_file(os.path.join(txt_folder, file_name))

            # 调用API进行语音转换
            audio_data = text_to_speech(input_text, reference_audio, reference_text)

            # 保存输出文件
            if audio_data:
                output_path = os.path.join(wav_folder, file_name.replace(".txt", ".wav"))
                save_audio_file(audio_data, output_path)
            else:
                print(f"无法生成音频文件: {file_name}")
            
            # 如果是测试模式,标记该角色已处理
            if test_mode:
                processed_roles.add(role)
            
            # 如果是测试模式且已处理两个角色,则退出循环
            if test_mode and len(processed_roles) == 2:
                break

    print("所有文件处理完成")

# 主程序
if __name__ == "__main__":
    # 设置测试模式,True为测试模式(只处理A和B各一个文件),False为正常模式(处理所有文件)
    process_files(TEST_MODE)
    
    print("处理完成，API服务仍在运行。")