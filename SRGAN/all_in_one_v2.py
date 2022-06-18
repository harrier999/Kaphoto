import time
import cv2
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage
from model import Generator

def denoise_and_upscale(IMAGE_NAME, UPSCALE_FACTOR = 4, DENOISE_STRENGTH = 2, TEST_MODE = True, MODEL_NAME = 'netG_epoch_4_100.pth'):
    
    #model
    model = Generator(UPSCALE_FACTOR).eval()
    if TEST_MODE:
        model.cuda()
        model.cpu()
        model.load_state_dict(torch.load('inference_model/' + MODEL_NAME)) #모델 경로
    else:
        model.load_state_dict(torch.load('inference_model/' + MODEL_NAME, map_location=lambda storage, loc: storage))

    #denoise
    path = './inference_input_image/' + IMAGE_NAME 

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    dst = cv2.fastNlMeansDenoisingColored(img,None,DENOISE_STRENGTH,DENOISE_STRENGTH,7,21)

    temp_image = './inference_de_image/' + 'de_' + str(DENOISE_STRENGTH) + '_' + IMAGE_NAME

    cv2.imwrite(temp_image, dst)

    #upscale
    # 
    image = dst
    image = Variable(ToTensor()(image), volatile=True).unsqueeze(0)
    if TEST_MODE:
        image = image.cuda()
        pass

    start = time.perf_counter()
    out = model(image)
    elapsed = (time.perf_counter() - start)
    print('cost' + str(elapsed) + 's')
    out_img = ToPILImage()(out[0].data.cpu())
    out_img.save("./inference_output_image/" + 'out_srf_' + str(UPSCALE_FACTOR) + '_' + IMAGE_NAME)

    return out_img

#denoise_and_upscale("Cat_Ori.jpg")
