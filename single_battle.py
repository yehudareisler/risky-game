#
# for attacker in range(1,7):
#     for defender in range(1,7):
#         if defender>=attacker:
#             defense+=1
# print(defense)

from itertools import product


def win_rates(num_of_attackers, num_of_defenders):
    defense = 0
    attack = 0
    both = 0
    num_of_dice = num_of_defenders + num_of_attackers
    for dice in product(range(1, 7), repeat=num_of_dice):
        defense_dice = sorted(dice[:num_of_defenders], reverse=True)
        attack_dice = sorted(dice[num_of_defenders:], reverse=True)
        diff = [a - d for a, d in zip(attack_dice, defense_dice)]
        if diff[0] > 0 and diff[1] > 0:
            attack += 1  # defender loses two
        elif diff[0] <= 0 and diff[1] <= 0:
            defense += 1  # attacker loses two
        else:
            both += 1  # each loses one
    print(f"defender loses two:{attack}, attacker loses two: {defense}, each loses one {both}")
    print(
        f"defender loses two:{round(100 * attack / 6 ** num_of_dice, 2)}%, "
        f"attacker loses two: {round(100 * defense / 6 ** num_of_dice, 2)}%, "
        f"each loses one {round(100 * both / 6 ** num_of_dice, 2)}%")
    # print(defense / 6 ** 5, attack / 6 ** 5, both / 6 ** 5)
    # print(defense, attack, both)


win_rates(num_of_attackers=3, num_of_defenders=2)
