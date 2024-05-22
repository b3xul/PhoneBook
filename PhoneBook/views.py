# -*- coding: utf-8 -*-

"""Views to manage the contatti table."""

from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (QMainWindow, QWidget, QTableView, QMessageBox, QVBoxLayout, QToolBar, QDialog, QLineEdit,
                             QFormLayout, QDialogButtonBox, QAbstractItemView, QLabel)

from PhoneBook import APPLICATION_NAME
from .model import ContactsModel, Persona


def setupButtons(parent, acceptText, rejectText):
    buttonsBox = QDialogButtonBox(parent)
    buttonsBox.setOrientation(Qt.Orientation.Horizontal)
    buttonsBox.addButton(acceptText, QDialogButtonBox.ButtonRole.AcceptRole)
    buttonsBox.addButton(rejectText, QDialogButtonBox.ButtonRole.RejectRole)
    buttonsBox.accepted.connect(parent.accept)
    buttonsBox.rejected.connect(parent.reject)
    return buttonsBox


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APPLICATION_NAME}")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.contactsModel = ContactsModel()

        self.table = None
        self.table_columns = ["nome", "cognome", "telefono"]
        self.toolBar = None
        self.actionAdd = None
        self.actionEdit = None
        self.actionDelete = None
        self.editorWindow = None
        self.setupMainWindow()

    def setupMainWindow(self):

        self.setupToolbar()
        self.addToolBar(self.toolBar)

        self.setupTable()
        self.layout.addWidget(self.table)

        self.resize(450, 450)

    def setupTable(self):
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setCurrentIndex(QModelIndex())

        # Hide columns based on field names
        record = self.contactsModel.model.record()
        fields_count = record.count()
        for i in range(fields_count):
            field_name = record.fieldName(i)
            if field_name not in self.table_columns:
                self.table.setColumnHidden(i, True)
        self.table.resizeColumnsToContents()

    def setupToolbar(self):
        self.toolBar = QToolBar()
        self.toolBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        buttonIconPath = "PhoneBook/resources/nuovo_icon.png"
        buttonText = "nuovo"
        self.actionAdd = QAction(QIcon(buttonIconPath), buttonText, self.toolBar)
        self.actionAdd.triggered.connect(lambda: self.openEditorDialog("add"))
        self.toolBar.addAction(self.actionAdd)

        buttonIconPath = "PhoneBook/resources/modifica_icon.png"
        buttonText = "modifica"
        self.actionEdit = QAction(QIcon(buttonIconPath), buttonText, self.toolBar)
        self.actionEdit.triggered.connect(lambda: self.openEditorDialog("edit"))
        self.toolBar.addAction(self.actionEdit)

        buttonIconPath = "PhoneBook/resources/elimina_icon.png"
        buttonText = "elimina"
        self.actionDelete = QAction(QIcon(buttonIconPath), buttonText, self.toolBar)
        self.actionDelete.triggered.connect(lambda: self.openDeleteDialog())
        self.toolBar.addAction(self.actionDelete)

    def openEditorDialog(self, mode):
        """Open the Contact Editor dialog."""
        selectedRow = self.table.selectionModel().selectedIndexes()[
            0].row() if self.table.selectionModel().selectedIndexes() else None
        if mode == "edit" and selectedRow is None:
            QMessageBox.warning(
                self,
                f"{APPLICATION_NAME}",
                "Per modificare è necessario prima selezionare una persona!",
            )
            return

        edit_dialog = EditorDialog(mode, selectedRow, self.contactsModel)

        if edit_dialog.exec() == QDialog.DialogCode.Accepted:
            if mode == "add":
                self.contactsModel.addContact(edit_dialog.currentPersona)
            elif mode == "edit":
                self.contactsModel.editContact(selectedRow, edit_dialog.currentPersona)
            self.table.resizeColumnsToContents()

    def openDeleteDialog(self):
        """Open the Contact Delete dialog."""
        selectedRow = self.table.selectionModel().selectedIndexes()[
            0].row() if self.table.selectionModel().selectedIndexes() else None
        if selectedRow is None:
            QMessageBox.warning(
                self,
                f"{APPLICATION_NAME}",
                "Per eliminare è necessario prima selezionare una persona!",
            )
            return

        delete_dialog = DeleteConfirmationDialog(selectedRow, self.contactsModel)
        if delete_dialog.exec() == QDialog.DialogCode.Accepted:
            self.contactsModel.deleteContact(selectedRow)
            self.table.resizeColumnsToContents()


