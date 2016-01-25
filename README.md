TSAR
====

Tsar is a management system designed for a particular Search and Rescue unit in Iceland. It may eventually be of use to others who have to manage members, groups, events and inviations to those events.

Requirements
------------

* virtualenvwrapper
* pip
* python 3
* git

Setting up a development environment
------------------------------------

For a primer on virtualenvwrapper and generally setting up a Django project, see: [Starting a Django 1.6 Project the Right Way](https://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/). This is pretty much how TSAR was set up. With a few exceptions: The functionality of South is now in the Django code and we're not using any tools to deploy or test (so no Frabric or automated tests, either).

Create a virualenv for the git repository:
```bash
mkvirualenv tsar
```
or whatever you want to call it. This will set up a virtual environment stored in `~/.virtualenv/`. This will also activate the virtual environment but later you can do so with the command
```bash
workon tsar
```
Move to where you wish to store your development work and then clone the git repository:
```bash
cd devel/
git clone https://github.com/ZmjbS/tsar.git
```
Then move into the repository and install the necessary packages:
```bash
cd tsar
pip install -r requirements.txt
```
You're now ready to generate the database, create an admin user and load some initial data from the available fixtures. First the database and superuser:
```bash
python manage.py migrate
python manage.py createsuperuser
```
Then load some member metadata and fire up the development server:
```bash
python manage.py loaddata fixtures/showcase-members_metadata.xml
python manage.py runserver
```
Now point a browser to http://127.0.0.1:8000/admin/ and log in with the username and password you created before. Create a member for yourself and any other member that you want to be able to log into the development system. You can also take the opportunity to modify the user object that you created before.

Before loading the rest of the data, dump the users into a json fixture so that you can load that on top of the dummy members.
```bash
python manage.py dumpdata auth.user members.member > fixtures/develop-members.json
```
Finally we can load the showcase fixtures:
```bash
python manage.py loaddata fixtures/showcase-events_metadata.xml
python manage.py loaddata fixtures/showcase-events.xml

python manage.py loaddata fixtures/showcase-3h-user_member.xml
python manage.py loaddata fixtures/develop-members.json

python manage.py loaddata fixtures/showcase-groups.group.xml
python manage.py loaddata fixtures/showcase-groups.membership.json
```

I hope all went well because that's it. You're now ready to fire up the development server (if it's not still running) and play around. Run:
```bash
python manage.py runserver
```
Point the browser to http://127.0.0.1:8000/ and off you go...

Setting up a production environment with apache2
------------------------------------------------

...
