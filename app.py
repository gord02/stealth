from flask import Flask, render_template, redirect, url_for, request, make_response

import emailing
import db



app = Flask(__name__)


@app.route('/')
def home():
    # db.add_confirmation("hord@gmail.com")
    return render_template('home.html')

@app.route('/blogs/confirmation_success')
def success():
    return render_template('success.html')

@app.route('/blogs/confirmation_failure')
def failure():
    return render_template('failure.html')


@app.route('/blogs')
def blogs():
    return render_template('blog.html')


@app.route('/create-blog',  methods=['GET', 'POST'])
def post_blog():
    if request.method == "GET":
        return render_template('login.html')
    else:
        user = request.form['user']
        password = request.form['password']
        
        valid = db.valid_auth(user, password)
        if valid:
            return render_template('blog_form.html')
        else:
            return render_template('failed_login.html')

@app.route('/get-blog', methods=['POST'])
def capture_blog():
    title = request.form['title']
    name = request.form['name']
    content = request.form['content']
    db.add_blog(title, name, content)
    return redirect(url_for('post_blog'))


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    
    db.add_confirmation(email)
    
    # send confirmation email
    emailing.confirm_sub(email)
    return redirect(url_for('blogs'))

# get route, after validation, redirect to proper page
@app.route('/confirm/<email>')
def confirm(email):
    
    is_valid = db.check_confirmation(email)
    
    # redirect to confirmation to subscription page
    if is_valid:
        # add user to mailing list
        db.add_user(email)
        return redirect(url_for('success'))
    else:
        return redirect(url_for('failure'))
    
# get route, after validation, redirect to proper page
@app.route('/unsubscribe/<email>')
def unsubscribe(email):
    
    is_valid = db.unsubscribe(email)
    
    # redirect to confirmation to subscription page
    if is_valid:
        return redirect(url_for('success'))
    else:
        return redirect(url_for('failure'))

@app.route('/inquiry')
def quote():
    return render_template('quote.html')

@app.route('/catch-quote',  methods=['POST'])
def catch_quote():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    name =  first_name + " " + last_name 
    email = request.form['email']
    company = request.form['company']
    message = request.form['message']
    
    # call to emailing module to send email about quote
    emailing.quote_inquiry(name, email, company, message)
    
    return redirect(url_for('quote'))


@app.errorhandler(404)
def catch_all(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
