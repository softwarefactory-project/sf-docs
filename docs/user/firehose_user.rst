.. _firehose-user:

Firehose
========

Firehose is an embedded MQTT broker that concentrates
events from services run within a Software Factory
deployment, making it easy for external processes to
consume these events and act upon them.

It is not possible to publish messages on the firehose outside of
the predefined services, however anyone is allowed to subscribe
anonymously to the feed by using the MQTT protocol.

Services supported
------------------

================= ============= ================
  Service           Topic         Source
================= ============= ================
 Zuul               zuul          `reporter`_
 keycloak           keycloak      `keycloakemitter`_
================= ============= ================

.. _reporter: https://zuul-ci.org/docs/zuul/5.0.0/drivers/mqtt.html#reporter-configuration
.. _keycloakemitter: https://github.com/softwarefactory-project/keycloak-event-listener-mqtt

Events published
----------------

Zuul
....

Every buildset results are published. A full description of the events can
be found here: `Message Schema <https://zuul-ci.org/docs/zuul/5.0.0/drivers/mqtt.html#message-schema>`_

Keycloak
........

EA Keycloak SPI that publishes events to a MQTT broker. A fuul description can
be found here: `Keycloak Deploy <https://github.com/softwarefactory-project/keycloak-event-listener-mqtt#deploy>`_

Subscribing to events
---------------------

Simple CLI example
..................

The mosquitto project provides a CLI subscriber client that can be used to easily
subscribe to any topic and receive the messages. On debian based distributions it
is included in the **mosquitto-clients** package; on Fedora or CentOS it can be found
in the **mosquitto** package.
For example, to subscribe to every topic on the firehose you would run::

    mosquitto_sub -h firehose.fqdn --topic '#'

You can adjust the value of the topic parameter to subscribe only to a specific service.

Simple desktop notifier
.......................

If you are using a GTK based desktop
environment such as gnome, this script can be used
to get notifications on specific, customizable events from the `Software Factory Firehose desktop notifications project <https://softwarefactory-project.io/cgit/software-factory/sf-desktop-notifications/tree/>`_.

Please see the project's README for more information.
