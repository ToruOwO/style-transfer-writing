from flask import Flask, render_template, jsonify, request
from shakespearize.code.main.script import demo

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    original = request.form['original']
    output = demo(original)
    print(original)
    print(output)
    return render_template("home.html", o=original, t=output)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)