import random
import string
import sys

from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QApplication

from PhoneBook.main import db_connect


def random_string_generator(length=10):
    chars = string.ascii_uppercase + string.ascii_lowercase
    while True:
        yield ''.join(random.choice(chars) for _ in range(length))


if __name__ == "__main__":
    N_RECORDS = 50

    app = QApplication(sys.argv)
    db_connect()

    insertDataQuery = QSqlQuery()
    insertDataQuery.prepare(
        """
        INSERT INTO contatti (
            nome,
            cognome,
            indirizzo, 
            telefono,
            eta
        )
        VALUES (?, ?, ?, ?, ?)
        """
    )

    # Sample data
    data = [
        (next(random_string_generator()),
         next(random_string_generator()),
         next(random_string_generator()),
         next(random_string_generator()),
         random.randint(0, 255))
        for _ in range(N_RECORDS)
    ]

    for (nome, cognome, indirizzo, telefono, eta) in data:
        insertDataQuery.addBindValue(nome)
        insertDataQuery.addBindValue(cognome)
        insertDataQuery.addBindValue(indirizzo)
        insertDataQuery.addBindValue(telefono)
        insertDataQuery.addBindValue(eta)

        insertDataQuery.exec()
