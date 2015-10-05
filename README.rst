=============
fleure-webui
==============

fleure-webui is a web ui frontend for fleure: https://github.com/ssato/fleure

- Author: Satoru SATOH <ssato at redhat.com>
- License: MIT

How to run
-------------

#. git clone https://github.com/ssato/fleure-webui fleure-webui.git
#. cd fleure-webui.git
#. yum install -y python-flask{,-bootstrap,wtf} python-jinja2 python-werkzeug

   (or pip install -r pkg/requirements.txt)

#. FLEURE_UPLOADDIR=/tmp/uploads FLEURE_WORKDIR=/tmp/w python manage.py runserver
#. open http://localhost:5000/ with an web browser such as firefox

.. vim:sw=2:ts=2:et:
