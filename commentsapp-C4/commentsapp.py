
from flask import Flask, render_template, url_for, request, redirect, flash, session

import time,random,os
from threading import Thread

app = Flask(__name__)

@app.route('/')
def display_home():
    return render_template("home.html",
                            the_title="Welcome to the Word Game, where all the fun is at.",
                            comment_url=url_for("getacomment"),
                            show_url=url_for("showallcomments"),
                            game_url=url_for("wordgame"),
			    the_person=session.get('last_visitor', 'unknown'), )

@app.route('/comment')
def getacomment():
    return render_template("enter.html",
                           the_title="Please make words from the word given!",
                           the_save_url=url_for("saveformdata") )

def update_log(name, comment):
    time.sleep(15)
    with open('comments.log', 'a') as log:
        print(name, 'said:', file=log)
        print(comment, file=log)

@app.route('/saveform', methods=["POST"])
def saveformdata():
    all_ok = True
    if request.form['user_name'] == '':
        all_ok = False
        flash("Sorry. You must tell me your name. Try again")
    #print('-->', request.form['the_comment'].strip(), '<--')
    if request.form['the_comment'] == '':
        all_ok = False
        flash("Sorry. You must give me a comment. Try again")
    if all_ok:
        t = Thread(target=update_log, args=(request.form['user_name'], request.form['the_comment']))
        t.start()
        session['last_visitor'] = request.form['user_name']
        return render_template("thanks.html",
				the_title="Thanks!",
				the_user=request.form['user_name'],
				home_link=url_for("display_home"), )
    else:
        return redirect(url_for("getacomment"))

@app.route('/displaycomments')
def showallcomments():
    with open('comments.log') as log:
        lines = log.readlines()
    return render_template("show.html",
                            the_title="Here are the comments to date",
                            the_data=lines,
                            home_link=url_for("display_home"))

@app.route('/wordgame')
def wordgame():
    return render_template("game.html",
                           the_title="Please make words from the word given!",
                           the_word=get_random_line(),
                           game_save_url=url_for("savegamedata") )
def get_random_line():
    total_bytes = os.stat('mysite/commentsapp-C4/longWords.txt').st_size
    random_point = random.randint(0, total_bytes)
    file = open('mysite/commentsapp-C4/longWords.txt')
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    return file.readline()#variables

def checkWords(sourceWord,words):
    shortWord = open("mysite/commentsapp-C4/shortWords.txt", "r")
    count = 0
    count = len(sourceWord)
    #for usrin in words:
    if words in shortWord:
        for i in words:
            if i in sourceWord:
                count -= 1
        if count == 0:
            return True
    return False

@app.route('/gameresults', methods=["POST"])
def savegamedata():

    words = [request.form['word1'],request.form['word2'],request.form['word3'],request.form['word4'],request.form['word5'],request.form['word6'],request.form['word7']]
    #t = Thread(target=update_log, args=(request.form['user_name'], request.form['the_comment']))
    #t.start()
    #if checkWords(request.form("sourceWord"),words):
    if checkWords("ringrod",request.form['word1']):
        return render_template("gameresult.html",
                               the_title=words[1],
                               home_link=url_for("display_home"), )
    else:
        return redirect(url_for("getacomment"))




app.config['SECRET_KEY'] = 'thisismysecretkeywhichyouwillneverguesshahahahahahahaha'
if __name__== "__main__":
    app.run(debug=True)
