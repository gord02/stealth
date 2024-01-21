from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/blogs')
def blogs():
    return render_template('blog.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    print("email: " + email)
    return redirect(url_for('blogs'))


@app.route('/inquiry')
def quote():
    return render_template('quote.html')

@app.route('/catch-quote',  methods=['POST'])
def catch_quote():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    email = request.form['email']
    company = request.form['company']
    message = request.form['message']
    return redirect(url_for('quote'))


@app.route('/<path>')
def catch_all(path):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
