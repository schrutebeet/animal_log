from animal_logger.src.animals.base_animal import BaseAnimal


class Mammal(BaseAnimal):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
