import sqlite3

class CodeDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    # SQL is maybe overkill? I don't know how cost efficient this is
    def create_table(self):
        # can't I make this into one execute call?
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prompt_code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                code TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS index_prompt ON prompt_code (prompt)
            """
        )
        self.connection.commit()


    def insert_code(self, prompt, code):
        self.cursor.execute(   
            "INSERT INTO prompt_code (prompt, code) VALUES (?, ?)", (prompt, code)
        )
        self.connection.commit()

    def delete_code(self, prompt):
        self.cursor.execute(
            "DELETE FROM prompt_code WHERE prompt = ?", (prompt,)
        )
        self.connection.commit()

    def get_code(self, prompt):
        self.cursor.execute(
            "SELECT code FROM prompt_code WHERE prompt = ?", (prompt,)                
        )
        row = self.cursor.fetchone()
        self.connection.commit()
        if row is not None:
            return row[0]
        else:
            return None
        
    def close(self):
        self.connection.close()
