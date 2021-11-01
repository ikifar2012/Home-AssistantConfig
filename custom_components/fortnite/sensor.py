"""Fortnite Sensor integration
to use, add something like this to HA config:

sensor:
 - platform: fortnite
   name: myfortnite_integration
   api_key: <your_api_key>
   player_id: <player_name>
   game_platform: "GAMEPAD"
   game_mode: "SQUAD"
"""

import logging

# from .fortnite import FortniteData
## use below instead of above
from fortnite_python import Fortnite
from fortnite_python.domain import Mode, Platform
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required("player_id"): cv.string,
        vol.Required("game_platform"): cv.string,
        vol.Required("game_mode"): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the fortnite sensor."""

    _LOGGER.info("init sensor")
    name = config.get(CONF_NAME)
    api_key = config.get(CONF_API_KEY)
    player_id = config.get("player_id")
    game_platform = config.get("game_platform")
    game_mode = config.get("game_mode")

    fn = FortniteData(name, api_key, player_id, game_platform, game_mode)

    if not fn:
        _LOGGER.error("Unable to create the fortnite sensor")
        return

    add_entities([FortniteSensor(hass, fn)], True)


class FortniteSensor(Entity):
    def __init__(self, hass, fn):
        self._hass = hass
        self.data = fn

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{}".format(self.data.name)

    @property
    def state(self):
        """Return the state of the device."""
        return self.data.attr["kills"]

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.data.attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "eliminations"

    def update(self):
        self.data.update_stats()


class FortniteData:
    def __init__(self, name, api_key, player, platform, mode):
        self.name = name
        self.api_key = api_key
        self.player = player
        self.platform = Platform[platform]
        self.mode = Mode[mode]
        self.stats = None
        self.attr = {}

        try:
            # create the fortnite object
            self.game = Fortnite(self.api_key)
            self.fplayer = self.game.player(self.player, self.platform)
            self.update_stats()
        except:
            pass

    def update_stats(self):
        self.stats = self.fplayer.get_stats(self.mode)
        # transform stats into a dict
        self.attr["top1"] = self.stats.top1
        self.attr["top3"] = self.stats.top3
        self.attr["top5"] = self.stats.top5
        self.attr["top6"] = self.stats.top6
        self.attr["top10"] = self.stats.top10
        self.attr["top12"] = self.stats.top12
        self.attr["top25"] = self.stats.top25
        self.attr["kills"] = self.stats.kills
        self.attr["kd"] = self.stats.kd
        self.attr["kpg"] = self.stats.kpg
        self.attr["matches"] = self.stats.matches
        self.attr["score"] = self.stats.score
        self.attr["score_per_match"] = self.stats.score_per_match
        # self.attr["to_snake"] = self.stats.to_snake ### doesn't work!
        self.attr["id"] = self.stats.id
        self.attr["win_ratio"] = self.stats.win_ratio
        # self.attr["trn_rating"] = self.stats.trn_rating
        # self.attr["from_json"] = self.stats.from_json
        # self.attr["winratio"] = self.stats.winratio

    def print_stats(self):
        print(self.stats)
