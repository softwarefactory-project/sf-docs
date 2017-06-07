.. _sfdib:

SF image building
=================

In order to have a ready-to-use diskimage with all the components pre-installed,
we are using a diskimage builder element to call the install tasks of each roles.

Rebuild the image
-----------------

Using the sf-elements project, execute the create_sf_image.sh script:

.. code-block:: bash

 $ git clone https://softwarefactory-project.io/r/software-factory/sf-elements
 $ cd sf-elements
 $ ./scripts/create_sf_image.sh
