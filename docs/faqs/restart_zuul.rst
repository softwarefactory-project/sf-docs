.. _restart_zuul:

How to restart zuul without losing builds in progress ?
-------------------------------------------------------

The zuul service is stateless and stopping the process will lose track
of running jobs. However the zuul-changes.py utility can be used
to save and restore the current state:

.. code-block:: bash

    # Print and save all builds in progress to /var/lib/zuul/zuul-queues-dump.sh
    /usr/share/sf-config/scripts/zuul-changes.py dump

    systemctl restart zuul-scheduler

    # Reload the previous state:
    /usr/share/sf-config/scripts/zuul-changes.py load

The periodic and post pipelines are not dumped by this tool.
