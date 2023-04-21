from states.space import Space

class Infinity(Space):
    def __init__(self, game):
        Space.__init__(self, game)
        
        
    def update(self, delta_time, action):
        Space.update(self, delta_time, action)
        
        
    
    def render(self, display):
        Space.render(self, display)