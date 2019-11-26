# GUI

## HUD

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

- rat: moves at random 1 out of 2 turns, contact damage
- orc: runs towards the player in a straight line
- knight: blocks when fired at (shield but not move)
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

2D GUI in separate branch `sdl`
