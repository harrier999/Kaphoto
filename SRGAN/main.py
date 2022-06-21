from fastapi import FastAPI, File
import uvicorn
from starlette.responses import Response
import io
from PIL import Image

from all_in_one_v2 import denoise_and_upscale
import cv2


app = FastAPI()


@app.post("/")
def read_root():
	'''
	backend의 root 경로로 request가 들어올 시 dict를 return
	Parameters: None
	return : 
	dict(dtype=dict) : name과 test 이미지 경로가 들어있는 dict를 반환. 
 	({"name"(dtype=str): "Backend/img_test"(dtype=str)}
  	
   	※현재 demo test를 위해 img 파일의 형식을 img_test로 강제로 바꿔서 추가했으며 이후 이 부분은 삭제될 예정 
	'''
	return {"name": "Backend/img_test"}


@app.post("/getSimilarFashionX2/{option_denoise}")
def get_similar_fashion(option_denoise, file: bytes = File(...)):
	img = io.BytesIO(file)
	img = Image.open(img)
	img = img.convert("RGB")
	img.save('./inference_input_image/' + 'test_image.jpg')
	image = denoise_and_upscale(IMAGE_NAME='test_image.jpg', UPSCALE_FACTOR = 2, DENOISE_STRENGTH = option_denoise, TEST_MODE = True, MODEL_NAME = 'netG_epoch_2_100.pth')
	
	bytes_io = io.BytesIO()
	image.save(bytes_io, format="PNG")

	return Response(bytes_io.getvalue(), media_type="image/png")
	
@app.post("/getSimilarFashionX4/{option_denoise}")
def get_similar_fashion(option_denoise, file: bytes = File(...)):
	img = io.BytesIO(file)
	img = Image.open(img)
	img = img.convert("RGB")
	img.save('./inference_input_image/' + 'test_image.jpg')
	image = denoise_and_upscale(IMAGE_NAME='test_image.jpg', UPSCALE_FACTOR = 4, DENOISE_STRENGTH = option_denoise	, TEST_MODE = True, MODEL_NAME = 'netG_epoch_4_100.pth')
	
	bytes_io = io.BytesIO()
	image.save(bytes_io, format="PNG")

	return Response(bytes_io.getvalue(), media_type="image/png")
	
	
@app.post("/getSimilarFashionX8/{option_denoise}")
def get_similar_fashion(option_denoise, file: bytes = File(...)):
	img = io.BytesIO(file)
	img = Image.open(img)
	img = img.convert("RGB")
	img.save('./inference_input_image/' + 'test_image.jpg')
	image = denoise_and_upscale(IMAGE_NAME='test_image.jpg', UPSCALE_FACTOR = 8, DENOISE_STRENGTH = option_denoise, TEST_MODE = True, MODEL_NAME = 'netG_epoch_8_100.pth')
	
	bytes_io = io.BytesIO()
	image.save(bytes_io, format="PNG")

	return Response(bytes_io.getvalue(), media_type="image/png")
	
	





# 앞으로 기능이 추가되면 사용될 예시
# @app.get("/users/{user_id}")
# def get_user(user_id):
#     return {"user_id":user_id}

if __name__ == '__main__':
	uvicorn.run("main:app", host="0.0.0.0", port = 8000, reload=True) 