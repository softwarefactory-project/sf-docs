.. _opendistro:

########################
Opendistro configuration
########################

This documment is about Opendistro configuration that has been done
in Software Factory 3.6.

Introduction
------------

Since Software Factory 3.6, the opensource version of ELK stack has been
replaced with `Opendistro for Elasticsearch version`_.
The Opendistro ELK stack is a "community-driven 100% open source distribution
of Elasticsearch with advanced security, alerting, SQL support,
automated index management, deep performance analysis, and more."

The main reason why we decide to switch ELK stack to Opendistro is that
we would like to hawve a Role Base Access Controll (RBAC) which is
provided in Opendistro. With that, we are able to give read-only access to
non-privileged users, so our visualizations, indexes, index patterns and others
components in Elasticsearch and Kibana are safe from interference
by third parties.
Before choosing Opendisto, we were comparing all available solutions like:

- Opensource version of Elasticsearch with X-Pack Community Edition
- Secure-Guard
- Readonlyrest

Some of them was not providing so many features, some has license that
are inconvenient for our project. Thats why we choose Opendistro which has
Apache2 license, community and multiple features that we would like to provide
in the future releases of Software Factory.

Main documentation related to :ref:`Opendistro for Elasticsearch you can find here <opendistro>`.

.. _`Opendistro for Elasticsearch version`: https://opendistro.github.io/


Authentication
--------------

There is multiple authentication solution available in Opendistro.
With Software Factory 3.6 only "basic internal" authentication is enabled.

Code, that is responsible by enabling that authentication, you can find
in **opendistro_security config directory** which is:

.. code-block::

   /usr/share/elasticsearch/plugins/opendistro_security/securityconfig/

in `config.yml` file. Example of such configuration:

.. code-block:: yaml

   # config.yml
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

Other available authentication, you can find `here`_

.. _`here`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/configuration/configuration/


Managing internal users
-----------------------

By using 'basic authentication', all users are done in the dedicated file
`internal_users.yml` located in Opendistro security config location
/usr/share/elasticsearch/plugins/opendistro_security/securityconfig.
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

There is a simple command that returns a hash that will be well known by
Elasticsearch.
Example:

.. code-block:: bash

   /usr/share/elasticsearch/plugins/opendistro_security/tools/hash.sh -p <MY PASSWORD>

The generated hash should be added into internal_users.yml file to "hash" key
for required user.
To apply that change, you need to run `securityadmin.sh` script.


Roles
-----

The roles are described in `roles.yml` file located in `opendistro_security
config directory`.
In this file, you are able to create own role, with defined rules.
For example, it will be good set `kibana` read only user permission limitation
to read-only access.

.. code-block:: yaml

   # roles.yml
   # (...)
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

The `kibana_viewer` user has `limited access`_ to run `allowed_actions`_
on current set `index_patterns`. The `tenant_permissions` are in that example
set to the empty list, so it will be applied on all available tenants.
The `cluster_permissions` is a Opendistro cluster-level `dedicated roles`_.

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
that is described in `this document`_.

.. _`limited access`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/permissions/#indices
.. _`allowed_actions`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/default-action-groups/#index-level
.. _`dedicated roles`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/default-action-groups/#cluster-level
.. _`this document`:  https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/users-roles/#sample-roles

Predefined roles
----------------

In the Opendistro, there are defined multiple roles with `dedicated usage`_.
For example `kibana_read_only` role (that should be used also with `kibana_user`
role) gives user only access to the dashboards and visualization. The user
is not able to search or make some API queries.

.. _`dedicated usage`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/users-roles/#predefined-roles

Role mappings
-------------

After creating roles, you map users (or backend roles) to them.
Example:

.. code-block:: yaml

   # role_mappings.yml
   # (...)
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
How to configure tenants, you can find in `document`_.

.. _`document`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/access-control/multi-tenancy/#add-tenants


Securityadmin.sh script
-----------------------

To apply created changes, you need to execute `dedicated script`_ script.
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

.. _`dedicated script`: https://opendistro.github.io/for-elasticsearch-docs/docs/security/configuration/generate-certificates/#run-securityadminsh


Elasticsearch users availble in Software Factory
------------------------------------------------

There are multiple users created in SF.
Created users:

