"""
The "hello world" custom component.

This component implements the bare minimum that a component should implement.

Configuration:

To use the hello_world component you will need to add the following to your
configuration.yaml file.

hass_chroma_integration:
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import *
import logging

_LOGGER = logging.getLogger(__name__)

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "hass_chroma_integration"

def a(event: Event) -> Coroutine[Any, Any, None] | None:
    _LOGGER.debug(event)
    return None


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""

    _LOGGER.info("This hopefully works!")

    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.set(f'{DOMAIN}.Hello_World', 'Works!')

    # hass.bus.async_listen(EVENT_ENTITY_REGISTRY_UPDATED, a, run_immediately=True)

    # Return boolean to indicate that initialization was successfully.
    return True


