=========================
Contributor documentation
=========================


How can I help?
---------------

Thanks for asking.

The easiest way to get involved is to join us on IRC: #softwarefactory channel on Freenode.

The mailing list is softwarefactory-dev@redhat.com , subscribe here: https://www.redhat.com/mailman/listinfo/softwarefactory-dev.

The project's feature and bug tracker is available here: https://softwarefactory-project.io/storyboard/#!/project_group/4.

New user stories should be submitted as a review to the **sf-specs** repository on Software Factory.
See https://softwarefactory-project.io/r/gitweb?p=software-factory/sf-specs.git;a=blob_plain;f=README.md for
details about how to format your patch.

Prepare a development environment
---------------------------------

Software Factory runs and is developed on CentOS 7. Provision a CentOS 7 system, then install the following prerequisites:

.. code-block:: bash

 sudo yum install -y centos-release-openstack-newton
 sudo yum install -y git git-review vim-enhanced tmux curl rpmdevtools createrepo mock python-jinja2 ansible
 sudo /usr/sbin/usermod -a -G mock $USER
 newgrp mock

It is recommended that your Centos 7 installation is dedicated to Software Factory development
to avoid thrid party components conflicts.

Then you will need to check out the Software Factory repositories:

.. code-block:: bash

 mkdir software-factory
 pushd software-factory
 git clone https://softwarefactory-project.io/r/software-factory/sfinfo
 git clone https://softwarefactory-project.io/r/software-factory/sf-ci
 for repo in $(python << EOF
 import yaml
 repos = yaml.load(open('sfinfo/sf-master.yaml'))
 for r in repos['packages']:
    suffix = r['name']
    if r['source'] == 'external':
       suffix += '-distgit'
    print suffix
    if 'distgit' in r:
       print r['distgit']
 EOF); do
   git clone https://softwarefactory-project.io/r/$repo;
 done
 popd
 ln -s software-factory/sfinfo/zuul_rpm_build.py .
 ln -s software-factory/sfinfo/sf-master.yaml distro.yaml

The file *sfinfo/sf-master.yaml* contains all repository's references that compose
the Software Factory distribution. The script above fetch all but you can just
fetch the needed ones.

Rebuilding packages
-------------------

Each component of Software Factory is distributed via a package and as a contributor you may
need to rebuild a package. You will find RPM package definition in
software-factory/<component>-distgit directories and sources in software-factory/<component>
directory.

Here is an example to rebuild the Zuul package.

.. code-block:: bash

 ./zuul_rpm_build.py --project software-factory/zuul

Newly built packages are available in the zuul-rpm-build directory.

Use the "--noclean" argument to speed-up the process. This argument prevents
the mock environment to be destroyed and rebuilt but does not clean the
zuul-rpm-build directory so you might want to clean it first.

