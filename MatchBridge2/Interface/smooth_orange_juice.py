import numpy as np
from faceAPI import FaceAPI
import pandas as pd
import os

class SmoothOrangeJuice():
    def __init__(self): 
         # face list
        self._facelistname = 'facelist_5'
        self.fa = FaceAPI(self._facelistname)
        self.fa.delete_facelist()
        self.fa.create_new_face_list()
        # running flag
        self.Running = True

        # initialise similarity average container
        self.similarity_average = pd.DataFrame(data={'PersistedFaceId':[], 'ImagePath':[], 'Confidence':[],})
        # main image dataset
        self.dataset_dir = './images/main'
        self.dataset = self.get_dataset(init=False)
        # initial image dataset
        self.init_dir = './images/initial'
        self.initial_size = 30
        self.image_set = self.get_dataset(init=True)
        
        # counter for number of images that have been considered
        self.count = 0 
        # initialise dictionary from filename to faceid
        self.file_to_face = {}       

    def get_dataset(self, init=False):
        # Get list of images in directory
        if init is False:
            files = os.listdir(self.dataset_dir)
            root = self.dataset_dir

        if init is True: 
            files = os.listdir(self.init_dir)
            root = self.init_dir
        
        container = [None]*len(files)
        
        for i,f in enumerate(files): 
            # save filename into dataset container
            container[i] = f
            path = root + '/' + f
            # load the faces in the image to facelist for main dataset
            if init is False:
                persisted_face_id = self.fa.allocate_to_face_list(path)
            # initialise the whole dataset with pfaceid, path and confidence
                to_append = pd.DataFrame(
                    [[persisted_face_id['persistedFaceId'], f, 0.0]], 
                    columns = ['PersistedFaceId','ImagePath','Confidence']
                    )
                self.similarity_average = (
                    self.similarity_average.append(to_append, ignore_index=True)
                    )
                print(self.similarity_average)
        return container

    def update_similarity_average(self, image, response, init=False):
        '''
        Function to get similarity scores for images in the dataset

        Args: 
            image: image dataframe

        Returns: 
            confidence: An array of confidence values
        '''
        if isinstance(image, pd.DataFrame):
            image_name = image.loc[image.Confidence==image.Confidence.max()].ImagePath.iloc[0]
        if isinstance(image, str):
            image_name = image

        if init is False: 
            path = self.dataset_dir + '/' + image_name
        else: 
            path = self.init_dir + '/' + image_name
        # Detect faces in image
        faces = self.fa.find_face_in_image(path)
        # Find similar faces
        self.fa.find_similar_faces(faces)
        # Input new face data into facelist
        if init is False:
            self.fa.allocate_to_face_list(path)
        # get similarities
        similar_faces = self.fa.find_similar_faces(faces)
        
        for f in similar_faces: 
            # Find row where persistedFaceId is, and update the confidence
            self.similarity_average.loc[
                self.similarity_average.PersistedFaceId == f['persistedFaceId'],
                'Confidence'
                ] += response*f['confidence']
        return None

    def get_best_image(self):
        '''
        Rank the faces and output the fact id of the best face
        Args: 
            face_dict: dictionary with keys faceid, similarity, confidence and 
            array of top ten face_id, similarity and confidence scores as values.
        Returns: 
            best_face_id: The face id corresponding to the best ranking
        '''
        # Get 7 dataframe rows with largest confidence values
        top_images = self.similarity_average.nlargest(7, 'Confidence')
        return top_images
    
    def send_image_to_console(self, image):
        a = np.random.choice([-1,1])
        print('send image to console')
        print('receive input')
        return a

    def initialisation_run(self):
        # array of images to use for initial average calculation
        for i in range(len(self.image_set)):
            image = self.image_set[i]
            # receive a +1 for YES, -1 for NO from user response
            response = self.send_image_to_console(image)
            self.update_similarity_average(image, response, init=True)
        
        print("Initialisation finished")
        # self.Running is set true/false
        return None

    def main_run(self):    
        while len(self.similarity_average) > 0: 
            # get top 7 best images from the dataset and remove the used image
            image = self.get_best_image()
            # Clean up our list of faces to prevent reusing ones used before
            self.similarity_average = self.similarity_average.loc[
                self.similarity_average.Confidence!=self.similarity_average.Confidence.max()
                ]
            response = self.send_image_to_console(image)
            self.fa.get_face_list()
            self.update_similarity_average(image, response)
            
        print("Ran out of images to give")
        self.fa.delete_facelist()
        return None
            
if __name__ == "__main__":
    prog = SmoothOrangeJuice()
    prog.initialisation_run()
    prog.main_run()