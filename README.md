# RISK-AI

### What problem are you going to solve?

We want to make a program that plays the game of Risk. In the discussion below, we assume familiarity with the game and it’s rules. The game, as can be seen on the wikipedia page has many variants. We will list several types of variants:
- The beginning of the game in some versions involves players taking turns choosing territories, and then placing the remainder of their units. Other versions have the territories given out randomly.
- Risk can be played on many different maps. The classic game uses 1800s political boundaries, but versions exist with maps for fictional stories such as Lord of the Rings or Star Wars.
- At the end of every turn, players who conquered a territory receive a card. They can then give these cards in for additional units at the beginning of their turn. The amount of units they receive can vary according to the version of play.
- Towards the end of the turn, players can move some amount of units around. Some rulesets allow moving units only from a single territory to a single adjacent territory; others allow moving of units throughout contiguous territory.
- Some versions of the game involve special missions, or packs of cards that are triggered in various ways and cause all kinds of events (addition/subtraction of troops, loss/gain of turn, etc.).

We intend to work under the following assumptions: 
- The logic of the game is mostly coherent even stripped down of some of its elements, so we will work first with a game with random initial distribution, a standard world map, ignoring cards or using the standard version of them, movement to all contiguous territory, and not special missions. We will then see whether our logic holds on several variations, especially other maps.
- Part of what interests us are the game theory aspects of the game. Consider the possibility of players cooperating: How could we allow “ceasefires” (think molotov-ribbontrop) between players that are losing, in an attempt to band together against the current strong player. In case of such a ceasefire, the crucial question is when to renege on the agreement and betray your ally. Other similar considerations may exist: for instance, in some situations a player may want to spread their attacks out among the rival players in order not to weaken one of them too much. This set of considerations is something we would like to deal with, but we consider it’s importance secondary, and will deal with this issue if time allows.

### How are you going to solve it?

We intend to create at least one agent that prioritizes heuristics. There are many heuristics useful to the game, such as “conquer continents with defensible borders” “focus your forces”, “attack the enemy where he is weak” and so on. We will use these to create a baseline agent.

We then intend to use a monte carlo search tree type technique (simulate semi-random branches in the tree in order to approximate the value of a state) in order to create a second agent.

Within tree search agents we will probably make use of some relatively simple heuristics (number of territories captured, or troop income) in order to approximate the unexpanded nodes in the game tree. Alternatively, we may also attempt to learn the value of a situation.

### Why do you think that your approach is the right one?

Experience playing the game indicates a subjective feeling that gameplay for beginning players can be significantly improved by several simple heuristics. Therefore, we suspect that use of such heuristics may be sufficient for a reasonable level of gameplay. 

Given that the game is a multiplayer game with turns, modeling it as a tree seems like the most reasonable thing to do. Taking advantage of this structure involves dealing with an immense set of possible moves (a single turn can end in a very large number of states), thus requiring use of randomness to approximate the situation.

### How are you going to test your results?

We intend to test our work in multiple ways. 

First of all, we will write multiple agents, and pit them against each other. We will be interested in seeing which agent wins. Since we will, as noted above, write at least one agent based strongly on heuristics, we expect to be able to use that agent as a baseline for the other agents, which will attempt to infer more of the gameplay from the structure of the game itself, through the lens of search and learning based methods.

Furthermore, we will “freeze” versions of agents (before some amount of learning, or befor some set of improvements) and test the new version against the old one. This will allow us to see that we are progressing.

Secondly, we intend to play against the agents ourselves and give a qualitative feeling as to how strong the agents are.

Thirdly, we expect to be able to lower the length of games given good players. Good players should be able to leverage a small advantage into a larger one, and should play efficiently, leading to shorter gameplay. Obviously, it will be easier to achieve such an advantage against a weaker agent.

Finally, we will search for agents on the internet to test against. Our initial search for such an agent has not turned up any particularly strong agents, relative to human capabilities, and finding agents against which we will be able to test may be complicated. 
