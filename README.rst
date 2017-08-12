marc2bib :book:
===================

.. image:: https://img.shields.io/pypi/v/marc2bib.svg
	:target: https://pypi.python.org/pypi/marc2bib
.. image:: https://travis-ci.org/xymaxim/marc2bib.svg?branch=master
	:target: https://travis-ci.org/xymaxim/marc2bib

marc2bib is a Python package that allows to convert bibliographic records
from MARC format to BibTeX entries. Requires Python 3.

It uses pymarc_ to read MARC data files.

Installation
------------

As *always*, use pip_ to install the latest release from PyPI:

.. code:: sh

	$ pip install marc2bib

Or for development:

.. code:: sh

	$ git clone https://github.com/mstolyarchuk/marc2bib
	$ pip install -e marc2bib

Quickstart
---------------

If you have not used ``pymarc`` before, nothing to worry about.

Now we are going to read some data from a MARC file and easily convert it to a BibTeX entry:

.. code:: python

          >>> from pymarc import MARCReader
          >>> from marc2bib import convert

          # Open a MARC file as you usually do this with pymarc.
          >>> with open('file.mrc', 'rb') as f:
          ...     reader = MARCReader(f)
          ...     record = next(reader)  # Read the first record
          ...     print(convert(record)) # and, ta-da, convert it to a BibTeX entry.
          ...
          @book{Hargittai2009,
           author = {Hargittai, István},
           . . .
          }

And that is it!

Contributing
------------

This project is `hosted on GitHub`_. There you can `create a new issue`_ or submit pull requests for review.

Running the tests
^^^^^^^^^^^^^^^^^

For testing our package we use pytest_. In order to run all tests, execute the following commands
(you probably want to set up a virtualenv_ first):

.. code::

	$ pip install pytest
	$ py.test tests

Acknowledgments
---------------

Thanks go to all the authors and contributors of the pymarc_ package.
This project would not have been possible without their work.

.. _pymarc: https://github.com/edsu/pymarc
.. _pip: https://pip.pypa.io/en/latest/installing.html
.. _pytest: http://pytest.org/latest/
.. _virtualenv: http://virtualenv.readthedocs.org/en/latest/
.. _hosted on GitHub: https://github.com/mstolyarchuk/marc2bib
.. _create a new issue: https://github.com/mstolyarchuk/marc2bib/issues/new
.. _MARC21: http://www.loc.gov/marc/bibliographic/
