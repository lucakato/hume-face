import os
import secrets
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

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        print('in POST if block')
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No image part')
            return redirect(url_for('index'))
        image = request.files['image']
        print('after getting image')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if image.filename == '':
            flash('No selected image')
            return redirect(url_for('index'))
        if image:
            print('before secure image')
            imagename = secure_filename(image.filename)
            print('before save')
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
            #return redirect(url_for('download_file', name=filename))
            # call to Hume API
            print('before hume call')
            client = HumeBatchClient(api_key)
            config = FaceConfig()
            print('before job submit')
            job = client.submit_job(image, [config])
            predictions = job.get_predictions()
            pprint(predictions)
        
        print('end')
        return 'end'
    else:
        # If it's a GET request, redirect to the index route
        return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
