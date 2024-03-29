import os
import time

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


mongo_pass = os.environ.get('mongoDBpass')
db_name = "stealth"
collection_name = "mailing"

uri = f"mongodb+srv://gordonh:{mongo_pass}@cluster0.ki54dtd.mongodb.net/?retryWrites=true&w=majority"

def valid_auth(user, password):
    BLOG_AUTH_USER = os.environ.get('BLOG_AUTH_USER')
    BLOG_AUTH_PASSWORD = os.environ.get('BLOG_AUTH_PASSWORD') 
    if BLOG_AUTH_USER == user and BLOG_AUTH_PASSWORD == password:
        return True
    return False

def check():
    print(uri)
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        admin_db = client.admin
        server_info = admin_db.command("serverStatus")
        # Extract the version information
        mongodb_version = server_info['version']
        print("MongoDB Server Version:", mongodb_version)
       

    except Exception as e:
        print("failed to create user with error: "+ e)

def add_blog(title, name, content):
    blog = {
        "title": title,
        "name": name, 
        "content": content
    }
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mydb = client[db_name]
        blogs = mydb["blogs"]
        blogs.insert_one(blog)

    except Exception as e:
        print("failed to add blog: "+ e)
 

def add_confirmation(email):
    user = {
        "email": email,
        "ttl": time.time()
    }

    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mydb = client[db_name]
        mailing = mydb[collection_name]
        mailing.insert_one(user)

    except Exception as e:
        print("failed to create user with error: "+ e)
        
def check_confirmation(user_email):
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mydb = client[db_name]
        mailing = mydb[collection_name]
        res = mailing.find_one({"email": user_email})
        mailing.delete_one({"email": user_email})
        time_sent = res['ttl']
        curr_time = time.time()
        
        if( int(curr_time - time_sent) < 86400):
            return True

    except Exception as e:
        print("failed to find user with error: "+ e)
        return False
    
    return False       

def remove_confirm(user_email):
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mydb = client[db_name]
        mailing = mydb["mailing"]
        return mailing.delete_one({"email": user_email})

    except Exception as e:
        print("failed to find user with error: "+ e)
        return False
    
# remove_confirm("hord@gmail.com")

def add_user(email):
    user = {
        "email": email,
    }

    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mydb = client[db_name]
        blog_list = mydb["blog_list"]
        blog_list.insert_one(user)

    except Exception as e:
        print("failed to create user for blog list: "+ e)

def unsubscribe(user_email):
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mydb = client[db_name]
        blog_list = mydb["blog_list"]
        return blog_list.delete_one({"email": user_email})

    except Exception as e:
        print("failed to find user with error: "+ e)
        return False
    

def get_mailing_list():
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mydb = client[db_name]
        blog_list = mydb["blog_list"]
        users = []
        documents = blog_list.find()
        for d in documents:
            users.append(d['email'])
        return users

    except Exception as e:
        print("failed to get mailing list: "+ e)
        return []
    
