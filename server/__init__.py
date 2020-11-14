from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def unknown_faces():
    return render_template('unknown_faces.html.jinja', crop_size=100)
