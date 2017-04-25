==================================================
Software-Factory project Contributor documentation
==================================================


How can I help?
---------------

Thanks for asking.

The easiest way to get involved is to join us on IRC: #softwarefactory channel on Freenode.

The mailing list is: softwarefactory-dev@redhat.com , subscribe here: https://www.redhat.com/mailman/listinfo/softwarefactory-dev

User stories and bug tracker is available here: https://softwarefactory-project.io/storyboard/#!/project_group/4


Prepare a development environment
---------------------------------

Manual setup
............

Software Factory runs and is developed on CentOS 7. Provision a CentOS 7 system, then install the following prerequisites:

.. code-block:: bash

 sudo yum install -y epel-release
 sudo yum install -y libvirt libvirt-daemon-lxc git git-review vim-enhanced tmux curl python-devel wget python-pip mariadb-devel python-virtualenv gcc libffi-devel openldap-devel openssl-devel python-sphinx python-tox python-flake8 ansible
 sudo systemctl enable libvirtd
 sudo systemctl start libvirtd
 sudo yum install -y rpmdevtools createrepo mock python-jinja2
 sudo /usr/sbin/usermod -a -G mock $USER

Then you will need to check out the Software Factory manifest, and install the Software Factory development repositories:

.. code-block:: bash

 mkdir software-factory
 sudo mkdir -p /var/lib/sf/zuul-rpm-build
 cd software-factory && git clone https://softwarefactory-project.io/r/software-factory/sfinfo
 sudo cp -v sfinfo/rpm-gpg/* /etc/pki/rpm-gpg/
 sudo yum install -y https://softwarefactory-project.io/repos/sf-release-2.5.rpm

You can now install **Zuul-cloner**, as packaged by the Software Factory development team:

.. code-block:: bash

 sudo yum install -y zuul-cloner

Finally, check out the repositories of the Software Factory project (assuming current directory is 'software-factory'):

.. code-block:: bash

 git clone https://softwarefactory-project.io/r/software-factory/software-factory
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

Vagrant box
...........

There is an included Vagrantfile in the tools directory of the software-factory repository to automate these tasks
and deploy a pre-provisioned CentOS 7 instance that can be used for testing and development:

.. code-block:: bash

 VAGRANT_CWD=./tools/vagrant/sf_dev_env vagrant up

It also comes with a custom bashrc file with some aliases and commands that make it
easier to package or manage projects.

Optional: use a local http cache
--------------------------------

If you're rebuilding images frequently, it might make sense to cache some
dependency downloads locally. The easiest way to do this is to use a local Squid
instance.

.. code-block:: bash

 sudo yum install -y squid
 sudo sed -ie 's/^http_port.*/http_port 127.0.0.1:3128/g' /etc/squid/squid.conf
 echo "maximum_object_size 100 MB" | sudo tee --append /etc/squid/squid.conf
 echo "cache_dir ufs /var/spool/squid 2000 16 256" | sudo tee --append /etc/squid/squid.conf
 sudo systemctl enable squid
 sudo systemctl start squid

Before you rebuild an image or run functional tests the next time, set the
following environment variables to use the cache. Once dependencies are cached,
it should significantly speed up image building.

.. code-block:: bash

 export http_proxy=http://127.0.0.1:3128
 export https_proxy=http://127.0.0.1:3128


How to run the tests locally
----------------------------

There are five kinds of tests one can run from the development environment (host
hypervisor):

* Unit tests
* Functional tests
* Upgrade tests
* package building
* GUI tests

Before sending a patch to the upstream software factory code, please run functional
and unit tests locally first to ensure the quality of your code.

unit testing
............

To run unit tests, cd into the repository's directory and run:

.. code-block:: bash

  ./run_tests.sh

Note that some repositories might lack unit tests, for example **distgits**.
Changes on these repositories must be tested by attempting to build packages.

testing RPM packaging
.....................

To build the package for a specific repository, use the following command:

.. code-block:: bash

 /path/to/sfinfo/zuul_rpm_build.py --project <repository> --distro-info /path/to/sfinfo/sf-master.yaml

You can check the help message for zuul_rpm_build.py for more details about its parameters.

functional testing
..................

Before you can test a change on any given component, you need to package it:

.. code-block:: bash

 /path/to/sfinfo/zuul_rpm_build.py --project <repository> --distro-info /path/to/sfinfo/sf-master.yaml  --local_output /var/lib/sf/zuul-rpm-build --noclean

(you need to make sure the directory /var/lib/sf/zuul-rpm-build exists and is writable)

You can then launch functional tests like this:

.. code-block:: bash

  ./path/to/software-factory/run_functional-tests.sh           # functional tests
  ./path/to/software-factory/run_functional-tests.sh upgrade   # upgrade tests


The functional tests will start LXC container(s) on the local VM to simulate
as close as possible a real deployment:

.. code-block:: bash

  ./run_functional-tests.sh    # run functional tests
  ssh -l root sftests.com      # /etc/hosts entry is automatically added


How to develop and/or run a specific functional test
----------------------------------------------------

Functional tests needs access to the keys and configuration of the deployment.
First you need to copy the sf-bootstrap-data/ from the managesf node.

.. code-block:: bash

  rsync -a root@sftests.com:/var/lib/software-factory/bootstrap-data/ sf-bootstrap-data/
  nosetests --no-byte-compile -s -v tests/functional

Tips:

* '-s' enables the use of 'import pdb; pdb.set_trace()' within a test
* Within a test insert 'from nose.tools import set_trace; set_trace()' to add breakpoint in nosetests
* '--no-byte-compile' makes sure no .pyc are run
* you can use file globs to select specific tests: [...]/tests/functional/\*zuul\*
* in order to have passwordless ssh and dns configuration, here is a convenient .ssh/config file:

.. code-block:: none

  Host sftests.com
    StrictHostKeyChecking no
    User root
    Hostname 192.168.135.101


How to contribute
-----------------

* Connect to http://softwarefactory-project.io/
* Register your public SSH key on your account. Have a look to: :ref:`Adding public key`.
* Check the bugtracker and the pending reviews
* Submit your change

.. code-block:: bash

  cd /srv/software-factory
  git-review -s # only relevant the first time to init the git remote
  git checkout -b"my-branch"
  # Hack the code, create a commit on top of HEAD ! and ...
  git review # Summit your proposal on softwarefactory-project.io

Have a look to http://softwarefactory-project.io/r/ where you will find the patch
you have just submitted. Automatic tests are run against it and Jenkins/Zuul will
report a status as comments on the Gerrit page related to your patch. You can
also check http://softwarefactory-project.io/zuul/ to follow the test process.

Note that Software Factory is developed using Software Factory. That means that you can
contribute to SF in the same way you would contribute to any other project hosted
on SF: :ref:`contribute`.
