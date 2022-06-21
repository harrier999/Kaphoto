


import streamlit as st
import requests
from streamlit_cropper import st_cropper
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import io
import time
import argparse
from yaml import parse

parser = argparse.ArgumentParser(description="--docker=True/False, default=False")
docker_choices = ('True', 'Fasle')
parser.add_argument('--docker', choices=docker_choices, default='False', help="--docker=True/False, default=False")

args = parser.parse_args()

if args.docker=='False':
    backend = "http://localhost:8000/"
elif args.docker=='True':
    backend = "http://fastapit:8000/"

def convert_pil_image_to_byte_array(img):
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='JPEG', subsampling=0, quality=100)
    img_byte_array = img_byte_array.getvalue()
    return img_byte_array


def getData(img_file, option, option_denoise):
    server_url = backend + 'get_image' + option + '/' + 'option_denoise=' + option_denoise
    # m = MultipartEncoder(fields={"category": category, "file": ("filename", img_file, "image/jpeg")}) # category 추가시 충돌 버그
    
    m = MultipartEncoder(fields={"file": ("filename", img_file, "image/jpeg")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )

    return r

# title 설정
st.title('Kaphoto upscaling')

# warning 제거 (https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465)
st.set_option('deprecation.showfileUploaderEncoding', False)

#소제목 설정
st.header("사진 업로드")

#사이드바에서 crop에 사용될 기능 설정(업로드 파일 형식/테두리 색상/image 비율 고정)
img_file = st.file_uploader(label='', type=['jpg','jpeg'])
aspect_ratio = None

upload = ''
#이미지 업로드시 crop 기능 실행
if img_file:
    img = Image.open(img_file)
    new_width  = img.width
    new_height = int(new_width * img.height / img.width)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    img_col,crop_col = st.columns(2)
    
    with img_col:
        st.subheader('원본 사진')
        cropped_img = st_cropper(img, realtime_update=True, box_color='#000000',
                                    aspect_ratio=(3, 4))
    
    # crop된 이미지를 출력 
    with crop_col:
        st.subheader('편집된 사진')
        #cropped_img = cropped_img.resize((new_width, new_height), Image.ANTIALIAS)
        st.image(cropped_img)
        upload = st.button("업로드 완료")

# select ratio
option = st.selectbox('업스케일 비율을 선택해 주세요',('X2', 'X4', 'X8'))
option_denoise = st.selectbox('노이즈 감소 비율을 선택해 주세요', ('0', '1', '2', '3', '4'))

# 업로드 버튼을 누를 시 crop된 이미지를 확인, backend로 post 후에 image가 있는 dict를 받아옴
if upload:
    if cropped_img :
        with st.spinner('로딩중...'):
            cropped_img_bytearray = convert_pil_image_to_byte_array(cropped_img)
            img_np_array = cropped_img_bytearray
            # ConnectionError: HTTPConnectionPool 방지
            try:
                result = getData(img_np_array, option, option_denoise) 
                pass
            except:
                time.sleep(2)
                result = getData(img_np_array, option, option_denoise)
        upscale_image = Image.open(io.BytesIO(result.content)).convert("RGB")

        st.image(upscale_image, use_column_width=True)

    else:
        st.write("좌측에서 이미지를 넣어주세요.")



# 이후 추가될 기능

# # 업스케일 비율 선택 기능
# st.write('You selected:', x8)