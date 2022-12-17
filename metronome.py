import pygame, sys, time


MIN_BPM = 20
MAX_BPM = 300


class DropDownMenu:
    def __init__(self, x, y, width, height, color, highlight, options):
        self.color = color
        self.highlight = highlight

        self.options = options
        self.options_visible = False
        self.option_rects = [pygame.Rect(x, y + height + height * i, width, height) for i in range(len(options))]

        self.selected_rect = pygame.Rect(x, y, width, height)
        self.selected_option = options[2]

    def draw(self, surface):
        pygame.draw.rect(surface, self.highlight if is_rect_hovered(self.selected_rect) else self.color, self.selected_rect)
        pygame.draw.polygon(surface, (255, 255, 255), ((self.selected_rect.right - 16, self.selected_rect.top + 6), (self.selected_rect.right - 6, self.selected_rect.top + 6), (self.selected_rect.right - 11, self.selected_rect.bottom - 6)))
        draw_text(surface, self.selected_option, (0, 0, 0), self.selected_rect.center, 25)

        if self.options_visible:
            selected_option_passed = False
            for index, option in enumerate(self.options):
                if option == self.selected_option:
                    selected_option_passed = True
                    continue

                option_rect = self.option_rects[index].copy()
                if selected_option_passed:
                    option_rect.top -= option_rect.height

                pygame.draw.rect(surface, self.highlight if is_rect_hovered(option_rect) else self.color, option_rect)
                draw_text(surface, option, (0, 0, 0), option_rect.center, 25)


class ArrowButton:
    def __init__(self, x, y, width, height, color, highlight, direction):
        self.color = color
        self.highlight = highlight
        self.direction = direction
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        if self.direction == "up":
            pygame.draw.polygon(surface, self.highlight if is_rect_hovered(self.rect) else self.color, (self.rect.bottomleft, self.rect.midtop, self.rect.bottomright))

        elif self.direction == "down":
            pygame.draw.polygon(surface, self.highlight if is_rect_hovered(self.rect) else self.color, (self.rect.topleft, self.rect.midbottom, self.rect.topright))


def is_rect_hovered(rect):
    return rect.collidepoint(pygame.mouse.get_pos())


def draw_text(surface, text, color, center, size):
    font = pygame.font.Font("freesansbold.ttf", size)
    font_surface = font.render(text, True, color)
    font_rect = font_surface.get_rect()
    font_rect.center = center
    surface.blit(font_surface, font_rect)


def draw_metronome(surface: pygame.Surface, current_beat):
    # renders the metronome visual guide (kinda like lights that light up) to the given surface
    radius = 20
    gap = radius * 2
    screen_center_x = surface.get_width() / 2
    center_y = surface.get_height() / 2 - 75

    pygame.draw.circle(surface, (255, 0, 0) if current_beat == 1 else (147, 0, 0), (screen_center_x - radius - gap - radius - gap, center_y), radius) # first light
    pygame.draw.circle(surface, (255, 225, 0) if current_beat == 2 else (147, 100, 0), (screen_center_x - radius - gap / 2, center_y), radius) # second light
    pygame.draw.circle(surface, (255, 225, 0) if current_beat == 3 or current_beat == 5 else (147, 100, 0), (screen_center_x + radius + gap / 2, center_y), radius) # third light
    pygame.draw.circle(surface, (255, 225, 0) if current_beat == 4 or current_beat == 6 else (147, 100, 0), (screen_center_x + radius + gap + radius + gap, center_y), radius) # fourth light

    # pygame.draw.line(surface, (255, 255, 255), (screen_center_x, 0), (screen_center_x, surface.get_height()))


def update_current_beat(current_beat, current_beat_time, seconds_per_beat, beats_per_bar):
    # update the current beat based on current time and the No. seconds per beat
    if current_beat_time < seconds_per_beat:
        return current_beat, current_beat_time

    current_beat += 1 if current_beat + 1 <= beats_per_bar else -beats_per_bar + 1
    current_beat_time = 0

    return current_beat, current_beat_time


def main():
    pygame.init()
    window_surface = pygame.display.set_mode((500, 500), flags=pygame.DOUBLEBUF, vsync=True)
    pygame.display.set_caption("Metronome")

    beats_per_bar_dropdown = DropDownMenu(125, 300, 75, 30, (147, 147, 147), (100, 100, 100), ["2", "3", "4", "5", "6"])
    bpm_up_arrow = ArrowButton(460, 280, 30, 30, (147, 147, 147), (100, 100, 100), "up")
    bpm_down_arrow = ArrowButton(460, 315, 30, 30, (147, 147, 147), (100, 100, 100), "down")

    bpm = 120
    beats_per_bar = 4
    seconds_per_beat = 60 / bpm
    current_beat_time = 0
    current_beat = 1

    current_time = 0
    last_time = time.time()
    delta_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_beat += 1 if current_beat + 1 <= 4 else -3

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_WHEELUP:
                    bpm += 1 if bpm + 1 <= MAX_BPM else 0
                    seconds_per_beat = 60 / bpm
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    bpm -= 1 if bpm - 1 >= MIN_BPM else 0
                    seconds_per_beat = 60 / bpm

                elif event.button == pygame.BUTTON_LEFT:
                    if beats_per_bar_dropdown.options_visible:
                        selected_option_passed = False
                        for index, option in enumerate(beats_per_bar_dropdown.options):
                            if option == beats_per_bar_dropdown.selected_option:
                                selected_option_passed = True
                                continue

                            option_rect = beats_per_bar_dropdown.option_rects[index].copy()
                            if selected_option_passed:
                                option_rect.top -= option_rect.height

                            if is_rect_hovered(option_rect):
                                beats_per_bar_dropdown.selected_option = option
                                beats_per_bar_dropdown.options_visible = False
                                beats_per_bar = int(beats_per_bar_dropdown.selected_option)
                                current_beat_time = 0
                                current_beat = 1

                    if is_rect_hovered(beats_per_bar_dropdown.selected_rect):
                        beats_per_bar_dropdown.options_visible = not beats_per_bar_dropdown.options_visible

                    if is_rect_hovered(bpm_up_arrow.rect):
                        bpm += 1 if bpm + 1 <= MAX_BPM else 0
                        seconds_per_beat = 60 / bpm
                    elif is_rect_hovered(bpm_down_arrow.rect):
                        bpm -= 1 if bpm - 1 >= MIN_BPM else 0
                        seconds_per_beat = 60 / bpm

        # ----------------- update metronome --------------------
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        current_beat_time += delta_time
        current_beat, current_beat_time = update_current_beat(current_beat, current_beat_time, seconds_per_beat, beats_per_bar)
        # -------------------------------------------------------

        window_surface.fill((0, 0, 0))

        draw_metronome(window_surface, current_beat)

        draw_text(window_surface, "Beats:", (255, 255, 255), (beats_per_bar_dropdown.selected_rect.left - 50, beats_per_bar_dropdown.selected_rect.centery), 25)
        beats_per_bar_dropdown.draw(window_surface)

        draw_text(window_surface, "BPM:", (255, 255, 255), (bpm_up_arrow.rect.left - 125, beats_per_bar_dropdown.selected_rect.centery), 25)
        draw_text(window_surface, str(bpm), (255, 255, 255), (bpm_up_arrow.rect.left - 50, beats_per_bar_dropdown.selected_rect.centery), 25)
        bpm_up_arrow.draw(window_surface)
        bpm_down_arrow.draw(window_surface)

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
