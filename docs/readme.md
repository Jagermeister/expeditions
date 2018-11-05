# Game, Search, Learn

Framework for running simulations on different games with different player strategies. Inspiration for this project was to utilize and understand the [Monte Carlo tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search).

## Installation
`pip install -r requirements.txt`

## Execution
`python src/main.py`

Selecting Game:
>![Introduction](./01_Intro.png)

Selecting Players
>![Players](./02_Players.png)


## Framework
We have Game and Agent (player) interfaces which establish the contract between the turn playing framework and the concrete implementations.

>![Framework](./Framework.png)


## Case Study: Tic Tac Toe
>"255,168 unique games of Tic Tac Toe to be played. Of these, 131,184 are won by the first player, 77,904 are won by the second player, and 46,080 are drawn." [Jesper Juul](https://www.jesperjuul.net/ludologist/2003/12/28/255168-ways-of-playing-tic-tac-toe/)