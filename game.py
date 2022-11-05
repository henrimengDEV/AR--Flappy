from config import *
from menu_manager import MenuManager
from objects import Player, Pipe


class Game:
    def __init__(self, manager: 'MenuManager'):
        super().__init__('game', manager)
        self.player = Player()
        self.manager = manager
        self.bg = load_image(os.path.join(IMAGES, 'bg.png'))
        self.ground_img = load_image(os.path.join(IMAGES, 'base.png'))
        self.show_score = False
        # self.game_over_msg = load_image(os.path.join(IMAGES, 'gameover.png'), alpha=True, scale=1.5)
        self.ground_offset = 0
        self.pipes = [Pipe(W // 2 + i * 200) for i in range(5)]
        self.speed = SPEED
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
            5: 250,
            6: 275,
            7: 275,
            8: 275,
            9: 300,
            10: 300
        }
        self.original_speed = self.speed

    def stop_game(self):
        self.manager.switch_mode('game', reset=True)

    def update(self, events: list[pygame.event.Event], dt):
        player_rect = self.player.rect
        self.pipes = [i for i in self.pipes if i.visible]

        if not self.stopped:
            self.handle_speed(dt)
            self.handle_map(dt)

            for pipe in self.pipes:
                self.handle_pipe(pipe, dt)
                if pipe.collision(player_rect):
                    self.stop_game()

        self.player.update(events, dt)

        if self.is_out_of_map(player_rect):
            self.stop_game()

    def draw(self, surf: pygame.Surface):
        surf.blit(self.bg, (0, 0))
        for i in range(4):
            surf.blit(self.ground_img, (i * self.ground_img.get_width() + round(self.ground_offset), H - 50))
        for i in self.pipes:
            i.draw(surf)

        self.display_next_goal(surf)
        self.player.draw(surf)

        # generate score image
        w, h = self.numbers[0].get_size()
        score = str(self.score)
        s = pygame.Surface((w * len(score), h), pygame.SRCALPHA)
        for i in range(len(score)):
            s.blit(self.numbers[int(score[i])], (i * w, 0))
        else:
            surf.blit(s, s.get_rect(center=(W // 2, 100)))

    def is_out_of_map(self, player_rect) -> bool:
        return player_rect.top < 0 or player_rect.bottom > H - 50

    def handle_speed(self, dt):
        self.original_speed += 0.0005 * dt
        self.original_speed = clamp(self.original_speed, SPEED, 10)
        self.speed = round(self.original_speed, 2)

    def handle_map(self, dt):
        self.ground_offset -= self.speed * dt
        self.pipe_spawner -= self.speed * dt
        if self.pipe_spawner < -self.pipe_spawn_distances[round(self.speed)]:
            self.pipe_spawner = 0
            self.pipes.append(Pipe(self.pipes[-1].x + self.pipe_spawn_distances[round(self.speed)]))
        if self.ground_offset < -self.ground_img.get_width():
            self.ground_offset = 0


    def handle_pipe(self, i, dt):
        i.move(self.speed, dt)
        # if i.x < self.player.x - 100:
        #     if not i.scored:
        #         self.score += 1
        #         i.scored = True
        # if i.x < -i.image.get_width():
        if i.x < self.player.x - round(i.x):
            i.visible = False
            if not i.scored:
                self.score += 1
                i.scored = True


    def display_next_goal(self, surf):
        self.pipes[0].draw(surf, True)