import os
import secrets
import requests
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from pprint import pprint

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)
# specify upload folder
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/image_uploads/'
app.config['SESSION_TYPE'] = 'filesystem'
# # secret key for session management
app.secret_key = secret_key

@app.route('/')
def index():
    return render_template('index.html')


def handle_hume(file_path):
    # Initialize HumeBatchClient
    client = HumeBatchClient(api_key)

    upload_url = "https://file.io"
    with open(file_path, "rb") as file:
        response = requests.post(upload_url, files={"file": file})
        uploaded_url = response.json()["link"]

    # Configuration for face processing
    config = FaceConfig()
    # Submit job using the local file path
    print(file_path)
    job = client.submit_job([uploaded_url], [config])
    # Wait for the job to complete
    job.await_complete()
    # Download predictions to a file
    print("Job completed with status: ", job.get_status())

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No image part')
            return redirect(url_for('index'))
        image = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if image.filename == '':
            flash('No selected image')
            return redirect(url_for('index'))
        if image:
            imagename = secure_filename(image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
            image.save(file_path)
            
            # call to Hume API
            handle_hume(file_path)

        print('end')
        return 'end'
    else:
        # If it's a GET request, redirect to the index route
        return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
