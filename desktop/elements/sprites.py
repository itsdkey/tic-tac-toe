from pygame.image import load
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.transform import flip

from desktop.config import STATICS_DIR
from desktop.elements.enums import Symbol


class ImageFactory:
    """A class that allows us to load images once and use them multiple times.

    This follows the Flyweight Design Pattern.
    """

    def __init__(self) -> None:
        self.images: dict[Symbol, Surface] = {}

    def get_image(self, symbol: Symbol) -> Surface:
        if symbol not in self.images:
            file_name = str(symbol).lower()
            surface = load(f"{STATICS_DIR}/graphics/{file_name}.png").convert_alpha()
            self.images[symbol] = surface
        return self.images[symbol]


class Marker(Sprite):
    image_factory = ImageFactory()

    def __init__(self, symbol: Symbol, center: tuple[int, int], *groups) -> None:
        super().__init__(*groups)
        self.symbol = symbol
        self.image = self.image_factory.get_image(symbol=self.symbol)
        self.rect = self.image.get_rect(center=center)
        self.rotate_angle = 0
        self.cooldown = 0

    def update(self, who_won: Symbol, win_state: bool = False, *args, **kwargs) -> None:
        if win_state:
            if self.symbol == who_won and not self.cooldown:
                self.flip()
            self.update_cooldown()

    def flip(self) -> None:
        self.image = flip(self.image, True, False)
        self.cooldown = 30

    def update_cooldown(self) -> None:
        if self.cooldown > 0:
            self.cooldown -= 1
