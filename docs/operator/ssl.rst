.. _configure_ssl_certificates:

SSL Certificates
================

By default, *sfconfig* creates a self-signed certificate. To use another certificate,
you need to copy the provided files to /var/lib/software-factory/bootstrap-data/certs and
apply the change with the sfconfig script.

* gateway.crt: the public certificate
* gateway.key: the private key
* gateway.chain: the TLS chain file

Automatic TLS certificate with Let's Encrypt
============================================

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
