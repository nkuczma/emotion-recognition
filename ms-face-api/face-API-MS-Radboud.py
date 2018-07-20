import requests
import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime

subscription_key = 'your-subscription-key'
assert subscription_key

face_api_url = 'your-api-url'

headers = { 
        'Ocp-Apim-Subscription-Key': subscription_key, 
        'Content-type': 'application/octet-stream' 
        }

params = {
    'returnFaceId': 'true',
    'returnFaceAttributes': 'emotion',
}

filedirectory = 'your/directory'

imgFiles = [f for f in listdir(filedirectory) if isfile(join(filedirectory, f))]


listt = []
indexes = []
dictEmotion = {
        'angry': 'anger',
        'contemptuous': 'contempt',
        'disgusted': 'disgust',
        'fearful': 'fear',
        'happy': 'happiness',
        'neutral': 'neutral',
        'sad': 'sadness',
        'surprised': 'surprise'
        }


for img in imgFiles:
    
    if ((img.split("_")[0]).split("d")[1])!="000" and ((img.split("_")[0]).split("d")[1])!="180" : 
        indexes.append(img)
        img_filename = filedirectory + img
        with open(img_filename, 'rb') as f:
            img_data = f.read()
        response = requests.post(face_api_url, params=params, headers=headers, data=img_data)
        faces = response.json()
        emotionFromFile = img.split("_")[4]
        emotionFromApi = faces[0]['faceAttributes']['emotion']
        maxEmotion = max(emotionFromApi, key=lambda k: emotionFromApi[k])
        wasTrueEncoded = True if (maxEmotion == dictEmotion.get(emotionFromFile)) else False
        error = 1 - faces[0]['faceAttributes']['emotion'][dictEmotion.get(emotionFromFile)] 
        listt.append({
                'name': img,
                'angle': img.split("_")[0].split("d")[1],
                'position': img.split("_")[5].split(".")[0],
                'emotion': img.split("_")[4],
                'person': img.split("_")[2] + "_" + img.split("_")[3],
                'anger': faces[0]['faceAttributes']['emotion']['anger'],
                'contempt': faces[0]['faceAttributes']['emotion']['contempt'],
                'disgust': faces[0]['faceAttributes']['emotion']['disgust'],
                'fear': faces[0]['faceAttributes']['emotion']['fear'],
                'happiness': faces[0]['faceAttributes']['emotion']['happiness'],
                'neutral': faces[0]['faceAttributes']['emotion']['neutral'],
                'sadness': faces[0]['faceAttributes']['emotion']['sadness'],
                'surprise': faces[0]['faceAttributes']['emotion']['surprise'],
                'emotionFromApi': maxEmotion,
                'wasTrueEncoded': wasTrueEncoded,
                'error': error
                })
        
res = pd.DataFrame(listt, index=indexes)
col_order = ['name','angle','position','emotion','person','anger','contempt','disgust','fear','happiness','neutral','sadness','surprise','emotionFromApi','wasTrueEncoded', 'error']
res.to_csv('ms_face_api_result_radboud.csv', encoding='utf-8', index=False, columns=col_order)

