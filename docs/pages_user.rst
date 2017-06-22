.. _pages-user:

Publish static WEB content
==========================

Please have a look to :ref:`Pages service for hosting static WEB content <pages-operator>` for
more informations about the service.

Create the source repository
----------------------------

Software Factory detects publication repositories named *<name>.<sfdomain>* and
handles them as special repositories that contain content to be published.

For example, the Sofware Factory instance your are using is accessible
via the hostname *sftests.com* and you want to host content accessible
via the hostname *myproject.sftests.com* then simply create the
repository *myproject.sftests.com*. The repository name determines whether
it is a publication repository and its publication hostname.

Please refer to this :ref:`section <resources-user>` for repository creation
instructions.

Publish content
---------------

The Git repository can be populated with raw content or pelican (https://blog.getpelican.com) sources.

Behind the scene Softare Factory attaches two CI jobs to publication repositories:

 * pages-render (triggered by the check and gate pipelines)
 * pages-update (triggered by the post pipeline)

The former detects the content type and runs some content check.
Actually only pelican content is checked. The source is processed
by the job thus any mistakes detected by pelican will generate a
negative feedback note on the code review service.

Both job detect pelican content by testing if the file *pelicanconf.py*
exists at the root of the repository.

The latter performs the two tasks rendering (for pelican source) and publication.
The *pages-updates* job run in the *post* pipeline meaning that the run occurs
once the code is merged in the Git repository.

As soon as the code is merged and the job finished then the content is accessible
under *http(s)://<repo-name>*.

Hostname resolution
-------------------

The Software instance domain DNS configuration must be setuped with a wildcard
for all subdomains to be redirected to the Software Factory gateway IP.
If you run a Software Factory in a test environment you might not have
a real DNS entry configured then you should setup your local resolver.

For exemple adding in /etc/hosts:

.. code-blosk:: bash

 echo "<SF IP> <repo-name>" | sudo tee -a /etc/hosts
