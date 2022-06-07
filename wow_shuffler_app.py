import random

from kivy.app import App    
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import (
    ObjectProperty, StringProperty, ListProperty, BoundedNumericProperty)


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
        self.shuffler = ObjectProperty()
        self.menu = MenuScreen(name='menu')
        self.shuffling = ShufflingScreen(name='shuffling')
        self.add_widget(self.menu)
        self.add_widget(self.shuffling)
    
    def refresh(self):
        self.clear_widgets([self.shuffling])
        self.add_widget(self.shuffling)


class WoWShuffler(BoxLayout):
    mode = StringProperty()
    empires = ListProperty(('horse', 'bear', 'lion', 'elephant', 'eagle'))
    players = ListProperty(('Raven', 'Spider', 'Rat', 'Snake'))
    current_player_index = BoundedNumericProperty(0, min=0, max=3, errorvalue=3)
    devouts = ListProperty()
    opposed = ListProperty()

    def _shuffle(self, empires):
        shuffled = random.sample(empires, len(empires))
        return shuffled

    def _shuffled_correctly(self, mode, shuffled, devouts, opposed):
        if mode == 'a':
            return shuffled[0] not in devouts
        return shuffled[0] not in devouts and shuffled[-1] not in opposed

    def get_empires_order(self, mode, empires, devouts, opposed, same_player=True):
        not_shuffled = True
        while not_shuffled:
            empires_order = self._shuffle(empires)
            if self._shuffled_correctly(mode, empires_order, devouts, opposed):
                not_shuffled = False
                if not same_player:
                    devouts.append(empires_order[0])
                if mode == 'b':
                    if not same_player:
                        opposed.append(empires_order[0])
                return empires_order

    def get_current_player(self, players, index):
        return players[index]

    def reset_properties(self):
        self.current_player_index = 0
        self.devouts.set([])
        self.opposed.set([])


class WoWApp(App):

    def build(self):
        wow_sm = WoWSceenManager()
        return wow_sm


if __name__ == '__main__':
    WoWApp().run()
