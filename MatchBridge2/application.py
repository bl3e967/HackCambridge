import sys
import numpy as np
sys.path.insert(0,'./Interface')

import faceAPI
from smooth_orange_juice import SmoothOrangeJuice
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
app = Flask(__name__)


dummy_data = [
    {
        'team_member': 'Alex Darch',
        'position': 'HTML bish',
        'date_updated': '2018/01/19'
    },
    {
        'team_member': 'Ben Williams',
        'position': 'Team Leader',
        'date_updated': '2018/01/19'
    },
    {
        'team_member': 'John Clay',
        'position': 'No idea',
        'date_updated': '2018/01/19'
    },
    {
        'team_member': 'Ben Lee',
        'position': 'ML monkey',
        'date_updated': '2018/01/19'
    }
]

image_data = {'image_src': "../static/images/test_img.jpg"}
# Need some way of allocating the top 6 images at any given point
image1 = {'image_src': ""}
image2 = {'image_src': ""}
image3 = {'image_src': ""}
image4 = {'image_src': ""}
image5 = {'image_src': ""}
image6 = {'image_src': ""}


@app.route("/")
@app.route("/home")
def hello():
	return render_template('home.html', image_data=image_data, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6)

@app.route('/switchimage', methods=['GET', 'POST'])
def switchimage():
    if request.method == 'POST' or request.method=='GET':
        # Allocate image accordingly
        image_data = {'image_src': "../static/images/image347.jpg"}
        return render_template('home.html', image_data=image_data,image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6)

@app.route("/about")
def about():
    return render_template('about.html', posts=dummy_data)


if  __name__ =='__main__':
    app.run(debug=True)

