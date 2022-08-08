from logging import Logger
from sqlite3 import Connection
from typing import List

from app.Database import Database
from app.validatable.ResultPath import ResultPath
from app.ResultType import ResultType
from app.inputValidator.ValidationError import ValidationError


class ResultRepository:

    def __init__(self, connection: Connection):
        self.__connection = connection

    def save(self, database: Database, resultPath: ResultPath, resultType: ResultType) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT 1 FROM results WHERE database_id = ? AND path = ?",
            (database.getId().asInt(), str(resultPath),)
        )

        # update the type if the path already exists.
        if cursor.fetchone():
            cursor.execute(
                "UPDATE results SET type = ? WHERE database_id = ? AND path = ?",
                (resultType.value, database.getId().asInt(), str(resultPath),)
            )
            self.__connection.commit()
            return

        # insert the result path.
        cursor.execute(
            """
            INSERT INTO results  (database_id, path, type) VALUES (?, ?, ?)
            """,
            (
                database.getId().asInt(),
                str(resultPath),
                resultType.value
            )
        )

        self.__connection.commit()
        cursor.close()

    def findTwoMostRecentForSuppliedIntersect(self, database: Database) -> List[ResultPath]:
        results: List[ResultPath] = []
        cursor = self.__connection.cursor()
        cursor.execute(
            """
            SELECT path FROM results WHERE database_id = ? AND type in (?, ?) ORDER BY created DESC
            """,
            (
                database.getId().asInt(),
                ResultType.INTERSECT.value,
                ResultType.DIFFERENCE.value
            )
        )

        for row in cursor:
            path = row["path"]

            try:
                resultPath = ResultPath(path)
                results.append(resultPath)
            except ValidationError:
                continue

            if len(results) == 2:
                break

        cursor.close()

        return results