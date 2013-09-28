allmychanges.com
================

A project for Django Dash 2013

How to setup
------------

    $ chmod +x scripts/create-env.sh
    $ scripts/create-env.sh
    $ source env/bin/activate
    $ echo 'SECRET_KEY = "some really secret string"' > secure_settings.py
    $ chmod +x manage.py
    $ ./manage.py syncdb --migrate
    $ ./manage.py runserver 0.0.0.0:8000

Maybe you need to create mysql database before `./manage.py syncdb --migrate`. Run `mysql -uroot`:

    mysql> CREATE DATABASE allmychanges CHARACTER SET utf8 COLLATE utf8_unicode_ci;
    mysql> CREATE USER 'allmychanges'@'localhost' IDENTIFIED BY 'allmychanges';
    mysql> GRANT ALL PRIVILEGES ON allmychanges.* TO 'allmychanges'@'localhost' WITH GRANT OPTION;