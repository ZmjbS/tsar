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
You're now ready to generate the database (you want to use this opportunity to create an admin user) and load some initial data from the available fixtures:
```bash
python manage.py syncdb
```
Log in, create a member for yourself and any other member that you want to be able to log into the development system. Then dump their data into a json fixture so that you can load that over the dummy members.
```bash
python manage.py dumpdata auth.user members.member > fixtures/actual-members.json
```
Now we can load the fixtures:
```bash
python manage.py loaddata fixtures/showcase-events_metadata.xml
python manage.py loaddata showcase_events.xml

python manage.py loaddata fixtures/showcase-members_metadata.xml
python manage.py loaddata fixtures/showcase-3h-user_member.xml
python manage.py loaddata fixtures/actual-members.json

python manage.py loaddata fixtures/showcase-groups.group.xml
python manage.py loaddata fixtures/showcase-groups.membership.json
```

Now you're ready to fire up the development server and play around. Run:
```bash
python manage.py runserver
```
and open a browser at http://127.0.0.1:8000/admin/ . Log in, create a member that points to the user you created when you sync-ed the database. Then point the browser to http://127.0.0.1:8000/ and off you go...
