from next_product_getter import Product, ProductCollection
import uuid
from flask import Flask, jsonify, session, redirect, url_for, request, render_template

class Game:
   def __init__(self):
      self.score = 0
      self.productLast = Product("testLast",100, "img1")
      self.productNext = Product("testNext", 150, "img2")
   
   def nextProduct(self):
      self.productLast = self.productNext
      self.productNext = "New Product"
      self.productNext
   
   def checkGuess(self, userGuess):
      rightGuess = ""
      if (self.productNext.price > self.productLast.price):
         rightGuess = "higher"
      elif (self.productNext.price < self.productLast.price):
         rightGuess = "lower"
      else: 
         return True # if prices are equal always correct
      if userGuess == rightGuess:
         return True
   
   def toDict(self, CencorNextPrice = True):
      return {
         "score": self.score,
         "productLast": self.productLast.price,
         "productNext": self.productNext.price if not CencorNextPrice else 0
      }

games = {}

app = Flask(__name__)
app.secret_key = "jalkdfekllypkekdkdpqwpeioxyvenljjlkjnsnvnasvnela"

@app.route("/")
def index():
   sesssionID = session.get('sessionID')
   if sesssionID is None:
     session['sessionID'] = uuid.uuid4()

   #Add score of last game if not first game
   firstgame =  True if session['sessionID'] not in games else False
   lastScore = 0 if firstgame else games[session['sessionID']].score
   
   games.pop(session['sessionID'], None) # remove old game if exists
   return render_template("index.html", firstGame = firstgame, score = lastScore)

@app.route("/new_game")
def new_game():
   if session["sessionID"] is None:
      return redirect(url_for("index"))
   else:    
      game = Game()
      games[session['sessionID']] = game
      return redirect(url_for('game'))

@app.route("/game")
def game():
   if "sessionID" not in session:
      return redirect(url_for('index'))
   elif session['sessionID'] not in games:
      return redirect(url_for('new_game'))
   else:
      currentGame = games[session['sessionID']]
      productLast = currentGame.productLast
      productNext = currentGame.productNext
      productNext.price = 0 # removing price for next product before send to user
      return render_template("game.html", score = currentGame.productLast.price)

@app.route("/guess", methods = ['POST'])
def guess():
   #Check if session and game exist
   if "sessionID" not in session:
      return redirect(url_for('index'))
   elif session['sessionID'] not in games:
      return redirect(url_for('new_game'))
   else:
      currentGame = games[session['sessionID']]
      #get user guess from form
      user_guess = request.form['guess']
      if currentGame.checkGuess(user_guess): # if correct guess deliver new product
         currentGame.score += 1
         currentGame.nextProduct()
         return jsonify(currentGame.toDict(True)) # censor next price
      else:
         # if wrong return to title screen with score
         return redirect(url_for("index"))

@app.route("/test")
def test():
   currentGame = games[session['sessionID']]
   currentGame.score = 10
   return redirect(url_for("index"))

if __name__ == '__main__':
   app.run(debug = True)