.. _opendistro:

Opendistro configuration
========================


Authentication
--------------

There is multiple authentication solution available in Opendistro.
With Software Factory 3.6 only "basic internal" authentication is enabled.

Code, that is responsible by enabling that authentication, you can find
in `opendistro_security config directory` which is:
`/usr/share/elasticsearch/plugins/opendistro_security/securityconfig/` in
`config.yml` file.
Example of such configuration:

.. code-block:: yaml

   _meta:
     config_version: 2
     type: config
   config:
     dynamic:
       kibana:
         multitenancy_enabled: false
       http:
         anonymous_auth_enabled: false
         xff:
           enabled: false
       authc:
         basic_internal_auth_domain:
           authentication_backend:
             type: intern
           description: Authenticate via HTTP Basic against internal users database
           http_authenticator:
             challenge: true
             type: basic
           http_enabled: true
           order: 4
           transport_enabled: true

Other available authentication, you can find here [1]_.


Managing internal users
-----------------------

By using 'basic authentication', all users are done in the dedicated file
`internal_users.yml` located in Opendistro security config location
/usr/share/elasticsearch/plugins/opendistro_security/securityconfig.
More information about the file [2]_.

Adding new user to internal database
------------------------------------

In that section, we will add a new user: `kibana` to the internal
database.

.. code-block:: yaml

   kibana:
     hash: <PASSWORD HASH>
     reserved: true
     backend_roles:
       - kibana_viewer
     description: Kibana viewer user

Generating password to new user
-------------------------------

There is a simple command that returns a hash that will be well known by
Elasticsearch.
Example:

.. code-block:: bash

   /usr/share/elasticsearch/plugins/opendistro_security/tools/hash.sh -p <MY PASSWORD>

The generated hash should be added into internal_users.yml file to "hash" key
for required user.
To apply that change, you need to run `securityadmin.sh` script.


Opendistro roles
----------------


Roles
-----

The roles are described in `roles.yml` file located in `opendistro_security
config directory`.
In this file, you are able to create own role, with defined rules.
For example, it will be good set `kibana` read only user permission limitation
to read-only access.

.. code-block:: yaml

   kibana_viewer:
     reserved: true
     cluster_permissions:
     - "cluster_composite_ops_ro"
     index_permissions:
     - index_patterns:
       - "?kibana*"
       - "?kibana"
       - "logstash-*"
       allowed_actions:
       - "read"
       - "get"
       - "search"
       - "indices:data/write/update"
       - "indices:data/write/index"
       - "indices:data/write/bulk*"
     tenant_permissions: []

The `kibana_viewer` user has limited access to run `allowed_actions` [3]_ [4]_
on current set `index_patterns`. The `tenant_permissions` are in that example
set to the empty list, so it will be applied on all available tenants.
The `cluster_permissions` is a Opendistro cluster-level dedicated roles [5]_.

IMPORTANT NOTE:
In the Software Factory 3.6, the `kibana` user uses `kibana_viewer` role, which
is same as in this example. It is because of multiple automatization is rasing
problems in access to the `.kibana` index in Elasticsearch.
The `kibana_read_only` role (which you can find in `predeinfed roles` section)
has only access to see dashboards and visualization and it does not have
access to search in the Elasticsearch, thats why we are not using the
predefined role in SF 3.6.
If the above `kibana_viewer` role gives to many permissions to the
user, you can always check sample `read-only` roles with bulk access
that is described in [7]_.


Predefined roles
----------------

In the Opendistro, there are defined multiple roles with dedicated usage [6]_.
For example `kibana_read_only` role (that should be used also with `kibana_user`
role) gives user only access to the dashboards and visualization. The user
is not able to search or make some API queries.

Role mappings
-------------

After creating roles, you map users (or backend roles) to them.
Example:

.. code-block:: yaml

   kibana_viewer:
     reserved: false
     backend_roles:
     - "kibana_viewer"
     description: "Maps kibana viewer role"

