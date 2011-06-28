from nose.plugins.skip import SkipTest
from nose.tools import eq_
import unittest

from testconfig import config as tc
from ..mock.mock_abstract_device import MockAbstractDevice

from .. import config


class DeviceTreeTest(unittest.TestCase):
	def testTree(self):
		"""
		Ensure the tree looks correct.
		"""

		tree = config.device_tree()

		assert 'Agilent' in tree
		assert 'Tektronix' in tree

		agi = tree['Agilent']
		tek = tree['Tektronix']

		assert '34410A' in agi
		assert 'AWG5014B' in tek

		dm = agi['34410A']
		awg = tek['AWG5014B']

		from ..agilent.dm34410a import DM34410A
		from ..agilent.mock.mock_dm34410a import MockDM34410A
		from ..tektronix.awg5014b import AWG5014B
		from ..tektronix.mock.mock_awg5014b import MockAWG5014B

		eq_(dm['real'], DM34410A)
		eq_(dm['mock'], MockDM34410A)
		eq_(awg['real'], AWG5014B)
		eq_(awg['mock'], MockAWG5014B)


class DeviceConfigTest(unittest.TestCase):
	def __obtain_device(self):
		"""
		Get a mock device with which to test.
		"""

		for name, device in tc['devices'].items():
			if 'has_mock' in device and device['has_mock']:
				return device

		raise SkipTest('No suitable device found.')

	def testMockConnect(self):
		"""
		Connect to a mock device.
		"""

		dev = self.__obtain_device()

		cfg = config.DeviceConfig()

		# These values don't matter.
		cfg.address_mode = cfg.address_modes.ethernet
		cfg.ip_address = '127.0.0.1'

		cfg.manufacturer = dev['manufacturer']
		cfg.model = dev['model']
		cfg.mock = True

		cfg.connect()

		assert isinstance(cfg.device, MockAbstractDevice)

	def testDiffResources(self):
		"""
		Try changing up some resources.
		"""

		cfg1 = config.DeviceConfig()
		cfg2 = config.DeviceConfig()
		eq_(cfg1.diff_resources(cfg2), (set(), set(), set()))

		cfg2.resources['something'] = 'new'
		eq_(cfg1.diff_resources(cfg2), (set(['something']), set(), set()))

		cfg1.resources['for'] = 'now'
		eq_(cfg1.diff_resources(cfg2), (set(['something']), set(), set(['for'])))

		cfg1.resources['something'] = 'now'
		eq_(cfg1.diff_resources(cfg2), (set(), set(['something']), set(['for'])))


if __name__ == '__main__':
	unittest.main()
