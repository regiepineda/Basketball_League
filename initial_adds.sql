CREATE TABLE IF NOT EXISTS "Team" (
        ID           INTEGER NOT NULL,
        TeamName     VARCHAR(100) NOT NULL,

        PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS "Player" (
        ID           INT NOT NULL PRIMARY KEY,
        FirstName    VARCHAR[30] NOT NULL,
        LastName     VARCHAR[30] NOT NULL,
        Height       INT NOT NULL,
        Weight       INT NOT NULL,
        Age          INT NOT NULL,
        TeamId       INT NOT NULL,
                
        FOREIGN KEY (TeamId) REFERENCES "Team" (Id)
);

CREATE TABLE IF NOT EXISTS "Season" (
                Year         INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS "Game" (
        ID           INT NOT NULL PRIMARY KEY,
	    SeasonYear   INT NOT NULL,
        HomeTeamId   INT NOT NULL,
	    AwayTeamID   INT NOT NULL,
        Result       VARCHAR[10],
	    GameDate	 DATE,	
	    FOREIGN KEY (SeasonYear) REFERENCES "Season" (Year),
	    FOREIGN KEY (HomeTeamId) REFERENCES "Team" (Id),
	    FOREIGN KEY (AwayTeamId) REFERENCES "Team" (Id)
);

CREATE TABLE IF NOT EXISTS "StatType" (
        ID           VARCHAR[5] NOT NULL PRIMARY KEY,
        Description  VARCHAR[30]
);

CREATE TABLE IF NOT EXISTS "StatInfo" (
        ID           INT NOT NULL PRIMARY KEY,
        StatValue    INT NOT NULL,
        PlayerID     INT NOT NULL,
        GameID       INT NOT NULL,
        Type         VARCHAR[5] NOT NULL,
                
        FOREIGN KEY (PlayerId) REFERENCES "Player" (Id),
        FOREIGN KEY (GameId) REFERENCES "Game" (Id),
        FOREIGN KEY (Type) REFERENCES "StatType" (Id)
);

CREATE TABLE IF NOT EXISTS "TeamInSeason" (
        SeasonId     INT NOT NULL,
        TeamId       INT NOT NULL,
                
        PRIMARY KEY (SeasonId, TeamId),
        FOREIGN KEY (SeasonId) REFERENCES "Season" (Year),
        FOREIGN KEY (TeamId) REFERENCES "Team" (Id)
);