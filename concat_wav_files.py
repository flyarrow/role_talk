import os
import random
import subprocess

def get_wav_files(folder):
    return sorted([f for f in os.listdir(folder) if f.endswith('.wav')])

def generate_silence(duration, output_path):
    command = [
        'ffmpeg', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono', '-t', str(duration), output_path
    ]
    subprocess.run(command, check=True)

def concat_wav_files(input_folder, output_wav_file, output_m4a_file):
    wav_files = get_wav_files(input_folder)
    temp_files = []

    for wav_file in wav_files:
        temp_files.append(os.path.join(input_folder, wav_file))
        silence_duration = random.uniform(0.5, 1.5)
        silence_file = os.path.join(input_folder, f'silence_{wav_file}')
        generate_silence(silence_duration, silence_file)
        temp_files.append(silence_file)

    # Remove the last silence file
    temp_files.pop()

    with open('file_list.txt', 'w') as f:
        for temp_file in temp_files:
            f.write(f"file '{temp_file}'\n")

    command = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', '-c', 'copy', output_wav_file
    ]
    subprocess.run(command, check=True)

    # Clean up temporary files
    os.remove('file_list.txt')
    for temp_file in temp_files:
        if 'silence_' in temp_file:
            os.remove(temp_file)

    # Convert wav to m4a
    command = [
        'ffmpeg', '-i', output_wav_file, '-c:a', 'aac', '-b:a', '192k', output_m4a_file
    ]
    subprocess.run(command, check=True)

# 主程序
if __name__ == "__main__":
    input_folder = 'out_wav'
    output_wav_file = 'out_cat_wav/cat_AB.wav'
    output_m4a_file = 'out_cat_wav/cat_AB.m4a'
    os.makedirs(os.path.dirname(output_wav_file), exist_ok=True)
    concat_wav_files(input_folder, output_wav_file, output_m4a_file)
    print(f"合并后的音频文件已保存: {output_wav_file}")
    print(f"转换后的音频文件已保存: {output_m4a_file}")