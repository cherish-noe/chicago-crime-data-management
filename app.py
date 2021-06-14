from flask import Flask, render_template, request,url_for, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
import os
import pymongo
import bcrypt
uri = "mongodb+srv://403project:403projectpsw@cdm-1msul.gcp.mongodb.net/test"

client = MongoClient(uri)
client.stats
Chicago_crime = client.Chicago_crime
test_data= Chicago_crime.crime_2015_present
users=Chicago_crime.users
app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        user_nm=session['username']
        return render_template('Dashboard.html',user_nm=user_nm)

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))

    return 'Invalid username/password combination'

@app.route('/logout', methods=['GET'])
def logout():
    return render_template('login.html')

@app.route('/dashboard')
#@login_required
def dashboard():
    user_nm=session['username']
    return render_template('Dashboard.html',user_nm=user_nm)

@app.route("/insert", methods=['get', 'post'])
def insert():   
    if "Case_Number" not in request.form:
        return render_template("Insert2.html")
    else:
        ID = str(request.form['ID'])
        Case_Number = str(request.form['Case_Number'])
        Date = str(request.form['Date'])
        Block = str(request.form['Block'])
        Primary_Type = str(request.form['Primary_Type'])
        Description = str(request.form['Description'])
        
        Arrest = str(request.form['Arrest'])
        Domestic = str(request.form['Domestic'])
        
        Community_Area = str(request.form['Community_Area'])
        Year = str(request.form['Year'])
        test_data.insert_one({"ID":ID, "Case Number":Case_Number, "Date":Date,"Block":Block, "Primary Type":Primary_Type, "Description":Description, "Arrest":Arrest, "Domestic":Domestic,  "Community Area":Community_Area, "Year":Year})
        return render_template("Insert2.html")

@app.route("/list")
def lists ():
    #Display the all Tasks

    c_2015_present = test_data.find()
    a1="active"
    return render_template('Crime_lists.html',a1=a1,test_data=c_2015_present)

@app.route("/")
def tasks():
    c_2015_present = test_data.find
    a2="active"
    return render_template('Crime_lists.html',a2=a2,test_data=c_2015_present)


@app.route("/remove")
def remove ():
    #Deleting a Task with various references
    key=request.values.get("_id")
    test_data.remove({"_id":ObjectId(key)})
    return redirect('/list')

@app.route("/update")
def update ():
    _id=request.values.get("_id")
    task=test_data.find({"_id":ObjectId(_id)})
    return render_template('Update.html', tasks=task)

@app.route("/action3", methods=['POST'])
def action3 ():
    #Updating a Task with various references
    ID=request.values.get("ID")
    Case_Number=request.values.get("Case_Number")
    Date=request.values.get("Date")
    Block=request.values.get("Block")
    Primary_Type=request.values.get("Primary_Type")
    Description=request.values.get("Description")
    Location_Description=request.values.get("Location_Description")
    Arrest=request.values.get("Arrest")
    Domestic=request.values.get("Domestic")
    District=request.values.get("District")
    Beat=request.values.get("Beat")
    Community_Area=request.values.get("Community_Area")
    Year=request.values.get("Year")
    id=request.values.get("_id")
    test_data.update({"_id":ObjectId(id)}, {'$set':{ "ID":ID, "Case Number":Case_Number, "Date":Date,"Block":Block, "Primary Type":Primary_Type, "Description":Description, "Location Description":Location_Description, "Arrest":Arrest, "Domestic":Domestic, "Beat":Beat, "District":District,  "Community Area":Community_Area,  "Year":Year }})
    return redirect("/list")

@app.route("/search", methods=['GET'])
def search():
    #Searching a Task with various references

    key=request.values.get("key")
    refer=request.values.get("refer")
    if(refer=="id"):
        try:
            todos_l = test_data.find({refer:ObjectId(key)})
            if not todos_l:
                return render_template('Crime_lists.html',a2=a2,test_data=todos_l,error="No such ObjectId is present")
        except InvalidId as err:
            pass
            return render_template('Crime_lists.html',a2=a2,test_data=todos_l,error="Invalid ObjectId format given")
    else:
        todos_l = test_data.find({refer:key})
    return render_template('Search_result.html',test_data=todos_l)

@app.route("/graph", methods=['GET'])
def graph():
    return render_template('Show_graph.html')


if __name__=="__main__":
    env = os.environ.get('APP_ENV', 'development')
    port = int(os.environ.get('PORT', 5000))
    debug = False if env == 'production' else True
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=port, debug=debug)
