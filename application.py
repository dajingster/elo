from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime, date
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import os 

from helpers import apology, login_required
from elo import New_Elo, standard_probability

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///elo.db")


@app.route("/")
@login_required
def index():

    information = []
    consistency_table = []
    gp_table = []
    averages = [0, 0, 0]
    counter = 1
    number = db.execute("SELECT COUNT(*) FROM ':i - Player Database'", i = session["user_id"])
    number = int(number[0]["COUNT(*)"])
    total = number
    while number != 0:
        row = db.execute("SELECT * FROM ':i - Player Database' WHERE ID = :c", i = session["user_id"], c = counter)
        if len(row) != 1:
            counter += 1
            continue
        else:
            rating = round(row[0]["Rating"], 1)
            rating = format(rating, '.1f')
            games_played = row[0]["Games Played"]
            name = row[0]["Name"]
            consistency = round(row[0]["Consistency"], 2)
            consistency = format(consistency, '.2f')
            averages[0] += float(rating)
            averages[1] += int(games_played)
            averages[2] += float(consistency)
            if len(information) == 0:
                information.append([name, rating, consistency, games_played])
            else:
                index = 0
                while index < len(information) and float(rating) < float(information[index][1]):
                    index +=1
                information.insert(index, [name, rating, consistency, games_played])
            if len(consistency_table) == 0:
                consistency_table.append([name, rating, consistency, games_played])
            else:
                index = 0
                while index < len(consistency_table) and float(consistency) < float(consistency_table[index][2]):
                    index +=1
                consistency_table.insert(index, [name, rating, consistency, games_played])
            if len(gp_table) == 0:
                gp_table.append([name, rating, consistency, games_played])
            else:
                index = 0
                print(gp_table[index])
                while index < len(gp_table) and games_played < gp_table[index][3]:
                    index +=1
                gp_table.insert(index, [name, rating, consistency, games_played])
                print(gp_table, index)
            counter +=1
            number -= 1
    for i in range(len(information)):
        for player in consistency_table:
            if player == information[i]:
                player.insert(0, i+1)
                break
    for i in range(len(information)):
        for player in gp_table:
            if player == information[i]:
                player.insert(0, i+1)
                break
    counter -= 1
    if total != 0:
        averages = [float(averages[i])/total for i in range(len(averages))]
        averages[0] = round(averages[0], 1)
        averages[0] = format(averages[0], '.1f')
        averages[1] = round(averages[1], 2)
        averages[1] = format(averages[1], '.2f')
        averages[2] = round(averages[2], 2)
        averages[2] = format(averages[2], '.2f')
    return render_template("index.html", information = information, counter = counter, consistency_table = consistency_table, gp_table = gp_table, averages = averages)


