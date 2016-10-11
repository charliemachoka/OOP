import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys



####FIXED GIRL SO SHE CAN STEAL ##################################################3
#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

GEM_COUNT = []

    # if len(GEM_COUNT) == (len(player.inventory) + len(newgirl.inventory)):
    #     game_over()

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True
   
class Character(GameElement):
    IMAGE = "Princess"
    can_steal = True
    opponent = None
    SOLID = True
  
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []



    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y -1)
        elif direction == "down":
            return (self.x, self.y +1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None

        if symbol == key.UP:
            self.move_character("up")
        elif symbol ==  key.DOWN:
            self.move_character("down")
        elif symbol == key.LEFT:
            self.move_character("left")
        elif symbol == key.RIGHT:
            self.move_character("right")

        # INTERACTION HAS HAPPENED

        
        # self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))
        
     


    def move_character(self, direction):
        next_location = self.next_pos(direction)
        if next_location:
            next_x = next_location[0]
            next_y = next_location[1]

            if next_x < 0 or next_y < 0 or next_x == 8 or next_y == 8:
                self.board.draw_msg("That's out of bounds! Can't go there!")
                return None

            existing_el = self.board.get_el(next_x, next_y)
            # print existing_el

            self.display_inventory()

            # if existing_el and isinstance(existing_el, Character):
               
            #     print "This element exists"   

            if existing_el:
                existing_el.interact(self)


            if existing_el and existing_el.SOLID:
                pass
 
            elif existing_el is None or not existing_el.SOLID:
                self.board.del_el(self.x, self.y)
                self.board.set_el(next_x, next_y, self)

    def interact(self, player):
        print "interact", self.can_steal, self.opponent.inventory
        if self.can_steal == True and len(self.opponent.inventory) > 0:
            gem = self.opponent.inventory.pop()
            self.inventory.append(gem)

            GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(self.inventory)))
        else: print GAME_BOARD.draw_msg("Try to get a gem!")
           
        if len(GEM_COUNT) == (len(self.opponent.inventory) + len(self.inventory)): # NEED to ADD CAT INVENTORY SOMEHOW
            self.game_over()


    def display_inventory(self):
        print "%s has %d" % (self.IMAGE, len(self.inventory))

    def game_over(self):
        if len(self.inventory) > len(self.opponent.inventory):
            print "Congrats %s" % self.IMAGE
        else:
            print "Congrats %s" % self.opponent.IMAGE

      

class NewCat(GameElement):
    IMAGE = 'Cat'
    SOLID = True


    def __init__(self):
        self.inventory = []

    def interact(self, player):
        print "You found a cat"
        # update players position when it interacts with cat                                               
        if len(player.inventory) > 0:
            gem = player.inventory.pop()
            self.inventory.append(gem)

            GAME_BOARD.draw_msg("The CAT just acquired a gem! The cat have %d items! CATITUDE"%(len(self.inventory)))
        else:
            GAME_BOARD.draw_msg("Ouch! The cat scratched you. Go away!")

        


class NewFriend (Character):
    IMAGE = 'Girl'

    def display_inventory(self):
        print "%s has %d" % (self.IMAGE, len(self.inventory))

    def keyboard_handler(self, symbol, modifier):
        direction = None

        if symbol == key.E:
            self.move_character("up")
        elif symbol ==  key.D:
            self.move_character("down")
        elif symbol == key.S:
            self.move_character("left")
        elif symbol == key.F:
            self.move_character("right")
        

        # self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))



class CollectibleGems(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))\

    def __init__(self):
        GEM_COUNT.append(self)

class OrangeGem(CollectibleGems):
    IMAGE = "OrangeGem"
    SOLID = True

    def interact(self, player):
        player.board.del_el(player.x, player.y)
        player.board.set_el(0, 0, player)

    def __init__(self):
        return None


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    total_gems_collected = []

    gem = CollectibleGems()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3,1, gem)

    orangegem = OrangeGem()
    GAME_BOARD.register(orangegem)
    GAME_BOARD.set_el(4,4, orangegem)

    newgirl = NewFriend()
    newgirl.name = "Girl"
    GAME_BOARD.register(newgirl)
    GAME_BOARD.set_el(3,3, newgirl)

    player = Character()
    player.name = "Princess"
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2,2,player)
    print player

    player.opponent = newgirl
    newgirl.opponent = player

    thecat = NewCat()
    GAME_BOARD.register(thecat)
    GAME_BOARD.set_el(7,5, thecat)

    gem2 = CollectibleGems()
    gem2.IMAGE = 'GreenGem'
    GAME_BOARD.register(gem2)
    GAME_BOARD.set_el(6,6, gem2)

    gem3 = CollectibleGems()
    gem3.IMAGE  = 'OrangeGem'
    GAME_BOARD.register(gem3)
    GAME_BOARD.set_el(7,1, gem3)

    gem4 = CollectibleGems()
    gem4.IMAGE  = 'OrangeGem'
    GAME_BOARD.register(gem4)
    GAME_BOARD.set_el(7,3, gem4)

    gem5 = CollectibleGems()
    gem5.IMAGE  = 'GreenGem'
    GAME_BOARD.register(gem5)
    GAME_BOARD.set_el(2,6, gem5)

    gem6 = CollectibleGems()
    gem6.IMAGE  = 'BlueGem'
    GAME_BOARD.register(gem6)
    GAME_BOARD.set_el(1,5, gem6)

    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
        (2,3)
    ]

    rocks = []

    for position in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(position[0], position[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    print len(GEM_COUNT)

    rocks[-1].SOLID = False

    GAME_BOARD.draw_msg("This game is wicked awesome.")


