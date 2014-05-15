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


#Il est necessaire de mettre **kwargs pour pouvoir imbriquer PuzzleGame dans la classe Principal, sinon error
class PuzzleGame(FloatLayout):
	
	atom_size = (0,0)
	interval = 0
	cols_max = 0
	
	def __init__(self, **kwargs):
		super(PuzzleGame, self).__init__(**kwargs)
		
		#Vu que cette classe est imbrique dans la principal il faut declare la position ici non dans le kv
		# self.pos = (Window.width / 20, Window.height / 20)
		#Pour pouvoir tracer un canvas bordure propre
		
		self.pos = (Window.height / 11, Window.height / 11)
		
		self.atoms_list = ['azote', 'carbone', 'chlore', 'hydrogene', 'oxygene', 'sodium']
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
		# print(self.cols_max)
			
		self.atom_size = (Window.height / 10, Window.height / 10)
		# self.interval = ((Window.width / 100) / 2) / 4
		self.interval = 1
		atom_pos = self.pos
		self.widgets_list = []
		self.widgets_list_clone = []
		self.user_combinaison = {}
		self.current_touch_widgets = []
		self.user_combinaison_clone = {}
		counter = 0
		#On defini la taille du widget qui contient le puzzle
		# self.size_hint = (None, None)
		# self.width = (self.atom_size[0] + self.interval) * self.cols_max
		# self.height = (self.atom_size[0] + self.interval) * self.rows_max
		# self.add_widget(restart_button)
		#On place le contour du puzzle
		# contour = Image(source='graphics/bordures/contour.png',allow_stretch=True, keep_ratio=False, pos=(0,0), size_hint=(None, None), size=(self.width + (self.x * 2),self.height + (self.y * 2)))
		# self.add_widget(contour)
		# print("SIZE IMAGE", contour.size, contour.pos)
		
		for i in rows_list:
			#decalage en x si le puzzle a des colonnes de taille differentes
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
				# print('KLZJHJZHKJZHJZHJZ', atom_pos, self.interval)
				counter += 1
				
			atom_pos = (self.x, atom_pos[1] + self.atom_size[1] + self.interval)
			counter = 0
			
		'''with self.canvas:
			# 0.2 de moins que la position du Floatlayout
			c_x = (Window.width * (0.8*100)) / 100
			c_y = (Window.height * (0.8*100)) / 100
			c_wh = (self.atom_size[0] * self.cols_max) + ((self.cols_max -1) * self.interval)
			c_ht = (self.atom_size[1] * rows_max)  + ((rows_max -1) * self.interval)
			Line(rectangle=(self.x, self.y, c_wh, c_ht))'''
			
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
				#On enregistre avec le canvas modifie
				self.current_touch_widgets.append(i)
				break
				
	def on_touch_move(self, touch):
		for i in self.widgets_list_clone:
			#si on est deja passe sur le widget (i) on stop la.
			if i in self.current_touch_widgets:
				break
			elif i.collide_point(touch.x, touch.y):
				pos_i = ([i.x, i.y])
				if pos_i == ([(self.current_touch_widgets[-1].x - i.size[0] - self.interval), (self.current_touch_widgets[-1].y)]):
					# print((self.current_touch_widgets[-1].x - i.size[0] - self.interval) , (self.current_touch_widgets[-1].y), pos_i)
					print('ca marche!!!!!!!!!!!!!')
					# print(self.current_touch_widgets[-1].x, i.size[0], i.size[1], self.interval, self.current_touch_widgets[-1].y)
				elif pos_i == ([(self.current_touch_widgets[-1].x + i.size[0] + self.interval), (self.current_touch_widgets[-1].y)]):
					# print((self.current_touch_widgets[-1].x + i.size[0] + self.interval), (self.current_touch_widgets[-1].y), pos_i)
					# print(self.current_touch_widgets[-1].x, i.size[0], i.size[1], self.interval, self.current_touch_widgets[-1].y)
					print('ca marche!!!!!!!!!!!!!')
				elif pos_i == ([self.current_touch_widgets[-1].x, (self.current_touch_widgets[-1].y + i.size[1] + self.interval)]):
					# print((self.current_touch_widgets[-1].x), (self.current_touch_widgets[-1].y + i.size[0] + self.interval), pos_i)
					# print(self.current_touch_widgets[-1].x, i.size[0], i.size[1], self.interval, self.current_touch_widgets[-1].y)
					print('ca marche!!!!!!!!!!!!!')
				elif pos_i == ([self.current_touch_widgets[-1].x, (self.current_touch_widgets[-1].y - i.size[1] - self.interval)]): 
					# print((self.current_touch_widgets[-1].x), (self.current_touch_widgets[-1].y - i.size[0] - self.interval), pos_i)
					# print(self.current_touch_widgets[-1].x, i.size[0], i.size[1], self.interval, self.current_touch_widgets[-1].y)
					print('ca marche!!!!!!!!!!!!!')
				else:
					# print((self.current_touch_widgets[-1].x - i.size[0] - self.interval), (self.current_touch_widgets[-1].y))
					# print((self.current_touch_widgets[-1].x))
					# print((self.current_touch_widgets[-1].x + i.size[0] + self.interval), (self.current_touch_widgets[-1].y))
					# print((self.current_touch_widgets[-1].x), (self.current_touch_widgets[-1].y + i.size[0] + self.interval))
					# print((self.current_touch_widgets[-1].x), (self.current_touch_widgets[-1].y - i.size[0] - self.interval))
					# print(pos_i, 'pos', 'ca marche pas')
					# print(self.current_touch_widgets[-1].x, i.size[0], i.size[1], self.interval, self.current_touch_widgets[-1].y)
					break

				#sinon on continue
				self.user_combinaison_clone = dict(self.user_combinaison)
				if i.source[15:-4] in self.user_combinaison.keys():
					self.user_combinaison_clone[i.source[15:-4]] += 1
				else:
					self.user_combinaison_clone[i.source[15:-4]] = 1
				# print('clone', self.user_combinaison_clone, 'pas clone', self.user_combinaison)
				
				# print(data)
			
				for combinaison in self.combinaisons_list:
					pf = self.user_combinaison_clone.keys()
					pf.sort()
					counter = 0
					data = 0
					# print('my combi', pf, 'combi', combinaison.keys())
					for element in pf:
						if element in combinaison:
							counter +=1
					if counter == len(pf):
						# print('ca passe')
						for atome_touche in pf:
							# print(self.user_combinaison_clone[atome_touche], combinaison[atome_touche])
							if self.user_combinaison_clone[atome_touche] <= combinaison[atome_touche]:
								('atome + nombre match')
								data += 1
							# print('TAILLE DE MES COMBINAISONS', len(self.user_combinaison_clone), 'DATA', data)
							if data == len(self.user_combinaison_clone):
								# print('les atomes touches sont OK')
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
		parent = self.parent
		counter = 0
		key_user_combinaison = self.user_combinaison.keys()
		key_user_combinaison.sort()
		for combinaison in self.combinaisons_list:
			#Il est necessaire de faire un sort sur combinaison pour que ce soit dans le meme ordre
			key_combinaison = combinaison.keys()
			key_combinaison.sort()
			print(key_user_combinaison, key_combinaison, combinaison, 'a et combi keys')
			counter = 0
			val = 0
			if key_user_combinaison == key_combinaison:
				name_combinaison = str()
				for element in key_user_combinaison:
					#on reforme le nom qui correspond au nom de l'image du tableau
					if element == 'sodium':
						symbole = 'na'
					elif element == 'azote':
						symbole = 'n'
					elif element == 'clhore':
						symbole = 'cl'
					else:
						symbole = element[:1]
					name_combinaison += ''.join(symbole) + ''.join(str(self.user_combinaison[element]))
					print('NAME SOURCE', name_combinaison, symbole)
					val += 1
					print('c quoi ce truc,', self.user_combinaison[element], combinaison[element]) 
					if self.user_combinaison[element] == combinaison[element]:
						print('final', key_user_combinaison, key_combinaison)
						counter += 1
						print(counter, val, element, len(key_user_combinaison))
						
						if counter == len(key_user_combinaison):
							self.remove_widgets_list = []
							self.x_list = []
							#Liste qui contient les points qui s'affiche, qui doivent etre efface
							self.erase_points_list = []
							#On supprime les widgets qui ont formes une combinaison
							for wid in self.current_touch_widgets:			
								#Si jamais il y a deux meme pos dans la liste
								# if wid.pos in self.remove_widgets_list or wid.pos == self.remove_widgets_list:
									# pass
								self.remove_widgets_list.append(wid.pos)
								self.remove_widget(wid)
								self.x_list.append(wid.x)
								#Mise a jour du score
								parent.update_score(2)
								#creation du widget point + animation + schedule pour effacer
								wid_point = Label(text="+2", font_size='20sp', size_hint=(None, None), pos=wid.pos)
								self.add_widget(wid_point)
								self.erase_points_list.append(wid_point)
								anim = Animation(y=wid.y+10, d=1)
								anim.start(wid_point)
								Clock.schedule_once(self.erase_points, 1)
								#Combinaisons
								for clone_combi in self.combinaisons_list_clone:
									if combinaison == clone_combi:
										#Mise a jour du nombre de combinaison trouvees
										#Modification du canvas de la formule trouvee
										self.combinaisons_list_clone.remove(combinaison)
										
										parent.draw_board(name_combinaison)
								
							#On les supprime egalement de la liste qui contient les pieces du puzzle
							self.widgets_list = list(self.widgets_list_clone)
							#On deplace les pieces vers le bas
							self.move_puzzle_pieces()
							# self.move_puzzle_pieces()

							#Il y a une seule combinaison gagnante a moins d'integrer des joker pour enchainer sur d'autre formule d'atomes
							break
						
						elif val == len(key_user_combinaison):
							print('en fait ca match pas', val, counter)
							val = 0
							counter = 0
						
					elif val == len(key_user_combinaison):
						print('en fait ca match pas', val, counter)
						val = 0
						counter = 0
					
				if counter == len(key_user_combinaison):
					break
		
		if counter == 0:
			#si la combinaison n'est pas bonne, on supprime les canvas dessine
			for touch_widget in self.current_touch_widgets:
				with touch_widget.canvas:
					Color(0, 0, 0)
					Line(rectangle=(touch_widget.x, touch_widget.y, touch_widget.width, touch_widget.height))

		
		self.user_combinaison = {}
		self.current_touch_widgets = []
		self.widgets_list_clone = list(self.widgets_list)
		print('leve le doligt', 'clone',len(self.widgets_list_clone), 'pas clone', len(self.widgets_list))
		
	def move_puzzle_pieces(self):
		move_widgets_list = []	#Liste qui contiendra les widgets qui doivent descendre
		counter = 0
		for position in self.remove_widgets_list:
			for piece in self.widgets_list:
				if piece.pos[0] == position[0] and piece.pos[1] > position[1]:
					#Si le x de la piece est egale au x de la piece supprime
					# et que le y de la piece est superieur au y de la piece supprime
					#c'est que les pieces sont dans la meme colonnes et qu'elles sont au dessus de celle supprime
					# print('on bouge cette piece', piece.pos[0], position[0], piece.pos[1], position[1])
					move_widgets_list.append(piece) #On enregistre les pieces qui descendent
					

		for piece in move_widgets_list:
			# print('position piece avant anim', piece.pos)
			#anim = Animation(pos=(piece.x, piece.y - piece.size[1] - self.interval), d=0.5)
			#anim.start(piece)
			piece.pos = (piece.x, piece.y - piece.size[1] - self.interval)
			with piece.canvas:
				Color(0, 0, 0)
				Line(rectangle=(piece.x, piece.y, piece.width, piece.height))
			# print('position piece apres anim', piece.pos)
		
		#Boucle qui permet de verifier que les positions modifier dans la boucle au dessus
		#sont bien modifie egalement dans la widgets_list principale
		# for piece in move_widgets_list:
			# for elem in self.widgets_list:
				# if elem == piece:
					# print('tout est OK', piece.pos, elem.pos)
						
			
		values_x = []
		#Nombre de fois ou x a la meme valeur sur 6 colonne maxi etant donne que 6 est le maximum d'atome pour former une combinaison
		#La combinaison serait donc de la forme de 6 atomes a l'horizontal donc 6 colonnes 6 valeurs de x differentes
		
		for x in self.x_list:
			# print('liste des x', self.x_list)
			if counter >= 1:
				if x == old_x:
					values_x[(counter-1)][str(old_x)] += 1
				else:
					values_x.append({str(x):1})
					counter += 1
			else:
				values_x.append({str(x):1})
				counter = 1
			# print('liste des dicos', values_x)
			#On cherche a savoir si les pieces supprimees sont dans la meme colonne ou pas
			#pour agir differemment si elles sont dans des colonnes differentes
			old_x = x

		self.coord_y = self.y + (self.rows_max * self.atom_size[1]) + (self.rows_max * self.interval)
		#coordonnee y de la piece la plus haute
		for dico in values_x:
			#On recupere le nombre de fois que la valeur de dico.keys apparait
			nb = dico.values()
			nb_fin = int(nb[0])
			counter = 0
			nb_fin_size = nb_fin
			while counter != nb_fin:
				# print('counter nb fin', counter, nb_fin)
				#On recupere la valeur de dico.keys
				cord_x = dico.keys()
				self.coord_x = int(cord_x[0])
				# print(self.coord_x, 'coord_x', self.coord_y, 'coord_y')
				#On ajoute un atome qui apparait tout en haut
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
				t=0
				# print(self.img.y, 'coord y', 'coord y a atteindre', self.coord_y - (self.atom_size[1] * nb_fin_size) - (self.interval * nb_fin_interval))
				self.img.y -= (self.atom_size[1] + self.interval) * nb_fin_size
				print('after', self.img.y)
				counter += 1
			
				nb_fin_size -= 1
				with self.img.canvas:
					Color(0, 0, 0)
					Line(rectangle=(self.img.x, self.img.y, self.img.width, self.img.height))
				self.widgets_list.append(self.img)
				
	#Clock_schedule_once qui execute la fonction qui efface les points affiche, qui sont contenu dans une liste
	def erase_points(self, dt):
		for wid_point in self.erase_points_list:
			self.remove_widget(wid_point)