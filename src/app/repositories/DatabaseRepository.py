from sqlite3 import Connection
from typing import Dict, Optional

from app.Database import Database
from app.DatabaseLoadingException import DatabaseLoadingException
from app.inputValidator.InputValidator import InputValidator
from app.inputValidator.ValidationError import ValidationError
from app.utils import tr
from app.validatable.CorpusPath import CorpusPath
from app.validatable.DatabaseNGramLengths import DatabaseNGramLengths
from app.validatable.DatabaseName import DatabaseName
from app.validatable.DatabasePath import DatabasePath
from app.validatable.Id import Id


class DatabaseRepository:

    def __init__(self, connection: Connection):
        self._connection = connection

    def save(self, database: Database) -> Optional[Id]:
        if database.getId() is None:
            return self._insert(database)
        else:
            self._update(database)
            return None

    def _update(self, database: Database) -> None:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            UPDATE 
                databases 
            SET 
                name = ?, 
                path = ?,
                corpus_path = ?,
                ngram_min_length = ?, 
                ngram_max_length = ?
            WHERE
                id = ?
            """
            ,
            (
                str(database.getName()),
                str(database.getPath()),
                str(database.getCorpusPath()),
                database.getNGramMinLength(),
                database.getNGramMaxLength(),
                database.getId().asInt()
            ))

        self._connection.commit()
        cursor.close()

    def _insert(self, database: Database) -> Id:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT INTO databases 
                (name, path, corpus_path, ngram_min_length, ngram_max_length)
            VALUES
                (?, ?, ?, ?, ?)
            """
            ,
            (
                str(database.getName()),
                str(database.getPath()),
                str(database.getCorpusPath()),
                database.getNGramMinLength(),
                database.getNGramMaxLength()
            ))

        self._connection.commit()
        cursor.close()

        return Id(cursor.lastrowid)

    def findAllNames(self) -> Dict[Id, DatabaseName]:
        databases: Dict[Id, DatabaseName] = {}
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name FROM databases ORDER BY name")

        for row in cursor:
            databases[Id(row["id"])] = DatabaseName(row["name"])

        cursor.close()

        return databases

    def count(self) -> int:
        return len(self.findAllNames())

    def findById(self, id: Id) -> Optional[Database]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM databases WHERE id = ?", [id.asInt()])

        row = cursor.fetchone()

        if not row:
            return None

        return self._createFromRow(row)

    def existsByName(self, name: DatabaseName) -> bool:
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM databases WHERE name = ?", [str(name)])

        return cursor.fetchone() is not None

    def validateName(self, name: str, inputValidator: InputValidator, checkNameExists: bool) -> Optional[DatabaseName]:
        name: Optional[DatabaseName] = inputValidator.validate(
            lambda: DatabaseName(name)
        )

        if checkNameExists and self.existsByName(name):
            errorMsg = tr("A database with the name '{}' already exists.") \
                .format(str(name))
            inputValidator.addError(errorMsg)

        return name

    def _createFromRow(self, row) -> Optional[Database]:
        try:
            return Database(
                Id(row["id"]),
                DatabaseName(row["name"]),
                DatabasePath(row["path"]),
                CorpusPath(row["corpus_path"]),
                DatabaseNGramLengths(row["ngram_min_length"], row["ngram_max_length"])
            )
        except ValidationError as error:
            errorMessage = str(error) + tr(
                " If you have moved the database file to a different location, you may either move it back the original"
                " position (see \"Database Path\" below), import it again, or generate a new database from the related "
                "corpus. Clicking \"Delete Database\" will only delete the record kept by the GUI about this database."
            )
            raise DatabaseLoadingException(errorMessage, row["name"], row["path"], row["corpus_path"])

    def deleteById(self, databaseId: Id) -> None:
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM databases WHERE id = ?", [databaseId.asInt()])

        self._connection.commit()
        cursor.close()

    def findNameByDatabasePath(self, path: DatabasePath) -> Optional[str]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT name FROM databases WHERE path = ?", [str(path)])

        row = cursor.fetchone()

        if not row:
            return None

        return row["name"]

    def deleteByDatabasePath(self, path: DatabasePath) -> None:
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM databases WHERE path = ?", [str(path)])

        self._connection.commit()
        cursor.close()
