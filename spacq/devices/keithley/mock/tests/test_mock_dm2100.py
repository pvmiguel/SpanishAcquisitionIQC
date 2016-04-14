from unittest import main

from ... import dm2100
from .. import mock_dm2100

from ...tests.server.test_dm2100 import DM2100Test


# Don't lose the real device.
real_DM2100 = dm2100.DM2100
is_mock = DM2100Test.mock


def setup():
	# Run the tests with a fake device.
	dm2100.DM2100 = mock_dm2100.MockDM2100
	DM2100Test.mock = True

def teardown():
	# Restore the real device for any remaining tests.
	dm2100.DM2100 = real_DM2100
	DM2100Test.mock = is_mock


if __name__ == '__main__':
	main()
