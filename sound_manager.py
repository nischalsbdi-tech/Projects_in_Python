"""Handles all audio for the game: paddle hits, wall bounces, scoring,
and looping background music. Uses pygame's mixer module purely for
audio playback (no pygame window/display is created).

If pygame isn't installed, or no audio device is available, the game
will still run normally with sound silently disabled.
"""

import os
import pygame

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds")


class SoundManager:
    def __init__(self, sounds_dir=SOUNDS_DIR):
        self.enabled = True
        try:
            pygame.mixer.init()
            self.hit_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "paddle_hit.wav"))
            self.wall_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "wall_bounce.wav"))
            self.score_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "score.wav"))
            self.music_path = os.path.join(sounds_dir, "background_music.wav")
        except Exception as error:
            print(f"[SoundManager] Audio disabled ({error}). The game will run silently.")
            self.enabled = False

    def play_hit(self):
        if self.enabled:
            self.hit_sound.play()

    def play_wall(self):
        if self.enabled:
            self.wall_sound.play()

    def play_score(self):
        if self.enabled:
            self.score_sound.play()

    def play_music(self):
        if self.enabled:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(loops=-1)

    def pause_music(self):
        if self.enabled:
            pygame.mixer.music.pause()

    def unpause_music(self):
        if self.enabled:
            pygame.mixer.music.unpause()

    def stop_music(self):
        if self.enabled:
            pygame.mixer.music.stop()
