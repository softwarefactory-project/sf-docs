.. _nodepool3-user:

.. danger::

  Nodepool(V3) is still under heavy development and breaking changes might occur from one
  version of Software Factory to another. It is strongly advised to follow
  Nodepool's upstream developments, for example by registering to OpenStack Infra's
  `mailing list <http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-infra>`_.

.. note::

  This is a lightweight documentation intended to get users started with defining
  test nodes. For more insight on what Nodepool can do, please refer
  to its upstream documentation_.

.. _documentation: https://docs.openstack.org/infra/nodepool/feature/zuulv3/


Nodepool(V3) configuration
==========================

Labels, providers and diskimage are defined in config/nodepool/nodepoolV3.yaml,
below is an example of the configuration for using the OCI driver provided by
the hypervisor-oci role:

.. code-block:: yaml

  labels:
    - name: centos-oci

  providers:
    - name: oci
      driver: oci
      # Hypervisor hostname
      hypervisor: centos.example.org
      pools:
        - name: main
          max-servers: 10
          labels:
            - name: centos-oci


The centos.example.org can be configured using the 'hypervisor-oci' role in the arch
file. Basically, the oci driver needs:

* nodepool user needs root access to the instance
* zuul user needs zuul access
* /var/lib/zuul/src needs to be created
* runc and all test tools needs to be installed
