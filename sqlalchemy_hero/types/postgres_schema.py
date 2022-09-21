from dataclasses import dataclass

from sqlalchemy_hero.types.table import HeroTable


@dataclass
class HeroPostgresSchema:
    postgres: HeroTable
