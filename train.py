from flask import Flask, render_template,request,redirect


app = Flask(__name__)

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signin/upload')
def upload():
    return render_template('upload.html')




if __name__ == "__main__":
    app.run(debug=True, port=8002)