.. _nodepool3-user:

Refer to the upstream documentation_ first.

.. _documentation: https://docs.openstack.org/infra/nodepool/feature/zuulv3


Nodepool(V3) configuration
==========================

Labels, providers and diskimage are defined in *config/nodepoolV3/*.

Below is an example of a cloud provider configuration and an associated
diskimage/label:

.. code-block:: yaml

  ---
  diskimages:
    - name: centos7
      formats:
        - raw
      elements:
        - centos-minimal
        - nodepool3-minimal
        - sf-zuul3-worker

  labels:
    - name: centos7
      min-ready: 1

  providers:
    - name: nodepool-provider
      cloud: default
      clean-floating-ips: true
      image-name-format: '{image_name}-{timestamp}'
      boot-timeout: 120
      rate: 10.0
      diskimages:
        - name: centos7
      pools:
        - name: main
          max-servers: 20
          networks:
             - workers
          labels:
            - name: centos7
              min-ram: 1024
              diskimage: centos7

