import os
import cloudconvert
import requests
import time
import json
from PIL import Image
from flask import Flask, session, render_template, flash, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from utilities import get_emotions
from pprint import pprint

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("API_KEY")
cc_api_key = os.getenv('CC_KEY')
secret_key = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)
# specify upload folder
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/'
app.config['SESSION_TYPE'] = 'filesystem'
# # secret key for session management
app.secret_key = secret_key

@app.route('/')
def index():
    return render_template('index.html')


def handle_hume(file_path):
    try:
        upload_url = "https://file.io"
        with open(file_path, "rb") as file:
            response = requests.post(upload_url, files={"file": file})
            uploaded_url = response.json()["link"]

        # Convert .heic or .heif to jpeg, start job
        # commented out for now, instead will enforce .png or .jpg submissions
        '''
        cloudconvert.configure(api_key=cc_api_key)

        job = cloudconvert.Job.create(payload={
            "tasks": {
                'import-my-file': {
                    'operation': 'import/url',
                    'url': uploaded_url
                },
                'convert-my-file': {
                    'operation': 'convert',
                    'input': 'import-my-file',
                    'output_format': 'png',
                    'some_other_option': 'value'
                },
                'export-my-file': {
                    'operation': 'export/url',
                    'input': 'convert-my-file'
                }
            }
        })
        # wait for job completion
        job = cloudconvert.Job.wait(id=job['id'])

        export_task = None

        #print('job:', json.dumps(job, indent=4)) to test job output
        # download output
        for task in job["tasks"]:
            if task.get("name") == "export-my-file" and task.get("status") == "finished":
                export_task = task

        print('exported task', export_task)
        file = export_task['result']['files'][0]
        image_to_submit = file['url']
        '''
        # Initialize HumeBatchClient
        client = HumeBatchClient(api_key)
        # Configuration for face processing
        config = FaceConfig()
        # Submit job using the local file path
 
        start_time = time.time()

        job = client.submit_job([uploaded_url], [config])
        # Wait for the job to complete
        job.await_complete()
        # Download predictions to a file
        print("Job completed with status: ", job.get_status())
        emotion_scores = []
        full_predictions = job.get_predictions()
        # print('full predictions', full_predictions)
        for source in full_predictions:
            predictions = source["results"]["predictions"]
            for prediction in predictions:
                face_predictions = prediction["models"]["face"]["grouped_predictions"]
                for face_prediction in face_predictions:
                    for frame in face_prediction["predictions"]:
                        emotion_scores = get_emotions(frame["emotions"])

        total_time = str((time.time() - start_time))
        print(total_time)
        return emotion_scores
    except Exception as e:
        # Log the exception or handle it accordingly
        print(f"Exception in handle_hume: {e}")
        return None

@app.route('/visualize_emotions')
def visualize_emotions():
    emotion_scores = session.pop('ret_emotion_scores', None)
    image_path = session.get('image_path', None)
    return render_template('visualize_emotions.html', emotion_scores=emotion_scores, image_path=image_path)


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
            file_path = os.path.join(app.root_path, 'static', imagename)
            image.save(file_path)
            
            # call to Hume API
            print('file path', file_path)
            ret_emotion_scores = handle_hume(file_path)
            print(ret_emotion_scores)
            # Store the emotion scores and image in the session
            session['ret_emotion_scores'] = ret_emotion_scores
            session['image_path'] = imagename

        return redirect(url_for('visualize_emotions'))
    else:
        # If it's a GET request, redirect to the index route
        return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)
