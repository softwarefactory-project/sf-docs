==================================================
Software-Factory project Contributor documentation
==================================================


How can I help?
---------------

Thanks for asking.

The easiest way to get involved is to join us on IRC: #softwarefactory channel on Freenode.

The mailing list is softwarefactory-dev@redhat.com , subscribe here: https://www.redhat.com/mailman/listinfo/softwarefactory-dev

User stories and bug tracker are available here: https://softwarefactory-project.io/storyboard/#!/project_group/4

New user stories should be submitted as a review to the **sf-specs** repository on Software Factory.
See https://softwarefactory-project.io/r/gitweb?p=software-factory/sf-specs.git;a=blob_plain;f=README.md for
details about how to format your patch.

Prepare a development environment
---------------------------------

Software Factory runs and is developed on CentOS 7. Provision a CentOS 7 system, then install the following prerequisites:

.. code-block:: bash

 sudo yum install -y git git-review vim-enhanced tmux curl rpmdevtools createrepo mock python-jinja2
 sudo /usr/sbin/usermod -a -G mock $USER

Then you will need to check out the Software Factory repositories:

.. code-block:: bash

 $ mkdir software-factory
 $ pushd software-factory
 $ git clone https://softwarefactory-project.io/r/software-factory/sfinfo
 $ for repo in $(python << EOF
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
 $ popd
 $ ln -s software-factory/sfinfo/zuul_rpm_build.py .
 $ ln -s software-factory/sfinfo/zuul_koji_lib.py .
 $ ln -s software-factory/sfinfo/sf-master.yaml distro.yaml


Rebuilding packages
-------------------

Integration tests use packaged version of all the repository, the easiest
way to test a local change is to rebuild package locally with this command:

.. code-block:: bash

 $ ./zuul_rpm_build.py --project software-factory/zuul-distgit

Newly built packages are available in the zuul-rpm-build directory. Use
the "--noclean" argument to speed-up the process.


How to run the tests locally
----------------------------

Using the sf-ci project, you can easily test local changes:

.. code-block:: bash

 $ git clone https://softwarefactory-project.io/r/software-factory/sf-ci
 $ sudo ansible-playbook -e "local_repo_path=$(pwd)/zuul-rpm-build" -e "sf_user=${USER}" -e "sf_ci=$(pwd)/sf-ci" sf-ci/playbooks/deploy.yml

This uses the zuul-rpm-build local repository to deploy local change.
To test small changes, it's also possible to install the code directly in place,
for example:

* sf-config repository content can be rsynced to /usr/share/sf-config
* managesf can be installed using "python setup.py install"

To undo a deployment and start over, uses the "--erase" argument:

.. code-block:: bash

 $ sudo sfconfig.py --erase


How to run CI tests
-------------------

There are two kinds of tests:

* Functional tests
* Upgrade tests


functional testing
..................

The second argument to run_tests.sh define the architecture to use:

.. code-block:: bash

 $ cd sf-ci
 $ ./run_tests.sh functional allinone


upgrade test
............

.. code-block:: bash

 $ ./run_tests.sh upgrade allinone



How to develop and/or run a specific functional test
----------------------------------------------------

After a sf-ci deployment, run:

.. code-block:: bash

 $ nosetests -s -v ./tests/functional/test_gerrit.py

Tips:

* **-s** enables using 'import pdb; pdb.set_trace()' within a test
* Within a test insert 'from nose.tools import set_trace; set_trace()' to add a breakpoint in nosetests
* **--no-byte-compile** makes sure no .pyc are run
* you can use file globs to select specific tests: [...]/tests/functional/\*zuul\*



How to contribute
-----------------

* Connect to https://softwarefactory-project.io/ to create an account
* Register your public SSH key on your account. Have a look to: :ref:`Adding public key`.
* Check the bug tracker and the pending reviews
* Submit your change

.. code-block:: bash

  git-review -s # only relevant the first time to init the git remote
  git checkout -b"my-branch"
  # Hack the code, create a commit on top of HEAD ! and ...
  git review # Summit your proposal on softwarefactory-project.io

Your patch will be listed on the reviews pages at https://softwarefactory-project.io/r/ .
Automatic tests are run against it and Jenkins/Zuul will
report results on your patch's Gerrit page. You can
also check https://softwarefactory-project.io/zuul/ to follow the test process.

Note that Software Factory is developed using Software Factory. That means that you can
contribute to Software Factory in the same way you would contribute to any other project hosted
on an instance: :ref:`contribute`.
