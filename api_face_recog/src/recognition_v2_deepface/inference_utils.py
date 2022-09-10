from deepface.DeepFace import build_model,represent
import warnings
warnings.filterwarnings("ignore")

import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import time
import numpy as np
import pandas as pd
from tqdm import tqdm
import pickle
from deepface.detectors import FaceDetector
import cv2
from deepface.basemodels import Boosting
from deepface.commons import functions, distance as dst

import tensorflow as tf
tf_version = int(tf.__version__.split(".")[0])
if tf_version == 2:
	import logging
	tf.get_logger().setLevel(logging.ERROR)


	
def find(img_path, db_path, model_name ='VGG-Face', distance_metric = 'cosine', model = None, enforce_detection = True, detector_backend = 'opencv', align = True, prog_bar = True, normalization = 'base', silent=False):

	"""
	This function applies verification several times and find an identity in a database

	Parameters:
		img_path: exact image path, numpy array (BGR) or based64 encoded image. If you are going to find several identities, then you should pass img_path as array instead of calling find function in a for loop. e.g. img_path = ["img1.jpg", "img2.jpg"]

		db_path (string): You should store some .jpg files in a folder and pass the exact folder path to this.

		model_name (string): VGG-Face, Facenet, OpenFace, DeepFace, DeepID, Dlib or Ensemble

		distance_metric (string): cosine, euclidean, euclidean_l2

		model: built deepface model. A face recognition models are built in every call of find function. You can pass pre-built models to speed the function up.

			model = DeepFace.build_model('VGG-Face')

		enforce_detection (boolean): The function throws exception if a face could not be detected. Set this to True if you don't want to get exception. This might be convenient for low resolution images.

		detector_backend (string): set face detector backend as retinaface, mtcnn, opencv, ssd or dlib

		prog_bar (boolean): enable/disable a progress bar

	Returns:
		This function returns pandas data frame. If a list of images is passed to img_path, then it will return list of pandas data frame.
	"""

	tic = time.time()

	img_paths, bulkProcess = functions.initialize_input(img_path)

	#-------------------------------

	if os.path.isdir(db_path) == True:

		if model == None:

			if model_name == 'Ensemble':
				if not silent: print("Ensemble learning enabled")
				models = Boosting.loadModel()

			else: #model is not ensemble
				model = build_model(model_name)
				models = {}
				models[model_name] = model

		else: #model != None
			if not silent: print("Already built model is passed")

			if model_name == 'Ensemble':
				Boosting.validate_model(model)
				models = model.copy()
			else:
				models = {}
				models[model_name] = model

		#---------------------------------------

		if model_name == 'Ensemble':
			model_names = ['VGG-Face', 'Facenet', 'OpenFace', 'DeepFace']
			metric_names = ['cosine', 'euclidean', 'euclidean_l2']
		elif model_name != 'Ensemble':
			model_names = []; metric_names = []
			model_names.append(model_name)
			metric_names.append(distance_metric)

		#---------------------------------------

		file_name = "representations_%s.pkl" % (model_name)
		file_name = file_name.replace("-", "_").lower()

		f = open(db_path+'/'+file_name, 'rb')
		representations = pickle.load(f)
		if not silent: print("There are ", len(representations)," representations found in ",file_name)

		#----------------------------
		#now, we got representations for facial database

		if model_name != 'Ensemble':
			df = pd.DataFrame(representations, columns = ["identity", "%s_representation" % (model_name)])
		else: #ensemble learning

			columns = ['identity']
			[columns.append('%s_representation' % i) for i in model_names]

			df = pd.DataFrame(representations, columns = columns)

		df_base = df.copy() #df will be filtered in each img. we will restore it for the next item.

		resp_obj = []
		results = []
		global_pbar = tqdm(range(0, len(img_paths)), desc='Analyzing', disable = prog_bar)
		detector = FaceDetector.build_model(detector_backend) #set opencv, ssd, dlib, mtcnn or retinaface

		for j in global_pbar:
			img_path = img_paths[j]
			# find faces in image
			img = cv2.imread(img_path)			
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			faces = FaceDetector.detect_faces(detector, detector_backend, img)

			for face in faces:
				print(face[1])
				detected_face = {}
				# print(face[0])
				
				#find representation for passed image

				for j in model_names:
					custom_model = models[j]

					target_representation = represent(img_path = face[0]
						, model_name = model_name, model = custom_model
						, enforce_detection = False, detector_backend = detector_backend
						, align = align
						, normalization = normalization
						)

					for k in metric_names:
						distances = []
						for index, instance in df.iterrows():
							source_representation = instance["%s_representation" % (j)]

							if k == 'cosine':
								distance = dst.findCosineDistance(source_representation, target_representation)
							elif k == 'euclidean':
								distance = dst.findEuclideanDistance(source_representation, target_representation)
							elif k == 'euclidean_l2':
								distance = dst.findEuclideanDistance(dst.l2_normalize(source_representation), dst.l2_normalize(target_representation))

							distances.append(distance)

						#---------------------------

						if model_name == 'Ensemble' and j == 'OpenFace' and k == 'euclidean':
							continue
						else:
							df["%s_%s" % (j, k)] = distances

							if model_name != 'Ensemble':
								threshold = dst.findThreshold(j, k)
								print("threshold: ",threshold)
								df = df.drop(columns = ["%s_representation" % (j)])
								df = df[df["%s_%s" % (j, k)] <= threshold]

								df = df.sort_values(by = ["%s_%s" % (j, k)], ascending=True).reset_index(drop=True)
								df_dict = df.to_dict('records')
								if df_dict and not detected_face:
									class_name = "Unknown"
									if "\\" in df_dict[0]['identity']:
										class_name = df_dict[0]['identity'].split("\\")[-1]
									else:
										class_name = df_dict[0]['identity'].split("/")[-1]
									if "/" in class_name:
										class_name = class_name.split("/")[0]
									detected_face = {
										"class":class_name,
										"bbox":{
											"x_min":face[1][0],
											"y_min":face[1][1],
											"x_max":face[1][2]+face[1][0],
											"y_max":face[1][3]+face[1][1],
										},
										"match":True
									}
									results.append(detected_face)
									resp_obj.append(df)
								df = df_base.copy() #restore df for the next iteration

				#----------------------------------

				if model_name == 'Ensemble':

					feature_names = []
					for j in model_names:
						for k in metric_names:
							if model_name == 'Ensemble' and j == 'OpenFace' and k == 'euclidean':
								continue
							else:
								feature = '%s_%s' % (j, k)
								feature_names.append(feature)

					#print(df.head())

					x = df[feature_names].values

					#--------------------------------------

					boosted_tree = Boosting.build_gbm()

					y = boosted_tree.predict(x)

					verified_labels = []; scores = []
					for i in y:
						verified = np.argmax(i) == 1
						score = i[np.argmax(i)]

						verified_labels.append(verified)
						scores.append(score)

					df['verified'] = verified_labels
					df['score'] = scores

					df = df[df.verified == True]
					#df = df[df.score > 0.99] #confidence score
					df = df.sort_values(by = ["score"], ascending=False).reset_index(drop=True)
					df = df[['identity', 'verified', 'score']]

					resp_obj.append(df)
					df = df_base.copy() #restore df for the next iteration

				#----------------------------------

		toc = time.time()

		if not silent: print("find function lasts ",toc-tic," seconds")

		if len(resp_obj) == 1:
			return resp_obj[0],results

		return resp_obj,results

	else:
		raise ValueError("Passed db_path does not exist!")

	return None