from io import BytesIO
from flask import Flask, jsonify, request
from text_analyzer import TextAnalyzer

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


@app.route('/emoji_usage')
def get_emoji_usage():
    chat0 = 'jessicaandnatalie_p54k8tywpw'
    chat1 = "nataliesuboc_3kprn6_mtg"
    chat2 = 'juliadeng_ceaz1qgcsg'
    chat3 = 'juliaandnatalie_ut8vdbynta'
    chat4 = 'up_d9qf1gvmwg'

    text_analyzer = TextAnalyzer()
    emoji_usage = text_analyzer.get_emoji_usage(chat0)
    return jsonify(emoji_usage)


if __name__ == "__main__":
    app.run(debug=True)