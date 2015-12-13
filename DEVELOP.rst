

Developing dkfileutils
======================

.. note:: if you're using this as a template for new projects, remember to
          `python setup.py register <projectname>` before you upload to 
          PyPi.

Uploading to PyPI
-----------------

- only source distribution::

    python setup.py sdist upload

- source and windows installer::

    python setup.py sdist bdist_wininst upload

- source, windows, and wheel installer::

    python setup.py sdist bdist_wininst bdist_wheel upload

- create a documentation bundle to upload to PyPi::

    cd build/sphinx/html && zip -r ../../../pypi-docs.zip *


Running tests
-------------
One of::

    python setup.py test
    py.test dkfileutils
    python runtests.py

with coverage (one of)::

    py.test --cov=.
    python runtests.py --cov=.
    coverage run runtests.py && coverage report



Building documentation
----------------------
::

    python setup.py build_sphinx
