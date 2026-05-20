"""
Класс Game — основной игровой цикл и состояния
Спринт 1: Главное меню + интро-катсцена

TODO для сложных анимаций (lamp flicker, hero silhouette walk, light shaders):
Генерировать промт для Gemini / Antigravity
"""

import pygame
import sys
from .constants import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # для звуков (TODO: загрузить ассеты)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU | CUTSCENE | ...

        # Фонты (TODO: заменить на кастомный из assets/fonts)
        self.title_font = pygame.font.SysFont("arial", TITLE_FONT_SIZE)
        self.button_font = pygame.font.SysFont("arial", BUTTON_FONT_SIZE)

        # Элементы меню
        self.title_alpha = 0
        self.title_fade_speed = 2
        self.door_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 100, 120, 200)  # дверь
        self.settings_buttons = [
            {"text": "Графика", "rect": pygame.Rect(50, 200, 150, 40), "action": "graphics"},
            {"text": "Аудио", "rect": pygame.Rect(50, 260, 150, 40), "action": "audio"},
            {"text": "Разрешение", "rect": pygame.Rect(50, 320, 150, 40), "action": "resolution"},
        ]
        # Лампочка (TODO: анимация мигания и свет)
        self.lamp_on = False
        self.lamp_timer = 0

        # Для катсцены
        self.cutscene_phase = 0  # 0: voices, 1: hero walk, 2: enter, 3: slam, 4: turn, 5: void
        self.cutscene_timer = 0
        self.cutscene_start_time = 0

        # TODO: звуки (assets/audio/)
        # self.sound_voices = pygame.mixer.Sound("assets/audio/voices.ogg")
        # self.sound_scream = ...
        # self.sound_wheeze = ...
        # self.sound_door_slam = ...

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == "MENU":
                    mouse_pos = pygame.mouse.get_pos()
                    # Клик на дверь = Старт
                    if self.door_rect.collidepoint(mouse_pos):
                        self.start_cutscene()
                    # Кнопки настроек (placeholder)
                    for btn in self.settings_buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            print(f"Настройка: {btn['action']} (TODO: открыть меню)")

    def start_cutscene(self):
        self.state = "CUTSCENE"
        self.cutscene_phase = 0
        self.cutscene_start_time = pygame.time.get_ticks()
        # TODO: проиграть звуки
        # self.sound_voices.play(-1)

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.state == "MENU":
            # Fade-in названия
            if self.title_alpha < 255:
                self.title_alpha += self.title_fade_speed
            # Мигание лампочки (TODO: улучшить в промте)
            self.lamp_timer += 1
            if self.lamp_timer > 30:
                self.lamp_on = not self.lamp_on
                self.lamp_timer = 0

        elif self.state == "CUTSCENE":
            elapsed = current_time - self.cutscene_start_time

            # Фазы катсцены (по сценарию)
            if self.cutscene_phase == 0 and elapsed > 1500:
                # Пугающие голоса, детский крик, хрип
                self.cutscene_phase = 1
                # TODO: звуки
            elif self.cutscene_phase == 1 and elapsed > 3500:
                # Силуэт героя подходит к двери (TODO: анимация хромы)
                self.cutscene_phase = 2
            elif self.cutscene_phase == 2 and elapsed > 5500:
                # Входит в дверь
                self.cutscene_phase = 3
            elif self.cutscene_phase == 3 and elapsed > 7000:
                # Грохот закрытия двери
                self.cutscene_phase = 4
                # TODO: sound_door_slam.play()
            elif self.cutscene_phase == 4 and elapsed > 8500:
                # Герой оборачивается — двери нет
                self.cutscene_phase = 5
            elif self.cutscene_phase == 5 and elapsed > 11000:
                # Конец спринта — вернуться в MENU или завершить
                self.state = "MENU"
                self.title_alpha = 0  # сброс

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == "MENU":
            # 1. Чёрный экран + fade-in названия
            title_surface = self.title_font.render(GAME_TITLE, True, WHITE)
            title_surface.set_alpha(self.title_alpha)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
            self.screen.blit(title_surface, title_rect)

            # 2. Лампочка сверху (TODO: улучшить анимацию и свет)
            lamp_color = (255, 255, 200) if self.lamp_on else (100, 100, 80)
            pygame.draw.circle(self.screen, lamp_color, (SCREEN_WIDTH // 2, 80), 15)
            # Луч света на дверь (TODO: шейдер / particle)
            if self.lamp_on:
                pygame.draw.rect(self.screen, (200, 200, 150), self.door_rect, 2)

            # Дверь в центре
            pygame.draw.rect(self.screen, (80, 60, 40), self.door_rect)  # дерево
            # Ручка
            handle_rect = pygame.Rect(self.door_rect.centerx + 20, self.door_rect.centery - 10, 15, 40)
            pygame.draw.rect(self.screen, (200, 180, 100), handle_rect)

            # Надпись "Старт" на двери
            start_text = self.button_font.render("Старт", True, WHITE)
            self.screen.blit(start_text, start_text.get_rect(center=self.door_rect.center))

            # Кнопки настроек по бокам
            for btn in self.settings_buttons:
                pygame.draw.rect(self.screen, DARK_BLUE, btn["rect"], border_radius=5)
                text_surf = self.button_font.render(btn["text"], True, WHITE)
                self.screen.blit(text_surf, text_surf.get_rect(center=btn["rect"].center))

            # Подсказка
            hint = self.button_font.render("Нажмите на дверь, чтобы начать", True, (150, 150, 150))
            self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)))

        elif self.state == "CUTSCENE":
            # Мини-катсцена (базовая, TODO: улучшить силуэт и анимацию)
            if self.cutscene_phase <= 2:
                # Тёмно, силуэт героя (простой прямоугольник)
                pygame.draw.rect(self.screen, (40, 40, 40), (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 150, 50, 120))  # тело
                pygame.draw.circle(self.screen, (30, 30, 30), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 170), 20)  # голова
            if self.cutscene_phase >= 3:
                # Экран темнеет
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(200)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
            if self.cutscene_phase == 5:
                # Двери нет — пустота
                void_text = self.title_font.render("Пустота...", True, RED_ACCENT)
                self.screen.blit(void_text, void_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            # Дебаг фазы
            phase_text = self.button_font.render(f"Фаза: {self.cutscene_phase}", True, WHITE)
            self.screen.blit(phase_text, (20, 20))

        pygame.display.flip()


if __name__ == "__main__":
    # Для теста в отдельности
    pass
