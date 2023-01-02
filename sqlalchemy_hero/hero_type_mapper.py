from typing import Any
from typing import Dict
from typing import Union

from sqlalchemy import JSON
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import SmallInteger
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy_utils import ArrowType

from sqlalchemy_hero.hero_database import HeroDatabase

# https://schemahero.io/databases/postgresql/column-types/
POSTGRES_TYPE_MAP = {
    ArrowType: "date",
    BigInteger: "bigint",
    Boolean: "boolean",
    Date: "date",
    Integer: "int",
    JSON: "json",
    Numeric: "numeric",
    SmallInteger: "smallint",
    Text: "text",
    Time: "time",
}


# https://schemahero.io/databases/mysql/column-types/
MYSQL_TYPE_MAP = {
    ArrowType: "date",
    BigInteger: "bigint",
    Date: "date",
    Integer: "int",
    SmallInteger: "smallint",
    Text: "text",
}


class HeroTypeMapper:
    def __init__(
        self,
        db_type: HeroDatabase,
        db_type_override: Union[Dict[Any, str], None] = None,
    ):
        self.db_type = db_type

        if self.db_type == HeroDatabase.postgres:
            self.map = POSTGRES_TYPE_MAP
        elif self.db_type == HeroDatabase.mysql:
            self.map = MYSQL_TYPE_MAP
        else:
            raise Exception("Selected database type not supported.")

        if db_type_override:
            for k, v in db_type_override.items():
                self.map[k] = v

    def get_for(self, sqlalchemy_obj: Any) -> str:
        sqlalchemy_type = type(sqlalchemy_obj)
        hero_type = self.map.get(sqlalchemy_type)
        if not hero_type:
            raise Exception("Type {sqlalchemy_type} not found.")
        return hero_type