- admin - the superuser in Kibana. It has all permissions to manage the Kibana and Elasticsearch cluster
- kibanaserver - this user is used by Kibana service to connect to the Elasticsearch
- logstash - dedicated user to communicate logstash service to the Elasticsearch
- repoxplorer - user that is used by RepoXplorer to connect to the ES cluster
- curator - user that is used by curator service to 'clean-up' the index
- kibana - a read-only user. This user shows on the login page


Affected services in Software Factory
-------------------------------------

By changing the ELK stack to the Opendistro, some services requires to
change the configuration:

- logstash - the service requires to add `ilm_enabled` `option set` to False.

.. code-block::

   output {
     elasticsearch {
       hosts => ['localhost:9200']
       index => "logstash-%{+YYYY.MM.dd}"
       user => 'logstash'
       password => 'password'
       ssl => true
       ssl_certificate_verification => true
       ilm_enabled => false
     }
   }

- curator - the curator tool requires to provide authentication credentials.

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

.. code-block:: python

   elasticsearch_user = 'repoxplorer'
   elasticsearch_password = 'password'

.. _`option set`: https://opendistro.github.io/for-elasticsearch-docs/docs/troubleshoot/#logstash


Default Opendistro settings
---------------------------

By default Opendistro is running the `install_demo_configuration.sh` script
on installing the package. The script is creating default environment,
configuration for Kibana and Elasticsearch service (also generating the
self-signed certificates).
It is recommended to disable the disable the demo configuration on
production environment (like we do in Software Factory).


Kibana configuration
--------------------

For using Kibana in the Opendistro for Elasticsearch, it is required to install
dedicated package `opendistroforelasticsearch-kibana` - it will be automatically
configured in Software Factory if the `kibana` role is set in `arch.yaml` file.

Sample configuration of the Kibana service that is in kibana.yml file:

.. code-block:: yaml

   elasticsearch.hosts: ["https://localhost:9200"]
   elasticsearch.ssl.verificationMode: full
   elasticsearch.username: kibanaserver
   elasticsearch.password: password
   elasticsearch.requestHeadersWhitelist: ["securitytenant","Authorization"]

   opendistro_security.multitenancy.enabled: false
   opendistro_security.multitenancy.tenants.preferred: ["Global"]
   opendistro_security.readonly_mode.roles: ["kibana_read_only"]

   # Use this setting if you are running kibana without https
   opendistro_security.cookie.secure: false

   newsfeed.enabled: false
   telemetry.optIn: false
   telemetry.enabled: false
   server.host: managesf.sftests.com
   server.basePath: "/analytics"
   elasticsearch.ssl.certificateAuthorities: ["/etc/kibana/certs/localCA.pem"]


Elasticsearch configuration
---------------------------

The Elasticsearch configuration that was made in Software Factory is big
part same as in default configuration file, but with changed certificates.
Example of `elasticsearch.yml` file:

.. code-block:: yaml

   opendistro_security.ssl.transport.pemcert_filepath: /etc/elasticsearch/certs/elasticsearch-admin.crt
   opendistro_security.ssl.transport.pemkey_filepath: /etc/elasticsearch/certs/elasticsearch-admin.key
   opendistro_security.ssl.transport.pemtrustedcas_filepath: /etc/elasticsearch/certs/localCA.pem
   opendistro_security.ssl.transport.enforce_hostname_verification: false
   opendistro_security.ssl.http.enabled: true
   opendistro_security.ssl.http.pemcert_filepath: /etc/elasticsearch/certs/elasticsearch-admin.crt
   opendistro_security.ssl.http.pemkey_filepath: /etc/elasticsearch/certs/elasticsearch-admin.key
   opendistro_security.ssl.http.pemtrustedcas_filepath: /etc/elasticsearch/certs/localCA.pem
   opendistro_security.allow_unsafe_democertificates: false
   opendistro_security.allow_default_init_securityindex: true
   opendistro_security.authcz.admin_dn:
     - CN=sftests.com,O=SoftwareFactory,C=FR

   opendistro_security.audit.type: internal_elasticsearch
   opendistro_security.enable_snapshot_restore_privilege: true
   opendistro_security.check_snapshot_restore_write_privileges: true
   opendistro_security.restapi.roles_enabled: ["all_access", "security_rest_api_access"]
   cluster.routing.allocation.disk.threshold_enabled: false
   node.max_local_storage_nodes: 3
