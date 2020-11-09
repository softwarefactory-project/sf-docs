.. _opendistro:

#################################
Setting up new Elasticsearch user
#################################


Managing internal users
-----------------------

By using 'basic authentication', all users are done in the dedicated file
`internal_users.yml` located in `opendistro_security config directory`.
`More information about the file`_.

.. _`More information about the file`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/configuration/yaml/#internal_usersyml


Adding new user to internal database
------------------------------------

In that section, we will add a new user: `kibana` to the internal
database.

.. code-block:: yaml

   # internal_users.yml
   # (...)
   kibana:
     hash: <PASSWORD HASH>
     reserved: true
     backend_roles:
       - kibana_viewer
     description: Kibana viewer user


Generating password to new user
-------------------------------

Opendistro comes with a CLI utility to generate password hashes for users.

Example:

.. code-block:: bash

   /usr/share/elasticsearch/plugins/opendistro_security/tools/hash.sh -p <MY PASSWORD>

The generated hash should be added into the `internal_users.yml` file as the "hash" property
for the user.

To apply that change, you need to run `securityadmin.sh` script.


Opendistro configuration directory
----------------------------------

The opendistro_security config directory you can find in:

.. code-block::

   /usr/share/elasticsearch/plugins/opendistro_security/securityconfig/


Roles
-----

The roles are described in `roles.yml` file located in `opendistro_security
config directory`. In that file, you are able to create your own roles,
with defined rules.
To limit access to the Kibana, please check document for `access-control`_.

.. _`access-control`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/


Securityadmin.sh script
-----------------------

To apply created changes, you need to execute the `dedicated script`_ script.
It is the most important step that you should not forget after doing some
changes.

In the Software Factory 3.6, the command below will setup the `securityadmin.sh`
script. What you need to do is to execute it on the Elasticsearch host.

.. code-block:: bash

   /usr/share/elasticsearch/plugins/opendistro_security/tools/securityadmin.sh   \
     -cd /usr/share/elasticsearch/plugins/opendistro_security/securityconfig/  \
     -icl -nhnv -cacert /etc/elasticsearch/certs/localCA.pem  \
     -cert /etc/elasticsearch/certs/elasticsearch-admin.crt  \
     -key /etc/elasticsearch/certs/elasticsearch-admin.key    \
     -h $(hostname)

.. _`dedicated script`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/configuration/generate-certificates/#run-securityadminsh
