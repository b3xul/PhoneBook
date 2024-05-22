# Installation instructions

```bash
# Install Python3.11 and MySql8.0
sudo apt-get install python3.11 python3.11-venv mysql-server

# Clone the repository (or unzip the project)
git clone git@github.com:b3xul/PhoneBook.git
cd PhoneBook

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install PyQt6 required library
python3.11 -m pip install -r requirements.txt

# Make PhoneBook.py executable
chmod +x PhoneBook.py

# Paste credenziali_database.properties file into folder (not required if project was unzipped)
# Substitute credenziali_database.properties in MySql
# Execute schema_database.sql to create and populate "contatti" table

# Double click PhoneBook.py or execute it from the command line to launch the application
./PhoneBook.py
```

# Usage notes

It is possible to deselect the selected row by using Ctrl+Click on the row.

# Implementation notes

The Graphical User Interface was created using the PyQt6 library, trying to mimic the requirements written for Java
SWING.
All mandatory requirements + extra requirements 3,4,5 were implemented.
