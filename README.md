# StuffNetwork

Basic college project by basic college kids ayyyy lmao.
A basic social network for CS3200 Database Design Final Project, by Kyle Alpert and Kurt Marcinkiewicz.

## Installation

If using virtualenv:
```
virtualenv --no-site-packages --distribute {path to env} && source {path to env}/bin/activate && pip install -r requirements.txt
```
IDEs such as pycharm can facilitate the above for you. Requirements.txt is provided for your convenience.

Once downloaded, run __init__.py to setup config file.

Before making any changes, make sure virtualenv is installed and you're working in the environment contained in env/

## Usage

Make sure mysql is running.

Run app.py.

Default app runs at localhost:5000

## Troubleshooting
Error:
```
Python mysqldb: Library not loaded: libmysqlclient.18.dylib
```

Solution:
```
sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib /Library/Python/2.7/site-packages/_mysql.so
```