.. _run_tests:

How to run the tests
--------------------

Software Factory's functional tests and health-check tests are located in the
sf-ci repository.

.. note::

  All commands below must be run as root user.

Deployment
..........

To deploy a software factory to hack and run tests just follow the
:ref:`quickstart guide <quickstart>` or the :ref:`sandbox section <how_to_setup_sf_sandbox>`.


Functional tests
................

After having deployed Software Factory, run functional tests:

1. Clone sf-ci repository, if it is not available on host:
.. code-block:: bash

  git clone https://softwarefactory-project.io/r/software-factory/sf-ci

2. Run tests:
.. code-block:: bash

 yum install -y python3-nose
 export PYTHONPATH=sf-ci/tests/functional/
 sudo .sf-ci/scripts/create_ns.sh
 nosetests-3 -sv tests/functional/

Most tests can be executed without the *create_ns.sh* script but some
of them require to be wrapped inside a network namespace to simulate
external remote access to the Software Factory gateway.


Health-check playbooks
......................

After having deployed Software Factory using sf-ci, run:

.. code-block:: bash

 export PYTHONPATH=sf-ci/tests/functional/
 pushd tests/functional/provisioner/ && python3 provisioner.py && popd
 ANSIBLE_ROLES_PATH=sf-ci/roles ansible-playbook \
   -i /var/lib/software-factory/ansible/hosts \
   -e @sf-ci/playbooks/health-check/group_vars/all.yaml \
   sf-ci/playbooks/health-check/sf-health-check.yaml

The health-check playbooks complete the functional tests coverage by testing:

* Zuul
* Gerritbot

Testinfra validation
....................

After having deployed Software Factory, run:

.. code-block:: bash

 sfconfig --skip-install --skip-setup --enable-insecure-workers

The testinfra checks are simple smoke tests validating Software Factory's
services are up and running.

Scratch a deployment
....................

To scratch a deployment and start over, use the "--erase" argument:

.. code-block:: bash

 sfconfig --erase

This command erases all data from the current deployment and uninstalls most of the
Software Factory packages. It is recommended to start working on new features or
bug fixes on a clean environment.

When switching from a *minimal* deployment to an *allinone* it is advised
to run that command beforehand to avoid some side effects during functional tests.
