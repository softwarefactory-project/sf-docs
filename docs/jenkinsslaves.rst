Configure slave nodes for Jenkins
=================================

This section describes the method to attach Jenkins slaves to the Jenkins master
provided by SF.


Automatic setup via the Jenkins UI
----------------------------------

The easiest way is to start a VM and allow the Jenkins master to connect via
SSH on it. Indeed Jenkins is able to convert a minimal VM to a Jenkins slave.
Nevertheless the minimal VM needs some adjustments in order to let Jenkins
start the slave process.

The instructions below are adapted to Centos 7 but should work on others Linux
distributions.

.. code-block:: bash

 $ sudo yum install -y epel-release
 $ sudo yum install -y java-1.8.0-openjdk python-pip gcc python-devel
 $ sudo pip install zuul
 $ sudo useradd -m jenkins
 $ sudo gpasswd -a jenkins wheel
 $ echo "jenkins ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/jenkins-slave
 $ echo 'Defaults   !requiretty' | sudo tee --append /etc/sudoers.d/jenkins-slave
 $ sudo chmod 0440 /etc/sudoers.d/jenkins-slave
 $ sudo mkdir /home/jenkins/.ssh
 $ sudo chown -R jenkins /home/jenkins/.ssh
 $ sudo chmod 700 /home/jenkins/.ssh
 $ sudo touch /home/jenkins/.ssh/authorized_keys
 $ sudo chmod 600 /home/jenkins/.ssh/authorized_keys

Then copy inside "/home/jenkins/.ssh/authorized_keys" the public key of Jenkins that you
can find in this file "/root/sf-bootstrap-data/ssh_keys/jenkins_rsa.pub" on the SF instance.

As the administrator, go in "Manage jenkins"/"Manage nodes"/"New node" and select
"Dumb node" plus add a node name. Keep the amount of executor to 1 if your jobs can't
run in paralllel. Set the "Remote root directory" to "/home/jenkins". Add the needed
label (your are going to use that label in the JJB descriptions of your jobs).
Keep "Launch slave agents on Unix machines via SSH" and the default credential
"jenkins (slave)" then enter the IP address of the VM you just created. Save, then
you should see the Slave appears in the Slave list.


Using nodepool to manage Jenkins slaves
---------------------------------------

See the :ref:`Nodepool operator documentation<nodepool-operator>` as well as the :ref:`Nodepool user documentation<nodepool-user>`
