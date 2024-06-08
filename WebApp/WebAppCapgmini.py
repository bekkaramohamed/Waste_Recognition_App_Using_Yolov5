import glob
import shutil
from PIL import Image
from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_command', methods=['POST'])
def run_command():
    image = request.files['image']
    image_path = os.path.join(os.getcwd(), 'images_a_detectee', 'image.jpg')
    image.save(image_path)

    yolov5_dir = os.path.join(os.getcwd(), 'yolov5')
    os.chdir(yolov5_dir)
    command = f'python3 detect.py --weights best.pt --source {image_path}'
    subprocess.call(command, shell=True)

    # Find the latest directory created in runs/detect
    list_of_dirs = [d for d in os.scandir('./runs/detect') if d.is_dir()]
    latest_dir = max(list_of_dirs, key=lambda x: x.stat().st_ctime)
    latest_name = os.path.basename(latest_dir)

    # Specify the source and destination paths for the detected image
    src_path = os.path.join(yolov5_dir, 'runs', 'detect', latest_name, 'image.jpg')
    dst_path = os.path.join(os.getcwd(), '..', 'images_detectee', 'image.jpg')

    # Copy the detected image to the destination
    shutil.copy(src_path, dst_path)
    img = Image.open(dst_path)
    img.show()
    
    os.chdir('..')
    return render_template('index.html')

@app.route('/run_live', methods=['GET'])
def run_live():
    yolov5_dir = os.path.join(os.getcwd(), 'yolov5')
    os.chdir(yolov5_dir)
    current_directory = os.getcwd()
    print("Le répertoire courant est:", current_directory)
    import pickle


    command = f'python3 detect.py --weights best.pt --source 0'
    p = subprocess.Popen(command, shell=True)

    os.chdir('..')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