@app.route("/result", methods=["GET", "POST"])
@login_required
def result():
    if request.method == "POST":
        if (not request.form.get("a")) or (not request.form.get("b")) or (not request.form.get("result")):
            return apology("Need players and result", 403)

        name_one = request.form.get("a")
        name_two = request.form.get("b")
        result = request.form.get("result")
        info = db.execute("SELECT * FROM ':i - Player Database' WHERE NAME = :n", i = session["user_id"], n = name_one)
        if len(info) != 1:
            return apology("Player one does not exist", 403)
        player_one = [info[0]["Rating"], info[0]["Games Played"], info[0]["Consistency"]]
        games_one = info[0]["Games Played"]
        info = db.execute("SELECT * FROM ':i - Player Database' WHERE NAME = :n", i = session["user_id"], n = name_two)
        if len(info) != 1:
            return apology("Player two does not exist", 403)
        player_two = [info[0]["Rating"], info[0]["Games Played"], info[0]["Consistency"]]
        updated = New_Elo(player_one, player_two, result)
        db.execute("UPDATE ':i - Player Database' SET Rating = :r WHERE NAME = :n", i = session["user_id"], n = name_one, r = updated[0])
        db.execute("UPDATE ':i - Player Database' SET Consistency = :r WHERE NAME = :n", i = session["user_id"], n = name_one, r = updated[1])
        db.execute("UPDATE ':i - Player Database' SET Rating = :r WHERE NAME = :n", i = session["user_id"], n = name_two, r = updated[2])
        db.execute("UPDATE ':i - Player Database' SET Consistency = :r WHERE NAME = :n", i = session["user_id"], n = name_two, r = updated[3])
        db.execute("UPDATE ':i - Player Database' SET 'Games Played' = :g WHERE NAME = :n", i = session["user_id"], n = name_one, g = games_one + 1)
        db.execute("UPDATE ':i - Player Database' SET 'Games Played' = :g WHERE NAME = :n", i = session["user_id"], n = name_two, g = info[0]["Games Played"] + 1)
        db.execute("INSERT INTO ':i - Result History' ('Player_A', 'A_Change', 'A_New_Rating', 'A_Consistency', 'Player_B', 'B_Change', 'B_New_Rating', 'B_Consistency', 'Result') VALUES (:n1, :c1, :r1, :co1, :n2, :c2, :r2, :co2, :r)", i = session["user_id"], n1 = name_one, n2 = name_two, r = result, r1 = updated[0], c1 = updated[0] - player_one[0], r2 = updated[2], c2 = updated[2] - player_two[0], co1 = updated[1], co2 = updated[3])
        print(updated)
        flash('Result Added!')
        return redirect("/")

    else:
        return render_template("result.html")


@app.route("/player", methods=["GET", "POST"])
@login_required
def player():
    if request.method == "POST":
        if (not request.form.get("player")) and (not request.form.get("remove_player")):
            return apology("Need player name", 403)

        if request.form.get("player") and request.form.get("remove_player"):
            return apology("Fill only one box", 403)

        if request.form.get("player"):
            info = request.form.get("player")
            info = info.split(",")

            for i in range(len(info)):
                info[i] = info[i].strip()
            while len(info) != 0:

                try:
                    name, rating = info[0].split(":")
                    name = name.strip()
                    rating = rating.strip()
                    break
                except (ValueError, TypeError, NameError, RuntimeError):
                    return apology("Wrong new player format", 403)

                name_exists = db.execute("SELECT * FROM ':i - Player Database' WHERE Name = :n", i = session["user_id"], n = name)
                if len(name_exists) != 0:
                    return apology("Name exists", 403)

                else:
                    db.execute("INSERT INTO ':i - Player Database' ('Name', 'Games Played', 'Rating', 'Consistency') VALUES (:n, 0, :r, 1.0)", i = session["user_id"], n = name, r = rating)
                del info[0]
            flash('Player(s) Added!')
            return redirect("/")
        if request.form.get("remove_player"):
            name_exists = db.execute("SELECT * FROM ':i - Player Database' WHERE Name = :n", i = session["user_id"], n = request.form.get("remove_player"))
            if len(name_exists) == 0:
                return apology("Name doesn't exist", 403)

            else:
                db.execute("DELETE FROM ':i - Player Database' WHERE Name = :n", i = session["user_id"], n = request.form.get("remove_player"))
            flash('Player Removed!')
            return redirect("/")

    else:
        return render_template("player.html")


