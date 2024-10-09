import sqlite3


class CodeDatabase:
    """Tools for interacting with the Pythoness sqllite database"""

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        """Creates a new 'prompt_code' table if one doesn't exist"""
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

    def insert_code(self, prompt: str, code: str) -> None:
        """Inserts (prompt, code) into the table"""
        self.cursor.execute(
            "INSERT INTO prompt_code (prompt, code) VALUES (?, ?)", (prompt, code)
        )
        self.connection.commit()

    def delete_code(self, prompt: str) -> None:
        """Deletes any instances where prompt = prompt"""
        self.cursor.execute("DELETE FROM prompt_code WHERE prompt = ?", (prompt,))
        self.connection.commit()

    def get_code(self, prompt: str) -> None:
        """Gets the first instance of code corresponding to prompt"""
        self.cursor.execute("SELECT code FROM prompt_code WHERE prompt = ?", (prompt,))
        row = self.cursor.fetchone()
        self.connection.commit()
        if row is not None:
            return row[0]
        else:
            return None
