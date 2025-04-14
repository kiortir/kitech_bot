from httpx import Auth, Request, AsyncClient
from schema import TheCatApiResponseListDto, TheCatApiResponseDto


class TheCatApiKeyAuth(Auth):
    def __init__(self, api_key):
        self.api_key = api_key

    def auth_flow(self, request: Request):
        request.headers["x-api-key"] = self.api_key
        yield request


class CatApiClient(AsyncClient):
    def __init__(self, *args, auth: TheCatApiKeyAuth, **kwargs):
        super().__init__(
            *args, auth=auth, base_url="https://api.thecatapi.com", **kwargs
        )

    async def get_images(self) -> list[TheCatApiResponseDto]:
        url = "/v1/images/search"
        response = await self.get(url, params={"limit": 5, "order": "RAND"})
        response.raise_for_status()
        cats = TheCatApiResponseListDto.validate_json(response.content)
        return cats
