.. _how_to_contribute:

How to contribute
-----------------

* Connect to `softwarefactory-project.io`_ to create an account
* Register your public SSH key on your account. See: :ref:`Adding public key`
* Check the `bug tracker`_ and the `pending reviews`_

The product is made out of `several repositories`_  and you can
just copy the link from the name column and use it for git cloning. For example
you can see how to clone documentation:

.. code-block:: bash

    # clone docs
    git clone https://softwarefactory-project.io/cgit/software-factory/sf-docs/


Submit a change
...............

.. code-block:: bash

  git-review -s # only relevant the first time to init the git remote
  git checkout -b"my-branch"
  # Hack the code, create a commit on top of HEAD ! and ...
  git review # Summit your proposal on softwarefactory-project.io

Your patch will be listed on the `reviews dashboard`_.
Automatic tests are run against it and the CI will
report results on your patch's summary page. You can
also visit `/zuul/`_  to check where your patch is in the pipelines.

Note that Software Factory is developed using Software Factory. That means that you can
contribute to it in the same way you would contribute to any other project hosted
on an instance: :ref:`contribute`.

.. _`bug tracker`: https://tree.taiga.io/project/morucci-software-factory/backlog?q=
.. _`pending reviews`: https://softwarefactory-project.io/r/#/q/project:%255Esoftware-factory.*
.. _`several repositories`: https://softwarefactory-project.io/cgit/?q=software-factory%2Fsf
.. _`reviews dashboard`: https://softwarefactory-project.io/r/
.. _`/zuul/`: https://softwarefactory-project.io/zuul/
.. _`softwarefactory-project.io`: https://softwarefactory-project.io/