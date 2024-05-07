from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
    jsonify,
)
from werkzeug.utils import secure_filename
from PIL import Image
import os

# To install the Python SDK, use this CLI command:
# pip install google-cloud-aiplatform

import vertexai
from vertexai.generative_models import GenerativeModel, Image

PROJECT_ID = "gemini-api-quickstart"
REGION = "us-central1"  # e.g. us-central1

vertexai.init(project=PROJECT_ID, location=REGION)
        

# The rate limits are low on this model, so you might need to switch to `gemini-pro`
model = GenerativeModel('gemini-1.5-pro-preview-0409')

app = Flask(__name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = 'uploads' 
if not os.path.exists(UPLOAD_FOLDER):
    # Create the directory
    os.makedirs(UPLOAD_FOLDER)
    print(f"Directory '{UPLOAD_FOLDER}' created.")
else:
    print(f"Directory '{UPLOAD_FOLDER}' already exists.")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

chat_session = model.start_chat(history=[])
next_message = ""
next_image = ""

def allowed_file(filename):
    """Returns if a filename is supported via its extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    global next_image

    if "file" not in request.files:
        return jsonify(success=False, message="No file part")

    file = request.files["file"]

    if file.filename == "":
        return jsonify(success=False, message="No selected file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(file_path)  # Save file to disk

        try:
            # Load the image from the saved file
            next_image = Image.load_from_file(file_path)
        except Exception as e:
            return jsonify(success=False, message=f"Failed to load image file: {str(e)}")

        return jsonify(
            success=True,
            message="File uploaded successfully and added to the conversation",
            filename=filename,
        )
    return jsonify(success=False, message="File type not allowed")

@app.route("/", methods=["GET"])
def index():
    """Renders the main homepage for the app"""
    return render_template("index.html", chat_history=chat_session.history)

@app.route("/chat", methods=["POST"])
def chat():
    """Takes in the message the user wants to send to the Gemini API, saves it"""
    global next_message
    next_message = request.json["message"]
    print(chat_session.history)

    return jsonify(success=True)

@app.route("/stream", methods=["GET"])
def stream():
    """Streams the response from the serve for both multi-modal and plain text requests"""
    def generate():
        global next_message
        global next_image
        assistant_response_content = ""

        if next_image != "":
            # This only works with `gemini-1.5-pro-latest`
            response = chat_session.send_message([next_message, next_image], stream=True)
            next_image = ""
        else:
            response = chat_session.send_message(next_message, stream=True)
            next_message = ""
        
        for chunk in response:
            assistant_response_content += chunk.text
            yield f"data: {chunk.text}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)