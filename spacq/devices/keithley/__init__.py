import logging
log = logging.getLogger(__name__)


name = 'Keithley'

from . import voltagesource230, dm2100
models = [voltagesource230, dm2100]
log.debug('Found models for "{0}": {1}'.format(name, ''.join(str(x) for x in models)))

from .mock import mock_voltagesource230
mock_models = [mock_voltagesource230]
log.debug('Found mock models for "{0}": {1}'.format(name, ''.join(str(x) for x in mock_models)))