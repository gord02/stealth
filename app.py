from flask import Flask, render_template, redirect, url_for, request, make_response

import emailing

app = Flask(__name__)


@app.route('/')
def home():
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

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    print("email: " + email)
    # generate custom key to verify email
    key = ""
    
    # function from emailing module
    emailing.confirm_sub(key, email)
    
    return redirect(url_for('blogs'))

# get route, after validation, redirect to proper page
@app.route('/confirm/<key>')
def confirm(key):
    
    # check validity of key, whether it has been used before or if it is expected key
    is_valid = True
    print("captured: " + key)
    
    
    # redirect to confirmation to subscription page
    if is_valid:
        
        # add user to mailing list
        
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
