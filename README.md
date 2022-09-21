# SQLAlchemy Hero

SQLAlchemy Hero is a package to generate table YAMLs for
[SchemaHero](https://schemahero.io/) from a
[SQLAlchemy](https://www.sqlalchemy.org/) Base.

Let's look at an example how to use it.
There is a `Parent` and a `Child` model both
inheriting from a abstract base model with some common fields.
The goal is to generate the table YAML files for `SchemaHero`.

The `HeroGenerator` class implements the methods to extract the model.
It is initialized with your declarative base from `SQLAlchemy`,
the database type you're using (currently `postgres` and `mysql`),
the namespace where the tables should be deployed and the database name.

The `to_yaml_files` method allowes to specify the output path for the
generated YAMLs (defaults to `Path("./out")`).

```python
from pathlib import Path

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ArrowType

from sqlalchemy_hero.hero_database import HeroDatabase
from sqlalchemy_hero.hero_generator import HeroGenerator

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(ArrowType, default=func.now())
    updated_on = Column(ArrowType, default=func.now(), onupdate=func.now())


class Parent(Base):
    __tablename__ = "parent"

    name = Column(Text)
    ss_number = Column(Integer, autoincrement=True)
    children = relationship("Child")


class Child(Base):
    __tablename__ = "child"

    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))


hero_generator = HeroGenerator(
    base=Base,
    db_type=HeroDatabase.postgres,
    namespace="hero-ns",
    database="hero-db",
)
hero_generator.to_yaml_files(out_path=Path("./out"))
```

### Type Overrides

The library tries to implement the most common types but it's hard to
keep up with all the possiblities for the different databases.
If you find a not yet mapped type (commonly used with `SQLAlchemy`) please
open a pull request to add it.

For custom types or quick fixes you can override the types
(the dict entries override/add to the current types).

```python
CUSTOM_TYPE_MAPPINGS = {
    MyCustomType: "text",  # add new type mappings
    Integer: "serial",  # override existing mappings
}

hero_generator = HeroGenerator(
    base=Base,
    db_type=HeroDatabase.postgres,
    namespace="hero-ns",
    database="hero-db",
    db_type_override=CUSTOM_TYPE_MAPPINGS,  # add the mappings on init
)
hero_generator.to_yaml_files()
```

### API Version

We try to update the default API version for `SchemaHero` to the latest.
If you wish to use another version or if we haven't updated yet it can be
specified on initializing the `HeroGenerator`.

```python
hero_generator = HeroGenerator(
    base=Base,
    db_type=HeroDatabase.postgres,
    namespace="hero-ns",
    database="hero-db",
    api_version="schemas.schemahero.io/custom-version",
)
hero_generator.to_yaml_files()
```

## QA Commands

The below commands are run in the pipeline and the according checks
are expected to pass.

```bash
poetry run pytest
poetry run black .
poetry run isort .
poetry run pylint tests sqlalchemy_hero
poetry run -r sqlalchemy_hero
```
