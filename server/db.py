import sqlite3

class leaderBoard:
    def __init__(self, dbPath):
        print(dbPath)
        try:
            open(dbPath, 'x').close()
        except:
            pass
        self.conn = sqlite3.connect(dbPath, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_leaderboard("normal")
        self.create_leaderboard("hard")
        self.create_leaderboard("extreme")

    def create_leaderboard(self, name):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS leaderboard_{name} (name TEXT, score INTEGER)")
        self.conn.commit()

    def add_score(self, difficulty, name, score):
        self.cursor.execute(f"INSERT INTO leaderboard_{difficulty} (name, score) VALUES (?, ?)", (name, score))
        self.conn.commit()
    
    def get_top_scores(self, difficulty, limit=5):
        self.cursor.execute(f"SELECT name, score FROM leaderboard_{difficulty} ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()
    
    def get_top_scores_dict(self, difficulty, limit=5):
        difficulties = []
        if difficulty == "all": difficulties = ["normal","hard", "extreme"]
        else: difficulties = [difficulty]

        scoreDict = {}
        for diff in difficulties:
            scores = self.get_top_scores(diff, limit)
            
            for i in range(len(scores)):
                scoreDict[f"{diff}_name_{i+1}"] = scores[i][0]
            for i in range(len(scores)):
                scoreDict[f"{diff}_score_{i+1}"] = scores[i][1]

        return scoreDict
    
    def get_position(self, difficulty, score):
        self.cursor.execute(f"SELECT COUNT(*) FROM leaderboard_{difficulty} WHERE score > ?", (score,))
        return self.cursor.fetchone()[0] + 1
    