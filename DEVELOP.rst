

Developing dkfileutils
======================

.. note:: if you're using this as a template for new projects, remember to
          ``python setup.py register <projectname>`` before you upload to
          PyPi.

Uploading to PyPI
-----------------
This requires pyinvoke (``pip install invoke``) and dk-tasklib
(``pip install dk-tasklib``). These are not listed as requirements.

Create a new version::

    inv upversion

Check in new version numbers:

    git add ...
    git commit ...

Verify that everything is copacetic::

    inv publish

Tag the release (replace 1.2.3 with the new version number)::

    git tag -a v1.2.3 -m "Version 1.2.3"
    git push origin --tags

then push to PyPi::

    inv publish -f


Running tests
-------------
One of::

    python setup.py test
    py.test dkfileutils

with coverage (one of)::

    py.test --cov=.
    coverage run runtests.py && coverage report



Building documentation
----------------------
::

    python setup.py build_sphinx

