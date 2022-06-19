import random

from kivy.app import App    
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import (
    StringProperty, ListProperty, BoundedNumericProperty)


class MenuScreen(Screen):
    heading = Label(text="Choose shuffling constraints (a or b)")


class ShufflingScreen(Screen):
    player_label = Label(text="Current player: Raven")
    order_label = Label(text="Shuffle the loyalty tokens!")
    next_player_btn = Button(text='Next player', disabled=True)

    def update(self, player_txt, order_txt):
        self.player_label.text = player_txt
        self.order_label.text = order_txt

    def disable_btn(self, btn):
        if btn == 'next_player_btn':
            self.next_player_btn.disabled = True

    def enable_btn(self, btn):
        if btn == 'next_player_btn':
            self.next_player_btn.disabled = False


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
    current_player_index = BoundedNumericProperty(0, min=0, max=3, errorvalue=3)
    current_shuffle = ListProperty([])
    devouts = ListProperty()
    opposed = ListProperty()

    def _shuffle(self):
        shuffled = random.sample(self.empires, len(self.empires))
        return shuffled

    def _shuffled_correctly(self, shuffled):
        if self.mode == 'a':
            return shuffled[0] not in self.devouts
        return shuffled[0] not in self.devouts and shuffled[-1] not in self.opposed

    def get_empires_order(self):
        not_shuffled = True
        while not_shuffled:
            empires_order = self._shuffle()
            if self._shuffled_correctly(empires_order):
                not_shuffled = False
                return empires_order

    def commit_shuffle(self):
        try:
            self.devouts.append(self.current_shuffle[0])
            if self.mode == 'b':
                self.opposed.append(self.current_shuffle[-1])
        except IndexError:
            pass
     
    def get_current_player(self):
        return self.players[self.current_player_index]

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

    def build(self):
        wow_sm = WoWSceenManager()
        return wow_sm


if __name__ == '__main__':
    WoWApp().run()
