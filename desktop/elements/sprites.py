from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import flip

from desktop.config import STATICS_DIR


class Sign(Sprite):
    def __init__(self, index: int, center: tuple[int, int]) -> None:
        super().__init__()
        self.image_index = index
        self.images = [
            load(f"{STATICS_DIR}/graphics/x.png").convert_alpha(),
            load(f"{STATICS_DIR}/graphics/o.png").convert_alpha(),
        ]
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=center)
        self.rotate_angle = 0
        self.cooldown = 0

    def update(
        self, who_won: int = 0, win_state: bool = False, *args, **kwargs
    ) -> None:
        if win_state:
            if self.image_index == who_won and not self.cooldown:
                self.flip()
        self.update_cooldown()

    def flip(self) -> None:
        self.image = flip(self.image, True, False)
        self.cooldown = 30

    def update_cooldown(self) -> None:
        if self.cooldown > 0:
            self.cooldown -= 1
