from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    print('post route')
    if 'image' in request.files:
        image = request.files['image']
        # Replace the following logic with your API call using the image file
        # For demonstration, just returning a success message
        return jsonify({'message': 'Image uploaded successfully'})
    else:
        return jsonify({'error': 'No image file received'})

if __name__ == '__main__':
    app.run(debug=True)
