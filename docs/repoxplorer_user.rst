.. _repoxplorer-manual-configuration:

RepoXplorer manual configuration
================================

Please have a look to :ref:`repoxplorer admin configuration <repoxplorer-operator>` for
more informations about the service.

Configuration
-------------

Manual configuration is done via the config repository of Software Factory.
Each time a change is proposed under the config/repoxplorer tree a config
validator is run.

Thanks to the config/repository tree you can:

- define author identities
- define custom group and group's memberships
- define indexation of projects/repositories not defined into Software Factory
- overwrite automatic configuration

How to define author's identities and emails
--------------------------------------------

You can add a .yaml file in config/repoxplorer/ such as:

.. code-block:: yaml

 identities:
  0000-0000:
    name: John Doe
    default-email: john.doe@server.com
    emails:
      john.doe@server.com:
        groups: {}
      jdoe@server.com:
        groups: {}

Please refer to repoXplorer upstream documentation for more details
about the format `Sanitize author identities <https://github.com/morucci/repoxplorer/blob/015c87543a01badf896df66e299a1b48e4aefbf7/README.md#sanitize-author-identities>`_.
