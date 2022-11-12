import config
from ia.ia_basic import *
from config import *
from pipe import Pipe

class Environment:
    def __init__(self, player):
        self.player = player
        self.has_scored = False
        self.failed = False
        self.delta_time = 1
        self.reset = False
        self.background = load_image(os.path.join(IMAGES, 'bg.png'))
        self.ground_img = load_image(os.path.join(IMAGES, 'base.png'))
        self.show_score = False
        self.ground_offset = 0
        self.pipes = [Pipe(W // 2 + i * 200) for i in range(5)]
        self.speed = START_SPEED
        self.stopped = False
        self.score = 0
        self.score_img = load_image(os.path.join(IMAGES, 'score.png'), alpha=True)
        self.numbers = {i: load_image(os.path.join(IMAGES, f'{i}.png'), alpha=True) for i in range(10)}
        self.font = pygame.font.Font(os.path.join(ASSETS, 'flappy bird font.ttf'), 20)
        self.pipe_spawner = 0
        self.pipe_spawn_distances = {
            2: 200,
            3: 225,
            4: 250,
            5: 275,
            6: 300,
            7: 325,
            8: 350,
            9: 375,
            10: 400
        }
        self.original_speed = self.speed

    def stop_game(self):
        global BEST_SCORE
        if self.score > BEST_SCORE:
            BEST_SCORE = self.score
        self.reset = True

    def step(self):
        player_rect = self.player.rect
        self.pipes = [i for i in self.pipes if i.visible]

        if not self.stopped:
            self.handle_speed()
            self.handle_map()

            for pipe in self.pipes:
                self.handle_pipe(pipe)
                if pipe.collision(player_rect):
                    self.failed = True
                    self.stop_game()

            if self.is_out_of_map(player_rect):
                self.failed = True
                self.stop_game()

            self.player.step(self.delta_time)

    def draw(self, surf: pygame.Surface):
        self.default_surface(surf)
        self.display_next_goal(surf)
        self.player.draw(surf)
        self.display_score(surf)
        self.display_info_position(surf)

    def is_out_of_map(self, player_rect) -> bool:
        return player_rect.top < 0 or player_rect.bottom > H - 50

    def handle_speed(self):
        self.original_speed += 0.0005 * self.delta_time
        self.original_speed = clamp(self.original_speed, START_SPEED, END_SPEED)
        self.speed = round(self.original_speed, 2)

    def handle_map(self):
        self.ground_offset -= math.ceil(self.speed) * self.delta_time
        self.pipe_spawner -= math.ceil(self.speed) * self.delta_time
        if self.pipe_spawner <= -self.pipe_spawn_distances[round(self.speed)]:
            self.pipe_spawner = 0
            self.pipes.append(Pipe(self.pipes[-1].x + self.pipe_spawn_distances[round(self.speed)]))
        if self.ground_offset < -self.ground_img.get_width():
            self.ground_offset = 0

    def handle_pipe(self, i):
        i.move(self.speed, self.delta_time)
        if i.x < self.player.x - round(i.x):
            i.visible = False
            if not i.scored:
                self.score += 1
                i.scored = True
                self.has_scored = True

    def display_next_goal(self, surf):
        self.pipes[0].draw(surf, True)

    def default_surface(self, surf):
        surf.blit(self.background, (0, 0))
        for i in range(4):
            surf.blit(self.ground_img, (i * self.ground_img.get_width() + round(self.ground_offset), H - 50))
        for i in self.pipes:
            i.draw(surf)

    def display_score(self, surf: pygame.Surface):
        w, h = self.numbers[0].get_size()
        score = str(self.score)
        s = pygame.Surface((w * len(score), h), pygame.SRCALPHA)
        for i in range(len(score)):
            s.blit(self.numbers[int(score[i])], (i * w, 0))
        else:
            surf.blit(s, s.get_rect(center=(W // 2, 100)))

    def display_info_position(self, surf: pygame.Surface):
        font = pygame.font.SysFont(None, 24)
        font_h1 = pygame.font.SysFont("impact", 32)
        best_score = font_h1.render(f"BEST: {BEST_SCORE} ", True, pygame.Color('white'))
        speed = font.render(f"speed: {self.speed}", True, pygame.Color('white'))
        surf.blit(speed, (W - 120, 20))
        surf.blit(best_score, ((W / 2) - 55, 25))