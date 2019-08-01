allmychanges.com
================

[![Join the chat at https://gitter.im/AllMyChanges/allmychanges.com](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/AllMyChanges/allmychanges.com?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A project for Django Dash 2013

How to setup
------------

    $ sudo apt-get install mysql-server redis-server python-dev libxml2-dev libxslt1-dev logtail
    $ chmod +x scripts/create-env.sh
    $ scripts/create-env.sh
    $ source env/bin/activate
    $ echo 'SECRET_KEY = "some really secret string"' > secure_settings.py
    $ chmod +x manage.py
    $ sudo mkdir -p /var/log/allmychanges
    $ sudo chmod 777 /var/log/allmychanges
    $ sudo mkdir -p /var/log/logster
    $ sudo chmod 777 /var/log/logster
    $ sudo mkdir -p /var/run/logster
    $ sudo chmod 777 /var/log/logster
    $ ./manage.py syncdb --migrate
    $ ./manage.py runserver 0.0.0.0:8000
    $ # and in other console
    $ ./manage.py rqworker

Maybe you need to create mysql database before `./manage.py syncdb --migrate`. Run `mysql -uroot`:

    mysql> CREATE DATABASE allmychanges CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    mysql> GRANT ALL ON allmychanges.* TO `allmychanges`@`localhost` IDENTIFIED BY 'allmychanges';

In production you will need additional steps like:

    $ sudo mkdir -p /var/www/.ssh
    $ sudo chown www-data:www-data /var/www/.ssh
    $ sudo -u www-data ssh-keygen
    $ cat /var/www/.ssh/id_rsa.pub
    $ echo "Now create a new GitHub account and put this ssh key there."
