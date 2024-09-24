#!/bin/bash

# 激活 Conda 环境，使用你确认的 Conda 安装路径
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate GPTSoVits  # 替换为你的虚拟环境名称

# 切换到 GPT-SoVITS 的目录
cd /Users/xiaohanchen/GPT-SoVITS

# 启动 API 服务
python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
