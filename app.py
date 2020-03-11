from flask import Flask, render_template
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

try:
    db = psycopg2.connect(
            host = "localhost",
            port = "5432",
            database = "test"
    )

    cursor = db.cursor()
    #cursor.execute(open("initial_adds.sql", )
    
    """
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
                ID           SERIAL NOT NULL PRIMARY KEY,
                FirstName    VARCHAR[30] NOT NULL,
                LastName     VARCHAR[30] NOT NULL,
                Height       INT NOT NULL,
                Weight       INT NOT NULL,
                Age          INT NOT NULL,
                TeamId       INT NOT NULL,
                
                FOREIGN KEY (TeamId) REFERENCES "Team" (Id)
        );'''
    )
    print("Player: Works")

    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS "Season" (
                Year         INT PRIMARY KEY
        ); '''
    )
    print("Season: Works")

    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS "Game" (
                ID           SERIAL NOT NULL PRIMARY KEY,
	            SeasonYear   INT NOT NULL,
	            HomeTeamId   INT NOT NULL,
	            AwayTeamID   INT NOT NULL,
	            Result       VARCHAR[10],
	            GameDate	 DATE,	
	            FOREIGN KEY (SeasonYear) REFERENCES "Season" (Year),
	            FOREIGN KEY (HomeTeamId) REFERENCES "Team" (Id),
	            FOREIGN KEY (AwayTeamId) REFERENCES "Team" (Id)
        ); '''
    )
    print("Game: Works")

    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS "StatType" (
                ID           VARCHAR[5] NOT NULL PRIMARY KEY,
                Description  VARCHAR[30]
        );'''
    )
    print("StatType: Works")

    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS "StatInfo" (
                ID           SERIAL NOT NULL PRIMARY KEY,
                StatValue    INT NOT NULL,
                PlayerID     INT NOT NULL,
                GameID       INT NOT NULL,
                Type         VARCHAR[5] NOT NULL,
                
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
    """

    postgres_insert_query = '''INSERT INTO "Team" (TeamName) VALUES
                  (%s),
                  (%s),
                  (%s),
                  (%s),
                  (%s),
                  (%s);'''

    record_to_insert = ('Team1', 'Team2', 'Team3', 'Team4', 'Team5', 'Team6')

    cursor.execute(postgres_insert_query, record_to_insert) 

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

@app.route('/')
def home():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)