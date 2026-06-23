"""Generates simple placeholder sound effects and background music as
plain .wav files using only Python's standard library (no external
dependencies, no internet, no audio software required).

Run this once to (re)create the files in assets/sounds/. Feel free to
swap any of the generated files for your own recorded/downloaded
sounds later -- just keep the same filenames.
"""

import wave
import struct
import math
import os

SAMPLE_RATE = 44100


def _fade(sample, i, n_samples, fade_len):
    if i < fade_len:
        return sample * (i / fade_len)
    if i > n_samples - fade_len:
        return sample * ((n_samples - i) / fade_len)
    return sample


def make_tone(filename, frequency, duration, volume=0.5):
    n_samples = int(SAMPLE_RATE * duration)
    fade_len = max(1, int(SAMPLE_RATE * 0.01))
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / SAMPLE_RATE
            sample = math.sin(2 * math.pi * frequency * t)
            sample = _fade(sample, i, n_samples, fade_len)
            value = int(sample * volume * 32767)
            wav_file.writeframes(struct.pack("<h", value))


def make_melody(filename, notes, note_duration, volume=0.35):
    n_samples_per_note = int(SAMPLE_RATE * note_duration)
    fade_len = max(1, int(SAMPLE_RATE * 0.01))
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        for freq in notes:
            for i in range(n_samples_per_note):
                t = i / SAMPLE_RATE
                sample = math.sin(2 * math.pi * freq * t)
                sample = _fade(sample, i, n_samples_per_note, fade_len)
                value = int(sample * volume * 32767)
                wav_file.writeframes(struct.pack("<h", value))


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds")
    os.makedirs(out_dir, exist_ok=True)

    make_tone(os.path.join(out_dir, "paddle_hit.wav"), frequency=440, duration=0.08, volume=0.5)
    make_tone(os.path.join(out_dir, "wall_bounce.wav"), frequency=220, duration=0.08, volume=0.5)
    make_melody(os.path.join(out_dir, "score.wav"), notes=[523, 659, 784], note_duration=0.12, volume=0.45)
    make_melody(
        os.path.join(out_dir, "background_music.wav"),
        notes=[262, 294, 330, 349, 392, 349, 330, 294] * 2,
        note_duration=0.25,
        volume=0.18,
    )

    print(f"Sound files generated in: {out_dir}")


if __name__ == "__main__":
    main()
