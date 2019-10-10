from flask import Flask, render_template, redirect, request, session
from mysqlconnection import connectToMySQL
from datetime import datetime

app = Flask(__name__)

app.secret_key = "shhhhhhh"

@app.route('/')
def toUsers():
    return redirect('/users/')

@app.route('/users/')
def users():
    mysql = connectToMySQL('semi-restful_users')	        
    friends = mysql.query_db('SELECT * FROM friends;')  
   
    
    return render_template("index.html", all_friends = friends)

@app.route('/users/new')
def create():
    return render_template("newuser.html")

@app.route('/users/addfriend', methods=['POST'])
def update():
    mysql = connectToMySQL('semi-restful_users')
    # friends = mysql.query_db('SELECT * FROM friends;')  

    query = "INSERT INTO friends (first_name, last_name, email) VALUES (%(fn)s, %(ln)s, %(em)s);"

    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["femail"]
    }

    new_friend_id = mysql.query_db(query, data)
    print(new_friend_id)
    return redirect("/users/" + str(new_friend_id))



@app.route('/users/<user_id>')
def show(user_id):
    mysql = connectToMySQL('semi-restful_users')

    query = "SELECT * FROM friends WHERE friend_id = %(idf)s"
    data = {
        "idf": user_id
    }

    user = mysql.query_db(query, data)
    print(user)
   
    cd = user[0]['created_at']
    cdf = datetime.strftime(cd, '%B %d %Y %I:%M %p')
    md = user[0]['updated_at']
    mdf = datetime.strftime(md, '%B %d %Y %I:%M %p')

    friend_info = {
        'id' : user[0]['friend_id'],
        'firstname' : user[0]['first_name'],
        'lastname' : user[0]['last_name'],
        'email' : user[0]['email'],
        'created_at' : cdf,
        'updated_at': mdf
    }

    return render_template('create.html', cfriend = friend_info)


@app.route('/users/<user_id>/edit')
def edit(user_id):
    mysql = connectToMySQL('semi-restful_users')
   

    query = "SELECT * FROM friends WHERE friend_id = %(idf)s"

    data = {
        "idf": user_id
    }
 
    user = mysql.query_db(query, data)

    friend_info = {
        'id' : user[0]['friend_id'],
        'firstname': user[0]['first_name'],
        'lastname': user[0]['last_name'],
        'email' : user[0]['email'],
        'created_at': user[0]['created_at'],
        'updated_at': user[0]['updated_at']
    }

    return render_template('edit.html', efriend = friend_info)

@app.route('/edituser', methods = ['POST'])
def edituser():

    query = "UPDATE friends SET first_name = %(firstname)s, last_name = %(lastname)s, email = %(email)s WHERE friend_id = %(ide)s"

    data = {
        "ide" : request.form["eid"],
        "firstname" : request.form["efname"],
        "lastname" : request.form["elname"],
        "email" : request.form["eemail"]
    }

    mysql = connectToMySQL('semi-restful_users')
    mysql.query_db(query, data)

    return redirect('/users/')

@app.route('/users/<user_id>/delete/')
def deleteuser(user_id):

    query = "DELETE FROM friends WHERE friend_id = %(idd)s"

    data = {
        "idd": user_id
    }

    mysql= connectToMySQL('semi-restful_users')
    user = mysql.query_db(query, data)
    return redirect('/users/')


    



if __name__ == "__main__":
    app.run(debug=True)