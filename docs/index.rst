============================================
Welcome to software-factory's documentation!
============================================

.. figure:: imgs/logo.svg
   :width: 30%
   :align: center

Introduction to Software Factory
================================

Software Factory (also called SF) is a collection of services that provides
a powerful platform to build software. It's designed to
use an OpenStack-based cloud for resources, but it can also be used with static
resources.

Setting up a development environment manually can really be
time consuming and sometimes leads to a lot of configuration
trouble. SF provides an easy way to get all services configured
and running.

SF feature an automated upgrade process continuously tested with integration test.

.. image:: imgs/landing_page.png
   :scale: 50 %
   :align: right

SF integrates services matching each step in the software
production chain:

* Code review system: `Gerrit <http://en.wikipedia.org/wiki/Gerrit_%28software%29>`_
* Task tracker: `Storyboard <http://docs.openstack.org/infra/storyboard/>`_
* Pipelines manager: `Zuul <http://ci.openstack.org/zuul/>`_
* Test instance management: `Nodepool <http://docs.openstack.org/infra/system-config/nodepool.html>`_
* Collaborative tools: `Etherpad <http://en.wikipedia.org/wiki/Etherpad>`_, `Pastebin <http://en.wikipedia.org/wiki/Pastebin>`_
* Repositories metrics: `Repoxplorer <https://github.com/morucci/repoxplorer>`_
* Log management (ARA, ELK, Log server)
* System metrics

SF offers a seamless user experience with:

* Single Sign-On authentication,
* Unified REST API,
* Top-menu to access all the services, and
* Command line tool and web interface.

Table of contents
=================

.. toctree::
   :maxdepth: 1

   main_components
   user/user
   operator/operator
   contributor/contributor
   faqs
