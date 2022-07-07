import os
import shelve
from datetime import datetime
from typing import Any

from nextcord import Interaction
from nextcord.ext import tasks

from ._db import Handler
from ._defaults import DB_PATH, SQLITE_PATH

markets = Handler(SQLITE_PATH)


@tasks.loop(minutes=2)
async def check_expired_interactions():
    for inter in markets.fetchall():
        if inter[2] - datetime.utcnow().timestamp() < 0:
            os.remove(DB_PATH + str(inter[1]))
            markets.remove(inter[1])


check_expired_interactions.start()


class Market:
    """Market class for contain key-value data by interaction"""

    def __init__(self, interaction: Interaction) -> None:
        self._set_inter(interaction)

        markets.insert(interaction.id, int(interaction.expires_at.timestamp()))

    def get(self, key: str) -> Any:
        """Get value from db by key

        Args:
            key (str): key to locate value

        Returns:
            Any: returns value if exist else None
        """

        if not self._check_valid(key):
            return

        with shelve.open(self.db_path) as db:
            try:
                value = db[key]
            except KeyError:
                return None

            return value

    def remove(self, key: str) -> bool:
        """Remove value from db by key

        Args:
            key (str): key to locate value

        Returns:
            bool: returns True if succes else False
        """

        if not self._check_valid(key):
            return

        with shelve.open(self.db_path, writeback=True) as db:
            try:
                del db[key]
                return True
            except KeyError:
                return False

    def set(self, key: str, value: Any):
        """Set value by key

        Args:
            key (str): key to locate value
            value (Any): value to save
        """

        if not self._check_valid(key):
            return

        with shelve.open(self.db_path, writeback=True) as db:
            db[key] = value

    def update_interaction(self, interaction: Interaction):
        """Update interaction

        for example:
            store = market(interaction)
            interaction.defer()
            store.update_interaction(interaction.followup)

        Args:
            interaction (Interaction): new interaction
        """

        with shelve.open(self.db_path) as old_db:
            self._set_inter(interaction)

            with shelve.open(self.db_path, writeback=True) as db:
                old_db.pop("_id")
                for key in old_db:
                    db[key] = old_db.get(key)

    def _set_inter(self, interaction: Interaction):
        """Update interaction

        Args:
            interaction (Interaction): new interaction
        """

        self.db_path = DB_PATH + str(interaction.id)

        with shelve.open(self.db_path, writeback=True) as db:
            db["_id"] = interaction.id

    def clean(self):
        """Delete database"""

        os.remove(self.db_path)

    def _check_valid(self, key: Any) -> bool:
        """Check for key is valid

        Args:
            key (Any): key for check

        Raises:
            TypeError: key is not a string
            ValueError: key is blank string

        Returns:
            bool: return True if all okay
        """

        if not isinstance(key, str):
            raise TypeError

        if key == "":
            raise ValueError

        return True
