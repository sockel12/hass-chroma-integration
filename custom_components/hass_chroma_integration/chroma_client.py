import logging, requests
from typing import List
import json

_LOGGER = logging.getLogger(__name__)

class HttpClient:

    @staticmethod
    def get(url: str) -> dict:
        url = "http://" + url
        res = requests.get(url)
        if 200 <= res.status_code < 300:
            try:
                _LOGGER.info(f"Response: {res.json()}")
                return res.json()
            except Exception as e:
                _LOGGER.error(f"HASS-Chroma-Integration GET error: {e} from URL: {url}")
                pass
        else:
            _LOGGER.error(f"HASS-Chroma-Integration GET error: {res.status_code} from URL: {url} with response: {res.text}")
        return {}
    
    @staticmethod
    def post(url, body: dict) -> dict:
        url = "http://" + url
        res = requests.post(url, json.dumps(body))
        if 200 <= res.status_code < 300:
            try:
                _LOGGER.info(f"Response: {res.json()}")
                return res.json()
            except Exception as e:
                _LOGGER.error(f"HASS-Chroma-Integration POST error: {e} from URL: {url}")
                pass
        else:
            _LOGGER.error(f"HASS-Chroma-Integration POST error: {res.status_code} from URL: {url} with response: {res.text}")

        return {}


class Collection:
    # Connection members
    hostname: str
    port: int
    baseurl: str
    # Collection members
    name: str
    id: str
    metadata: dict
    tenant: str
    database: str

    def __init__(self, name: str, id: str, metadata: dict, tenant: str, database: str, hostname: str, port: int) -> None:
        self.name = name
        self.id = id
        self.metadata = metadata
        self.tenant = tenant
        self.database = database
    
        self.hostname = hostname
        self.port = port
        self.baseurl = f"{hostname}:{port}"



    # Entity is a RegistryEntry but could not find the type
    def add(self, entity_id):
        body = {
            "documents": ["Empty Document"],
            "ids": [entity_id],
            "embeddings": ["Test Embedding"],
            "uris": [entity_id],
            "metadatas": [{"description": "HASS Chroma Integration Entity", "type": "HASS Chroma Integration Entity"}]
        }
        data = HttpClient.post(f"{self.baseurl}/api/v1/collections/{self.id}/add?tenant={self.tenant}&database={self.database}", body)

        if(len(data)):
            return data

    def query(self, query: str) -> List:
        pass


class Client:
    hostname: str
    port: int
    baseurl: str

    tenant: str
    database: str

    def __init__(self, hostname: str, port: int, tenant: str, database: str) -> None:
        self.hostname = hostname
        self.port = port
        self.baseurl = f"{hostname}:{port}"

        self.tenant = tenant
        self.database = database

    
    def create_or_get_collection(self, collection_name: str) -> Collection:
        body = {
            "name": collection_name,
            "metadata": {"description": "HASS Chroma Integration Collection", "type": "HASS Chroma Integration Collection"},
            "get_or_create": True
        }

        data = HttpClient.post(f"{self.baseurl}/api/v1/collections?tenant={self.tenant}&database={self.database}", body)

        _LOGGER.info(f"Data: {data}")

        if len(data):
            return Collection(data["name"], data["id"], data["metadata"], data["tenant"], data["database"], self.hostname, self.port)

        return None
    