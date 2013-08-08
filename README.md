TSAR
====

Tsar is a management system designed for a particular Search and Rescue unit in Iceland. It may eventually be of use to others who have to manage members, groups, events and inviations to those events.

Setting up a development environment
------------------------------------

Create a virualenv for the git repository:
```bash
virualenv tsar-zmjbs
```
or whatever you want to call it. Move into the virualenv, activate it and then clone the git repository:
```bash
cd tsar-zmjbs
source bin/activate
git clone https://github.com/ZmjbS/tsar.git
```
Then move into the repository and install the necessary packages:
```bash
cd tsar
pip install -r requirements.txt
```
You're now ready to run the code, though you're still missing the database. You can start your own or download the showcase one:
```bash
wget http://tsar.swift.is/sqlite3.db
```

Now you're ready to fire up the development server and play around. Run:
```bash
python manage.py runserver
```
and open a browser at http://127.0.0.1:8000
