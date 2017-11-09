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
