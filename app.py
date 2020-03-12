from flask import Flask, render_template
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
                    GameDate	 DATE,	

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
                cursor.close()
                db.close()
                print("PostgreSQL connection is closed")

"""
try:
    db = psycopg2.connect(
            host = "localhost",
            port = "5432",
            database = "test"
    )

    cursor = db.cursor()
 """   

db = connectToDB()
cursor = db.cursor()
#createTables(cursor)

@app.route('/')
def home():
    try:
        cursor.execute(
            ''' SELECT FirstName, LastName, Age, Height, Weight, TeamName
                FROM "Player"
                     INNER JOIN "Team" ON ( "Team".Id = "Player".TeamId );
            '''
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    result = cursor.fetchall()
    for row in result:
        print(result)
    return render_template("home.html", results = result)

if __name__ == "__main__":
    app.run(debug=True)