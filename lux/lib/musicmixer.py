import logging

import arcade
from arcade.types import Color
import pyglet.media as media

logger = logging.getLogger("lux")


class RGBMusicMixer:
    def __init__(self, sounds: arcade.Sound, volume = 1.0):
        """Plays exactly three tracks based on color.

        Implements most of the functions of pyglet.media.Player.
        """
        if len(sounds) != 3:
            raise ValueError("RGBMusicMixer requires three sounds!")
        self.tracks: list[media.Player] = [s.play(volume = volume) for s in sounds]
        self.volume = volume
        self.pause()
        self.seek(0)

        self._red = True
        self._green = True
        self._blue = True

    @property
    def red(self) -> bool:
        return self._red

    @red.setter
    def red(self, v: bool):
        self._red = v
        self.r.volume = self.volume if v else 0

    @property
    def green(self) -> bool:
        return self._green

    @green.setter
    def green(self, v: bool):
        self._green = v
        self.g.volume = self.volume if v else 0

    @property
    def blue(self) -> bool:
        return self._blue

    @blue.setter
    def blue(self, v: bool):
        self._blue = v
        self.b.volume = self.volume if v else 0

    @property
    def r(self) -> media.Player:
        return self.tracks[0]

    @r.setter
    def r(self, sound: arcade.Sound):
        self.tracks[0] = sound.play(volume = self.volume if self._red else 0)
        self.tracks[0].seek(self.time)

    @property
    def g(self) -> media.Player:
        return self.tracks[1]

    @g.setter
    def g(self, sound: arcade.Sound):
        self.tracks[1] = sound.play(volume = self.volume if self._green else 0)
        self.tracks[1].seek(self.time)

    @property
    def b(self) -> media.Player:
        return self.tracks[2]

    @b.setter
    def b(self, sound: arcade.Sound):
        self.tracks[2] = sound.play(volume = self.volume if self._blue else 0)
        self.tracks[2].seek(self.time)

    @property
    def color(self) -> Color:
        return Color(255 if self._red else 0, 255 if self._green else 0, 255 if self._blue else 0)

    @color.setter
    def color(self, color: Color):
        self.red = 255 if color.r > 127 else 0
        self.green = 255 if color.g > 127 else 0
        self.blue = 255 if color.b > 127 else 0

    @property
    def time(self) -> float:
        if not self.tracks:
            return 0.0
        return self.tracks[0].time

    @property
    def duration(self) -> float:
        if not self.tracks:
            return 0.0
        return max([t.source.duration if t.source else 0 for t in self.tracks])

    @property
    def playing(self) -> bool:
        if not self.tracks:
            return False
        return self.tracks[0].playing

    def seek(self, time):
        playing = self.playing
        if playing:
            self.pause()
        for t in self.tracks:
            t.seek(time)
        if playing:
            self.play()

    def play(self):
        self.sync()
        for t in self.tracks:
            t.play()

    def pause(self):
        for t in self.tracks:
            t.pause()

    def close(self):
        self.pause()
        for t in self.tracks:
            t.delete()
        self.tracks = []

    @property
    def loaded(self) -> bool:
        return bool(self.tracks)

    def sync(self):
        maxtime = max(t.time for t in self.tracks)
        self.seek(maxtime)
