import random
import os

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import (
    StringProperty, ListProperty, BoundedNumericProperty, BooleanProperty)


class MenuScreen(Screen):
    heading = StringProperty("Choose shuffling constraints (a or b)")


class ShufflingScreen(Screen):
    player_label = StringProperty("Current player: Raven")
    next_player_label = StringProperty("Next player: Spider")
    order_label = StringProperty("Shuffle the loyalty tokens!")
    order_images = ListProperty()
    next_player_btn = Button(text='Next player', disabled=True)

    def update(self, player_txt, next_player_txt,
               order="Shuffle the loyalty tokens!"):
        self.player_label = f"Current player: {player_txt}"
        self.next_player_label = f"Next player: {next_player_txt}"
        if isinstance(order, tuple):
            self.order_label = order[0]
            self.order_images = order[1]
        else:
            self.order_label = order
            if order == "Shuffle the loyalty tokens!":
                for i in range(len(self.order_images)):
                    self.order_images[i] = ""

    def disable_btn(self, btn):
        if btn == 'next_player_btn':
            self.next_player_btn.disabled = True

    def enable_btn(self, btn):
        if btn == 'next_player_btn':
            self.next_player_btn.disabled = False

    def display_order(self, current_shuffle):
        as_string = f"{' || '.join(current_shuffle)}"
        try:
            return as_string, [os.environ[empire] for empire
                               in current_shuffle]
        except KeyError:
            return as_string


class WoWSceenManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = MenuScreen(name='menu')
        self.shuffling = ShufflingScreen(name='shuffling')
        self.add_widget(self.menu)
        self.add_widget(self.shuffling)


class WoWShuffler(Widget):
    mode = StringProperty()
    empires = ListProperty(('horse', 'bear', 'lion', 'elephant', 'eagle'))
    players = ListProperty(('Raven', 'Spider', 'Rat', 'Snake'))
    current_player_index = BoundedNumericProperty(0, min=0, max=3,
                                                  errorvalue=3)
    current_shuffle = ListProperty([])
    devouts = ListProperty()
    opposed = ListProperty()

    def _shuffle(self):
        shuffled = random.sample(self.empires, len(self.empires))
        return shuffled

    def _shuffled_correctly(self, shuffled):
        if self.mode == 'a':
            return shuffled[0] not in self.devouts
        return (shuffled[0] not in self.devouts and shuffled[-1]
                not in self.opposed)

    def get_empires_order(self):
        not_shuffled = True
        while not_shuffled:
            empires_order = self._shuffle()
            if self._shuffled_correctly(empires_order):
                not_shuffled = False
                self.current_shuffle = empires_order
                return self.current_shuffle

    def commit_shuffle(self):
        try:
            self.devouts.append(self.current_shuffle[0])
            if self.mode == 'b':
                self.opposed.append(self.current_shuffle[-1])
        except IndexError:
            pass

    def get_current_player(self):
        return self.players[self.current_player_index]

    def get_next_player(self):
        if self.current_player_index < len(self.players) - 1:
            return self.players[self.current_player_index + 1]
        return ""

    def change_player(self):
        if self.current_shuffle:
            self.current_player_index += 1

    def reset_properties(self):
        self.current_player_index = 0
        self.devouts = []
        self.opposed = []
        self.current_shuffle = []


class WoWApp(App):
    shuffler = WoWShuffler()
    use_images = BooleanProperty(False)

    def check_for_images(self):
        if os.getenv('horse'):
            self.use_images = True

    def build(self):
        self.check_for_images()
        wow_sm = WoWSceenManager()
        return wow_sm


if __name__ == '__main__':
    WoWApp().run()
