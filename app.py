from groq import Groq
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os

os.environ['API_KEY'] = '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'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = 'kevin2009' 
app.config['SESSION_TYPE'] = 'filesystem' 

db = SQLAlchemy(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

login_manager = LoginManager(app)

app.app_context().push()
with app.app_context():
    db.drop_all()
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):

    return Users.query.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/interpreter')
def interpreter():
    return render_template('interpreter.html')

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/museum')
def museum():
    return render_template('museum.html')

@app.route('/process', methods=["POST"])
def process(): 
    file = request.files['file']
    if file.filename == '':
        return 'no file selected'
    if file:
        folder = os.path.join("static", "library") 
        path = os.path.join(folder, file.filename)
        file.save(path)
        client = Groq(api_key=os.environ.get("API_KEY"))
        completion1 = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Convey the emotions, motive and thinking behind this image. I want an emotional response, not technical terms. I also want to know what the author must have been thinking/feeling while making this image. I also want to know if there is any historical significance behind this image"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (request.host_url + 'static/library/' + file.filename).replace(" ", "%20")
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        completion2 = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is one tag that can describe this image ( answer in one word )"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (request.host_url + 'static/library/' + file.filename).replace(" ", "%20")
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        interpretation = completion1.choices[0].message.content
        tags = completion2.choices[0].message.content
        print(interpretation)
        print(tags)
        return jsonify({
            "interpretation":interpretation,
            "tags":tags,
            "image_path":"/static/library/" +file.filename
        })
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host ="0.0.0.0", port = 10000, debug=False)