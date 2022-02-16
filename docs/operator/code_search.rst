.. _hound-operator:

Source code search engine
-------------------------

Software Factory bundles with `Hound`_, an extremely fast source code search engine that allow users to search
in all the git repositories hosted on your Software Factory deployment.

.. _`Hound`: https://github.com/hound-search/hound

Activating Hound
^^^^^^^^^^^^^^^^
Hound is not deployed by default but can be activated by adding them in /etc/software-factory/arch.yaml.

You can deploy Hound on different host if needed. To activate hound, just add the "hound" role to *arch.yaml* file:

.. code-block:: yaml

   inventory:
      - name: managesf
        ip: 192.168.0.10
        roles:
          ...
          - hound


Then run :ref:`sfconfig  <configure_reconfigure>` to deploy all components.

This will automatically enable the Code search menu within the landing page.