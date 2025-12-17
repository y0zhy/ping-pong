from pygame import *
import os

class Animation:
    def __init__(self, frame_paths, x, y, frame_duration=100, loop=True, scale=None):
        """
        frame_paths - список шляхів до кадрів
        x, y - позиція для малювання (ліворуч-верхній кут)
        frame_duration - тривалість одного кадру в ms
        loop - чи зациклювати анімацію
        scale - кортеж (width, height) для масштабування кадрів, 'half' для зменшення в 2 рази або None
        """
        self.frames = []
        for path in frame_paths:
            try:
                img = image.load(path).convert_alpha()
                self.frames.append(img)
            except Exception as e:
                print(f"Warning: failed to load animation frame '{path}': {e}")

        if not self.frames:
            # запасний кадр щоб уникнути помилок при малюванні
            self.frames = [Surface((1, 1), SRCALPHA)]

        # Визначаємо реальний кортеж для масштабування лише якщо кадри завантажені
        scale_tuple = None
        if scale == 'half' and self.frames:
            w = max(1, self.frames[0].get_width() // 2)
            h = max(1, self.frames[0].get_height() // 2)
            scale_tuple = (w, h)
        elif isinstance(scale, tuple):
            scale_tuple = scale

        if scale_tuple:
            try:
                self.frames = [transform.scale(img, scale_tuple) for img in self.frames]
            except Exception as e:
                print(f"Warning: failed to scale frames: {e}")

        self.current_frame = 0
        self.frame_duration = frame_duration
        self.elapsed_time = 0
        self.x = x
        self.y = y
        self.loop = loop
        self.finished = False

    def update(self, dt):
        """Оновлення анімації (dt в мс)."""
        if self.finished or not self.frames:
            return

        self.elapsed_time += dt
        # підтримуємо ситуацію, коли dt > frame_duration
        while self.elapsed_time >= self.frame_duration:
            self.elapsed_time -= self.frame_duration
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    break

    def draw(self, screen):
        """Малює поточний кадр на екран."""
        if not self.frames:
            return
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def is_finished(self):
        return self.finished

    def reset(self):
        """Почати анімацію спочатку."""
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False


def create_info_book(WIDTH, HEIGHT=None, loop=True, frame_duration=100, scale=None, x=None, y=180):
    """
    Створює та повертає Animation для магічної книжки.
    Якщо scale='half' — кадри зменшаться в 2 рази.
    Передайте x,y щоб задати позицію; якщо x=None — центрує по WIDTH.
    """
    base = os.path.join("assets", "animations", "magic_book")
    frame_paths = [os.path.join(base, f"{i}.png") for i in range(0, 11)]

    # Передаємо тимчасове x (0) щоб Animation міг завантажити кадри і ми могли скоригувати позицію
    anim = Animation(frame_paths, x if x is not None else 0, y, frame_duration=frame_duration, loop=loop, scale=scale)

    # Якщо x не задано — центруємо анімацію по WIDTH з урахуванням реальної ширини кадру
    if x is None and anim.frames:
        anim.x = WIDTH // 2 - (anim.frames[0].get_width() // 2)

    return anim