import os
import json
import torch
from PIL import Image
import torchvision.transforms as transforms
from transformers import ResNetForImageClassification


current_path  = os.getcwd()
model_file = "model.pth"
classes_file = 'data.json'

model_path = os.path.join(current_path, 'spddwebsite/', model_file)
classes_path = os.path.join(current_path, 'spddwebsite/' , classes_file)

def prepare_model():
	model_state_dict = torch.load(model_path, map_location=torch.device('cpu'))
	model = ResNetForImageClassification.from_pretrained('microsoft/resnet-152')
	model.load_state_dict(model_state_dict)
	return model

def get_tensor(image_file):
	# Get image as RGB 
	image = Image.open(image_file).convert("RGB")
	# Define a transform to resize the image to 64x64
	predict_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()])
    # Convert the image to a tensor
	img_tensor = predict_transform(image).unsqueeze(dim=0)
	return img_tensor

def get_predict(model, image):
	outputs = model(image)
	_, predicted = torch.max(outputs.logits, 1)
	return [outputs, predicted]

# Find the probability of the predicted class
def get_prop(outputs_, predicted_):
	probabilities = torch.softmax(outputs_.logits, dim=1)
	probability = probabilities[0][predicted_]
	return probability

def get_percent_prop(probability__):
	percent_prop = probability__.item()
	percent_prop *= 100
	return "{:.2f}".format(percent_prop)

def get_data():
	# Open the JSON file for reading
	with open(classes_path, 'r') as json_file:
	    data = json.load(json_file)
	return data

def classify_plant(image):
	img_tensor = get_tensor(image)
	spdd_model = prepare_model()
	outputs, predicted = get_predict(spdd_model, img_tensor)
	probability_ = get_prop(outputs, predicted)
	data = get_data()
	response={
        "name": data[str(int(predicted))]['name'],
        "plant": data[str(int(predicted))]['plant'],
        "healthy": data[str(int(predicted))]['healthy'],
        "disease": data[str(int(predicted))]['disease'],
        "plant_probability": get_percent_prop(probability_),	
		}
	return response