class EditorDialog(QDialog):
    def __init__(self, mode, selectedRow, contactsModel, parent=None):
        super().__init__(parent=parent)
        self.mode = mode
        self.selectedRow = selectedRow
        self.contactsModel = contactsModel

        self.titles = {"add": "Aggiungi nuovo contatto", "edit": "Modifica contatto"}
        self.setWindowTitle(self.titles[self.mode])

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # dict[formName]: QLineEdit
        self.forms = {}
        self.currentPersona = None

        self.formLayout = None
        self.buttonsBox = None

        self.setupEditorDialog()
        self.adjustSize()

    def setupEditorDialog(self):
        self.formLayout = self.setupForms()
        self.layout.addLayout(self.formLayout)

        self.buttonsBox = setupButtons(self, "salva", "annulla")
        self.layout.addWidget(self.buttonsBox)

    def setupForms(self):
        formLayout = QFormLayout()

        record = self.contactsModel.model.record()
        fields_count = record.count()

        for field_index in range(fields_count):
            field_name = record.fieldName(field_index)
            if field_name != "id":
                form = self.setupForm(field_name, field_index)
                form_name = field_name.capitalize()
                self.forms[form_name] = form
                formLayout.addRow(form_name, form)
        return formLayout

    def setupForm(self, formName, field_index):
        form = None
        if self.mode == "add":
            form = QLineEdit()
        elif self.mode == "edit":
            field_data = self.contactsModel.model.index(self.selectedRow, field_index).data()
            if field_data == b"\x00":
                # Handle empty fields
                form = QLineEdit()
            else:
                form = QLineEdit(str(field_data))
        form.setObjectName(formName)
        return form

    def accept(self):
        """Accept the data provided through the dialog."""

        if not self.validateForms():
            return

        # Valid form
        super().accept()

    def validateForms(self):

        formName = "Nome"
        nome = formContent = self.forms[formName].text()
        if len(formContent) == 0 or (not all(char.isalpha() or char.isspace() for char in formContent)):
            self.invalidForm(formName)
            return False

        formName = "Cognome"
        cognome = formContent = self.forms[formName].text()
        if len(formContent) == 0 or (not all(char.isalpha() or char.isspace() for char in formContent)):
            self.invalidForm(formName)
            return False

        # No validation for Indirizzo
        formName = "Indirizzo"
        indirizzo = self.forms[formName].text()

        formName = "Telefono"
        telefono = formContent = self.forms[formName].text()
        if len(formContent) == 0 or (not all(char in "0123456789 +" for char in formContent)):
            self.invalidForm(formName)
            return False

        formName = "Eta"
        eta = formContent = self.forms[formName].text()
        if len(formContent) > 0 and (not formContent.isdigit() or int(formContent) < 0 or int(formContent) > 255):
            self.invalidForm(formName)
            return False

        # All fields are valid
        self.currentPersona = Persona(nome, cognome, indirizzo, telefono, eta)
        return True

    def invalidForm(self, formName):
        QMessageBox.warning(
            self,
            f"{APPLICATION_NAME}",
            f"Campo {formName} non valido!",
        )


class DeleteConfirmationDialog(QDialog):
    def __init__(self, selectedRow, contactsModel, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(f"Elimina contatto")

        self.selectedRow = selectedRow
        self.contactsModel = contactsModel

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.messageLabel = None
        self.buttonsBox = None

        self.setupDeleteConfirmationDialog()
        self.adjustSize()

    def setupDeleteConfirmationDialog(self):

        self.messageLabel = self.setupMessageLabel()
        self.layout.addWidget(self.messageLabel)

        self.buttonsBox = setupButtons(self, "si", "no")
        self.layout.addWidget(self.buttonsBox)

    def setupMessageLabel(self):
        record = self.contactsModel.model.record()
        fields_count = record.count()

        nome = None
        cognome = None
        for field_index in range(fields_count):
            field_name = record.fieldName(field_index)
            if field_name == "nome":
                nome = str(self.contactsModel.model.index(self.selectedRow, field_index).data())
            elif field_name == "cognome":
                cognome = str(self.contactsModel.model.index(self.selectedRow, field_index).data())

            if nome is not None and cognome is not None:
                break

        return QLabel(f"Eliminare la persona {nome} {cognome}?")
