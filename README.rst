marc2bib :book:
***************

.. image:: https://img.shields.io/pypi/v/marc2bib.svg
	:target: https://pypi.python.org/pypi/marc2bib

marc2bib is a Python package that allows to convert bibliographic
records from MARC 21 format to BibTeX entries.

Installation
============

marc2bib is available on PyPI:

.. code:: sh

	$ pip install marc2bib

Or for development:

.. code:: sh

	$ git clone https://github.com/xymaxim/marc2bib
	$ pip install -e marc2bib

Quickstart
==========

The package works along with `pymarc
<https://gitlab.com/pymarc/pymarc>`_ utilized to read MARC files. If
you have not used it before, nothing to worry about. Let's read some
data from a MARC file and convert it to a BibTeX entry:

.. code:: python

          >>> from pymarc import MARCReader
          >>> from marc2bib import convert

          >>> with open("file.mrc", "rb") as f:
          ...     reader = MARCReader(f)
          ...     record = next(reader)  # read the first record
          ...     print(convert(record)) # convert it to a BibTeX entry
          ...
          @book{author2022,
           author = {Author, Name},
           . . .
          }

And that is it!
	  
Overview
========

Convert to BibTeX or just map tags
----------------------------------

The main function of this package is ``convert()``. It combines two
steps: (1) mapping MARC fields to BiBTex tags, ``map_tags()``,
and (2) converting the tags to BibTeX string,
``tags_to_bibtex()``. However, instead of converting MARC data to
BibTeX string in one call, you can first map it to a dictionary of
BibTeX tags, for example, for inspection or post-processing (step 1):

.. code:: python

	  >>> from marc2bib import map_tags

	  >>> tags = map_tags(record)
	  >>> print(tags["author"])
	  Author, Name

Then, you can convert these mapped tags to a BibTeX string (step 2): 

.. code:: python

	  >>> from marc2bib import tags_to_bibtex

	  >>> new_bibkey = tags["author"].split(",")[0] + tags["year"]
	  >>> # By the way, the indentation is customizable.
	  >>> bibtex = tags_to_bibtex(tags, bibkey=new_bibkey, indent=4)
	  >>> print(bibtex)
	  @book{Author2022,
              author = {Author, Name},
              . . .
          }

Of course, the example below can be coded with ``convert()``
function and the choice depends on your needs:

.. code:: python

	  # The bibkey argument can be callable.
	  def new_bibkey(tags):
	     return tags["author"].split(",")[0] + tags["year"]
	     
	  convert(record, bibkey=new_bibkey, indent=4)

Tag-functions
-------------

To parse a value of BibTeX tags (fields), we use so-called
*tag-functions* which operate on one tag per function. Currently
``marc2bib`` fully supports book BibTeX entries—the tag-functions are
defined for the related required and optional tags. The user can
extend or override them easily:

.. code:: python

	  from marc2bib import BOOK_REQ_TAGFUNCS

	  def title_title(record):
	      return BOOKS_REQ_TAGFUNCS["title"](record).title()
	      
	  convert(record, tagfuncs={"title": title_title}) 

Customize returning tags
------------------------

The returned tags can be either all (required and optional), only
required (default), or required with user-provided ones (``include``
argument):

.. code:: python

	  # Return required tags and "pages".
	  convert(record, include=["pages"]) # or "all", "required" 

A note: if you use tag-functions, no need to specify these tags for
including separately.

Default, user-defined, and pre-defined post-hooks
-------------------------------------------------

While tag-functions work with parsing MARC 21 fields, post-hooks run
at the end of translation of the parsed fields to BibTeX tags. There
are *default* and *user-defined* post-hooks which execute in the
presented order.

The hook's function may look as follows:

.. code:: python
	  
	  def hook(tag: str, value: str) -> str:
	      return do_something(value)
	      
Every hook will be called with two arguments: the tag currently
processing and its value. 

See *Cookbook* section for examples on mastering hooks.

Default post-hooks
^^^^^^^^^^^^^^^^^^

The default hooks include two hooks which execution can be controlled
via the corresponding arguments (in parentheses) of ``convert`` and
``map_tags`` functions:

