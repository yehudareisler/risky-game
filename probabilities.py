from sys import argv
import random

three_vs_one = 0.659  # 1/6(1 + 125/216 + 64/216 + 27/216 + 8/216 1/216)
three_vs_two = 2
def avrage_battle_result(attak_die ,defend_die):
    if attak_die == 3 and defend_die == 1:
       return three_vs_one

def avrage_war_result (attak_sold, defend_sold) :
    while attak_sold >1 and defend_sold > 0:
        attak_die = min(attak_sold-1,3)
        defend_die = min(attak_sold,2)
        battle_probabilty = avrage_battle_result(attak_die,defend_die)
        battle_result




def succeed_attak_task(state,battles,):
     without_final = battles[0,-1]
     for battle in without_final:
         curr_battle_result = battle_result(battle)[0]
         if (curr_battle_result == 0 )




def main():
   avrage_battle_result(3,1)


if argv[1] == "main":
    main()