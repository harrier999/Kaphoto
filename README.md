# Kaphoto
인공지능 기술을 이용해 사진의 화질을 개선합니다.

## AI model
SRGAN paper: Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network (https://arxiv.org/abs/1609.04802)
SRGAN refence code: https://github.com/leftthomas/SRGAN

## Training
### Dataset
- VOC2012
- Flicker2K
- DIV2K
- self-made Dataset 


### hyperparameter
- epochs: 100

# How to Run
## With Docker
```bash
docker-compose build
docker-compose up
```

## Without Docker
```bash
streamlit run frontend/frontend.py
python3 SRGAN/main.py
```
