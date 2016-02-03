Installation
============

Requirements
------------
This solution has been tested on Debian 8 "Jessie" server, but any GNU/Linux distribution which can provide basic dependencies should work.

First, you must provide a MySQL database and install pip for Python 3.
::

    apt-get install python3-pip python-dev git build-essential mysql-server libmysqlclient-dev



Then, you must use pip to install the python packages needed for TouSIX-Manager:
::

    pip install git+https://github.com/umbrella-fabric/TouSIX-Manager.git

Or, you can install with any other method (distribution packages for example) the python packages.
Make sure the python environment inclues the packes listed below:
::

        'django >= 1.8, < 1.9',
        'django-bootstrap3==6.2.2',
        'django-debug-toolbar==1.4',
        'django-formtools',
        'django-fsm',
        'django-localflavor',
        'django-sb-admin',
        'django-fsm-admin==1.2.2',
        'django-registration-redux',
        'django-reversion',
        'mysqlclient',
        'requests'

Basic installation
------------------
The only way to obtain TouSIX-Manager is through Github.
If it is not already done, you can use pip to clone and install the package:
::

    pip install git+https://github.com/umbrella-fabric/TouSIX-Manager.git

Or you can build the package from a local repository.


Then, you can use tousix-manager package like a Django application.
A proper way to use this package is to create a new Django project:
::

    django-admin startproject ixp_manager

After that, you can copy the example settings file into your project, and adapt it to your context.

For the url configuration, you can either use the configuration included in the tousix-manager app:
::

    url(r'^manager/', include('tousix-manager.urls'))

Or you can attach directly the views and forge your own URLs.

Before launching the server, initialize your database:
::

    python ./manage.py migrate

Don't forget to create a superuser for modify the models once you start the application:
::

    python ./manage.py createsuperuser

Then, you can launch the Django application by any method proposed on the Django official website.
Here is an example with the included web server:
::

    python ./manage.py runserver 8000

After running Django you will be able to access the web gui interface to start adding the first IXP member router to the fabric.

Use Ryu apps
------------
If you want to run the Ryu applications used in the TouSIX project, all the files are in the ryu-apps folder.

You will need Ryu and requests python packages to launch these applications :
::

    pip install ryu requests

It is possible to launch all the applications in one instance. Here is a launch command example :
::

    ryu-manager --config-file ./ryu-apps/ryu.conf --verbose ./ryu-apps/send_event_async.py ./ryu-apps/ofctl_rest_tousix.py ./ryu-apps/stateful_ctrl.py ./ryu-apps/send_stats.py