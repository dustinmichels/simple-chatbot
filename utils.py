from termcolor import colored
import nltk

fmt = lambda x: colored(x, "yellow", attrs=["bold"])

robo_print = lambda x: print(fmt(x))


def print_face():
    robo_print(
        """\n
      ***          
    *******       
   *********       
/\* ### ### */\   
|    @ / @    |  
\/\    ^    /\/   
   \  ===  /     
    \_____/      
     _|_|_         
  *$$$$$$$$$*       
"""
    )


def prompter(usr_prompt):
    return input(f"{fmt(usr_prompt)}\n\t> ")
