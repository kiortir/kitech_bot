from pydantic import BaseModel, TypeAdapter


class TheCatApiResponseDto(BaseModel):

    id: str
    url: str
    width: int
    height: int
    breeds: list


TheCatApiResponseListDto = TypeAdapter(list[TheCatApiResponseDto])
