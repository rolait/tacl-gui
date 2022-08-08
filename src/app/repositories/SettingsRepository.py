from sqlite3 import Connection
from typing import Optional

from app.validatable.Id import Id
from app.Settings import Settings


class SettingsRepository:

    def __init__(self, connection: Connection):
        self.__connection = connection

    def save(self, settings: Settings) -> None:
        cursor = self.__connection.cursor()

        lastSelectedDatabaseId = None
        if settings.getLastSelectedDatabaseId() is not None:
            lastSelectedDatabaseId = settings.getLastSelectedDatabaseId().asInt()

        cursor.execute("DELETE FROM settings")
        cursor.execute(
            """
            INSERT INTO settings VALUES(?, ?, ?)
            """,
            (
                lastSelectedDatabaseId,
                settings.getLastOpenPath(),
                settings.getLastSavePath()
            )
        )

        self.__connection.commit()
        cursor.close()

    def find(self) -> Settings:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM settings LIMIT 1")

        row = cursor.fetchone()

        # return default settings in case no settings are stored in the database.
        if not row:
            return Settings(
                None, "", ""
            )

        lastSelectedDatabaseId: Optional[Id] = \
            None if row["last_selected_database_id"] is None else Id(row["last_selected_database_id"])

        return Settings(
            lastSelectedDatabaseId,
            row["last_open_path"],
            row["last_save_path"]
        )
