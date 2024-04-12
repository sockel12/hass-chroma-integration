"""
The "hello world" custom component.

This component implements the bare minimum that a component should implement.

Configuration:

To use the hello_world component you will need to add the following to your
configuration.yaml file.

hass_chroma_integration:
"""
from __future__ import annotations
from typing import Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import *
import homeassistant.helpers.entity_registry as er
from homeassistant.helpers.entity import Entity
from .chroma_client import Client
from .entities import *
import os
import logging


_LOGGER = logging.getLogger(__name__)

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "hass_chroma_integration"
CHROMA_HOSTNAME="chromadb"
CHROMA_PORT=8000
CHROMA_COLLECTION_NAME = "hass_entity_action"
CHROMA_DEFAULT_TENANT = "default_tenant"
CHROMA_DEFAULT_DATABASE = "default_database"

# class EntityType:
#     def __init__(self, entity_type: str, actions: List[str], location: str = "None"):
#         self.entity_type = entity_type
#         self.actions = actions
#         self.location = location

#     def get_embedding(self, entity_id: str, action: str) -> str:
#         if action not in self.actions:
#             return ""
        
#         return [f"Entity: {entity_id}; Location: {self.location}; Action: {action}"]
    
#     def is_entity_type_of(self, entity_type: str) -> bool:
#         return entity_type == self.entity_type


        
entities: Dict[str, object] = {}
hass_obj = None

async def a(event: Event) -> Coroutine[Any, Any, None] | None:
    global entities
    global hass_obj


    _LOGGER.info(event)
    # return None


    entity_id = event.data["entity_id"]

    _LOGGER.info(entity_id)
    
    if not entity_id:
        return None 
    
    registry = er.async_get(hass_obj)
    e = registry.async_get(entity_id)

    entities[entity_id] = e


    _LOGGER.info(entities)

    # collection.add(
    #     ids=[entity_id],
    #     metadatas=[],
    #     documents=[f"Entity: {entity_id}; Location: {}; Action: {};"]
    # )

    return None


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    global entities
    global hass_obj

    hass_obj = hass

    _LOGGER.info("HASS Chroma Integration started!")

    # States are in the format DOMAIN.OBJECT_ID.
    # hass.states.set(f'{DOMAIN}.Hello_World', 'Works!')

    hass.bus.async_listen(EVENT_ENTITY_REGISTRY_UPDATED, a)

    cc = chroma_client.Client(CHROMA_HOSTNAME, CHROMA_PORT, CHROMA_DEFAULT_TENANT, CHROMA_DEFAULT_DATABASE)

    collection = cc.create_or_get_collection(CHROMA_COLLECTION_NAME)


    registry = er.async_get(hass)

    for entity in registry.entities:
        e = registry.async_get(entity)
        entities[e.entity_id] = e

        entity_id = e.entity_id
        type = entity_id.split(".")[0]

        entity = get_entity(type, entity_id)

        collection.add(entity_id)

        # collection.add(e)

        
    

    # Return boolean to indicate that initialization was successfully.
    return True


