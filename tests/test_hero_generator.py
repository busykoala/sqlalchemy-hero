from pathlib import Path

from sqlalchemy_hero.hero_database import HeroDatabase
from sqlalchemy_hero.hero_generator import HeroGenerator
from tests.models import Base


def test_hero_generator_to_dict():
    hero_generator = HeroGenerator(
        base=Base,
        db_type=HeroDatabase.postgres,
        namespace="hero-ns",
        database="hierarchy-db",
    )
    dict_ = hero_generator.to_dict()
    expected_first = {
        "apiVersion": "schemas.schemahero.io/v1alpha4",
        "kind": "Table",
        "metadata": {
            "name": "hierarchy-db-parent",
            "namespace": "hero-ns",
        },
        "spec": {
            "database": "hierarchy-db",
            "name": "parent",
            "schema": {
                "postgres": {
                    "primaryKey": ["id"],
                    "indexes": [],
                    "columns": [
                        {
                            "attributes": {},
                            "constraints": {"notNull": True},
                            "name": "id",
                            "type": "int",
                        },
                        {
                            "attributes": {},
                            "constraints": {},
                            "name": "created_on",
                            "type": "date",
                        },
                        {
                            "attributes": {},
                            "constraints": {},
                            "name": "updated_on",
                            "type": "date",
                        },
                        {
                            "attributes": {},
                            "constraints": {},
                            "name": "name",
                            "type": "text",
                        },
                        {
                            "attributes": {"autoIncrement": True},
                            "constraints": {},
                            "name": "ss_number",
                            "type": "int",
                        },
                    ],
                },
            },
        },
    }
    expected_second_indexes = [
        {"columns": ["description"], "isUnique": False, "name": "ix_child_description"},
    ]

    parent = [x for x in dict_ if "parent" in x["metadata"]["name"]][0]
    child = [x for x in dict_ if "child" in x["metadata"]["name"]][0]

    assert len(dict_) == 2
    assert parent == expected_first
    assert child["spec"]["schema"]["postgres"]["indexes"] == expected_second_indexes


def test_hero_generator_to_yamls():
    hero_generator = HeroGenerator(
        base=Base,
        db_type=HeroDatabase.postgres,
        namespace="hero-ns",
        database="hierarchy-db",
    )
    yaml_ = hero_generator.to_yamls()

    parent_path = Path("./tests/assets/parent.yaml")
    child_path = Path("./tests/assets/child.yaml")
    with parent_path.open("rb") as f_:
        expected_parent = f_.read().decode("utf-8")
    with child_path.open("rb") as f_:
        expected_child = f_.read().decode("utf-8")

    parent = [x for x in yaml_ if "hierarchy-db-parent" in x][0]
    child = [x for x in yaml_ if "hierarchy-db-child" in x][0]
    assert len(yaml_) == 2
    assert parent == expected_parent
    assert child == expected_child
