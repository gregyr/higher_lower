from next_product_getter import Product, ProductCollection
from threading import Lock
import uuid
from flask import Flask, jsonify, session, redirect, url_for, request, render_template
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
from db import leaderBoard

dirname = str(Path(__file__).parent.parent)

class Game:
   def __init__(self, article_file_path = None):
      self.score = 0
      self.collection = ProductCollection((dirname + r'/scraper/articles.json') if article_file_path is None else article_file_path)
      self.productLast = self.collection.next_product()
      self.productNext = self.collection.next_product(self.productLast)
      self.expiresAt = datetime.datetime.now() + datetime.timedelta(minutes=5) # game expires in 30 minutes
   
   def expired(self):
      return datetime.datetime.now() > self.expiresAt
   
   def extend_time(self, minutes=5):
      self.expiresAt = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

   def nextProduct(self):
      self.productLast = self.productNext
      self.productNext = self.collection.next_product(self.productLast)
   
   def checkGuess(self, userGuess):
      self.extend_time()

      rightGuess = ""
      if (self.productNext.price > self.productLast.price):
         rightGuess = "higher"
      elif (self.productNext.price < self.productLast.price):
         rightGuess = "lower"
      else: 
         return True # if prices are equal always correct
      if userGuess == rightGuess:
         return True
   
   def toDict(self, CensorNextPrice = True):
      return {
         "score": self.score,
         "productLast_brand": self.productLast.brand,
         "productLast_price": self.productLast.price,
         "productLast_name": self.productLast.name,
         "productLast_img": self.productLast.img,
         "productLast_high_q_img": self.productLast.high_q_img,

         "productNext_brand": self.productNext.brand,
         "productNext_price": self.productNext.price if not CensorNextPrice else "???",
         "productNext_name": self.productNext.name,
         "productNext_img": self.productNext.img,
         "productNext_high_q_img": self.productNext.high_q_img,
      }

games = {}
games_lock = Lock() # to prevent simultaneous access to games dict from cleanup and main thread

leaderBoard = leaderBoard(dirname + r'/server/DB/leaderboard.db')

def cleanup_games():
   with games_lock:
      for game in list(games.items()):
         if game[1].expired():
            games.pop(game[0], None)
         

app = Flask(__name__)
app.secret_key = "jalkdfekllypkekdkdpqwpeioxyvenljjlkjnsnvnasvnela"

@app.route("/")
def index():
   sesssionID = session.get('sessionID')
   if sesssionID is None:
     session['sessionID'] = uuid.uuid4()

   with games_lock:
      #Add score of last game if not first game
      firstgame =  True if session['sessionID'] not in games else False
      lastScore = 0 if firstgame else games[session['sessionID']].score
      
      #leaderboard logic
      if not firstgame: #leaderboard update
         leaderBoard.add_score(session.get('name'), lastScore)
      leaderBoardData = leaderBoard.get_top_scores_dict(5) # get leaderboard from leaderboard.db

      if not firstgame: # adding own score and name to leaderboard data if not first game
         leaderBoardData["own_name"] = session.get('name')
         leaderBoardData["own_score"] = lastScore
         leaderBoardData["own_position"] = leaderBoard.get_position(lastScore)
      
      games.pop(session['sessionID'], None) # remove old game if exists
      return render_template("index.html", firstGame = firstgame, **leaderBoardData)

@app.route("/new_game")
def new_game():
   if session["sessionID"] is None:
      return redirect(url_for("index"))
   else:    
      game = Game()
      with games_lock:
         games[session['sessionID']] = game
      return redirect(url_for('game'))

@app.route("/game")
def game():
   with games_lock:
      if "sessionID" not in session:
         return redirect(url_for('index'))
      elif session['sessionID'] not in games:
         return redirect(url_for('new_game'))
      else:
         currentGame = games[session['sessionID']]
         return render_template("game.html", **currentGame.toDict(True))

@app.route("/guess", methods = ['POST'])
def guess():
   with games_lock:
      #Check if session and game exist
      if "sessionID" not in session:
         return redirect(url_for('index'))
      elif session['sessionID'] not in games:
         return redirect(url_for('new_game'))
      else:
         currentGame = games[session['sessionID']]
         #get user guess from form
         user_guess = request.json['guess']
         if currentGame.checkGuess(user_guess): # if correct guess deliver new product
            print("Guessed correctly")
            currentGame.score += 1
            currentGame.nextProduct()
            return jsonify(currentGame.toDict(True)) # censor next price
         else:
            # if wrong return to title screen with score
            return redirect(url_for("index"))

@app.route("/setname", methods = ['POST'])
def setname():
   name = request.form['username']
   session['name'] = name
   if(name == ""):
      session['name'] = "Anonym" #add a funny name genration later
   return redirect(url_for('new_game'))

@app.route("/test")
def test():
   name = session["name"]
   return name
   
sheduler = BackgroundScheduler()
sheduler.add_job(func=cleanup_games, trigger="interval", minutes=1)
sheduler.start()

if __name__ == '__main__':
   app.run(debug = True)