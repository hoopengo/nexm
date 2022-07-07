import sqlite3
from typing import Any


class Handler:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self._connect()

    def _connect(self):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS markets(
                id INTEGER PRIMARY KEY,
                inter_id BIGINT NOT NULL,
                expired BIGINT NOT NULL
            );
            """

            cursor.executescript(query)

    def insert(self, inter_id: int, expired: int) -> bool:
        try:
            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()

            # Check for in db
            cursor.execute("SELECT inter_id FROM markets WHERE inter_id = ?", [inter_id])
            if cursor.fetchone() is None:
                # Insert to db
                cursor.execute(
                    "INSERT INTO markets(inter_id, expired) VALUES(?,?)",
                    [inter_id, expired],
                )
                db.commit()

                return True

            return False

        except Exception:
            return None

        finally:
            cursor.close()
            db.close()

    def fetch(self, inter_id: int) -> Any:
        try:
            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()

            cursor.execute("SELECT inter_id FROM markets WHERE inter_id = ?", [inter_id])
            return cursor.fetchone()

        except Exception:
            return None

        finally:
            cursor.close()
            db.close()

    def fetchall(self) -> Any:
        try:
            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()

            cursor.execute("SELECT * FROM markets")
            return cursor.fetchall()

        except Exception:
            return None

        finally:
            cursor.close()
            db.close()

    def remove(self, inter_id: int) -> bool:
        try:
            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()

            # Check for in db
            cursor.execute("SELECT inter_id FROM markets WHERE inter_id = ?", [inter_id])
            if cursor.fetchone() is not None:
                cursor.execute(
                    "DELETE FROM markets WHERE inter_id = ?",
                    [inter_id],
                )
                db.commit()

                return True

            return False

        except Exception:
            return None

        finally:
            cursor.close()
            db.close()
