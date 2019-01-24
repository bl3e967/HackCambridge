# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 16:26:22 2019

@author: benwi
"""
import requests
# from IPython.display import HTML
# from PIL import Image
# from io import BytesIO


class FaceAPI:

    subscription_key = '6d1691bf159940679209d2d734d2e2e0'

    def __init__(self, face_list_id):
        self.api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0'
        self.face_list_id = face_list_id

    def create_new_face_list(self):
        """Create new FaceList"""
        face_list_create_api_url = self.api_url + '/facelists/' + self.face_list_id
        response = requests.put(face_list_create_api_url,
                                params={'faceListId': self.face_list_id},
                                headers={'Ocp-Apim-Subscription-Key': FaceAPI.subscription_key},
                                json={"name": self.face_list_id})
        #print(response.json())

    def find_face_in_image(self, path):
        """Find faces in an image"""
        image_binary = open(path, "rb")
        face_detect_api_url = self.api_url + '/detect'
        headers = {'Ocp-Apim-Subscription-Key': FaceAPI.subscription_key, 'content-type': 'application/octet-stream'}
        params = {'returnFaceId': 'true',
                  'returnFaceLandmarks': 'true',
                  'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,'
                                          'hair,makeup,occlusion,accessories,blur,exposure,noise'
                  }
        response = requests.post(face_detect_api_url, params=params, headers=headers, data=image_binary)
        faces_features = response.json()
        print(faces_features)
        return faces_features

    def allocate_to_face_list(self, path):
        """Allocate new faces to FaceList"""
        image_binary = open(path, "rb")

        new_face_to_face_list_api_url = self.api_url + '/facelists/' + self.face_list_id + '/persistedFaces'

        headers = {'Ocp-Apim-Subscription-Key': FaceAPI.subscription_key,
                   'content-type': 'application/octet-stream'
                   }
        params = {'faceListId': self.face_list_id}
        response = requests.post(new_face_to_face_list_api_url,
                                 params=params,
                                 headers=headers,
                                 data=image_binary)
        # {'persistedFaceId': 'e0f09159-9c0a-4603-b492-9310d747f25d'}
        return response.json()

    def find_similar_faces(self, face_features_dict)->list:
        """Face similarity"""
        if type(face_features_dict)==dict:
            face_id = face_features_dict['faceId']
        if type(face_features_dict)==list:
            face_id = face_features_dict[0]['faceId']
        face_similarity_api_url = self.api_url + '/findsimilars'
        headers = {'Ocp-Apim-Subscription-Key': FaceAPI.subscription_key}
        response = requests.post(face_similarity_api_url,
                                 headers=headers,
                                 json={'faceId': face_id,
                                       'faceListId': self.face_list_id,
                                       'mode': 'matchFace',
                                       'maxNumOfCandidatesReturned': 30}
                                 )
        similar_faces = response.json()  # Returns persistedFaceId and confidence for each response
        print("similar_faces ", similar_faces)

        return similar_faces    # list of dictionaries of face characteristics

    def get_face_list(self)-> list:
        """See what's in the FaceList"""

        get_face_list_api_url = self.api_url + '/facelists/' + self.face_list_id
        headers = {'Ocp-Apim-Subscription-Key': FaceAPI.subscription_key}
        params = {'faceListId': self.face_list_id}
        response = requests.get(get_face_list_api_url,
                                params=params,
                                headers=headers)

        print("response.json()2: ", response.json())
        return response.json()
    
    def delete_facelist(self):
        """Create new FaceList"""
        face_list_create_api_url = self.api_url + '/facelists/' + self.face_list_id
        
        response = requests.delete(face_list_create_api_url,
                                params={'faceListId': self.face_list_id},
                                headers={'Ocp-Apim-Subscription-Key': FaceAPI.subscription_key},
                                json={"name": self.face_list_id})
        #print(response.json())

##pass in some test ids and urls
#face_api = FaceAPI(face_list_id='19012019facelist')
#face_api.create_new_face_list()
#image_faces = face_api.find_face_in_image(path='test_img.jpg')
#
#for face_dict in image_faces:
#    face_api.allocate_to_face_list('test_img.jpg')
#    face_api.find_similar_faces(face_dict)
#
#face_api.get_face_list()
#
#image_data = 'test_img.jpg'
#
#faces = face_api.find_face_in_image(image_data)