Configure zuul
--------------

External logserver
^^^^^^^^^^^^^^^^^^

You can configure Zuul to use an external log server.

* First you need to authorize the zuul process to connect to the server
  (with scp). Add the zuul public key to the authorized_key of the remote user:
  /var/lib/zuul/.ssh/id_rsa.pub

* Edit /etc/software-factory/sfconfig.yaml:

.. code-block:: yaml

  zuul:
    external_logservers:
      - name: logs.example.com
        user: loguser
        path: /var/www/logs/sftests.com/

* Then define in the config repository a custom publisher using this site
  (in the jobs-zuul directory):

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

* To export console-log to this new site, change the default_log_site and log_url
  so that it's readily available to change author, in
  /etc/software-factory/sfconfig.yaml:

.. code-block:: yaml

  zuul:
    default_log_site: logs.example.com
    log_url: https://logs.example.com/logs/sftests.com/{build.parameters[LOG_PATH]}

* The provided console-log macros is not automatically updated, it must be
  manually changed in the config repo zuul-jobs/_macros.yaml:

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