In that example, the `kibana_viewer` role mapping is using `kibana_viewer`
role that was described in `roles.yml` file. For more information, check the
`Roles` section.

Tenants
-------

The Software Factory 3.6 is only configuring one tenant: `global` and
it also disable mutlitenancy (check Kibana configuration file).
How to configure tenants, you can find in documment [8]_.


Securityadmin.sh script
-----------------------

To apply created changes, you need to execute dedicated script [9]_ script.
It is the most important step that you should not forget after doing some
changes.

In the Software Factory 3.6, below command will setup the `securityadmin.sh`
script. What you need to do is to execute it on Elasticsearch host.

.. code-block:: bash

   /usr/share/elasticsearch/plugins/opendistro_security/tools/securityadmin.sh   \
     -cd /usr/share/elasticsearch/plugins/opendistro_security/securityconfig/  \
     -icl -nhnv -cacert /etc/elasticsearch/certs/localCA.pem  \
     -cert /etc/elasticsearch/certs/elasticsearch-admin.crt  \
     -key /etc/elasticsearch/certs/elasticsearch-admin.key    \
     -h $(hostname)


Elasticsearch users availble in Software Factory
------------------------------------------------

There are multiple users created in SF.
Created users:

- admin - the superuser in Kibana. It has all permissions to manage the
          Kibana and Elasticsearch cluster
- kibanaserver - this user is used by Kibana service to connect to
                 the Elasticsearch
- logstash - dedicated user to communicate logstash service to the Elasticsearch
- repoxplorer - user that is used by RepoXplorer to connect to the ES cluster
- curator - user that is used by curator service to 'clean-up' the index
- kibana - a read-only user. This user shows on the login page


Affected services in Software Factory
-------------------------------------

By changing the ELK stack to the Opendistro, some services requires to
change the configuration:

- logstash - the service requires to add `ilm_enabled` option set
             to `False` [10]_. Example:

.. code-block:: json

   output {
     elasticsearch {
       hosts => [ 'localhost:9200']
       index => "logstash-%{+YYYY.MM.dd}"
       user => 'logstash'
       password => 'password'
       ssl => true
       ssl_certificate_verification => true
       ilm_enabled => false
     }
   }

- curator - the curator tool requires to provide authentication credentials.
            Example:

.. code-block:: yaml

   client:
     hosts:
       - localhost:9200
     timeout: 30
     use_ssl: True
     ssl_no_validate: False
     certificate:  /etc/elasticsearch/certs/localCA.pem
     http_auth: curator:password

- RepoXplorer- same as `curator` tool, it requires to set proper credentials.
               Example:

.. code-block:: python

   elasticsearch_user = 'repoxplorer'
   elasticsearch_password = 'password'


Default Opendistro settings
---------------------------

By default Opendistro is running the `install_demo_configuration.sh` script
on installing the package. The script is creating default environment,
configuration for Kibana and Elasticsearch service (also generating the
self-signed certificates).
It is recommended to disable the disable the demo configuration on
production environment (like we do in Software Factory).


References
----------

.. [1] https://opendistro.github.io/for-elasticsearch-docs/docs/security/configuration/configuration/
.. [2] https://opendistro.github.io/for-elasticsearch-docs/docs/security/configuration/yaml/#internal_usersyml
.. [3] https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/permissions/#indices
.. [4] https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/default-action-groups/#index-level
.. [5] https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/default-action-groups/#cluster-level
.. [6] https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/users-roles/#predefined-roles
.. [7] https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/users-roles/#sample-roles
.. [8] https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/multi-tenancy/#add-tenants
.. [9] https://opendistro.github.io/for-elasticsearch-docs/docs/security/configuration/generate-certificates/#run-securityadminsh
.. [10] https://opendistro.github.io/for-elasticsearch-docs/docs/troubleshoot/#logstash
