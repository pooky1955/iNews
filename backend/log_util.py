from colorama import init
from termcolor import colored, cprint

init()

alert = lambda x : cprint(x,'white','on_red')
finish = lambda x : cprint(x,"white","on_green")
info = lambda x : cprint(x,"white","on_blue")