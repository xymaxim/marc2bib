marc2bib :book:
===============

.. image:: https://img.shields.io/pypi/v/marc2bib.svg
	:target: https://pypi.python.org/pypi/marc2bib
.. image:: https://app.travis-ci.com/xymaxim/marc2bib.svg?branch=master
	:target: https://app.travis-ci.com/github/xymaxim/marc2bib

marc2bib is a Python package that allows to convert bibliographic
records from MARC format to BibTeX entries.

Installation
------------

marc2bib is available on PyPI:

.. code:: sh

	$ pip install marc2bib

Or for development:

.. code:: sh

	$ git clone https://github.com/mstolyarchuk/marc2bib
	$ pip install -e marc2bib

Quickstart
----------

If you have not used ``pymarc`` before, nothing to worry about.

Let's read some data from a MARC file and convert it to a BibTeX
entry:

.. code:: python

          >>> from pymarc import MARCReader
          >>> from marc2bib import convert

          >>> with open('file.mrc', 'rb') as f:
          ...     reader = MARCReader(f)
          ...     record = next(reader)  # read the first record
          ...     print(convert(record)) # convert it to a BibTeX entry
          ...
          @book{author2022,
           author = {Author, Name},
           . . .
          }

And that is it!

Tag-functions and customized return
-----------------------------------

To parse a value of BibTeX tags (fields), we use so-called
tag-functions. Currently ``marc2bib`` fully supports book BibTeX
entries—the tag-functions are defined for the related required
and optional tags. The user can extend or override them easily:

.. code:: python

	  from marc2bib import BOOK_REQ_TAGFUNCS

	  def title_title(record):
	      return BOOKS_REQ_TAGFUNCS['title'](record).title()
	      
	  convert(record, tagfuncs={'title': title_title}) 

The returned tags can be either all (required and optional—default),
only required, or required with user-defined ones:

.. code:: python

	  # Return required tags and 'pages'
	  convert(record, include=['pages']) # or 'all', 'required' 

Testing
-------

For testing the package we use `pytest
<http://pytest.org/latest/>`_. In order to run all tests, check out
this repository and type:

.. code::

	$ pytest

Acknowledgments
---------------

Thanks go to all the authors and contributors of the `pymarc
<https://gitlab.com/pymarc/pymarc>`_ package.  This project would not
have been possible without their work.
