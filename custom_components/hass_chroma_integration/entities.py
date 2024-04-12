from typing import List

class Entity:
    entity_id: str
    states: List[str]
    active_states: [str]
    passive_states: [str]

    def __init__(self, entity_id: str, active_states: List[str], passive_states: List[str]) -> None:
        self.entity_id = entity_id
        self.active_states = active_states
        self.passive_states = passive_states

    def get_states(self) -> List[str]:
        return self.states
    
    def get_active_state(self) -> str:
        return self.active_state
    
    def get_entity_id(self) -> str:
        return self.entity_id

class Light(Entity):
    def __init__(self, entity_id: str) -> None:
        super().__init__(entity_id, ["On", "Off"], None)

class Fan(Entity):
    def __init__(self, entity_id: str) -> None:
        super().__init__(entity_id, ["On", "Off"], None)
        
class Sensor(Entity):
    def __init__(self, entity_id: str) -> None:
        super().__init__(entity_id, None, ["Read"])

def get_entity(type_string: str, entity_id: str) -> Entity:
    if type_string == "Light":
        return Light(entity_id)
    elif type_string == "Fan":
        return Fan(entity_id)
    return None

