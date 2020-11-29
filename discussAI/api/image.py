""" Azure OCR Processing done here """
import os
import sys
from io import BytesIO

import requests

os.environ['COMPUTER_VISION_ENDPOINT'] = 'https://dicussai.cognitiveservices.azure.com/'

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    SUBSCRIPTION_KEY = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print(f"\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n"
          "**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    END_POINT = os.environ['COMPUTER_VISION_ENDPOINT']

OCR_URL = END_POINT + "vision/v3.0/ocr"

def image_to_json(image_paths):
    """ Converting the image to JSON """
    json_arr = []
    bounded_top = -3

    for image_path in image_paths:
        # Read the image into a byte array
        response = requests.get(image_path)
        image_data = BytesIO(response.content)
        # Set Content-Type to octet-stream
        headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
                   'Content-Type': 'application/octet-stream'}
        params = {'language': 'unk'}
        # put the byte array into your post request
        response = requests.post(OCR_URL, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        analysis = response.json()

        # Extract the word bounding boxes and text.
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    if word_info['text'] == 'DEFINITION' or word_info['text'] == 'THEOREM':
                        word_infos.append(word_info)
                        bounded_top = int(word_info['boundingBox'].split(',')[1]) + 3
                    if int(word_info['boundingBox'].split(',')[1]) == bounded_top:
                        word_infos.append(word_info)

        json_arr.append([image_path, word_infos])
    # Create a new array
    new_arr = []
    page_count = 1

    for i in json_arr:
        sub_arr = []
        sub_arr.append(i[0])
        sub_arr.append(page_count)
        page_count += 1
        if i[1] != []:
            arr_pos = i[1][0]["boundingBox"].split(',')
            left_pos = int(arr_pos[0]) - 25
            top_pos = int(arr_pos[1])
            right_pos = left_pos + 1385
            bottom_pos = top_pos + 325
            sub_arr.append(left_pos)
            sub_arr.append(top_pos)
            sub_arr.append(right_pos)
            sub_arr.append(bottom_pos)
            sub_arr.append(i[1][0]["text"])

            str_counter = 1
            empty_str = ''
            while str_counter < len(i[1]):
                empty_str += i[1][str_counter]['text']
                if str_counter != len(i[1]) - 1:
                    empty_str += ' '
                str_counter += 1
            if empty_str != '':
                sub_arr.append(empty_str)
        new_arr.append(sub_arr)

    return new_arr
# More test cases
#print(image_to_json(['https://discussai.blob.core.windows.net/media/page1_77tCnWq.png',
#                     'https://discussai.blob.core.windows.net/media/page1_77tCnWq.png']))
