:orphan:

.. _configure:

Configuration
=============

Once the instance is running, you may adjust the configuration
file, for example to change the domain name and admin password.

.. code-block:: bash

  # vim /etc/software-factory/sfconfig.yaml
  # sfconfig --skip-install


Currently located in /etc/software-factory/sfconfig.yaml,
this is THE SF configuration entry point. Ansible roles variable can be
over-written in /etc/software-factory/custom-vars.yaml file too.

.. tip::
   The /etc/software-factory is versioned with git, you can use git diff and
   git commit to check files modifications.

.. note::

  Any modification to sfconfig.yaml needs to be manually applied with the sfconfig script.
  Run sfconfig after saving the sfconfig.yaml file.



.. _configure_reconfigure:

Configuration and reconfiguration
---------------------------------

* Connect as (root) via SSH to the install-server (the first instance deployed).
* Edit the configuration file /etc/software-factory/sfconfig.yaml

  * set the configuration according to your needs.
  * all parameters are editable and should be self-explanatory.

* Edit the architecture file /etc/software-factory/arch.yaml (see :ref:`Architecture documentation <architecture>`)

  * set the architecture according to your needs.

* Run sfconfig to apply the configuration.

You can find some useful information on the following pages about the services
provides by Software Factory:


Fully Qualified Domain Name
---------------------------

The "fqdn" parameter defines the hostname used to access SF services.
It is an important parameter since it is used by external identity provider
to redirect user after authentication. Thus the name needs to be resolvable,
either manually with the /etc/hosts, either with a proper DNS record.

This parameter will be used to create virtual host name for each services,
such as zuul.fqdn and gerrit.fqdn.

.. warning::

    If the *fqdn* parameter is not set, the deployment will use the default
    **sftests.com** domain and users need to set their local /etc/hosts file with:

      ip-of-deployment sftests.com

.. note::

    For consistency, hosts defined in the :ref:`arch inventory<architecture>` will
    have their fqdn hostname set to: name.fqdn


.. _configure_ssl_certificates:

SSL Certificates
----------------

By default, *sfconfig* creates a self-signed certificate. To use another certificate,
you need to copy the provided files to /var/lib/software-factory/bootstrap-data/certs and
apply the change with the sfconfig script.

* gateway.crt: the public certificate
* gateway.key: the private key
* gateway.chain: the TLS chain file

Authorizing the localCA
.......................

When deployed using a self-signed certificate, you can authorize the local CA
by adding: http://fqdn/localCA.pem to your browser CA trust.


Automatic TLS certificate with Let's Encrypt
............................................

SF comes with the `lecm <https://github.com/Spredzy/lecm>`_ utility to automatically
manages TLS certificate. To support let's encrypt https security, you need to
enable this option in sfconfig.yaml (and run sfconfig after).

.. code-block:: yaml

  network:
    use_letsencrypt: true


Certificate will be automatically created and renewed, you can check the status using
the *lecm* utility:

.. code-block:: bash

  $ lecm -l
  +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+
  |               Item               |     Status    |                          subjectAltName                          |                          Location                         | Days |
  +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+
  |   softwarefactory-project.io     |   Generated   |                 DNS:softwarefactory-project.io                   |    /etc/letsencrypt/pem/softwarefactory-project.io.pem    |  89  |
  +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+


Services configuration
----------------------

Check the :ref:`management documentation<management>` for more informations about the
services configuration and how to manage them.
