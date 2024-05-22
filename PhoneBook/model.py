# -*- coding: utf-8 -*-

"""Model to manage the contatti table."""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel


class Persona:
    def __init__(self, nome, cognome, indirizzo, telefono, eta):
        self.nome = nome
        self.cognome = cognome
        self.indirizzo = indirizzo
        self.telefono = telefono
        self.eta = eta

    def __str__(self):
        return (f"Nome: {self.nome}\nCognome: {self.cognome}\nIndirizzo: {self.indirizzo}\nTelefono: {self.telefono}"
                f"\nEtà: {self.eta}")


class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        tableModel.setTable("contatti")
        tableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        tableModel.select()
        headers = ("id", "nome", "cognome", "indirizzo", "telefono", "eta")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel

    def updateDBRow(self, row_index, persona):
        column = 1
        for field_name, field_value in persona.__dict__.items():
            if field_value:
                self.model.setData(self.model.index(row_index, column), field_value)
            else:
                self.model.setData(self.model.index(row_index, column), None)
            column += 1

    def addContact(self, persona):
        """Add a contact to the database."""
        row_index = self.model.rowCount()
        self.model.insertRows(row_index, 1)
        self.updateDBRow(row_index, persona)

        self.model.submitAll()
        self.model.select()

    def editContact(self, selectedRow, persona):
        """Edit selected contact in the database."""
        self.updateDBRow(selectedRow, persona)

        self.model.submitAll()
        self.model.select()

    def deleteContact(self, selectedRow):
        """Delete selected contact from the database."""
        self.model.removeRow(selectedRow)

        self.model.submitAll()
        self.model.select()
