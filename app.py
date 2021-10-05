from flask.signals import template_rendered
from flask.templating import render_template
from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, jsonify
from flask.globals import session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "BFKLD235SF4V3X>^SDFSD"

boggle_game = Boggle()


@app.route('/')
def start_game():
    """Generate the game board and start the game"""

    board = boggle_game.make_board()
    session['board'] = board
    playthroughs = session.get("playthroughs", 0)
    highscore = session.get("highscore", 0)

    return render_template('home.html', highscore=highscore, playthroughs=playthroughs)


@app.route('/check-word')
def check_word():
    """Check if word is in dictionary"""

    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})


@app.route('/post-score', methods=['POST'])
def post_score():
    """Get score from game and compare against highscore, update the amount of playthoughs"""

    current_score = request.json["current_score"]
    playthroughs = session.get("playthroughs", 0)
    highscore = session.get("highscore", 0)

    session['playthroughs'] = playthroughs + 1
    playthroughs = playthroughs + 1
    if current_score >= highscore:
        session['highscore'] = current_score
    else:
        session['highscore'] = highscore
    return jsonify(highscore, playthroughs)
