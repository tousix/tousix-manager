# TouSIX-Manager

Welcome to the TouSIX-Manager project.

Overview
--------

The name TouSIX comes from Toulouse SDN Internet eXchange.

The TouSIX-Manager is an Python application to run with ryu-manager and Django framework for automating openflow generation and BIRD router server configuration. 

An statistic collector and web graphic renderer it also present allowing the IXP member to visualized in details the amount of traffic exchanged  with their peers. 

The TouSIX-Manager has been designed to run on the Toulouse Internet eXchange at the beginning and could be easily extended to run Umbrella Fabric on other IXP topology.

The figure below show the actual TouSIX deployment with 3 PoPs with each an Pica8 P-3290 and separated OpenFlow control channel network. Any OpenFlow 1.3 switch hardware or software could be used in theory. 

TouSIX is running in production with Pica8 whitebox OpenFlow switch with PicOS 2.6 in OpenVSwitch mode. We have chosen PicOS 2.6 because it is able to maintain the last OpenFlow table state even after a reboot or a power outage even is there is no OpenFlow controller reachable. 



<img src="http://195.154.106.70/topo_touSIX.021.png" title="Topology of TouSIX" width="600" height="500" />

*Software architecture*

<img src="http://195.154.106.70/soft_archi_tousix.001.png" title="TouSIX software architecture" width="600" height="500" />

    
Installation
------------

This solution has been tested on Debian 8 "Jessie" server, but any GNU/Linux distribution which can provide basic dependencies should work.

First, you must provide a MySQL database and install pip for Python 3.


    apt-get install python3-pip build-essentials mysql-server mysql-client


Then, you must use pip to install the python packages needed for TouSIX-Manager:
    
    pip install -e https://github.com/umbrella-fabric/TouSIX-Manager.git

It is possible to create a new django project to automate some procedures:

    django-admin startproject ixp-manager

Copy the settings.py given in the tousix-manager package into your project settings, and customize it following your needs.

Include the tousix-manager URLconf in urls.py:

    url(r'^manager/', include('tousix-manager.urls'))

Before launching the server, you need do initialize the database :

    python ./manage.py migrate
    
Then, you can launch the Django application by any method proposed on the Django official website.
Here is an example with the included web server:

    python ./manage.py runserver 8000

After running Django you will be able to access the web gui interface to start adding the first IXP member router to the fabric.
More documentation and screenshot will be added soon.

### Ryu apps

If you want to run the Ryu applications used in the TouSIX project, all the files are in the ryu-apps folder.

You will need Ryu and requests python packages to launch these applications :

    pip install ryu requests

It is possible to launch all the applications in one instance. Here is a launch command example :

    ryu-manager --config-file ./ryu-apps/ryu.conf --verbose ./ryu-apps/send_event_async.py ./ryu-apps/ofctl_rest_tousix.py ./ryu-apps/stateful_ctrl.py ./ryu-apps/send_stats.py
   
For any questions please contact us !

Contact
-------
Rémy Lapeyrade (remy.lapeyrade@laas.fr)

Marc Bruyère (marc.bruyere@laas.fr)

