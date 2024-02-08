from flask import Flask, render_template

app = Flask(__name__) # referencing this file

@app.route('/')

def index():
    return 'hello world'


if __name__ == '__main__':
    app.run(debug=True)

    