@app.route("/prediction", methods=["GET", "POST"])
@login_required
def prediction():
    if request.method == "POST":
        if (not request.form.get("a")) or (not request.form.get("b")):
            return apology("Need players", 403)

        name_one = request.form.get("a")
        name_two = request.form.get("b")
        info = db.execute("SELECT * FROM ':i - Player Database' WHERE NAME = :n", i = session["user_id"], n = name_one)
        if len(info) != 1:
            return apology("Player one does not exist", 403)
        player_one = [name_one, info[0]["Rating"], info[0]["Games Played"], info[0]["Consistency"]]
        info = db.execute("SELECT * FROM ':i - Player Database' WHERE NAME = :n", i = session["user_id"], n = name_two)
        if len(info) != 1:
            return apology("Player two does not exist", 403)
        player_two = [name_two, info[0]["Rating"], info[0]["Games Played"], info[0]["Consistency"]]

        player_one[1] = round(player_one[1], 1)
        player_one[1] = format(player_one[1], '.1f')
        player_one[2] = round(player_one[2], 2)
        player_one[2] = format(player_one[2], '.2f')

        player_two[1] = round(player_two[1], 1)
        player_two[1] = format(player_two[1], '.1f')
        player_two[2] = round(player_two[2], 2)
        player_two[2] = format(player_two[2], '.2f')

        probabilities = []
        probabilities.append(standard_probability(float(player_one[1]), float(player_two[1])))
        probabilities.append(standard_probability(float(player_two[1]), float(player_one[1])))

        print(probabilities)
        probabilities[0]  = round(probabilities[0]*100 , 1)
        probabilities[0] = format(probabilities[0], '.1f')
        probabilities[1]  = round(probabilities[1]*100 , 1)
        probabilities[1] = format(probabilities[1] , '.1f')

        history_table = []
        counter = 1
        total = 0
        while True:
            row = db.execute("SELECT * FROM ':i - Result History' WHERE ID = :c", i = session["user_id"], c = counter)
            if len(row) != 1:
                break
            if not ((row[0]["Player_A"] == name_one and row[0]["Player_B"] == name_two) or (row[0]["Player_A"] == name_two and row[0]["Player_B"] == name_one)):
                counter += 1
                continue
            else:
                row[0]['A_Change'] = round(row[0]['A_Change'], 1)
                row[0]['A_Change'] = format(row[0]['A_Change'], '.1f')
                row[0]['A_New_Rating'] = round(row[0]['A_New_Rating'], 1)
                row[0]['A_New_Rating'] = format(row[0]['A_New_Rating'], '.1f')
                row[0]['A_Consistency'] = round(row[0]['A_Consistency'], 2)
                row[0]['A_Consistency'] = format(row[0]['A_Consistency'], '.2f')
                row[0]['B_Change'] = round(row[0]['B_Change'], 1)
                row[0]['B_Change'] = format(row[0]['B_Change'], '.1f')
                row[0]['B_New_Rating'] = round(row[0]['B_New_Rating'], 1)
                row[0]['B_New_Rating'] = format(row[0]['B_New_Rating'], '.1f')
                row[0]['B_Consistency'] = round(row[0]['B_Consistency'], 2)
                row[0]['B_Consistency'] = format(row[0]['B_Consistency'], '.2f')
                history_table.append([row[0]['Player_A'], row[0]['A_Change'], row[0]['A_New_Rating'], row[0]['A_Consistency'], row[0]['Player_B'], row[0]['B_Change'], row[0]['B_New_Rating'], row[0]['B_Consistency'], row[0]['Result'], row[0]['Timestamp']])
                counter +=1
                total += 1
        counter -= 1
        history_table.reverse()
        return render_template("predicresults.html", probabilities = probabilities, history_table = history_table, total = total, player_one = player_one, player_two = player_two)
    else:
        return render_template("prediction.html")



