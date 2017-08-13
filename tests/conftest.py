import pytest
from pymarc import MARCReader


@pytest.fixture(scope='function')
def rec_hargittai(request):
    # This MARC file has been downloaded from
    # http://pi.lib.uchicago.edu/1001/cat/bib/8888814
    reader = MARCReader(open('tests/hargittai2009.mrc', 'rb'))
    request.addfinalizer(reader.close)
    return next(reader)

@pytest.fixture(scope='function')
def rec_tsing(request):
    # This MARC file has been downloaded from
    # https://lccn.loc.gov/2014037624
    reader = MARCReader(open('tests/tsing2015.mrc', 'rb'))
    request.addfinalizer(reader.close)
    return next(reader)

@pytest.fixture(scope='function')
def rec_sholokhov(request):
    # This MARC file has been downloaded from
    # https://lccn.loc.gov/60035484
    reader = MARCReader(open('tests/sholokhov.mrc', 'rb'))
    request.addfinalizer(reader.close)
    return next(reader)
