import streamlit as st
from pymongo import MongoClient

if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "username" not in st.session_state:
    st.session_state['username'] = ''
@st.cache_resource()
def init_connection():
    return MongoClient(
        "mongodb+srv://"
        + st.secrets.mongo.db_username
        + ":"
        + st.secrets.mongo.db_pswd
        + "@"
        + st.secrets.mongo.cluster_name
        + ".mhyxv.mongodb.net/?retryWrites=true&w=majority"
    )


client = init_connection()
db = client.chatbot


def get_users():
    items = db.users.find()  
    items = list(items)
    return items


def add_user(username, password):
    new_user = db.users.insert_one({"username": username ,"password" : password})
    return new_user


def check_credentials(username, password):
    data = get_users()
    for entry in data:
        if entry["username"] == username and entry["password"] == password:
            return True  # Found a matching username and password
    return False

if(st.session_state.auth == False):
    page = st.sidebar.radio("Select an action:", ["Login", "Signup"])
if(st.session_state.auth == False):
    if page == "Signup":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        signup_button = st.button("Signup")

        if signup_button:
            if check_credentials(username, password):
                st.toast("User Already Exists")
                
            else:
                new_user = add_user(username, password)
                st.toast("User " + username + " Added")
            username =""
            password =""

    elif page == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if check_credentials(username, password):
                st.session_state.auth = True
                st.session_state.username = username
                st.toast("Logged in successfully")
                st.write("Navigate to home page to utilize the chatbot")
            else:
                st.toast("Invalid username or password")
            username =""
            password =""