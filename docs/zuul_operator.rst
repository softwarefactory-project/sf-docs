Configure zuul
--------------

Running multiple zuul-merger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run multiple zuul-merger:

* Starts a new CentOS instance, either with the sf default secgroup security group, either externally and
  enabling gearman server access to the zuul-server.

* Adds the new host using a slave reachable ip address in /etc/software-factory/arch.yaml:

.. code-block:: yaml

  - name: zuul-merger01
    ip: x.x.x.x
    roles:
      - zuul-merger

* If the host has a public url, set the public url:

.. code-block:: yaml

  - name: zuul-merger01
    ip: x.x.x.x
    public_url: https://zm01.example.com
    roles:
      - zuul-merger

* If the host doesn't have a hostname, then the slave will use the host ip.

External logserver
^^^^^^^^^^^^^^^^^^

You can configure Zuul to use an external log server.

* First you need to authorize the zuul process to connect to the server (scp).
  Add the zuul public key to the authorized_key of the remote user:
  /var/lib/zuul/.ssh/id_rsa.pub

* Edit /etc/software-factory/sfconfig.yaml:

.. code-block:: yaml

  zuul:
    external_logservers:
      - name: logs.example.com
        user: loguser
        path: /var/www/logs/sftests.com/

* Then add this site to a custom publisher, for example in
  /root/config/zuul-jobs/my_macros.yaml:

.. code-block:: yaml

  - publisher:
      name: logs.example.com
      publishers:
        - scp:
	    # Site name must match external_logserver name
            site: 'logs.example.com'
            files:
              - target: '$LOG_PATH'
                source: 'artifacts/**'
                keep-hierarchy: true
                copy-after-failure: true

* Run sfconfig.py to configure the logserver in zuul.conf, and merge the config
  repo change.

* To change the default site for console-log publisher,
  edit /etc/software-factory/sfconfig.yaml:

.. code-block:: yaml

  zuul:
    default_log_site: logs.example.com
    log_url: https://logs.example.com/logs/sftests.com/{build.parameters[LOG_PATH]}

* The provided console-log macros is not automatically updated, it must be
  manually changed: /root/config/zuul-jobs/_macros.yaml

.. code-block:: yaml

  - publisher:
      name: console-log
      publishers:
        - scp:
            site: 'logs.example.com'
            files:
              - target: '$LOG_PATH'
                copy-console: true
                copy-after-failure: true

* Run sfconfig.py to configure the logserver in zuul.conf, and merge the config
  repo change.


Third-party CI configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can configure Zuul to connect to a remote gerrit event stream.
First you need a Non-Interactive Users created on the external gerrit.
Then you need to configure that user to use the local zuul ssh public key:
/var/lib/zuul/.ssh/id_rsa.pub
Finally you need to activate the gerrit_connections setting in sfconfig.yaml:

.. code-block:: yaml

   gerrit_connections:
        - name: openstack_gerrit
          hostname: review.openstack.org
          puburl: https://review.openstack.org/r/
          username: third-party-ci-username


To benefit from Software Factory CI capabilities as a third party CI, you
also need to configure the config repository to enable a new gerrit trigger.
For example, to setup a basic check pipeline, add a new 'zuul/thirdparty.yaml'
file like this:

.. code-block:: yaml

    pipelines:
        - name: 3rd-party-check
          manager: IndependentPipelineManager
          source: openstack_gerrit
          trigger:
              openstack_gerrit:
                  - event: patchset-created


Notice the source and trigger are called 'openstack_gerrit' as set in the
gerrit_connection name, instead of the default 'gerrit' name.

See the :ref:`Zuul user documentation<zuul-user>` for more details.
