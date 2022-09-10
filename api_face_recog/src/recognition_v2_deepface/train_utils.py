import warnings
warnings.filterwarnings("ignore")

import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from os import path
from tqdm import tqdm
import pickle
from deepface.basemodels import Boosting
from deepface.DeepFace import build_model,represent

def update_database(db_path,trained_model_path, model_name ='VGG-Face', distance_metric = 'cosine', model = None, enforce_detection = True, detector_backend = 'opencv', align = True, prog_bar = True, normalization = 'base', silent=False):

	if os.path.isdir(db_path) == True:

		# Load or build model
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

		#find representations for db images
		employees = []
		# for r, d, f in os.walk(db_path): # r=root, d=directories, f = files
		# 		for file in f:
		# 			if ('.jpg' in file.lower()) or ('.png' in file.lower()):
		# 				exact_path = r + "/" + file
		# 				employees.append(exact_path)
		
		for f in os.listdir(db_path):
			if ('.jpg' in f.lower()) or ('.png' in f.lower()) or ('.jpeg' in f.lower()):
				exact_path = db_path + "/" + f
				employees.append(exact_path)
		
		print("employees: ",employees[0])

		if len(employees) == 0:
			raise ValueError("There is no image in ", db_path," folder! Validate .jpg or .png files exist in this path.")
		
		# generate representations
		representations = []
		pbar = tqdm(range(0,len(employees)), desc='Finding representations', disable = prog_bar)

		#for employee in employees:
		for index in pbar:
			employee = employees[index]

			instance = []
			instance.append(employee)

			for j in model_names:
				custom_model = models[j]

				representation = represent(img_path = employee
					, model_name = model_name, model = custom_model
					, enforce_detection = False, detector_backend = detector_backend
					, align = align
					, normalization = normalization
					)

				instance.append(representation)

			#-------------------------------

			representations.append(instance)
			
		# if path.exists(trained_model_path+file_name):
		# 	os.remove(trained_model_path+file_name)

		prev_representations = []
		if os.path.exists(os.path.join(trained_model_path,file_name)):
			with open(os.path.join(trained_model_path,file_name),'rb+') as f:			
				prev_representations = pickle.load(f)

		with open(os.path.join(trained_model_path,file_name),'wb') as f:
			# print(representations)
			combined_data = prev_representations
			for x in representations:
				combined_data.append(x)
			pickle.dump(combined_data, f)

		if not silent: print("Representations stored in ",trained_model_path,"/",file_name," file. This file has been updated!")
	
	else:
		raise ValueError("Passed db_path does not exist!")