.. _log-classify:

Log Classify
============

To simplify CI jobs failure, Software Factory integrates logs processing
utilities to analyze and reports root cause.

The log-classify process is based on the logreduce_ utility. The base
principle is to query the build database for nominal builds outputs
and search for novelties in failed builds to extract failure root causes.
More information about logreduce_ can be found
`here <https://opensource.com/article/18/9/quiet-log-noise-python-and-machine-learning>`_.

Check the :ref:`operator documentation <log-classify-operator>` to enable
the process and the :ref:`user documentation <log-classify-user>` to
configure it for your job.

.. _logreduce: https://pypi.org/project/logreduce/
