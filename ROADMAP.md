# GUI

- handle window resize

## HUD

- small screen &rarr; display only field icon
- display aliments

## Title screen

- New game
- Continue game
- Settings

## Preferences dialog

Description of each setting value.

# Player

- mage: casts magic bullets
- warrior: shockwave attack

# Enemies

## Minions

Spawn ${difficulty} per room except player start.
A\* hunt once player within enemy's visible set until not visible **AND** far away (threshold distance).

- blob: moves 1 in 2 turns, contact damage
- ninja: moves every turn, contact damage
- mage: moves 1 in 3 turns, no contact damage, casts magic bullet

## Boss

‗†‗
‖∫‖
╚═╝

Takes up several map tiles.
One boss in exit room. (exit locked until defeated)
Moves 1 in 2 turns, shockwave paralysis.

# Coop Mode

La carte est sur le serveur (joueur hôte) envoyée au client (joueur invité).

Une ligne d'ITH par joueur.

# General TODO

master: fix ITH
2D GUI in separate branch
