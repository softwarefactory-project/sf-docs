.. _nodepool3-user:

Refer to the upstream `documentation <https://docs.openstack.org/infra/nodepool/feature/zuulv3/>`
first.


Nodepool(V3) configuration
==========================

Labels, providers and diskimage are defined in config/nodepool/nodepoolV3.yaml:

.. code-block:: yaml

  labels:
    - name: centos-oci

  providers:
    - name: oci
      driver: oci
      hypervisor: centos.example.org
      pools:
        - name: main
          max-servers: 10
          labels:
            - name: centos-oci


The centos.example.org can be configured using the 'hypervisor' role in the arch
file. Basically, the oci driver needs:

* nodepool user needs root access to the instance
* zuul user needs zuul access
* /var/lib/zuul/src needs to be created
* runc and all test tools needs to be installed
