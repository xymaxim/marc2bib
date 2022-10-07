import pytest
from pymarc import MARCReader


def pytest_addoption(parser):
    parser.addoption(
        "--runall",
        action="store_true",
        default=False,
        help="enable all tests including validation",
    )


@pytest.fixture(scope="function")
def rec_hargittai(request):
    # This file has been downloaded from
    # https://lccn.loc.gov/2010920
    reader = MARCReader(open("tests/records/hargittai2009.mrc", "rb"))
    request.addfinalizer(reader.close)
    return next(reader)


@pytest.fixture(scope="function")
def rec_tsing(request):
    # This file has been downloaded from
    # https://lccn.loc.gov/2014037624
    reader = MARCReader(open("tests/records/tsing2015.mrc", "rb"))
    request.addfinalizer(reader.close)
    return next(reader)


@pytest.fixture(scope="function")
def rec_sholokhov(request):
    # This file has been downloaded from
    # https://lccn.loc.gov/60035484
    reader = MARCReader(open("tests/records/sholokhov.mrc", "rb"))
    request.addfinalizer(reader.close)
    return next(reader)


@pytest.fixture(scope="function")
def rec_clusters(request):
    # This file has been downloaded from
    # https://lccn.loc.gov/990155550
    reader = MARCReader(open("tests/records/clusters.mrc", "rb"))
    request.addfinalizer(reader.close)
    return next(reader)
