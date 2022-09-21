from dataclasses import asdict
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Union

import yaml
from sqlalchemy.orm.decl_api import DeclarativeMeta

from sqlalchemy_hero.hero_database import HeroDatabase
from sqlalchemy_hero.hero_type_mapper import HeroTypeMapper
from sqlalchemy_hero.types.column import HeroColumn
from sqlalchemy_hero.types.file import HeroFile
from sqlalchemy_hero.types.index import HeroIndex
from sqlalchemy_hero.types.metadata import HeroMetadata
from sqlalchemy_hero.types.mysql_schema import HeroMysqlSchema
from sqlalchemy_hero.types.postgres_schema import HeroPostgresSchema
from sqlalchemy_hero.types.spec import HeroSpec
from sqlalchemy_hero.types.table import HeroTable


class HeroGenerator:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        base: DeclarativeMeta,
        db_type: HeroDatabase,
        namespace: str,
        database: str,
        api_version: str = "schemas.schemahero.io/v1alpha4",
        db_type_override: Union[Dict[Any, str], None] = None,
    ):
        self.base = base
        self.database = database
        self.namespace = namespace
        self.db_type = db_type
        self.api_version = api_version
        self.mapper = HeroTypeMapper(db_type, db_type_override)

    def to_dict(self):
        hero_tables = self.extract_tables()
        hero_files = self.extract_files(hero_tables)
        return [asdict(x) for x in hero_files]

    def extract_files(self, hero_tables):
        hero_files = []
        for hero_table_name, hero_table in hero_tables:
            if self.db_type == HeroDatabase.postgres:
                schema = HeroPostgresSchema(
                    postgres=hero_table,
                )
            elif self.db_type == HeroDatabase.mysql:
                schema = HeroMysqlSchema(
                    mysql=hero_table,
                )
            else:
                raise Exception("DB not supported.")

            metadata = self.build_metadata(hero_table_name)
            spec = self.build_spec(hero_table_name, schema)
            hero_files.append(self.build_file(metadata, spec))
        return hero_files

    def build_file(self, metadata, spec):
        return HeroFile(
            apiVersion=self.api_version,
            kind="Table",
            metadata=metadata,
            spec=spec,
        )

    def build_spec(self, hero_table_name, schema):
        return HeroSpec(
            database=self.database,
            name=hero_table_name,
            schema=schema,
        )

    def build_metadata(self, hero_table_name):
        return HeroMetadata(
            name=f"{self.database}-{hero_table_name}",
            namespace=self.namespace,
        )

    def extract_tables(self):
        hero_tables = []
        for table_value in self.base.metadata.tables.values():
            hero_columns, hero_primary_keys = self.extract_columns_and_pks(table_value)
            indexes = self.extract_indexes(table_value)
            hero_tables.append(
                (
                    str(table_value.name),
                    HeroTable(
                        primaryKey=hero_primary_keys,
                        indexes=indexes,
                        columns=hero_columns,
                    ),
                )
            )
        return hero_tables

    @staticmethod
    def extract_indexes(table_value):
        indexes = []
        for index in table_value.indexes:
            indexes.append(
                HeroIndex(
                    name=str(index.name),
                    columns=[str(col.name) for col in index.columns],
                    isUnique=index.unique,
                )
            )
        return indexes

    def extract_columns_and_pks(self, table_value):
        hero_primary_keys = []
        hero_columns = []
        for column in table_value.columns:
            if not self.mapper.get_for(column.type):
                raise Exception(f"Type {column.type} not implemented.")
            if column.primary_key:
                hero_primary_keys.append(column.name)
            hero_columns.append(
                HeroColumn(
                    name=column.name,
                    type=self.mapper.get_for(column.type),
                    constraints={} if column.nullable else {"notNull": True},
                    attributes={"autoIncrement": True} if column.autoincrement is True else {},
                )
            )
        return hero_columns, hero_primary_keys

    def to_yamls(self):
        return [yaml.dump(t, sort_keys=False) for t in self.to_dict()]

    def to_yaml_files(self, out_path: Path = Path("./out")):
        dict_tables = self.to_dict()
        for dict_table in dict_tables:
            path = out_path.joinpath(f"{dict_table['metadata']['name']}.yaml")
            with path.open("w+", encoding="utf-8") as f_:
                yaml.dump(dict_table, f_, sort_keys=False)
