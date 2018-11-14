from flask import Flask, render_template, jsonify, request

import subprocess

app = Flask(__name__)
model_process = None

@app.route('/translate', methods=['POST'])
def translate():
    global model_process
    original = request.form['original']
    model_process.stdin.write(original + "\n")
    output = model_process.stdout.readline()
    return render_template("home.html", o=original, t=output)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    model_process = subprocess.Popen(['python2', 'script.py'], cwd='shakespearize/code/main', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    model_process.stdout.readline() # Wait for the 'Model is loaded' line to print
    print('Model has been successfully loaded.')
    app.run(debug=True, threaded=True)