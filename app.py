from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return 'hello world'
    # return render_template('index.html')


@app.route('/blogs')
def blogs():
    return ' blogs'

@app.route('/subscribe')
def subscribe():
    return redirect(url_for('/blogs'))


@app.route('/inquiry')
def quote():
    return 'form page'

@app.route('/catch-quote')
def catch_quote():
    return redirect(url_for('/inquiry'))


@app.route('/<path>')
def catch_all(path):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
