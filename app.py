from flask import Flask, render_template, request
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

def connectToDB():
    try:
        return psycopg2.connect(host = "localhost", port = "5432", database = "test")
    except (Exception, psycopg2.Error) as error:
        print("Can't connect to database")
        print(error)

def createTables(cursor):
    try:
        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS "Team" (
                    ID           SERIAL NOT NULL,
                    TeamName     VARCHAR(100) NOT NULL UNIQUE,

                    PRIMARY KEY (ID)
            );'''
        )
        print("Team: Works")

        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS "Player" (
                    ID           SERIAL NOT NULL,
                    FirstName    VARCHAR(30) NOT NULL,
                    LastName     VARCHAR(30) NOT NULL,
                    Height       VARCHAR(5),
                    Weight       INT,
                    Age          INT,
                    TeamId       INT NOT NULL,
                    
                    PRIMARY KEY (ID),
                    FOREIGN KEY (TeamId) REFERENCES "Team" (Id)
            );'''
        )
        print("Player: Works")

        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS "Season" (
                    Year         INT UNIQUE,

                    PRIMARY KEY (YEAR)
            ); '''
        )
        print("Season: Works")

        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS "Game" (
                    ID           SERIAL NOT NULL,
                    SeasonYear   INT NOT NULL,
                    HomeTeamId   INT NOT NULL,
                    AwayTeamId   INT NOT NULL,
                    WinnerId     INT,
                    LoserId      INT,
                    GameDate	 TIMESTAMPTZ,	

                    PRIMARY KEY (ID),
                    FOREIGN KEY (SeasonYear) REFERENCES "Season" (Year),
                    FOREIGN KEY (HomeTeamId) REFERENCES "Team" (Id),
                    FOREIGN KEY (AwayTeamId) REFERENCES "Team" (Id)
            ); '''
        )
        print("Game: Works")

        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS "StatType" (
                    ID           VARCHAR(5) NOT NULL,
                    Description  VARCHAR(30),

                    PRIMARY KEY (ID)
            );'''
        )
        print("StatType: Works")

        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS "StatInfo" (
                    ID           SERIAL NOT NULL,
                    PlayerID     INT NOT NULL,
                    GameID       INT NOT NULL,
                    Type         VARCHAR(5) NOT NULL,
                    StatValue    INT NOT NULL,
                    
                    PRIMARY KEY (ID),
                    FOREIGN KEY (PlayerId) REFERENCES "Player" (Id),
                    FOREIGN KEY (GameId) REFERENCES "Game" (Id),
                    FOREIGN KEY (Type) REFERENCES "StatType" (Id)
            );'''
        )
        print("StatInfo: Works")

        cursor.execute(
            ''' CREATE TABLE IF NOT EXISTS "TeamInSeason" (
                    SeasonId     INT NOT NULL,
                    TeamId       INT NOT NULL,
                    
                    PRIMARY KEY (SeasonId, TeamId),
                    FOREIGN KEY (SeasonId) REFERENCES "Season" (Year),
                    FOREIGN KEY (TeamId) REFERENCES "Team" (Id)
            );'''
        )
        print("TeamInSeason: Works")
        db.commit()


    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table", error)
        db.rollback()
    finally:
        #closing database connection.
            if(db):
                #cursor.close()
                # db.close()
                print("PostgreSQL connection is closed") 

def queryTeam(game):
    cursor.execute(
        ''' 
        SELECT FirstName, LastName, TeamName, Type, StatValue
        FROM "StatInfo"
             INNER JOIN "Player" ON ( "StatInfo".PlayerId = "Player".Id )
             INNER JOIN "Team" ON ( "Player".TeamId = "Team".Id )
        WHERE gameid = %s
        ORDER BY TeamName, "Team".Id, "Player".Id;
        ''', (game[4:]))
    rows = cursor.fetchall()

    return rows

"""
# NEED TO WORK ON STANDINGS
def showStandings():
    cursor.execute(
        '''
        SELECT TeamName, COUNT(WinnerID), COUNT(LoserID)
        FROM "Game"
             INNER JOIN "Team" ON ( "Game".HomeTeamID = "Team".ID AND "Game".AwayTeamID = "Team".ID )
        GROUP BY TeamName;
        '''
    )
    standing = cursor.fetchall()
    return standing

# IF THE GAME HAS NOT BEEN PLAYED YET AND USER SEARCHES THE GAME, SHOW GAME TIME, HOME TEAM, AWAY TEAM
def gamePreview(game):
    cursor.execute(
        '''
        SELECT TeamName, GameDate
        FROM "Game"
             INNER JOIN "Team" ON ( "Game".HomeTeamID = "Team".ID )
             INNER JOIN "Team" ON ( "Game".AwayTeamID = "Team".ID )
        WHERE "Game".Id = %s;
        ''', (game[4:]))
    
    rows = cursor.fetchall()
    return rows
"""

db = connectToDB()
cursor = db.cursor()
#createTables(cursor)

@app.route('/')
@app.route('/home')
def home():
    #standing = showStandings()
    return render_template("home.html", title='Home')

@app.route('/player')
def player():
    return render_template("player.html", title='Player')

@app.route('/team')
def team():
    return render_template("team.html", title='team')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == "POST":
        game = request.form['game']
        print(game)
        teams = queryTeam(game)
        if teams is not None:
            return render_template("game.html", title='Game', teams=teams)
        else:
            gameInfo = gamePreview(game)
            print(gameInfo)
            return render_template("game.html", title='Game', gameInfo = gameInfo)
            
    return render_template("game.html", title='Game')

@app.route('/insertplayer', methods=['GET', 'POST'])
def insert_player():
    return render_template("insert_player.html", title='Insert Player')

"""
@app.route('/submit', methods=['POST'])
def viewStats():
    game = request.form['game']
    print(game)
    
    teams = queryTeam(game)
    return render_template("game.html", Teams=teams)
"""
    

if __name__ == "__main__":
    app.run(debug=True)