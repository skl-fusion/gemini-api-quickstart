# Gemini API Quickstart - Python (But for Europeans)

This repository was forked from [gemini-api-quickstart](https://github.com/logankilpatrick/gemini-api-quickstart) and migrated to the Vertex AI SDK to allow for use by Europeans, due to regional restrictions on the Gemini API. This repository contains a simple Python Flask App, designed to get you started building with Gemini's multi-modal capabilities. The app comes with a basic UI and a Flask backend.

<img width="1271" alt="Screenshot 2024-05-07 at 7 42 28 AM" src="https://github.com/logankilpatrick/gemini-api-quickstart/assets/35577566/156ae3e0-cffa-47a3-8a71-1bded78c4632">

## Basic request

To send your first API request to Gemini with the [Vertex AI SDK for Python](https://github.com/googleapis/python-aiplatform), make sure you have the right dependencies installed (see installation steps below) and then run the following code:

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Image

PROJECT_ID = "gemini-api-quickstart"
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)

model = GenerativeModel('gemini-1.5-pro-preview-0409')

chat = model.start_chat(history=[])
response = chat.send_message("In one sentence, explain how AI works to a child.")
# Note that the chat object is temporarily stateful, as you send messages and get responses, you can 
# see the history changing by doing `chat.history`.

print(response.text)
```

## Setup

1. If you don’t have Python installed, install it [from Python.org](https://www.python.org/downloads/).

2. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository.

3. Create a new virtual environment:

   - macOS:

     ```bash
     $ python -m venv venv
     $ . venv/bin/activate
     ```

   - Windows:
     ```cmd
     > python -m venv venv
     > .\venv\Scripts\activate
     ```

4. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

5. Log in to Gcloud:

   ```bash
   $ gcloud auth application-default login
   ```

6. Run the app:

```bash
$ flask run
```

You should now be able to access the app from your browser at the following URL: [http://localhost:5000](http://localhost:5000)!

#### Attribution

This repo includes code that was forked from [another repo made by Logan Kilpatick](https://github.com/openai/openai-quickstart-python), under an MIT license. All copyright for the work remains with Logan Kilpatrick. My contributions were strictly limited to following the [migration guide provided by Google](https://cloud.google.com/vertex-ai/generative-ai/docs/migrate/migrate-google-ai).