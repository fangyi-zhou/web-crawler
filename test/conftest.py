import pytest

RUN_INTEG = "integ"


def pytest_addoption(parser):
    parser.addoption(
        "--{}".format(RUN_INTEG),
        action="store_true",
        default=False,
        help="run {} tests".format(RUN_INTEG),
    )


def pytest_configure(config):
    config.addinivalue_line("markers", RUN_INTEG)


def pytest_collection_modifyitems(config, items):
    if config.getoption("--{}".format(RUN_INTEG)):
        return

    skip_mark = pytest.mark.skip(reason="need --{} option to run".format(RUN_INTEG))
    for item in items:
        if RUN_INTEG in item.keywords:
            item.add_marker(skip_mark)
