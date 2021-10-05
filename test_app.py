from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_board_made(self):
        """Test the game makes a gameboard when we start up the root page"""
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(session['board']), 5)

    def test_word_validation_not_on_board(self):
        """Test if we get not-on board when we submit a word that's not on the board"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=computer')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_word_validation_not_word(self):
        """Test if we get not-word result if we submit an invalid word"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=sldjfnlgoskjn')
            self.assertEqual(response.json['result'], 'not-word')

    def test_word_validation_ok(self):
        """Test if word result is ok when we know word is in board"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "O", "G", "S", "A"],
                                    ["V", "P", "N", "F", "S"],
                                    ["X", "L", "F", "R", "F"],
                                    ["Z", "K", "D", "H", "H"],
                                    ["T", "J", "D", "A", "D"]]
            response = client.get('/check-word?word=dog')
            self.assertEqual(response.json['result'], 'ok')
