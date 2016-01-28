

=====
TouSIX-Manager
=====
Description of TouSIX-Manager (details, purpose, etc...)

Quick start
-----------

1. Install the base files with pip (on your system or inside a virtual environment):

    ```bash
        pip install -e URL_projet
    ```
2. Create a new django project to automate some procedures:

    ```bash 
        django-admin startproject ixp-manager
    ```

3. Copy the settings.py.example given in the package into your project settings, and customize it following your needs.

4. Include the tousix-manager URLconf in urls.py:

    `url(r'^manager/', include('tousix-manager.urls'))`

5. Run `python manage.py migrate` to create tousix-manager's models.

6. You can now run the project : `python manage.py runserver 8000`

Don't forget to create a super user for editing some models in the admin interface.

