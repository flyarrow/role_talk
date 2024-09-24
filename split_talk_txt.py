import re
import os
from config import ROLE_A, ROLE_B, INPUT_FILE, OUTPUT_DIR

def split_dialogue(input_file, output_dir):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式分割对话
    pattern = rf'({ROLE_A}：|{ROLE_B}：)'
    parts = re.split(pattern, content)
    
    # 初始化计数器和当前说话者
    count = 1
    current_speaker = None

    # 处理每个部分
    for part in parts:
        if part == f'{ROLE_A}：':
            current_speaker = 'A'
        elif part == f'{ROLE_B}：':
            current_speaker = 'B'
        elif part.strip() and current_speaker:
            # 确定文件名
            filename = f'{count:03d}-{current_speaker}.txt'
            file_path = os.path.join(output_dir, filename)
            count += 1

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(part.strip())

            print(f'已创建文件: {filename}')

# 使用函数
split_dialogue(INPUT_FILE, OUTPUT_DIR)