#. ``marc2bib.hooks.remove_isbd_punctuation_hook``
   (``remove_punctuation``, default: True) — remove terminal periods
   and separating punctuation corresponding to MARC 21 format (see the
   below section for details).
  
#. ``marc2bib.hooks.latexify_hook`` (``latexify``, default: True) —
   convert tag value to make it suitable for LaTeX. Currently, it
   escapes LaTeX special characters and normalizes number ranges by
   replacing hyphens with en-dashes.

User-defined hooks
^^^^^^^^^^^^^^^^^^

After default hooks, the user-defined ones are executed. The
``post_hooks`` argument accepts a list of these hooks:

.. code:: python
	  
	  convert(record, post_hooks=[hook1, hook2])

Pre-defined hooks
^^^^^^^^^^^^^^^^^

In addition to the default hooks, the *pre-defined* hooks for some
common cases are supplied with the package:

* ``marc2bib.hooks.strip_outer_square_brackets_hook`` — remove square
  brackets used to mark the additions made by cataloger;
  
* ``marc2bib.hooks.protect_uppercase_letters_hook`` — enclose
  uppercase letters in curly braces to protect the case from changes.


Removal of ISBD punctuation
---------------------------

In the MARC 21 format, the fields and subfields historically may
contain and be separated by terminal periods and various punctuation
marks
[https://www.loc.gov/aba/pcc/documents/isbdmarc2016.pdf]. However, in
BibTeX entries we do not need it. To clean up such punctuation we
partially follow rules described in the link above (Appendix C). The
initials, ordinal numbers and some common abbreviations from AACR2R
[https://www.worldcat.org/title/847471922] (Appendix B) are kept.

Testing
=======

For testing the package we use `pytest
<http://pytest.org/latest/>`_. In order to run tests, check out
the repository and type:

.. code::

	$ pytest

By default, it runs all tests excluding validation test to do quick
testing. The validation test was added for testing the removal of ISBD
punctuation on two NLM's test record sets, with some punctuation
removed and not removed, from
[https://www.loc.gov/aba/pcc/documents/test-records-punctuation.html]. For
all tests, do:

.. code::

	$ pytest --runall

Cookbook
========

Applying hooks not for all tags
-------------------------------

Sometimes you will need to apply a hook not for all tags. With
``apply_not_for()`` it is possible to make an existing hook
tag-conditional. Taking the conditional statement out of a hook could
be useful, for example, to (temporarily) exclude it from the
post-processing of certain record(s).

Let us illustrate it with the following example. Suppose a title of a
bibliographic work ends with a dot and you need to keep it. To do it,
we can turn off the default hook (``remove_isbd_punctuation_hook``)
and instead make it applying later for all tags except *title* tag:

.. code:: python

        from marc2bib.hooks import apply_not_for

	def hook(tag: str, value: str) -> str:
	    ...

	convert(record, post_hooks=[apply_not_for(hook, ["tag"])])

Passing arguments to hooks
--------------------------

It is possible to customize hooks by adding keywords arguments to a
hook's function and passing them later with
``functools.partial()``. Suppose a title of a bibliographic work ends
with an abbreviation and you need to keep a period. Here is an example
of customizing ``remove_isbd_punctuation_hook(tag, value, *,
abbreviations)`` hook by providing an extended list of abbreviations:

.. code:: python

        from functools import partial

	from marc2bib.core import COMMON_ABBREVIATIONS
        from marc2bib.hooks import remove_isbd_punctuation_hook

	abbreviations = COMMON_ABBREVIATIONS + ("abbrev.",)
	remove_punctuation_call = partial(
	    remove_isbd_punctuation_hook, abbreviations=abbreviations
	)
	
        convert(record, remove_punctuation=False, post_hooks=[remove_punctuation_call])

As an alternative, especially when working interactively, you can just modify the translated value of *title* tag:

.. code:: python
	  
        from marc2bib import map_tags, tags_to_bibtex

	tags = map_tags(record)
	tags["title"] = tags["title"] + "."
	
        tags_to_bibtex(tags)
	
Acknowledgments
===============

Thanks go to all the authors and contributors of `pymarc
<https://gitlab.com/pymarc/pymarc>`_ package.
