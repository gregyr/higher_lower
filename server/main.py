import uuid
from flask import Flask, session, redirect, url_for, request, render_template

class Product:
   def __init__(self, price):
      self.price = price

class Game:
   def __init__(self):
      self.score = 0
      self.productLast = Product(100)
      self.productNext = Product(150)
   
   def nextProduct(self):
      self.productLast = self.productNext
      self.productNext = "New Product"
      self.productNext
   
   def checkGuess(self, userGuess):
      rightGuess = True
      return rightGuess

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
   user_guess = request.form['guess']
   if "sessionID" not in session:
      return redirect(url_for('index'))
   elif session['sessionID'] not in games:
      return redirect(url_for('new_game'))
   else:
      currentGame = games[session['sessionID']]
      if currentGame.checkGuess(user_guess):
         currentGame.score += 1
         currentGame.nextProduct()
         return redirect(url_for('game'))
      else:
         score = currentGame.score
         del games[session['sessionID']]
         return redirect(url_for("index"))

@app.route("/test")
def test():
   currentGame = games[session['sessionID']]
   currentGame.score = 10
   return redirect(url_for("index"))

if __name__ == '__main__':
   app.run(debug = True)