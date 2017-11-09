.. _zuul3-user:

Zuul3 user documentation
========================

.. danger::

  Zuul3 is still under heavy development and breaking changes might occur from one
  version of Software Factory to another. It is strongly advised to follow
  Zuul's upstream developments, for example by registering to OpenStack Infra's
  `mailing list <http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-infra>`_.

.. note::

  This is a lightweight documentation intended to get users started with setting
  up CI pipelines and jobs. For more insight on what Zuul3 can do, please refer
  to its upstream documentation_.

.. _documentation: https://docs.openstack.org/infra/zuul/feature/zuulv3/user/

In Software Factory:

* Projects are added to the main configuration in the config repo zuulV3 directory
* Jobs can inherit from the zuul-jobs repository base jobs
* Projects can also define custom jobs in their repositories
* Projects can come from different sources, depending on Software Factory's
  configuration:
  * Software Factory's own internal gerrit and git server
  * external gerrit servers
  * Github

For each source, there are 2 types of projects:

* *config-projects* hold configuration information such as logserver access.
  Jobs defined in config-projects run with elevated privileges.
* *untrusted-projects* are projects being tested or deployed.


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

Adding a predefined job to a project
------------------------------------

Project CI configuration is happening in repositories, a project can define a job by
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

* **name** is the name of the project
* **check**, **gate** are pipelines defined in Software Factory.

A default deployment of Software Factory comes with the following base jobs:

============= =============================================================
 Name          Description
============= =============================================================
**linters**    Run the bashate, flake8 and yaml linters on relevant files
============= =============================================================

Software Factory can be configured to import the **openstack-infra/zuul-jobs**
jobs library; ask your instance operator if this is the case. A list of the jobs in this
library can be found `here <https://docs.openstack.org/infra/zuul-jobs/jobs.html>`_.

A full list of all the jobs that have been built at least once on Software Factory
can be accessed at https://<fqdn>/zuul3/local/jobs.html.

Defining a custom job within a project
--------------------------------------

It is possible to define jobs specific to a project within its repository. This
is done in the *.zuul.yaml* file at the root of the repository. Jobs are based
on Ansible playbooks.

For example, the following .zuul.yaml file will define a job called **special-job**
to be run in the **check** pipeline along the linters:

.. code-block:: yaml

  - job:
      name: special-job
      parent: base
      description: this is a special job just for this project
      run: playbooks/specialjob
      nodeset:
        nodes:
          - name: test-node
            label: dib-centos-7

  - project:
      name: project-name
      check:
        jobs:
          - special-job
          - linters

* setting **parent: base** allows this job to inherit from the default *pre* and
  *post* playbooks which are run before and after the custom job's playbook.
  These playbooks prepare the work environment and automatically publish artifacts,
  so while not mandatory, it is advised to add this setting to make use of
  Software Factory's integrations.
* **nodeset** defines the nodes that will be spawned to build the job. *Label*
  refers to nodepool label definitions, see the :ref:`nodepool documentation <nodepool3-user>`
  for further details. *Name* is the name of the node as it will be available in
  the job's playbook inventory.

The previous example expects the Ansible playbook "playbooks/specialjob.yaml" (or
"playbooks/specialjob/run.yaml") to be present in the project's repository. Here
is an example of what this playbook could contain:

.. code-block:: yaml

  ---
  - hosts: test-node
    tasks:
      - name: install supertester package
        yum:
          name: supertester
          state: present
        become: yes
      - name: run supertester
        command: supertester {{ zuul.project.src_dir }}/myfile.py

Further documentation can be found online:

* Ansible `playbooks <http://docs.ansible.com/ansible/latest/playbooks.html>`_,
  `modules <http://docs.ansible.com/ansible/latest/modules_by_category.html>`_ documentation
* `Predefined variables available in jobs <https://docs.openstack.org/infra/zuul/feature/zuulv3/user/jobs.html#variables>`_

Create a secret to be used in jobs
----------------------------------

Zuul provides a public key for every project that needs to be used to encrypt
secret data. To fetch a given project's public key:

.. code-block:: bash

  curl -O https://<fqdn>/zuul3/keys/gerrit/project-name.pem

The *encrypt_secret.py* tool, from the Zuul repository (branch *feature/zuulv3*), can be used to
create the YAML tree to be pushed in the project *.zuul.d/* directory.

.. code-block:: bash

  ./encrypt_secret.py https://<fqdn>/zuul3/ gerrit project-name --infile secret.data --outfile secret.yaml

Then *<name>* and *<fieldname>* fields that are placeholders must be replaced in the
generated *secret.yaml* file.

A secret used in a job must be defined in the same project than the job is defined.
The user should read carefully the section_ about secrets.

.. _section: https://docs.openstack.org/infra/zuul/user/config.html?highlight=secret#secret
