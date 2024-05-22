# -*- coding: utf-8 -*-

"""Phone Book application"""

import configparser
import sys

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QApplication, QMessageBox

from PhoneBook import APPLICATION_NAME
from .views import MainWindow


def db_connect():
    config = configparser.ConfigParser()
    config.read('credenziali_database.properties')
    db_properties = config["DatabaseProperties"]

    con = QSqlDatabase.addDatabase("QMYSQL")
    con.setDatabaseName(db_properties["DB_NAME"])
    con.setHostName(db_properties["DB_HOST"])
    con.setPort(int(db_properties["DB_PORT"]))
    con.setUserName(db_properties["DB_USERNAME"])
    con.setPassword(db_properties["DB_PASSWORD"])

    if not con.open():
        QMessageBox.critical(
            None,
            f"{APPLICATION_NAME}",
            f"Unable to connect to {db_properties['DB_NAME']} database\n"
            f"{con.lastError().driverText()}\n{con.lastError().databaseText()}",
        )
        sys.exit(1)


def main():
    app = QApplication(sys.argv)
    db_connect()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
