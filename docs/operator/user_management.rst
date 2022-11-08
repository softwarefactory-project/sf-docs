.. _user_management:

User Management
===============

.. note::

  The section on Interactive Users is only relevant when Keycloak is part of your
  Software Factory deployment.

There are two types of users in Software Factory:

* **Interactive Users**, ie human users who follow the browser-based login workflow to authenticate
  on services when needed.
* **Service (or Non-interactive) Users**, ie users that are defined for automation and are
  not expected to follow the web login workflow before interacting with services.

Service Users
-------------

Service users are created within the components they are meant to be used with. They are not
managed in Keycloak and therefore do not appear there, and can't be assigned a group or a role that way.

Default service users
^^^^^^^^^^^^^^^^^^^^^

When deploying Software Factory, several service users are automatically created:

* **zuul CI user**: used by Zuul to report back buildset results on Gerrit and set the CI vote on patchsets.
* **SF_SERVICE_USER**: an all-purpose service account. It is currently used by the firehose,
  as the only account with write access to the MQTT stream.

Creating a service user
^^^^^^^^^^^^^^^^^^^^^^^

Gerrit
......

Creating a service user on Gerrit may be necessary when setting up a third-party CI, so that
this CI can report back results and vote on patchsets that are open on your instance of Software Factory.

You can use a helper script to easily create a gerrit service user. As root, run:

.. code-block:: bash

  /usr/share/sf-config/scripts/gerrit-set-ci-user.sh "<USERNAME>" "$(cat <PATH/TO/SSH_KEY>)" "<EMAIL>"

This user will belong to the `"Service Users" group <https://gerrit-review.googlesource.com/Documentation/access-control.html#service_users>`_ in Gerrit by default.

As a follow-up action you can use the Gerrit SSH API to create HTTP credentials for this
user if you intend to use Gerrit's REST API with it.

Firehose
........

Note that by default, unauthenticated access to the firehose is allowed - only the "keycloak"
topic is not world-readable. If you need to create another authenticated account on the firehose,
you can do so this way:

.. code-block:: bash

  podman exec -it mosquitto /bin/bash
  mosquitto_passwd -b /etc/mosquitto/passwords <USERNAME> <PASSWORD>

If needed, edit the access rules in `/etc/mosquitto/acl.conf` according to mosquitto's documentation.

Interactive Users
-----------------

Interactive users are managed through Keycloak.

Admin user
^^^^^^^^^^

The admin user is hard coded and only the password can be set in the deployment's configuration file.
To change the admin user password, edit /etc/software-factory/sfconfig.yaml:

.. code-block:: yaml

  authentication:
    admin_password: userpass

Then run sfconfig to apply the change.

About roles
^^^^^^^^^^^

Roles must be managed (creation, deletion, assignment) through Keycloak, either via the Web UI or the admin CLI.

Default Roles
.............

Software Factory comes with the following default roles, and the following services are pre-configured to make use of these roles:

============================== =================== =========================    ===============================================================
Role Name                      Service(s)          Default?                     Description and Usage
============================== =================== =========================    ===============================================================
zuul_admin                     Zuul                Admin user                   This role grants admin access to every tenant defined on Zuul.
<tenant>_zuul_admin            Zuul                Must be assigned manually    This role grants admin access to the tenant <tenant> on Zuul.
sf_opensearch_dashboards_user  Opensearch, Kibana  All users                    This role grants read access to the OpenSearch database.
============================== =================== =========================    ===============================================================

The tenant-scoped admin roles get created automatically whenever a Zuul tenant is created in the Zuul section of the config repository.

These roles shouldn't be deleted, or some functionalities will be disabled in the related services.

Authorization management
........................

The OpenID Connect protocol used by Keycloak to authenticate users on Software Factory services rely on JSON-formatted
tokens, also known as JWT (JSON Web Tokens). These tokens hold various keys, or claims, and their associated values.

Examples of standard claims include:

* preferred_username
* email
* iss, or the issuer, usually set to the Keycloak service's FQDN

In Software Factory the custom claim **roles** is also included in the JWT. As its name suggests, it contains a list of all the roles
the user was assigned with or inherited through groups.

.. note::

  **Why isn't there a groups claim ?**

  In Software Factory, groups are strongly tied to Gerrit. And in Gerrit, access control to repositories is groups based. We have noticed that as the
  amount of repositories increases on Gerrit, so does the amount of groups, as a frequent behavior is to create at least one group per repository. This
  means that some privileged users can end up belonging to dozens or hundreds of groups. Listing all these groups in the JWT could potentially increase
  its size to a point where it cannot be handled properly by browsers or the services themselves.
  
  It is therefore wiser to manage authorization via roles, which tend to be less numerous.

  You are free to configure Keycloak so that a *groups* claim is added to JWTs, but do this at your own risk! 


Note that not every authenticated service uses claims-based authorization rules. The most notable - and unique - exception being
**Gerrit**; Gerrit's access rules are handled through the resources in Software Factory's config repository, and are based on the groups
defined in the resources.

Other services like Zuul and Opensearch Dashboards let you however define access control to features and resources by setting conditions
on claims. Please refer to their respective documentations to learn more about how to do this.
