from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.uix.button import Button
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
	
	def __init__(self):
		super(Principal, self).__init__()

		self.board_box.bind(minimum_height=self.board_box.setter('height'))
		
		self.coordonnee_x = ((PuzzleGame().atom_size[0] + PuzzleGame().interval) * PuzzleGame().cols_max)
		self.space = PuzzleGame().atom_size[0] 
		self.position_x = PuzzleGame().x
		self.position_y = PuzzleGame().y
		curdir = dirname(__file__)
		
		for board_name in glob(join(curdir, 'graphics\\formulaboards', '*')):
			board = Image(allow_stretch=True, keep_ratio=False, source=board_name, size_hint=(None, None), size=(self.board_box.width, Window.height / 10))
			self.board_box.add_widget(board)
			
	def display_popup_restart(self):
		self.popup_restart = PopupRestart()
		self.popup_restart.yes_button.bind(on_press=self.restart)
		self.popup_restart.open()
	
	def restart(self, *args):
		parent = self.parent
		parent.clear_widgets()
		self.popup_restart.dismiss()
		parent.add_widget(Principal())
		
	def display_exit_popup(self):
		print('ok')


class PopupRestart(ModalView):
	yes_button = ObjectProperty()
		

class AtomiaApp(App):
	my_time = NumericProperty()
	
	def build(self):
		Clock.schedule_interval(self.my_clock, 1 / 60.)
		root = Start()
		return root
		
	def my_clock(self, dt):
		self.my_time = time()
		
if __name__ == '__main__':
	AtomiaApp().run()
		
