import abc
import typing

from utils import config

ModelType = typing.TypeVar("ModelType")
GetModelType = typing.TypeVar("GetModelType")


class BaseRepository(abc.ABC, typing.Generic[ModelType, GetModelType]):
    def __init__(self, db):
        self._db = db

    @property
    @abc.abstractmethod
    def __collection_name__(self):
        raise NotImplementedError

    @property
    def __model__(self):
        return typing.get_args(self.__class__.__orig_bases__[0])[0]  # type: ignore

    def get_collection(self):
        return self._db[self.__collection_name__]

    # TODO:
    #  1. add get, get_or_create, update, delete_by_id, delete, create

    async def get_many(
            self,
            get_model: GetModelType,  # type: ignore
            offset: int = 0,
            limit: int = config.GET_ENTITIES_DEFAULT_LIMIT,
    ) -> list[ModelType]:
        kwargs = get_model.dict(exclude_none=True)
        c = self.get_collection().find(kwargs, skip=offset, limit=limit)
        return [self.__model__(**raw_result) async for raw_result in c]
