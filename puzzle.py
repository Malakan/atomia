from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty
from kivy.core.window import Window
from kivy.graphics import Rectangle, Line, Color
from random import randint

class PuzzleGame(FloatLayout):
	score = NumericProperty()
	nb_combi_find = StringProperty()
	atom_size = (0,0)
	interval = 0
	cols_max = 0
	
	def __init__(self, **kwargs):
		super(PuzzleGame, self).__init__(**kwargs)
		
		self.score = int()
		
		self.pos = (Window.height / 11, Window.height / 11)
		
		self.atoms_list = ['azote', 'carbone', 'hydrogene', 'oxygene', 'sodium']
		au = ['bore', 'carbone', 'azote', 'oxygene', 'fluor', 'neon', 'sodium', 'magnesium',
			'aluminium', 'silicium', 'phosphore', 'soufre', 'chlore', 'argon', 'potassium', 'calcium', 'titane', 'vanadium', 'manganese',
			'fer', 'cobalt', 'nickel', 'cuivre', 'zinc', 'brome', 'argent', 'etain', 'iode', 'xenon', 'tungstene', 'platine',
			'or', 'mercure']
			
		self.combinaisons_list = [{'hydrogene':2}, {'oxygene':2}, {'azote':2}, {'hydrogene':2, 'oxygene':1}, {'carbone':1, 'oxygene':2},
			{'chlore':1, 'sodium':1}, {'hydrogene':2, 'oxygene':2}, {'carbone':2, 'hydrogene':2}, {'hydrogene':1, 'carbone':1, 'azote':1}, {'azote':1, 'hydrogene':3},
			{'carbone':1, 'hydrogene':4}, {'carbone':2, 'hydrogene':6}, {'carbone':3, 'hydrogene':8}, {'carbone':4, 'hydrogene':10}, {'carbone':5, 'hydrogene':12},
			{'carbone':6, 'hydrogene':14}, {'carbone':7, 'hydrogene':16}, {'carbone':8, 'hydrogene':18}, {'carbone':9, 'hydrogene':20},
			{'carbone':10, 'hydrogene':22}, {'carbone':2, 'hydrogene':6, 'oxygene':1}, {'carbone':10, 'hydrogene':16, 'oxygene':1},
			{'carbone':6, 'hydrogene':6}, {'carbone':2, 'hydrogene':4, 'oxygene':2}]
		
		self.combinaisons_list_clone = [{'hydrogene':2}, {'oxygene':2}, {'azote':2}, {'hydrogene':2, 'oxygene':1}, {'carbone':1, 'oxygene':2},
			{'chlore':1, 'sodium':1}, {'hydrogene':2, 'oxygene':2}, {'carbone':2, 'hydrogene':2}, {'hydrogene':1, 'carbone':1, 'azote':1}, {'azote':1, 'hydrogene':3},
			{'carbone':1, 'hydrogene':4}, {'carbone':2, 'hydrogene':6}, {'carbone':3, 'hydrogene':8}, {'carbone':4, 'hydrogene':10}, {'carbone':5, 'hydrogene':12},
			{'carbone':6, 'hydrogene':14}, {'carbone':7, 'hydrogene':16}, {'carbone':8, 'hydrogene':18}, {'carbone':9, 'hydrogene':20},
			{'carbone':10, 'hydrogene':22}, {'carbone':2, 'hydrogene':6, 'oxygene':1}, {'carbone':10, 'hydrogene':16, 'oxygene':1},
			{'carbone':6, 'hydrogene':6}, {'carbone':2, 'hydrogene':4, 'oxygene':2}]
		
		rows_list = [8,8,8,8,8,8,8,8]
		self.rows_max = len(rows_list)
		self.cols_max = 0
		
		for i in rows_list:
			if i > self.cols_max:
				self.cols_max = i
		
		self.number_find = 0
		self.nb_combi_find = str(self.number_find) + ' / ' + str(len(self.combinaisons_list))
			
		self.atom_size = (Window.height / 10, Window.height / 10)
		self.interval = 1
		atom_pos = self.pos
		self.widgets_list = []
		self.widgets_list_clone = []
		self.user_combinaison = {}
		self.current_touch_widgets = []
		self.user_combinaison_clone = {}
		counter = 0
		
		for i in rows_list:
			decalage = ((self.cols_max - i) / 2) * (self.atom_size[0] + self.interval)
			atom_pos = (atom_pos[0] + decalage, atom_pos[1])
			
			while counter != i:
				rand_number = randint(0, len(self.atoms_list) -1)
				image_path = 'graphics/atoms/' + self.atoms_list[rand_number] + '.png'
				img = Image(source=image_path, pos=atom_pos, size_hint=(None, None), size=self.atom_size)
				self.add_widget(img)
				self.widgets_list.append(img)
				self.widgets_list_clone.append(img)

				with img.canvas:
					Color(0, 0, 0)
					Line(rectangle=(img.x, img.y, img.width, img.height))
				
				atom_pos = (atom_pos[0] + self.atom_size[0] + self.interval, atom_pos[1])
				counter += 1
				
			atom_pos = (self.x, atom_pos[1] + self.atom_size[1] + self.interval)
			counter = 0
			
	def on_touch_down(self, touch):
		for i in self.widgets_list:
			if i in self.current_touch_widgets:
				break
			#print('self.widgets_list_clone', len(self.widgets_list_clone), len(self.widgets_list)) 
			if i.collide_point(touch.x, touch.y):
				self.user_combinaison[i.source[15:-4]] = 1
				self.widgets_list_clone.remove(i)
				with i.canvas:
					Color(0.6, 0.8, 0.5)
					Line(rectangle=(i.x, i.y, i.width, i.height))
				self.current_touch_widgets.append(i)
				break
				
	def on_touch_move(self, touch):
		for i in self.widgets_list_clone:
			if i in self.current_touch_widgets:
				break
			elif i.collide_point(touch.x, touch.y):
				pos_i = ([i.x, i.y])
				if pos_i == ([(self.current_touch_widgets[-1].x - i.size[0] - self.interval), (self.current_touch_widgets[-1].y)]):
					pass
				elif pos_i == ([(self.current_touch_widgets[-1].x + i.size[0] + self.interval), (self.current_touch_widgets[-1].y)]):
					pass
				elif pos_i == ([self.current_touch_widgets[-1].x, (self.current_touch_widgets[-1].y + i.size[1] + self.interval)]):
					pass
				elif pos_i == ([self.current_touch_widgets[-1].x, (self.current_touch_widgets[-1].y - i.size[1] - self.interval)]): 
					pass
				else:
					break

				#sinon on continue
				self.user_combinaison_clone = dict(self.user_combinaison)
				if i.source[15:-4] in self.user_combinaison.keys():
					self.user_combinaison_clone[i.source[15:-4]] += 1
				else:
					self.user_combinaison_clone[i.source[15:-4]] = 1
				# print('clone', self.user_combinaison_clone, 'pas clone', self.user_combinaison)
				
				for combinaison in self.combinaisons_list:
					pf = self.user_combinaison_clone.keys()
					pf.sort()
					counter = 0
					data = 0
					for element in pf:
						if element in combinaison:
							counter +=1
					if counter == len(pf):
						for atome_touche in pf:
							# print(self.user_combinaison_clone[atome_touche], combinaison[atome_touche])
							if self.user_combinaison_clone[atome_touche] <= combinaison[atome_touche]:
								('atome + nombre match')
								data += 1
							if data == len(self.user_combinaison_clone):
								self.widgets_list_clone.remove(i)
								with i.canvas:
									Color(0.6, 0.8, 0.5)
									Line(rectangle=(i.x, i.y, i.width, i.height))
									self.current_touch_widgets.append(i)
									
								if i.source[15:-4] in self.user_combinaison.keys():
									self.user_combinaison[i.source[15:-4]] += 1
								else:
									self.user_combinaison[i.source[15:-4]] = 1
								
						if data == len(self.user_combinaison_clone):
							break
							
					elif data == len(self.user_combinaison_clone):
							break
					else:
						print('match pas')
						
				if data == len(self.user_combinaison_clone):
					break
					
	def on_touch_up(self, touch):
		counter = 0
		a = self.user_combinaison.keys()
		a.sort()
		for combinaison in self.combinaisons_list:
			if a == combinaison.keys():
				counter = 0
				val = 0
				for element in a:
					val += 1
					if self.user_combinaison[element] == combinaison[element]:
						counter += 1
						
						if counter == len(a):
							self.remove_widgets_list = []
							self.x_list = []
							self.erase_points_list = []
							for wid in self.current_touch_widgets:			
								self.remove_widgets_list.append(wid.pos)
								self.remove_widget(wid)
								self.x_list.append(wid.x)
								
								self.score += 2
								wid_point = Label(text="+2", font_size='20sp', size_hint=(None, None), pos=wid.pos)
								self.add_widget(wid_point)
								self.erase_points_list.append(wid_point)
								anim = Animation(y=wid.y+10, d=1)
								anim.start(wid_point)
								Clock.schedule_once(self.erase_points, 1)
								#Combinaisons
								for clone_combi in self.combinaisons_list_clone:
									if combinaison == clone_combi:
										self.combinaisons_list_clone.remove(combinaison)
										self.number_find += 1
										self.nb_combi_find = str(self.number_find) + ' / ' + str(len(self.combinaisons_list))
								
								print('on augmente le score', self.score)
							self.widgets_list = list(self.widgets_list_clone)
							self.move_puzzle_pieces()

							break
						elif val == len(a):
							val = 0
							counter = 0
					
				if counter == len(a):
					break
		
		if counter == 0:
			for touch_widget in self.current_touch_widgets:
				with touch_widget.canvas:
					Color(0, 0, 0)
					Line(rectangle=(touch_widget.x, touch_widget.y, touch_widget.width, touch_widget.height))

		
		self.user_combinaison = {}
		self.current_touch_widgets = []
		self.widgets_list_clone = list(self.widgets_list)
		print('leve le doligt', 'clone',len(self.widgets_list_clone), 'pas clone', len(self.widgets_list))
		
	def move_puzzle_pieces(self):
		move_widgets_list = []	
		counter = 0
		for position in self.remove_widgets_list:
			for piece in self.widgets_list:
				if piece.pos[0] == position[0] and piece.pos[1] > position[1]:
					move_widgets_list.append(piece) 
					

		for piece in move_widgets_list:
			
			piece.pos = (piece.x, piece.y - piece.size[1] - self.interval)
			with piece.canvas:
				Color(0, 0, 0)
				Line(rectangle=(piece.x, piece.y, piece.width, piece.height))

						
			
		values_x = []

		for x in self.x_list:

			if counter >= 1:
				if x == old_x:
					values_x[(counter-1)][str(old_x)] += 1
				else:
					values_x.append({str(x):1})
					counter += 1
			else:
				values_x.append({str(x):1})
				counter = 1
	
			old_x = x

		self.coord_y = self.y + (self.rows_max * self.atom_size[1]) + (self.rows_max * self.interval)
		for dico in values_x:
			nb = dico.values()
			nb_fin = int(nb[0])
			counter = 0
			nb_fin_size = nb_fin
			while counter != nb_fin:
				cord_x = dico.keys()
				self.coord_x = int(cord_x[0])
				rand_number = randint(0, len(self.atoms_list) -1)
				image_path = 'graphics/atoms/' + self.atoms_list[rand_number] + '.png'
				self.img = Image(source=image_path, pos=(self.coord_x, self.coord_y), size_hint=(None, None), size=piece.size)
				self.add_widget(self.img)
				if nb_fin == 2:
					nb_fin_interval = 1
				else:
					nb_fin_interval = nb_fin - 2
				if nb_fin_size <= 0:
					nb_fin_size = 1

				self.img.y -= (self.atom_size[1] + self.interval) * nb_fin_size
				print('after', self.img.y)
				counter += 1
			
				nb_fin_size -= 1
				with self.img.canvas:
					Color(0, 0, 0)
					Line(rectangle=(self.img.x, self.img.y, self.img.width, self.img.height))
				self.widgets_list.append(self.img)
				
	def erase_points(self, dt):
		for wid_point in self.erase_points_list:
			self.remove_widget(wid_point)
