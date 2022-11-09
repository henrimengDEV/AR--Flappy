import math
import pickle

import pygame

import config
import qtbl
from agent import Player
from config import *
from pipe import Pipe
from qtbl import *


class Environment:
    def __init__(self, manager):
        self.spawn_i = 0
        self.best_score = 0
        self.i = 0
        self.manager = manager
        self.player = Player(config.ALPHA)
        self.bg = load_image(os.path.join(IMAGES, 'bg.png'))
        self.ground_img = load_image(os.path.join(IMAGES, 'base.png'))
        self.show_score = False
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
            2: 250,
        }
        self.original_speed = self.speed
        self.deltaRadarX = 100
        self.deltaRadarY = 100

    def stop_game(self):
        config.ITERATION += 1
        if config.EPSILON > 0:
            config.EPSILON -= 0.001
        if config.ALPHA > 0.1:
            config.ALPHA -= 0.00003
        print(F"ITERATION = {config.ITERATION}")
        self.manager.switch_mode('game', reset=True)

    def step(self, events: list[pygame.event.Event], dt, clock):


        player_rect = self.player.rect
        self.pipes = [i for i in self.pipes if i.visible]

        if not self.stopped:
            self.handle_speed(dt)
            self.handle_map(dt)

            for pipe in self.pipes:
                self.handle_pipe(pipe, dt)
                if pipe.collision(player_rect):
                    self.player.learn(-10000)
                    self.stop_game()

            if self.is_out_of_map(player_rect):
                self.player.learn(-10000)
                self.stop_game()

            #if self.score > 0 and self.score % 5 == 0:
                #self.player.learn(10)


            #if player_rect.y == self.pipes[0].rectangle_middle.y + 100:
                #self.player.learn(1)

            self.player.step(events, dt, (self.horizontal_distance_from_next_pipe_clamp(), self.vertical_bot_distance_from_next_pipe_clamp(), self.vertical_delta_distance_from_next_pipe_clamp()), clock)

    def draw(self, surf: pygame.Surface):
        self.default_surface(surf)
        self.display_next_goal(surf)
        self.player.draw(surf)
        self.display_score(surf)
        self.display_info_position(surf)

    def is_out_of_map(self, player_rect) -> bool:
        return player_rect.top < 0 or player_rect.bottom > H - 50

    def handle_speed(self, dt):
        self.original_speed += 0.0005 * dt
        self.original_speed = clamp(self.original_speed, SPEED, 10)
        self.speed = round(self.original_speed, 2)

    def handle_map(self, dt):
        self.ground_offset -= self.speed * dt
        self.pipe_spawner -= self.speed * dt
        if self.pipe_spawner < -self.pipe_spawn_distances[2]:
            self.pipe_spawner = 0
            self.pipes.append(Pipe(self.pipes[-1].x + self.pipe_spawn_distances[2]))
            self.spawn_i += 1
        if self.ground_offset < -self.ground_img.get_width():
            self.ground_offset = 0

    def handle_pipe(self, i, dt):
        i.move(self.speed, dt)
        if i.x < self.player.x - round(i.x):
            i.visible = False
            if not i.scored:
                self.score += 1
                i.scored = True
                self.player.learn(0)

    def display_next_goal(self, surf):
        self.pipes[0].draw(surf, True)

    def horizontal_distance_from_next_pipe(self):
        return round((self.player.rect.y - self.pipes[0].rectangle_middle.y - 150 / 2) / 50)

    def vertical_distance_from_next_pipe(self):
        return round((self.player.rect.x - self.pipes[0].rectangle_middle.x) / 50)

    def horizontal_distance_from_next_pipe_clamp(self):
        #if clamp(self.pipes[0].rectangle_middle.x / self.deltaRadar, -127, 255) > 1.88:
        return clamp(math.ceil(self.pipes[0].rectangle_middle.x / self.deltaRadarX), -127, 255)
        #else:
            #return clamp(math.ceil(self.pipes[1].rectangle_middle.x / self.deltaRadar), -127, 255)

    def vertical_top_distance_from_next_pipe_clamp(self):
        return clamp(math.ceil((self.player.rect.y - self.pipes[0].rectangle_top.bottom) / self.deltaRadarY), -127, 255)

    def vertical_bot_distance_from_next_pipe_clamp(self):
        return clamp(math.ceil((self.pipes[0].rectangle_bot.y - self.player.rect.y) / self.deltaRadarY), -127, 255)

    def vertical_delta_distance_from_next_pipe_clamp(self):
        return (self.vertical_bot_distance_from_next_pipe_clamp() - self.vertical_top_distance_from_next_pipe_clamp())

    def vertical_middle_distance_from_next_pipe_clamp(self):
        return clamp(math.ceil((self.player.rect.y - self.pipes[0].rectangle_middle.y) / self.deltaRadarY), -127, 255)

    def default_surface(self, surf):
        surf.blit(self.bg, (0, 0))
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
        iterations = font.render(f"Iteration: {config.ITERATION}", True, pygame.Color('white'))
        pos_x = font.render(f"x: {self.horizontal_distance_from_next_pipe_clamp()}", True, pygame.Color('white'))
        pos_delta_y = font.render(f"delta_y: {self.vertical_delta_distance_from_next_pipe_clamp()}", True, pygame.Color('white'))
        pos_y_bot = font.render(f"y_bot: {self.vertical_bot_distance_from_next_pipe_clamp()}", True, pygame.Color('white'))
        last_action = font.render(f"action: {self.player.last_action}", True, pygame.Color('white'))
        reward = font.render(f"reward: {self.player.last_reward}", True, pygame.Color('white'))
        epsilon = font.render(f"randomness: {config.EPSILON}", True, pygame.Color('white'))
        surf.blit(iterations, ((W / 2) - 33, 20))
        surf.blit(pos_x, (20, 20))
        surf.blit(pos_delta_y, (20, 40))
        surf.blit(pos_y_bot, (20, 60))
        surf.blit(last_action, (20, 80))
        surf.blit(reward, (20, 100))
        surf.blit(epsilon, (20, 120))
