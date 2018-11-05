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