.. code-block:: bash

 rm -Rf ./zuul-rpm-build/* && ./zuul_rpm_build.py --noclean --project software-factory/zuul

Multiple packages to rebuild can be specified.

.. code-block:: bash

 rm -Rf ./zuul-rpm-build/* && ./zuul_rpm_build.py --noclean --project software-factory/zuul --project software-factory/nodepool

No public DNS entry exist for the Software Factory koji host (where all SF
packages are built and stored) so for the time being you should:

.. code-block:: bash

 echo "46.231.133.231 koji koji.softwarefactory-project.io" | sudo tee -a /etc/hosts

How to run the tests
--------------------

Software Factory tests are in the sf-ci repository. You should use the run_tests.sh
script as an entry point to run test scenarios.

Deployment test
...............

.. code-block:: bash

 cd software-factory/sf-ci
 ./run_tests.sh deploy minimal

This will run the *deploy* ansible playbook with the *minimal* architecture
of Software Factory. The *allinone* architecture can be specified too.

The *deploy* playbook install the last development version of Software Factory
and run some smoke tests (serverspec) to verify services are well configured.
This is the recommended way to start with sf-ci. If the *deploy* scenario
does not end with success please ping us on IRC.

This scenario take around 15 minutes to execute.

If you want to use locally built packages then you can prefix the run_tests.sh command
with the LOCAL_REPO_PATH=$(pwd)/../zuul-rpm-build.

.. code-block:: bash

 LOCAL_REPO_PATH=$(pwd)/../../zuul-rpm-build ./run_tests.sh deploy minimal

To test small changes, it's also possible to install the code directly in place,
for example:

* sf-config repository content can be rsynced to /usr/share/sf-config
* managesf can be installed using "python setup.py install"

Access the SF UI
................

After a successful run of run_tests.sh the Software Factory UI is accessible
via a web browser. The default hostname of a deployment is *sftests.com*
so you should be able to access it using *http(s)://sftests.com*.

As sftests.com domain might be not resolvable it needs to be added to
your host resolver:

.. code-block:: bash

 echo "<sf-ip> sftests.com" | sudo tee -a /etc/hosts

Local authentication is enabled for the *admin* user using the
password *userpass*. Furthermore additional users are available:
*user2*, *user3*, *user4* with the password *userpass*.

Please note that *Toogle login form* link must be clicked in order to
display the login form.

Erase a deployment
..................

To undo a deployment and start over, uses the "--erase" argument:

.. code-block:: bash

 sudo sfconfig.py --erase

This command erases deployment data and uninstall most of the
SF packages. It helps to restart from a pretty clean environment.

When switching from a *minimal* deployment to a *allinone* it is adviced
to run that that command to avoid some side effects during functional tests.


Functional test
...............

The *functional* scenario extends the *deploy* scenario by:

* Provisionning random data (Git repos, reviews, stories, ...)
* Get a backup
* Run heath-check playbooks (see sf-ci/health-check/)
* Run functional tests (see sf-ci/tests/functional/)
* Check firefose events
* Erase data (sfconfig --erase)
* Recover the data from the backup (sfconfig --recover)
* Check provisionned data have been recovered

.. code-block:: bash

 ./run_tests.sh functional allinone

Note that you can use LOCAL_REPO_PATH to include your changes.

This scenario take around 60 minutes to execute.

Upgrade test
............

The *upgrade* scenario simulates an update from the previous released version
of Software Factory and the current development version.

The scenario is:

* Install and deploy the last released of SF
* Run serverspec validation
* Provision data
* Run the upgrade
* Check provisionned data
* Run heath-check playbooks
* Run functional tests

.. code-block:: bash

 ./run_tests.sh upgrade allinone

Note that you can use LOCAL_REPO_PATH to include your changes.

This scenario take around 60 minutes to execute.

Direct run of functional tests
..............................

After a sf-ci deployment, run:

.. code-block:: bash

 sudo ./scripts/create_ns.sh nosetests -sv tests/functional/

Most tests can be executed without the *create_ns.sh* script but some
of them require to be wrapped inside a network namespace to simulate
external remote access to the Software Factory gateway.

Tips:

* you can use file globs to select specific tests: [...]/tests/functional/\*zuul\*
* **-s** enables using 'import pdb; pdb.set_trace()' within a test
* Within a test insert 'from nose.tools import set_trace; set_trace()' to add a breakpoint in nosetests
* **--no-byte-compile** makes sure no .pyc are run

Direct run of health-check test playbooks
.........................................

After a sf-ci deployment, run:

.. code-block:: bash

 sudo ansible-playbook health-check/sf-health-check.yaml

The health-check playbooks complete the functional tests
coverage by testing:

* Zuul
* Gerritbot

Run the SF configuration script
-------------------------------

After a sf-ci deployment, run:

.. code-block:: bash

 sudo sfconfig.py

Use ARA for inspecting SF playbooks runs
----------------------------------------

Installation
............

ARA provides a browsing interface for Ansible playbook runs. Using it
during development is a good idea. Here are the steps to install it:

.. code-block:: bash

 sudo yum install https://softwarefactory-project.io/repos/sf-release-2.5.rpm
 sudo yum install ara
 sudo yum remove sf-release-2.5.0

If you already installed the sf-release package (will be the case if sf-ci
*run_tests.sh* script ran before) then you might need to run *yum downgrade*
instead.

Prepare the environment variables for ARA
.........................................

The *run_tests.sh* script handles that for you but in case you want to run
command directly without this script then you must export the following
variables to configure ARA callbacks in Ansible.

.. code-block:: bash

 export ara_location=$(python -c "import os,ara; print(os.path.dirname(ara.__file__))")
 export ANSIBLE_CALLBACK_PLUGINS=$ara_location/plugins/callbacks
 export ANSIBLE_ACTION_PLUGINS=$ara_location/plugins/actions
 export ANSIBLE_LIBRARY=$ara_location/plugins/modules

Access the UI
.............

.. code-block:: bash

 ara-manage runserver -h 0.0.0.0 -p 55666

Then connect to http://sftests.com:55666

Software Factory CI
-------------------

Changes proposed on Software Factory's repositories will be tested on the
Software Factory upstream CI by the following jobs:

* sf-rpm-build (build RPMs if needed by the change)
* sf-ci-functional-minimal (run_tests.sh functional minimal)
* sf-ci-upgrade-minimal (run_tests.sh upgrade minimal)
* sf-ci-functional-allinone (run_tests.sh functional allinone)
* sf-ci-upgrade-allinone (run_tests.sh upgrade allinone)

The Software Factory upstream CI is based on sf-ci too so you can
expect that a change working/or failing locally will behave similar
on the CI.

How to contribute
-----------------

* Connect to https://softwarefactory-project.io/ to create an account
* Register your public SSH key on your account. Have a look to: :ref:`Adding public key`.
* Check the bug tracker and the pending reviews

Propose a change
................

.. code-block:: bash

  git-review -s # only relevant the first time to init the git remote
  git checkout -b"my-branch"
  # Hack the code, create a commit on top of HEAD ! and ...
  git review # Summit your proposal on softwarefactory-project.io

Your patch will be listed on the reviews pages at https://softwarefactory-project.io/r/ .
Automatic tests are run against it and the CI will
report results on your patch's Gerrit page. You can
also check https://softwarefactory-project.io/zuul/ to follow the test process.

Note that Software Factory is developed using Software Factory. That means that you can
contribute to Software Factory in the same way you would contribute to any other project hosted
on an instance: :ref:`contribute`.
