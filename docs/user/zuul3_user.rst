.. _zuul3-user:

Zuul3 user documentation
========================

Refer to the upstream documentation_ regarding available pipelines and jobs options.

.. _documentation: https://docs.openstack.org/infra/zuul/feature/zuulv3/user/

In Software Factory:

* Projects are added to the main configuration in the config repo zuulV3 directory
* Jobs can inherit from the zuul-jobs repository base jobs
* Then projects job can also define custom jobs in their repo

For each sources, there are 2 types of projects:

* config-projects hold configuration information such as logserver access.
  Jobs defined in config-projects run with elevated privileges.
* untrusted-projects are projects being tested or deployed.


Adding a project to the zuulV3 service
--------------------------------------

Add a file in the config/zuulV3/project-name.yaml:

.. code-block:: yaml

  - tenant:
      name: local
      source:
        source-name:
          untrusted-projects:
            - project-name


* Leave the tenant name to *local*
* Replace source-name by the location of the repository (gerrit for internal gerrit)
* Replace project-name by the project name
* Replace untrusted-projects by config-project if the project is going to store secrets

After merging this change, the config-update job will reload the zuul scheduler.


Adding a job to a project
-------------------------

Project CI configuration is happening in repos, a project can define a job by
having a file named *.zuul.yaml* at the root of the project's repository:

.. code-block:: yaml

  - project:
      name: project-name
      check:
        jobs:
          - linters
      gate:
        jobs:
          - linters

Create a secret to be used in jobs
----------------------------------

Zuul provides a public key for every project that need to be used to encrypt
secret data. Getting a project key is as follow:

.. code-block:: bash

  curl -O https://sftests.com/zuul3/keys/gerrit/project-name.pem

The *encrypt_secret.py* tool, from the Zuul's repository (branch *feature/zuulv3*), can be used to
create the YAML tree to be pushed in the project *.zuul.d/* directory.

.. code-block:: bash

  ./encrypt_secret.py https://sftests.com/zuul3/ gerrit project-name --infile secret.data --outfile secret.yaml

Then *<name>* and *<fieldname>* fields that are placeholders must be replaced in the
generated *secret.yaml* file.

A secret used in a job must be defined in the same project than the job is defined.
The user should read carefully the section_ about secrets.

.. _section: https://docs.openstack.org/infra/zuul/user/config.html?highlight=secret#secret
