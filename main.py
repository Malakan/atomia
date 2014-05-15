'''
Atomia

Copyright (C) 2014  Stacy Maillot

This file is part of Atomia.

Atomia is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Atomia is distributed in the hope that it will be fun,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Atomia.  If not, see <http://www.gnu.org/licenses/>.
'''

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window
from kivy.graphics import Rectangle, Line, Color

from time import time
from random import randint
from math import ceil
from os.path import join, dirname
from glob import glob


from puzzle import PuzzleGame

from kivy.config import Config

# Config.set('graphics', 'width','600')
# Config.set('graphics', 'height', '800')

class Start(FloatLayout):
	def __init__(self):
		super(Start, self).__init__()
		self.add_widget(Welcome())


class Welcome(FloatLayout):
	blinking_text = ObjectProperty()
	
	def __init__(self):
		super(Welcome, self).__init__()
		self.anim = Animation(opacity=0, d=1)
		Clock.schedule_interval(self.blinking, 1)
		
	def blinking(self, dt):
		self.blinking_text.opacity = 1
		self.anim.start(self.blinking_text)
		
	def on_touch_down(self, touch):
		Clock.unschedule(self.blinking)
		self.anim.stop(self.blinking_text)
		parent = self.parent
		parent.clear_widgets()
		parent.add_widget(Principal())

		
class Principal(FloatLayout):
	board_box = ObjectProperty()
	restart_button = ObjectProperty()
	coordonnee_x = NumericProperty()
	space = NumericProperty()
	position_x = NumericProperty()
	position_y = NumericProperty()
	
	score = NumericProperty()
	nb_combi_find = StringProperty()
	
	def __init__(self, **kwargs):
		super(Principal, self).__init__(**kwargs)
		
		self.score = int()
		
		self.number_find = 0
		self.nb_combi_find = str(self.number_find) + ' / ' + str(24)
		self.boards_list = []
		self.board_box.bind(minimum_height=self.board_box.setter('height'))
		
		self.coordonnee_x = ((PuzzleGame().atom_size[0] + PuzzleGame().interval) * PuzzleGame().cols_max)
		self.space = PuzzleGame().atom_size[0]
		self.position_x = PuzzleGame().x
		self.position_y = PuzzleGame().y
		self.curdir = dirname(__file__)
		
		for board_name in glob(join(self.curdir, 'graphics', 'formulaboards', '*')):
			board = Image(allow_stretch=True, keep_ratio=False, source=board_name, size_hint=(None, None), size=(self.board_box.width, Window.height / 10))
			self.board_box.add_widget(board)
			self.boards_list.append(board)
	
	def display_popup_restart(self):
		self.popup_restart = PopupRestart()
		self.popup_restart.yes_button_restart.bind(on_press=self.restart)
		self.popup_restart.open()
	
	def restart(self, *args):
		parent = self.parent
		parent.clear_widgets()
		self.popup_restart.dismiss()
		parent.add_widget(Principal())
		
	def update_score(self, nb):
		self.score += nb
		
	def draw_line_board(self, name):
		img = name + '.png'
		path_img = glob(join(self.curdir, 'graphics', 'formulaboards', img))
		absolute_path = "".join(path_img)
		self.number_find += 1
		self.nb_combi_find = str(self.number_find) + ' / ' + str(28)

		for board in self.boards_list:
			if absolute_path == board.source:
				with board.canvas.after:
					Line(width=1.5, bezier=(board.x, board.y + board.height /2, board.x + board.width, board.y + board.height /2))
				break
				
	def display_exit_popup(self):
		popup_exit = PopupExit()
		# popup_exit.yes_button_exit.bind(on_press=App().stop())
		popup_exit.open()


class PopupRestart(Popup):
	yes_button_restart = ObjectProperty()
	
class PopupExit(Popup):
	yes_button_exit = ObjectProperty()

class AtomiaApp(App):
	title = 'Atomia'
    # icon = 'icon.png'
	my_time = NumericProperty()
	
	def build(self):
		Clock.schedule_interval(self.my_clock, 1 / 60.)
		root = Start()
		return root
		
	def my_clock(self, dt):
		self.my_time = time()
		
if __name__ == '__main__':
	AtomiaApp().run()
		