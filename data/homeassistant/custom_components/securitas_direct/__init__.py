"""Support for Securitas Direct alarms."""
import logging
import threading
from datetime import timedelta

import voluptuous as vol

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
    CONF_CODE,
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.helpers import discovery
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv


from . import securitas

_LOGGER = logging.getLogger(__name__)

CONF_ALARM = "alarm"
CONF_CODE_DIGITS = "code_digits"
CONF_COUNTRY = "country"

DOMAIN = "securitas_direct"

MIN_SCAN_INTERVAL = timedelta(minutes=1)
DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

HUB = None

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Optional(CONF_COUNTRY, default="ES"): cv.string,
                vol.Optional(CONF_ALARM, default=True): cv.boolean,
                vol.Optional(CONF_CODE_DIGITS, default=4): cv.positive_int,
                vol.Optional(CONF_CODE, default=""): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): (
                    vol.All(cv.time_period, vol.Clamp(min=MIN_SCAN_INTERVAL))
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Set up the Securitas component."""
    global HUB
    HUB = SecuritasHub(config[DOMAIN])
    HUB.update_overview = Throttle(config[DOMAIN][CONF_SCAN_INTERVAL])(
        HUB.update_overview
    )
    if not HUB.login():
        return False
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, lambda event: HUB.logout())
    HUB.update_overview()
    for component in ("alarm_control_panel",):
        discovery.load_platform(hass, component, DOMAIN, {}, config)
    return True


class SecuritasHub:
    """A Securitas hub wrapper class."""

    def __init__(self, domain_config):
        """Initialize the Securitas hub."""
        self.overview = {}
        self.config = domain_config
        self._lock = threading.Lock()
        country = domain_config[CONF_COUNTRY].upper()
        lang = country.lower() if country != "UK" else "en"
        self.session = securitas.SecuritasAPIClient(
            domain_config[CONF_USERNAME],
            domain_config[CONF_PASSWORD],
            country=country,
            lang=lang,
        )

    def login(self):
        """Login to Securitas."""
        ret = self.session.login()
        _LOGGER.debug("Log in Securitas: %s", ret)
        if not ret:
            _LOGGER.error("Could not log in to Securitas: %s", ret)
            return False
        return True

    def logout(self):
        """Logout from Securitas."""
        ret = self.session.logout()
        if not ret:
            _LOGGER.error("Could not log out from Securitas: %s", ret)
            return False
        return True

    def update_overview(self):
        """Update the overview."""
        _LOGGER.debug("update")
        self.overview = self.session.last_state()
        _LOGGER.debug(self.overview)
