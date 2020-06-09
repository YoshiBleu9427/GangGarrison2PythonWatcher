from misseter.imagepool import Imagepool

class Engine():

	def __init__(self, pygame):
		self.pygame = pygame
		self.imagepool = Imagepool()
		self.imagepool.init(self.pygame)
		self.fps = 30

		self.entities = []
		self.entities_by_class = {}
		self.to_destroy = []
		self.to_create = []
		self.menu = None
		self.overlays = {}

	def start_menu(self, menu_class, *args, **kwargs):
		self.menu = menu_class(self, *args, **kwargs)

	def exit_menu(self):
		self.menu = None

	def add_overlay(self, overlay_class, *args, **kwargs):
		self.overlays[overlay_class] = overlay_class(self, *args, **kwargs)

	def remove_overlay(self, overlay_class):
		del self.overlays[overlay_class]

	def new(self, entity_class, *args, **kwargs):
		new_ent = entity_class(self, *args, **kwargs)
		self.to_create.append(new_ent)
		return new_ent

	def delete(self, entity, immediately=False):
		self.to_destroy.append(entity)
		if immediately:
			entity.on_destroy()
			entity.disabled = True
		return entity

	def tick(self):
		for entity in self.to_create:
			entity.on_create()
			self.entities.append(entity)
			entclass = entity.__class__
			if entclass not in self.entities_by_class:
				self.entities_by_class[entclass] = []
			self.entities_by_class[entclass].append(entity)
		self.to_create.clear()

		if self.menu is not None:
			self.menu.tick()
		else:
			for entity in self.entities:
				if entity.disabled:
					continue
				entity.move()
				if entity.solid:
					for other in self.entities:
						if other.disabled:
							continue
						if not other.solid:
							continue
						if other == entity:
							continue
						if entity.intersects(other):
							entity.on_collide(other)
				entity.step()

		for entity in self.to_destroy:
			if not entity.disabled:
				entity.on_destroy()
			if entity in self.entities:
				self.entities.remove(entity)
			if entity in self.entities_by_class[entity.__class__]:
				self.entities_by_class[entity.__class__].remove(entity)
		self.to_destroy.clear()

	def draw(self, screen):
		if self.menu is not None:
			self.menu.draw(screen)
		else:
			for entity_set in self.entities_by_class.values():
				for entity in entity_set:
					entity.draw(screen)
			for overlay in self.overlays.values():
				overlay.draw(screen)
