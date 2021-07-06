from django.shortcuts import render
import base64
import json
from datetime import datetime, date
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
import os
import shutil


class Transform(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        print(kwargs['reference'])
        ref_name = kwargs['reference']
        input_image = str(kwargs['input_image'])
        # print(input_image)
        img_data = base64.b64decode(input_image.split(',')[-1])
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs('./image/'+now+'/testA')
        with open('./image/'+now+'/testA/input.jpg', 'wb') as f:
            f.write(img_data)
        os.makedirs('./results/step1_release_model/'+now)
        # os.makedirs('./results/step1_release_model/shoes/test_480/images')
        os.system(f'python -u ./step1/test.py  --only_fakephoto --sp_attention 1 --load_size 128 --crop_size 128 --results_dir ./results/step1_release_model/{now} --input_nc 1 --output_nc 1 --epoch 480 --dataroot ./image/{now} --name shoes --checkpoints_dir ./experiments/step1/step1_release_model/model/ --gpu_ids -1')
        os.rename(f'./results/step1_release_model/{now}/shoes/test_480/images', f'./results/step1_release_model/{now}/shoes/test_480/testA')
        os.makedirs('./results/step2_release_model/' + now)
        os.makedirs(f'./results/step1_release_model/{now}/shoes/test_480/testB')
        shutil.copyfile(f'./datasets/shoes_step2/reference/{ref_name}', f'./results/step1_release_model/{now}/shoes/test_480/testB/{ref_name}')
        os.system(f'python -u ./step2/test.py  --only_fakephoto --netG resnet_12blocks --load_size 128 --crop_size 128 --results_dir ./results/step2_release_model/{now} --input_nc 3 --output_nc 3 --epoch 290 --dataroot ./results/step1_release_model/{now}/shoes/test_480 --name shoes --checkpoints_dir ./experiments/step2/step2_release_model/model/ --gpu_ids -1')
        f = open(f'./results/step2_release_model/{now}/shoes/test_290/images/input_fake_B_fake_B.png', 'rb')
        output_data = base64.b64encode(f.read())
        f.close()
        return JsonResponse({'status': 200, 'output_image': str(output_data)})
