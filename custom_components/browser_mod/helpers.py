import logging

from homeassistant.helpers.entity import Entity, async_generate_entity_id

from .const import DOMAIN, DATA_DEVICES, DATA_ALIASES, DATA_ADDERS, CONFIG_DEVICES, DATA_CONFIG

_LOGGER = logging.getLogger(__name__)

def get_devices(hass):
    return hass.data[DOMAIN][DATA_DEVICES]

def get_alias(hass, deviceID):
    for k,v in hass.data[DOMAIN][DATA_ALIASES].items():
        if v == deviceID:
            return k
    return None

def get_config(hass, deviceID):
    config = hass.data[DOMAIN][DATA_CONFIG]
    return config.get(deviceID, config.get(deviceID.replace('-','_'), {}))

def create_entity(hass, platform, deviceID, connection):
    adder = hass.data[DOMAIN][DATA_ADDERS][platform]
    entity = adder(hass, deviceID, connection, get_alias(hass, deviceID))
    return entity

def setup_platform(hass, config, async_add_devices, platform, cls):
    def adder(hass, deviceID, connection, alias=None):
        entity = cls(hass, connection, deviceID, alias)
        async_add_devices([entity])
        return entity
    hass.data[DOMAIN][DATA_ADDERS][platform] = adder
    return True

class BrowserModEntity(Entity):

    def __init__(self, hass, connection, deviceID, alias=None):
        self.hass = hass
        self.connection = connection
        self.deviceID = deviceID
        self._data = {}
        self.entity_id = async_generate_entity_id(self.domain+".{}", alias or deviceID, hass=hass)

    def updated(self):
        pass

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, data):
        self._data = data
        self.updated()

    @property
    def device_id(self):
        return self.deviceID

    def send(self, command, **kwargs):
        self.connection.send(command, **kwargs)
