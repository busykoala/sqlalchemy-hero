from dataclasses import dataclass
from typing import Union

from sqlalchemy_hero.types.mysql_schema import HeroMysqlSchema
from sqlalchemy_hero.types.postgres_schema import HeroPostgresSchema


@dataclass
class HeroSpec:
    database: str
    name: str
    schema: Union[HeroPostgresSchema, HeroMysqlSchema]
