import tcod as libtcod

from game_messages import Message

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp # the xp it's worth, not how much it has

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            msg = Message(f"{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points.", libtcod.white)
            results.append({'message': msg})
            results.extend(target.fighter.take_damage(damage))
        else:
            msg = Message(f"{self.owner.name.capitalize()} attacks {target.name} but does no damage.", libtcod.white)
            results.append({'message': msg})

        return results
