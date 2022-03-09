marc2bib :book:
===============

.. image:: https://img.shields.io/pypi/v/marc2bib.svg
	:target: https://pypi.python.org/pypi/marc2bib

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

The package works along with `pymarc
<https://gitlab.com/pymarc/pymarc>`_ utilized to read MARC files. If
you have not used it before, nothing to worry about. Let's read some
data from a MARC file and convert it to a BibTeX entry:

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
	  
More examples
-------------

Tag-functions
*************

To parse a value of BibTeX tags (fields), we use so-called
tag-functions. Currently ``marc2bib`` fully supports book BibTeX
entries—the tag-functions are defined for the related required
and optional tags. The user can extend or override them easily:

.. code:: python

	  from marc2bib import BOOK_REQ_TAGFUNCS

	  def title_title(record):
	      return BOOKS_REQ_TAGFUNCS['title'](record).title()
	      
	  convert(record, tagfuncs={'title': title_title}) 

Customizing return
******************

The returned tags can be either all (required and optional),
only required (default), or required with user-defined ones:

.. code:: python

	  # Return required tags and 'pages'
	  convert(record, include=['pages']) # or 'all', 'required' 

A note: if you use tag-functions, no need to specify these tags for
including separately.

Convert to BibTeX or just map tags
**********************************

The main function of this package is ``convert(...)``. It combines two
steps: (1) mapping MARC fields to BiBTex tags and (2) converting the
tags to BibTeX string. However, instead of converting MARC data to
BibTeX string in one call, you can map it to a dictionary of BibTeX
tags (fields) for inspection or post-processing (step 1):

.. code:: python

	  >>> from marc2bib import map_tags

	  >>> tags = map_tags(record)
	  >>> print(tags['author'])
	  Author, Name

Then, you can convert these mapped tags to a BibTeX string (step 2): 

.. code:: python

	  >>> from marc2bib import tags_to_bibtex

	  >>> new_bibkey = tags['author'].split(',')[0] + tags['year']
	  >>> # By the way, the indentation is customizable.
	  >>> bibtex = tags_to_bibtex(tags, bibkey=new_bibkey, indent=4)
	  >>> print(bibtex)
	  @book{Author2022,
              author = {Author, Name},
              . . .
          }
	  
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
