

Developing dkfileutils
======================


Uploading to PyPI
-----------------
New versions are automatically uploaded to PyPI when a new tag is pushed to
GitHub. To create a new tag, run::

    git tag -a v0.1.0 -m "Version 0.1.0"
    git push --tags

(or internally ``dk upversion --tag``)


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

internally (``dk docs``).

