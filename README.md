# Q-Learning + World of Tanks

Yale CPSC 474 (Computational Intelligence for Games) Final Project. Using Q-Learning to build an agent for a simplified World of Tanks encounter.

## What is World of Tanks?

World of Tanks is a real-time MMO where players battle against each other in teams of tanks. The game is incredibly complex in terms of state-space, but the most common game mode is “Random Battles”, where a player chooses a tank, and they are assigned to a random team on a random map, filled with similar tanks. The objective is to win by destroying the entire other team, or by capturing their base or a shared capture zone in the middle.

Even before starting the match, the state space for a battle is enormous - 2 dozen or so maps, 3 different modes, over 600 tanks, hundreds of setups per tank, etc. Once in the match, the configuration is done, and the complexities of real-time player-vs-player action begins. Maps are commonly 1 km x 1km in size, and each tank can be moved by matters of inches in every direction. The tank’s gun is aimable in whatever direction is physically possible for the tank. The amount of states just for the locations and orientations of vehicles in a single battle is also incredibly large.

From an action standpoint, players can drive, aim, shoot, switch ammunition types, and use consumables, and communicate with their team. Some tanks can even switch into different “modes” where their movement behavior is changed.

While the actions are simplistic in and of themselves (move, aim, shoot, switch ammo, use consumables, communicate), the strategy comes about when trying to accomplish the goal of winning by destruction or base capture. Strategy is initially highly dependent on the map and the distribution of the tanks on each team, and then also dependent on the actions of your teammates and the enemies’. Players want to take advantage of the characteristics of their tanks, and take advantage of physical characteristics of the maps. From a results standpoint, player skill is measured on characteristics like damage dealt, damage blocked, tanks spotted, tanks destroyed, capture points earned & reset, etc. From a strategic standpoint, player skill is determined by their ability to read all the characteristics of the current battle’s state, their ability to take advantage of their tank’s characteristics and the physical characteristics of the map, and how proficient they are at the basic actions.

## My Approach

Given the incredibly huge state space before entering the match, and similarly huge state space once the battle has begun, I will be simplifying the game to a crayon-drawing approximation. I will consider 1 battle scenario, consisting of two teams of one medium tank each, on a single, very small map. The goal will be to maximize damage done to the enemy tank, winning if the other tank is destroyed. The action each tank can take is to move, shoot, or both, and there will be armor and reloading mechanics in the game. The map will have 3 different features - light cover, which protects the hull, and leaves the turret exposed; heavy cover, which protects the entire tank, but does not allow shooting; and open squares, which offer no protections or restrictions. There will be accuracy penalties for movement by either player. There will be a time limit of a certain number of ticks.

The real World of Tanks has an extremely important mechanic called spotting, which leverages the camouflage system and vision system to asymmetrically "spot"/discover the enemy tanks when the distance, vision, and camouflage rating, among others, meet certain conditions. For time’s sake, this will be a perfect information game, with all tanks knowing the exact location of the other tanks. A more interesting project would be including two tanks on each team - a light tank (which is fast, lightly-armored and very good at scouting) and a heavy tank (which is slow and well-armored, but horrible at scouting), and a scouting mechanic, to see how q-learning might take advantage of spotting (and not being spotted) to control the battle.

Initially, the enemy will be mostly random, aside from the requirement that it will shoot at the enemy tank whenever possible. If possible, I will build a heuristic that favors moving closer to the enemy and taking advantage of cover.

