from flask import render_template, jsonify, request
from spddwebsite import app
from PIL import Image
from spddwebsite.spdd_model import classify_plant
from spddwebsite.chatbot import get_response


class_name = ''

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/disease_detection")
def project():
    return render_template('disease_detection.html')


@app.route("/user_query", methods=['GET','POST'])
def user_query():
    context , gptresponse = get_response(prepareContext(class_name))
    if class_name:
        context = [{'role': 'system', 'content': f"""
            act as a Plant Pathologist and tell me more about {class_name}
            ***********************************************
            output: the output should take into consideration the following
            - make the output 100 words at most
            - use easy words to understand
        """}]
        if request.method == "GET":
            context, response = get_response(context)

        if request.method == "POST":
            if request.json['prompt']:
                prompt = request.json['prompt']
                context.append({'role': 'user', 'content': prompt})
                context, response = get_response(context)

        return  jsonify({"response" : response})
    else:
        return  jsonify({"response" : "No Plant Found!"})


@app.route("/team_member")
def about():
    return render_template('team_member.html')


@app.route("/resourses")
def resorce():
    return render_template('resourses.html')


@app.route("/datarespons", methods=['GET','POST'])
def response(): 
    print("hellllllllllo")
    global class_name
    image_file = request.files['image']
    outputs = classify_plant(image_file)
    print(outputs,"duhaaaa")

    if(outputs['healthy'] == False):
        outputs['healthy']='Sick'
    else:
        outputs['healthy']='Healthy'

    class_name = outputs['name']
    context , gptresponse = get_response(prepareContext(class_name))
   
    # print(gptresponse)
    response = { "name":  outputs['name'],
                "plant": outputs['plant'],
                "healthy": outputs['healthy'],
                "disease": outputs['disease'],
                "plant_probability": outputs['plant_probability'],
                "plant_info": gptresponse}
    
    return  jsonify(response)

def prepareContext(class_name):
	return [{'role': 'system', 'content': f"""
		act as a Plant Pathologist and tell me more about {class_name}
		***********************************************
		output: the output should take into consideration the following
		- make the output 100 words at most
		- use easy words to understand
	"""}]