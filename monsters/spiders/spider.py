from monsters.monster import Monster

#Venom on hit
#Can spin web that slows people
class Spider(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1110, name="Spider"): #1210 is also working render tag
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.character.experience_given = 10
        self.description = "These black and white spiders, each the size of a small dog, are swift and deadly predators of the forest. With their distinctive striped patterns, they move with alarming speed, darting through the underbrush and leaping onto unsuspecting prey. Their agile legs and sharp mandibles allow them to navigate any terrain, while their ability to weave intricate webs on tiles makes them formidable hunters and trappers. A single bite from a Rift Spider delivers potent poison, weakening and paralyzing its victims. Beware their sudden, silent approach and the venomous sting that follows, for these spiders are relentless and deadly in their pursuit."
        self.traits["spider"] = True
        self.character.change_action_cost("move", 50)
