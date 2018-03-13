.. _gerrit_rest_api:

How can I use the Gerrit REST API?
----------------------------------

The Gerrit REST API is open for queries by default on all Software Factory deployments.
There is an extensive documentation available online:

  https://gerrit-review.googlesource.com/Documentation/rest-api.html

To use the Gerrit REST API in Software Factory, you have to create an API
password first. To do so, go to the **User Settings** page (upper right corner on the top menu)
and click the Enable button for "Gerrit API key".

The Gerrit API is available at the following endpoint:

  https://fqdn/api/

and for authenticated requests, using the API password:

  https://fqdn/api/a/

For example, getting open, watched changes on the default deployment with cURL would be:

  curl -X GET http://sftests.com/api/changes/?q=status:open+is:watched&n=2

You can find a full working example to automate some tasks (in this case deleting a specific branch
on a list of projects) in `tools/deletebranches.py`.
