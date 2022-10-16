from io import BytesIO
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/members")
def members():
    return {"members": ["Natalie", "Jessica", "Harmony", "Vivian", "Harmony2", "Jungkook"]}

@app.route('/upload', methods=['POST'])
def upload_file():
    d = {}
    try:
        message_folder = request.files['message_folder']
        folder_name = message_folder.filename
        print(f"Uploading folder {folder_name}")
        message_folder_bytes = message_folder.read()
        content = BytesIO(message_folder_bytes).readlines()
        print(content)
        d['status'] = 1
    except Exception as e:
        print(f"Couldn't upload folder {e}")
        d['status'] = 0

    return jsonify(d)

if __name__ == "__main__":
    app.run(debug=True)