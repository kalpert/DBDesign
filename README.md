# Project Name

A basic social network for CS3200 Database Design Final Project, by Kyle Alpert and Kurt Marcinkiewicz.

## Installation

Dependencies: flask, flask-mysql

Once downloaded, run __init__.py to setup config file.

## Usage

Make sure mysql is running.

Run app.py.

Default app runs at localhost:5000

## Troubleshooting
Error:
Python mysqldb: Library not loaded: libmysqlclient.18.dylib
Solution:
sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib /Library/Python/2.7/site-packages/_mysql.so
