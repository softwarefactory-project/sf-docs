Firehose
--------

Firehose is an embedded MQTT broker that concentrates events from services
that are run within your Software Factory deployment.

See the :ref:`Firehose user documentation<firehose-user>` for more details.

Activating Firehose
^^^^^^^^^^^^^^^^^^^

Versions 2.5 and above
......................
Firehose is activated by default on fresh installations. The role "firehose" is present in the architecture
file in /etc/software-factory/arch.yaml.

The broker will then be available on firehose.fqdn on port 1883 (standard MQTT port).

After upgrading from Software Factory 2.4.X
...........................................
To enable Firehose after upgrading to 2.5, some manual steps are required:

#. Add the "firehose" role to the architecture file in /etc/software-factory/arch.yaml
#. run sfconfig.py on the managesf node of the deployment
#. Apply the following patch to config/jobs/_default_jobs.yaml:

::

  --- a/jobs/_default_jobs.yaml
  +++ b/jobs/_default_jobs.yaml
  @@ -11,6 +11,8 @@
         - ansicolor:
             colormap: gnome-terminal
         - timestamps
  +    publishers:
  +      - firehose-zuul
       concurrent: true

   - builder:
  @@ -28,6 +30,17 @@
             rm -Rf ./*
             echo "Clone $ZUUL_PROJECT"
             zuul-cloner http://softwarefactory-project.io/r $ZUUL_PROJECT
  +- publisher:
  +    name: firehose-zuul
  +    publishers:
  +      - mqtt:
  +          broker-url: tcp://managesf.sftests.com:1883
  +          topic: zuul_jobs
  +          credentials-id: 900936e8-a4e0-483e-8ab8-07bca5f80699
  +          message: |
  +            {"build": "${BUILD_NUMBER}", "job": "${JOB_NAME}", "status": "${BUILD_RESULT}", "node": "${NODE_NAME}", "ZUUL_UUID": "${ZUUL_UUID}", "ZUUL_PIPELINE": "${ZUUL_PIPELINE}", "ZUUL_URL": "${ZUUL_URL}", "ZUUL_PROJECT": "${ZUUL_PROJECT}", "ZUUL_BRANCH": "${ZUUL_BRANCH}", "ZUUL_CHANGES": "${ZUUL_CHANGES}", "ZUUL_REF": "${ZUUL_REF}", "ZUUL_COMMIT": "${ZUUL_COMMIT}", "ZUUL_CHANGE_IDS": "${ZUUL_CHANGE_IDS}", "ZUUL_CHANGE": "${ZUUL_CHANGE}", "ZUUL_PATCHSET": "${ZUUL_PATCHSET}"}
  +          qos: AT_MOST_ONCE
  +          retain-message: false

   - builder:
       name: zuul-swift-upload

This will define the mqtt publisher and call it whenever a job defined in the configuration repository is completed.

Security
^^^^^^^^

Only the service user can publish events to the broker. All other accesses will be
read-only.
