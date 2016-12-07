# SQL query that led to the table in my database. Wanted to make sure that it got saved incase I ever wondered how columns were calculated.

cur.execute("""
                SELECT playerid, 
                        AVG(age) AS "AGE", 
                        AVG("GS")/AVG("GP") AS "% GS", 
                        AVG("MIN")/AVG("GP") AS "MIN/G", 
                        AVG("FGA")/AVG("MIN") AS "FGA/MIN",
                        AVG("FG%") AS "FG%", 
                        AVG("3PA")/AVG("MIN") AS "3PA/MIN", 
                        AVG("3P%") AS "3P%", 
                        AVG("FTA")/AVG("MIN") AS "FTA/MIN", 
                        AVG("FT%") AS "FT%", 
                        AVG("ORB")/AVG("MIN") AS "ORB/MIN", 
                        AVG("DRB")/AVG("MIN") AS "DRB/MIN", 
                        AVG("TRB")/AVG("MIN") AS "TRB/MIN", 
                        AVG("AST")/AVG("MIN") AS "AST/MIN", 
                        AVG("STL")/AVG("MIN") AS "STL/MIN", 
                        AVG("BLK")/AVG("MIN") AS "BLK/MIN", 
                        AVG("PF")/AVG("MIN") AS "PF/MIN", 
                        AVG("TOV")/AVG("MIN") AS "TOV/MIN", 
                        AVG("PTS")/AVG("MIN") AS "PTS/MIN", 
                        AVG("TS%") AS "TS%", 
                        AVG("ORB%") AS "ORB%", 
                        AVG("DRB%") AS "DRB%", 
                        AVG("TRB%") AS "TRB%", 
                        AVG("AST%") AS "AST%", 
                        AVG("TOV%") AS "TOV%", 
                        AVG("STL%") AS "STL%", 
                        AVG("BLK%") AS "BLK%",
                        AVG("USG%") AS "USG%", 
                        AVG("PPR") AS "PPR", 
                        AVG("ORtg") AS "ORtg", 
                        AVG("DRtg") AS "DRtg", 
                        AVG("PER") AS "PER"  
                FROM prenbastats2003to2012
                GROUP BY playerid
            """)