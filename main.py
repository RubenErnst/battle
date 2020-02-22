from classes.game import Person, BColors
from classes.magic import Spell
from classes.inventory import Item

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 12, 120, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
megaelixir = Item("Mega Elixir", "elixir", "Fully restores HP/MP of all party members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 points of damage", 500)

# Instantiate People
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]

player = Person(460, 65, 60, 34, player_spells, player_items)
enemy = Person(1200, 65, 45, 25, [], [])

running = True
print(BColors.FAIL + BColors.BOLD + "AN ENEMY ATTACKS!" + BColors.ENDC)

while running:
    print("===============================")
    player.choose_action()
    choice = input("Choose action: ")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for", dmg, "points of damage.")
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Choose magic: ")) - 1

        if magic_choice == -1:
            continue

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(BColors.FAIL + "\n Not enough MP" + BColors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(BColors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + BColors.ENDC)
        elif spell.type == "black":
            enemy.take_damage(magic_dmg)
            print(BColors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage." + BColors.ENDC)
    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose item: ")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]["item"]

        if player.items[item_choice]["quantity"] == 0:
            print(BColors.FAIL + "None left..." + BColors.ENDC)
            continue
            
        player.items[item_choice]["quantity"] -= 1

        if item.type == "potion":
            player.heal(item.prop)
            print(BColors.OKGREEN + "\n" + item.name + " heals for", item.prop, "HP" + BColors.ENDC)
        elif item.type == "elixir":
            player.hp = player.max_hp
            player.mp = player.max_mp
            print(BColors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + BColors.ENDC)
        elif item.type == "attack":
            enemy.take_damage(item.prop)
            print(BColors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage." + BColors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg, "points of damage.")

    print("-----------------------------")
    print("Enemy HP:", BColors.FAIL, str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()), BColors.ENDC)
    print("Your HP:", BColors.OKGREEN, str(player.get_hp()) + "/" + str(player.get_max_hp()), BColors.ENDC)
    print("Your MP:", BColors.OKBLUE, str(player.get_mp()) + "/" + str(player.get_max_mp()), BColors.ENDC)

    if enemy.get_hp() == 0:
        print(BColors.OKGREEN + "You win!" + BColors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(BColors.FAIL + "Your enemy has defeated you!" + BColors.ENDC)
        running = False
