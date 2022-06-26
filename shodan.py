from datetime import datetime
from typing import Optional, Any, List

import httpx
from pydantic import BaseModel, Field


class ShodanIPResponse(BaseModel):
    hostnames: List[str]
    domains: List[str]
    country_code: str
    city: Optional[str]
    last_update: datetime = Field(default_factory=lambda x: datetime.fromisoformat(x))
    isp: Optional[str]
    ports: List[int]
    # data: Any


class Shodan:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.http = httpx.AsyncClient(base_url='https://api.shodan.io', params={'key': self.api_key})

    async def get_host(self, ip: str) -> ShodanIPResponse:
        response = await self.http.get(f'/shodan/host/{ip}')
        return ShodanIPResponse(**response.json())
