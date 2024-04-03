from abc import ABC


class BaseAnimal(ABC):

    def __init__(self,
                 name: str,
                 age: float,
                 species: str,
                 subspecies: str,
                 sex: str = None,
                 genus: str = None,
                 family: str = None,
                 order: str = None,
                 class_: str = None,
                 phylum: str = None,
                 kingdom: str = None,
                 domain: str = None) -> None:
        self._name = name
        self._age = age
        self._sex = sex
        self._domain = domain
        self._kingdom = kingdom
        self._phylum = phylum
        self._class = class_
        self._order = order
        self._family = family
        self._genus = genus
        self._subspecies = subspecies
        self._species = species

    def __str__(self) -> str:
        return f"{self._name.capitalize()} ({self._age}) - {self._sex} {self.species} ({self.subspecies})"

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> float:
        return self._age

    @property
    def sex(self) -> str:
        return self._sex

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def kingdom(self) -> str:
        return self._kingdom

    @property
    def phylum(self) -> str:
        return self._phylum

    @property
    def class_(self) -> str:
        return self._class

    @property
    def order(self) -> str:
        return self._order

    @property
    def family(self) -> str:
        return self._family

    @property
    def genus(self) -> str:
        return self._genus

    @property
    def subspecies(self) -> str:
        return self._subspecies

    @property
    def species(self) -> str:
        return self._species
