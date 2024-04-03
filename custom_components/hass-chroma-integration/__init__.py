"""
The "hello world" custom component.

This component implements the bare minimum that a component should implement.

Configuration:

To use the hello_world component you will need to add the following to your
configuration.yaml file.

hello_world:
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import *
from chromadb import HttpClient
import logging

_LOGGER = logging.getLogger(__name__)

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "hello_world"

def a(event: Event) -> Coroutine[Any, Any, None] | None:
    _LOGGER.debug(event)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""

    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.set('hello_world.Hello_World', 'Works!')

    hass.bus.async_listen(EVENT_ENTITY_REGISTRY_UPDATED, a)

    # Return boolean to indicate that initialization was successfully.
    return True
