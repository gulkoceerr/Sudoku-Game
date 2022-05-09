from flask import Flask, render_template, url_for, request
from sudoku import Sudoku
import random

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/rules',methods=['GET','POST'])
def rules():
    return render_template('rules.html')

@app.route('/leaderboard',methods=['GET','POST'])
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/profile',methods=['GET','POST'])
def profile():
    return render_template('profile.html')

@app.route('/sudoku',methods=['GET','POST'])
def sudoku():
    if request.method == 'GET':
        default_options = {
            "username": "someone",
            "grid_type": 9, 
            "level" : 0.75, 
            "version": "numbers",
            "last_game": [
                [5, 0, 3, 2, 9, 4, 0, 1, 0], 
                [4, 1, 0, 7, 0, 0, 2, 5, 9], 
                [8, 0, 0, 0, 1, 5, 3, 4, 0], 
                [1, 8, 0, 3, 0, 2, 9, 7, 4], 
                [0, 9, 2, 4, 7, 0, 8, 3, 5], 
                [3, 4, 0, 0, 5, 9, 0, 2, 6], 
                [2, 6, 1, 9, 4, 7, 5, 8, 3], 
                [9, 5, 4, 1, 8, 3, 7, 0, 2], 
                [7, 0, 8, 0, 2, 6, 4, 9, 1]
            ],
            "last_game_solved": [
                [5, 7, 3, 2, 9, 4, 6, 1, 8], 
                [4, 1, 6, 7, 3, 8, 2, 5, 9], 
                [8, 2, 9, 6, 1, 5, 3, 4, 7], 
                [1, 8, 5, 3, 6, 2, 9, 7, 4], 
                [6, 9, 2, 4, 7, 1, 8, 3, 5], 
                [3, 4, 7, 8, 5, 9, 1, 2, 6], 
                [2, 6, 1, 9, 4, 7, 5, 8, 3], 
                [9, 5, 4, 1, 8, 3, 7, 6, 2], 
                [7, 3, 8, 5, 2, 6, 4, 9, 1]
            ],
            "numpad": [1,2,3,4,5,6,7,8,9]
        }
        default_options["numpad"] = list(range(1,default_options["grid_type"]+1))
        default_options["last_game"]= [[0 if i == None or 0 else i for i in row] for row in default_options["last_game"]]
        if default_options["version"] == "shapes":
            emojiler = {
                0:0,
                1: "😁",
                2: "😂",
                3: "🥶",
                4: "😃",
                5: "😄",
                6: "😅",
                7: "😆",
                8: "😉",
                9: "😊",
            }
            default_options["numpad"] = [emojiler[i] for i in default_options["numpad"]]
            default_options["last_game"]= [[emojiler[i] for i in row] for row in default_options["last_game"]]
            default_options["last_game_solved"]= [[emojiler[i] for i in row] for row in default_options["last_game_solved"]]

        # Data burada bizim template variable'ımız
        return render_template('sudoku.html', data = default_options)
    elif request.method == 'POST':
        input = request.form
        default_options = {
            "username": "someone",
            "grid_type": int(input["grid_type"]), # selection
            "level" : float(input["level"]), # level
            "version": input["version"], # version
            "last_game": [[]],
            "last_game_solved": [[]],
            "numpad": [[]]
        }
        sudoku = []
        sudoku_solved = []
        numpad = 0
        _seed = random.randint(1,1000)
        if default_options["grid_type"] == 4:
            sudoku = Sudoku(2,2, seed = _seed).difficulty(default_options["level"])
        elif default_options["grid_type"] == 6:
            sudoku = Sudoku(3,2, seed = _seed).difficulty(default_options["level"])
        elif default_options["grid_type"] == 8:
            sudoku = Sudoku(4,2, seed = _seed).difficulty(default_options["level"])
        elif default_options["grid_type"] == 9:
            sudoku = Sudoku(3,3, seed = _seed).difficulty(default_options["level"])
        sudoku_solved = sudoku.solve().board
        sudoku = sudoku.board
        default_options["numpad"] = list(range(1,default_options["grid_type"]+1))
        default_options["last_game"]= [[0 if i == None or 0 else i for i in row] for row in sudoku]
        default_options["last_game_solved"] = sudoku_solved
        if default_options["version"] == "shapes":
            emojiler = {
                None:0,
                1: "😁",
                2: "😂",
                3: "🥶",
                4: "😃",
                5: "😄",
                6: "😅",
                7: "😆",
                8: "😉",
                9: "😊",
            }
            default_options["numpad"] = [emojiler[i] for i in default_options["numpad"]]
            default_options["last_game"] = [[emojiler[i] for i in row] for row in sudoku]
            default_options["last_game_solved"] = [[emojiler[i] for i in row] for row in sudoku_solved]


        # Data burada bizim template variable'ımız
        return render_template('sudoku.html', data = default_options)


if __name__ == "__main__":
    app.run(debug=True, port=8080)