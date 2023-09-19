from numpy import argmax
from keras.utils import load_img, img_to_array
from keras.models import load_model
from flask import Flask, render_template, request
from base64 import b64decode
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('main.html')

def load_image(filename):
    img = load_img(filename, color_mode="grayscale", target_size=(28, 28))
    img = img_to_array(img)
    img = img.reshape(1, 28, 28, 1)
    img = img.astype('float32')
    img = img / 255.0
    return img

@app.route('/recognize', methods=['GET', 'POST'])
def identify():
    if request.method == 'POST':
        imgData = request.form["img"]
        tempImg = Image.open(BytesIO(b64decode(imgData.split(',')[1])))
        tempImg.save("canvas.png")
        img = load_image("canvas.png")
        model = load_model('final_model')
        prediction = model.predict(img)[0]
        confidence = max(prediction)
        guess = argmax(prediction)
        
    return "Guess: " + str(guess) + ", " + str(round(confidence * 100, 2)) + "%"

if __name__ == "__main__":
    app.run(debug = True)