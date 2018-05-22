
from colorama import init, Fore, Back, Style
init()
from termcolor import cprint 
from pyfiglet import figlet_format, FigletFont

#fonts = FigletFont.getFonts()
#for f in fonts:
#    print(f)
#    try:
#        cprint(figlet_format('missile!', font=f), 'yellow', 'on_red', attrs=['bold'])
#    except:
#        continue

strings = ['missile!', 'winner!', 'Champ', 'GAME OVER', 'Good Luck!', '1', '32']
#strings = ['Expeditions!']
fonts = [
#All
'4max',
'basic',
'big',
'georgia11',
'starwars',
#Winner
'isometric3',
'merlin1',
'poison',
#Loser
'alpha',
'bear',
'blocks',
'cards',
'flowerpower',
'ghoulish',
'train',
]

for f in fonts:
    print(f)
    for s in strings:
        cprint(figlet_format(s, font=f), 'yellow', 'on_red', attrs=['bold'])


