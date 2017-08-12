marc2bib :book:
===============

.. image:: https://img.shields.io/pypi/v/marc2bib.svg
	:target: https://pypi.python.org/pypi/marc2bib
.. image:: https://travis-ci.org/xymaxim/marc2bib.svg?branch=master
	:target: https://travis-ci.org/xymaxim/marc2bib

marc2bib is a Python package that allows to convert bibliographic
records from MARC format to BibTeX entries. Requires Python 3.

It uses `pymarc <https://github.com/edsu/pymarc>`_ to read MARC data
files.

Installation
------------

As *always*, use `pip
<https://pip.pypa.io/en/latest/installing.html>`_ to install the
latest release from PyPI:

.. code:: sh

	$ pip install marc2bib

Or for development:

.. code:: sh

	$ git clone https://github.com/mstolyarchuk/marc2bib
	$ pip install -e marc2bib

Quickstart
----------

If you have not used ``pymarc`` before, nothing to worry about.

Now we are going to read some data from a MARC file and easily convert
it to a BibTeX entry:

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

This project is `hosted on GitHub
<https://github.com/mstolyarchuk/marc2bib>`_. There you can `create a
new issue`__ or submit pull requests for review.

__ https://github.com/mstolyarchuk/marc2bib/issues/new


Running the tests
~~~~~~~~~~~~~~~~~

For testing our package we use `pytest
<http://pytest.org/latest/>`_. In order to run all tests, execute the
following commands (you probably want to set up a `virtualenv
<http://virtualenv.readthedocs.org/en/latest/>`_ first):

.. code::

	$ pip install pytest
	$ pytest tests

Acknowledgments
---------------

Thanks go to all the authors and contributors of the `pymarc
<https://github.com/edsu/pymarc>`_ package.  This project would not
have been possible without their work.