@app.route("/analysis_search", methods=["GET", "POST"])
@login_required
def analysis_search():
    if request.method == "POST":
        name = request.form.get("player_name")
        if (not name):
            return apology("No player name", 403)
        player = db.execute("SELECT * FROM ':i - Player Database' WHERE Name = :n", i = session["user_id"], n = name)
        if len(player) != 1:
            return apology("Player does not exist", 403)
        elif len(player) > 1:
            return apology("Please enter unique name", 403)
        else:
            information = [player[0]["Name"], player[0]["Rating"], player[0]["Consistency"], player[0]["Games Played"]]
            information[1] = round(information[1], 1)
            information[1] = format(information[1], '.1f')
            information[2] = round(information[2], 2)
            information[2] = format(information[2], '.2f')

            month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            counter = 1
            dates = ['N/A', 'N/A', 'N/A', 'N/A']
            results = [0, 0, 0]
            progress = []
            avg_opp_rating = [0, 0, 0]
            extra_info = [1200.0, 1200.0, 0, 'N/A']
            date = datetime.now()
            date = date.strftime("%Y-%m-%d")
            today = datetime.now()
            today = today.strftime("%Y-%m-%d")

            if int(date[5:7]) != 1:
                date = date[:5] + str(int(date[5:7])-1).zfill(2) + date[7:]
            else:
                date = str(int(date[:4])-1) + str(-12) + date[7:]


            while True:
                games = db.execute("SELECT * FROM ':i - Result History' WHERE ID = :c", i = session["user_id"], c = counter)
                if len(games) != 1:
                    break
                if games[0]["Player_A"] != name and games[0]["Player_B"] != name:
                    counter += 1
                    continue
                else:
                    if dates[0] == 'N/A':
                        dates[0] = games[0]["Timestamp"]
                        dates[0] = dates[0][:10]
                    if games[0]["Player_A"] == name and float(games[0]["Result"]) == 1.0:
                        results[0] += 1
                        avg_opp_rating[0] += games[0]["B_New_Rating"] - games[0]["B_Change"]
                        if extra_info[2] <= games[0]["B_New_Rating"] - games[0]["B_Change"]:
                            extra_info[2] = games[0]["B_New_Rating"] - games[0]["B_Change"]
                            extra_info[3] = games[0]["Player_B"]
                            dates[3] = games[0]["Timestamp"]
                            dates[3] = dates[3][:10]
                    if games[0]["Player_B"] == name and float(games[0]["Result"]) == 0.0:
                        results[0] += 1
                        avg_opp_rating[0] += games[0]["A_New_Rating"] - games[0]["A_Change"]
                        if extra_info[2] <= games[0]["A_New_Rating"] - games[0]["A_Change"]:
                            extra_info[2] = games[0]["A_New_Rating"] - games[0]["A_Change"]
                            extra_info[3] = games[0]["Player_A"]
                            dates[3] = games[0]["Timestamp"]
                            dates[3] = dates[3][:10]
                    elif games[0]["Player_A"] == name and float(games[0]["Result"]) == 0.0:
                        results[1] += 1
                        avg_opp_rating[1] += games[0]["B_New_Rating"] - games[0]["B_Change"]
                    elif games[0]["Player_B"] == name and float(games[0]["Result"]) == 1.0:
                        results[1] += 1
                        avg_opp_rating[1] += games[0]["A_New_Rating"] - games[0]["A_Change"]
                    elif games[0]["Player_A"] == name and float(games[0]["Result"]) == 0.5:
                        results[2] += 1
                        avg_opp_rating[2] += games[0]["B_New_Rating"] - games[0]["B_Change"]
                    elif games[0]["Player_B"] == name and float(games[0]["Result"]) == 0.5:
                        results[2] += 1
                        avg_opp_rating[2] += games[0]["A_New_Rating"] - games[0]["A_Change"]
                    if games[0]["Player_A"] == name:
                        if games[0]["Timestamp"][0:4] > date[0:4] or (games[0]["Timestamp"][0:4] == date[0:4] and games[0]["Timestamp"][5:7] > date[5:7]) or (games[0]["Timestamp"][0:4] == date[0:4] and games[0]["Timestamp"][5:7] == date[5:7] and games[0]["Timestamp"][8:] > date[8:]):
                            if today[5:7] == games[0]["Timestamp"][5:7]:
                                progress.append([games[0]["A_New_Rating"], games[0]["A_Consistency"], int(today[8:]) - int(games[0]["Timestamp"][8:10])])
                            else:
                                progress.append([games[0]["A_New_Rating"], games[0]["A_Consistency"], int(today[8:]) + month[int(games[0]["Timestamp"][5:7])-1] - int(games[0]["Timestamp"][8:10])])
                            if len(progress) > 1 and progress[-1][2] == progress[-2][2]:
                                del progress[-2]
                        if games[0]["A_New_Rating"] >= extra_info[0]:
                            extra_info[0] = games[0]["A_New_Rating"]
                            dates[1] = games[0]["Timestamp"]
                            dates[1] = dates[1][:10]
                        if games[0]["A_New_Rating"] <= extra_info[1]:
                            extra_info[1] = games[0]["A_New_Rating"]
                            dates[2] = games[0]["Timestamp"]
                            dates[2] = dates[2][:10]
                    else:
                        if games[0]["Timestamp"][0:4] > date[0:4] or (games[0]["Timestamp"][0:4] == date[0:4] and games[0]["Timestamp"][5:7] > date[5:7]) or (games[0]["Timestamp"][0:4] == date[0:4] and games[0]["Timestamp"][5:7] == date[5:7] and games[0]["Timestamp"][8:] > date[8:]):
                            if today[5:7] == games[0]["Timestamp"][5:7]:
                                progress.append([games[0]["B_New_Rating"], games[0]["B_Consistency"], int(today[8:]) - int(games[0]["Timestamp"][8:10])])
                            else:
                                progress.append([games[0]["B_New_Rating"], games[0]["B_Consistency"], int(today[8:]) + month[int(games[0]["Timestamp"][5:7])-1] - int(games[0]["Timestamp"][8:10])])
                            if len(progress) > 1 and progress[-1][2] == progress[-2][2]:
                                del progress[-2]
                        if games[0]["B_New_Rating"] >= extra_info[0]:
                            extra_info[0] = games[0]["B_New_Rating"]
                            dates[1] = games[0]["Timestamp"]
                            dates[1] = dates[1][:10]
                        if games[0]["B_New_Rating"] <= extra_info[1]:
                            extra_info[1] = games[0]["B_New_Rating"]
                            dates[2] = games[0]["Timestamp"]
                            dates[2] = dates[2][:10]
                    counter +=1

            counter = 1
            c_rank = 1
            r_rank = 1
            gp_rank = 1
            number = db.execute("SELECT COUNT(*) FROM ':i - Player Database'", i = session["user_id"])
            number = int(number[0]["COUNT(*)"])
            total = number
            while number != 1:
                row = db.execute("SELECT * FROM ':i - Player Database' WHERE ID = :c", i = session["user_id"], c = counter)
                if len(row) != 1 or row[0]["Name"] == name:
                    counter += 1
                    continue
                print(row[0])
                if row[0]["Rating"] > float(information[1]):
                    r_rank += 1
                if row[0]["Consistency"] > float(information[2]):
                    c_rank += 1
                if row[0]["Games Played"] > float(information[3]):
                    gp_rank += 1
                counter +=1
                number -=1
            counter = total
            rank = [r_rank, c_rank, gp_rank]
            percentile = [round(100*(counter - rank[i])/counter) for i in range(len(rank))]

            avg_opp_rating.append(avg_opp_rating[0]+avg_opp_rating[1]+avg_opp_rating[2])

            for i in range(len(extra_info) - 1):
                extra_info[i] = round(extra_info[i], 1)

            if extra_info[2] == 0:
                extra_info[2] = 'N/A'

            results.append(results[0] +results[1] +results[2])

            for i in range(len(avg_opp_rating)):
                if avg_opp_rating[i] == 0:
                    avg_opp_rating[i] = 'N/A'
                else:
                    avg_opp_rating[i] = round(avg_opp_rating[i]/results[i], 1)
            return render_template("analysis.html", date = date, information = information, rank = rank, percentile = percentile, dates = dates, progress = progress, results = results, avg_opp_rating = avg_opp_rating, extra_info = extra_info, counter = counter)
    else:
        return render_template("analysis_search.html")



