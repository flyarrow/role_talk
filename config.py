# 角色设置
ROLE_A = "Alice"
ROLE_B = "张律师"

# 角色配置
ROLE_A_CONFIG = {
    "sovits_weights": "SoVITS_weights/yz-fz_e8_s464.pth",
    "gpt_weights": "GPT_weights/yz-fz-e15.ckpt",
    "reference_audio": "/Users/xiaohanchen/Downloads/GPT-SoVITS_proj/yz_rd_opt/tmp/vocal_source03.wav_0000387200_0000538560.wav",
    "reference_text": "遇到那个人之前，你的世界仿佛只有一种颜色。"
}

ROLE_B_CONFIG = {
    "sovits_weights": "SoVITS_weights/czy02_e8_s224.pth",
    "gpt_weights": "GPT_weights/czy02-e15.ckpt",
    "reference_audio": "/Users/xiaohanchen/Downloads/czy_music/tmp/source_czy_02.mp3_0003209920_0003507840.wav",
    "reference_text": "任何一个从现代穿越过来的，接受过九年义务教育的人，都可以在这两千多年以前的战国末期。"
}

# 文件路径设置
INPUT_FILE = "talk1.txt"
OUTPUT_DIR = "out_txt"

# 文件夹路径配置
TXT_FOLDER = "out_txt"
WAV_FOLDER = "out_wav"

# 测试模式设置
# 设置测试模式,True为测试模式(只处理A和B各一个文件),False为正常模式(处理所有文件)
TEST_MODE = False