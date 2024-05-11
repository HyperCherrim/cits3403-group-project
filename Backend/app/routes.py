from flask import render_template
from flask_login import current_user, login_user
from app import app
#@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Debug User'}
    availableGroups = [{"unit":"CITS2200: Data Structures and Algorithms"}, 
                       {"unit":"CITS1003: Introduction to Cybersecurity"}, 
                       {"unit":"MATH1721: Mathematics Foundations: Methods"}] # Populate this later once options for new tags are added
    return render_template("index.html",title="Study Group maker",user=user,groups=availableGroups)

@app.route('/making_request')
def making_request():
    return render_template("making_request.html",title="making request")

@app.route('/password_reset')
def password_reset():
    return render_template("password_reset.html",title="reset password")

@app.route('/responding_request')
def responding_request():
    return render_template("responding_request.html",title="respond to request")

@app.route('/user_creation')
def user_creation():
    return render_template("user_creation.html",title="account")

@app.route('/user_login')
def user_login():
    return render_template("user_login.html",title="login")

@app.route('/')
@app.route('/user/<username>')
#@login_required
def user_page(username = "TEST"):
    user = "TEMPORARY"
    groups = [
    "The Quantum Thinkers",
    "Code Crusaders",
    "Logic Lords",
    "Data Wizards",
    "The Algorithm Avengers",
    "Mind Mages",
    "Syntax Sorcerers",
    "Cyber Sages",
    "The Binary Brotherhood",
    "Machine Learning Maestros",
    "Tech Titans",
    "Computational Conquerors",
    "Digital Dynamos",
    "Programming Pioneers",
    "Innovation Inc.",
    "Byte Brigade",
    "Pixel Prodigies",
    "Cognitive Collective",
    "Byte Busters",
    "The Debugging Dream Team",
    "Analytical Architects",
    "Numeric Nomads",
    "The Insight Institute",
    "Logic Legends",
    "Data Doyens",
    "Coding Connoisseurs",
    "The Analytics Alliance",
    "Tech Trailblazers",
    "The Algorithm Assembly",
    "Digital Dreamers",
    "The Cybernetic Collective",
    "Infinite Innovators",
    "Binary Brainiacs",
    "Tech Transformers",
    "Hacker Heroes",
    "Byte Bandits",
    "The Data Dynasty",
    "Coders' Coalition",
    "The Logic League",
    "Innovation Invincibles",
    "Tech Titans",
    "Data Drifters",
    "The Quantum Quest",
    "Code Crafters",
    "Binary Builders",
    "The Tech Tribe",
    "Data Dream Team",
    "Logic Luminaries",
    "Digital Divas",
    "Code Cadets",
    "The Algorithm Association",
    "Data Dynamo",
    "Code Commanders",
    "Byte Bosses",
    "The Cyber Squad",
    "Innovation Icons",
    "Tech Titans",
    "Data Daredevils",
    "The Code Collective",
    "Logic Leaders",
    "The Binary Brigade",
    "Tech Trailblazers",
    "The Algorithmic Alliance",
    "Data Dynamos",
    "Coding Conquerors",
    "The Logic Legion",
    "The Tech Team",
    "Binary Braintrust",
    "The Data Dream Team",
    "The Code Consortium",
    "Logic Lords",
    "Digital Dynamos",
    "Tech Titans",
    "Data Divas",
    "The Algorithm Assembly",
    "Code Crusaders",
    "Binary Buddies",
    "The Cyber Crew",
    "Tech Troopers",
    "Data Detectives",
    "Logic Legends",
    "The Byte Brotherhood",
    "Code Commandos",
    "The Tech Tribe",
    "The Logic League",
    "Data Drifters",
    "The Quantum Quest",
    "Code Crafters",
    "Binary Builders",
    "The Tech Team",
    "Data Dynamo",
    "Code Commanders",
    "The Cyber Squad",
    "Innovation Icons",
    "Tech Titans",
    "Data Daredevils",
    "The Code Collective",
    "Logic Leaders",
    "The Binary Brigade",
    "Tech Trailblazers",
    "The Algorithmic Alliance",
    "Data Dynamos",
    "Coding Conquerors"
]




    notifications = [{"Title":"Example Title1", "date":"29th", "time":"0800 - 0900","emails":["email","email"]},
                     {"Title":"Example Title2", "date":"30th", "time":"0930 - 1100","emails":["email","email"]},
                     {"Title":"Example Title3", "date":"31th", "time":"2200 - 2345","emails":["email","email"]},
                     {"Title":"Example Title4", "date":" 1st", "time":"0000 - 0100","emails":["email","email"]},
                     ]
    
    return render_template("user_page.html",title = user , user=user , groups=groups[0:] , cssFile="../static/userpage.css" , notifications = notifications)

