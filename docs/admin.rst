Administration
==============


Philosophy
----------

The management of your IXP with this tool look like pretty much avy Django app.
We didn't want to break the base framework completely to provide our solution.
It is handled like a classic Django project, and many efforts have been provided to do this project "the Django way".
Thus, Django generic apps developed by the community would still be applicable on this project (especially on the Model side).

Nevertheless, some automation have been provided directly on the admin side of the app to facilitate workflow and reduce human error.


So basically, you can interact with any type of model created in the database.
Editing all the objects saved can be done via the admin interface.

But upon adding/removing/modifying certain elements, you will be faced to side-effects (like the :ref:`state-machine`).
All of these special cases will be detailed on this page.

Create/delete objects
---------------------

Some of them are restricted.

Actions
-------


.. _state-machine:

State-machine
-------------

There are some side-effects which can occur when an administrator or a user modify host values.
These modifications are ruled by a state machine defined in TouSIX-Manager model.

The life cycle of the state machine is defined in this schema:
.. image:: images/transitions.png


Let's decrypt Model status for the host:

    The inactive state is used to create the Host object, but not apply it in the production.
    It requres an admin action to get out of this state, and apply the Deploy transition method.