@app.route("/history")
@login_required
def history():
    history_table = []
    counter = 1
    while True:
        row = db.execute("SELECT * FROM ':i - Result History' WHERE ID = :c", i = session["user_id"], c = counter)
        if len(row) != 1:
            break
        else:
            row[0]['A_Change'] = round(row[0]['A_Change'], 1)
            row[0]['A_Change'] = format(row[0]['A_Change'], '.1f')
            row[0]['A_New_Rating'] = round(row[0]['A_New_Rating'], 1)
            row[0]['A_New_Rating'] = format(row[0]['A_New_Rating'], '.1f')
            row[0]['A_Consistency'] = round(row[0]['A_Consistency'], 2)
            row[0]['A_Consistency'] = format(row[0]['A_Consistency'], '.2f')
            row[0]['B_Change'] = round(row[0]['B_Change'], 1)
            row[0]['B_Change'] = format(row[0]['B_Change'], '.1f')
            row[0]['B_New_Rating'] = round(row[0]['B_New_Rating'], 1)
            row[0]['B_New_Rating'] = format(row[0]['B_New_Rating'], '.1f')
            row[0]['B_Consistency'] = round(row[0]['B_Consistency'], 2)
            row[0]['B_Consistency'] = format(row[0]['B_Consistency'], '.2f')
            history_table.append([row[0]['Player_A'], row[0]['A_Change'], row[0]['A_New_Rating'], row[0]['A_Consistency'], row[0]['Player_B'], row[0]['B_Change'], row[0]['B_New_Rating'], row[0]['B_Consistency'], row[0]['Result'], row[0]['Timestamp']])
            counter +=1
    counter -= 1
    history_table.reverse()
    return render_template("history.html", history_table = history_table, counter = counter)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("Must provide confirmation", 403)

        if not (request.form.get("password") == request.form.get("confirmation")):
            return apology("Your password and password confirmation do not match", 403)

        hash_password = generate_password_hash(request.form.get("password"))

        # Query database for username
        result = db.execute("INSERT INTO users (username, hash) VALUES (:u, :p)", u = request.form.get("username"), p = hash_password)

        if not result:
            return apology("Sorry, but that username is taken", 403)

        id = db.execute("SELECT id FROM users WHERE username = :u", u = request.form.get("username"))
        db.execute("CREATE TABLE ':i - Player Database' ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'Name' TEXT NOT NULL, 'Games Played' INTEGER NOT NULL, 'Rating' NUMERIC NOT NULL, 'Consistency' NUMERIC NOT NULL)", i = id[0]["id"])
        db.execute("CREATE TABLE ':i - Result History' ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'Player_A' TEXT NOT NULL, 'A_Change' NUMERIC NOT NULL, 'A_New_Rating' NUMERIC NOT NULL, 'A_Consistency' NUMERIC NOT NULL, 'Player_B' TEXT NOT NULL, 'B_Change' NUMERIC NOT NULL, 'B_New_Rating' NUMERIC NOT NULL, 'B_Consistency' NUMERIC NOT NULL, 'Result' NUMERIC NOT NULL, 'Timestamp' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)", i = id[0]["id"])


        session["user_id"] = id[0]["id"]

        # Redirect user to home page
        flash('Registered!')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("Must provide confirmation", 403)

        if not (request.form.get("password") == request.form.get("confirmation")):
            return apology("Your password and password confirmation do not match", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 1:
            return apology("This username does not exist", 403)


        hash_password = generate_password_hash(request.form.get("password"))

        result = db.execute("UPDATE users SET hash = :h WHERE ID = :i", i = session["user_id"], h = hash_password)
        # Redirect user to home page
        flash('Password Changed!')
        return redirect("/")

    else:
        return render_template("change_password.html")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
