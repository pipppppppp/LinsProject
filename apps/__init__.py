from flask import Flask, Blueprint, render_template, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template(
        template_name_or_list='pages/index.html'
    )