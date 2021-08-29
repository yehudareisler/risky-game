from random import randint

ATTACKERS_WIN = True
ATTACKERS_LOSE = False


def die():
    return randint(1, 6)


def single_battle(attackers, defenders):
    # print(attackers,defenders)
    attackers_dice = sorted([die() for attacker in range(attackers)], reverse=True)
    defenders_dice = sorted([die() for defender in range(defenders)], reverse=True)
    for attackers_die, defenders_die in zip(attackers_dice, defenders_dice):
        if attackers_die > defenders_die:
            defenders -= 1
            # print(attackers_die,defenders_die, "a")
        else:
            attackers -= 1
            # print(attackers_die, defenders_die, "d")
    # if attackers_dead > attackers or defenders_dead > defenders:
    # print(
    #     f"attackers:{attackers}, defenders:{defenders}, dead_a:{attackers_dead}, "
    #     f"dead_d:{defenders_dead}")
    return attackers, defenders


def war(attackers, defenders):
    """
    assumes that all of the attackers attack
    :param attackers:
    :param defenders:
    :return:
    """
    while attackers > 1 and defenders > 0:
        attack_attempters, defense_attempters = min(attackers - 1, 3), min(defenders, 2)
        attackers -= attack_attempters
        defenders -= defense_attempters
        attack_attempters, defense_attempters = single_battle(attack_attempters, defense_attempters)
        attackers+=attack_attempters
        defenders+=defense_attempters
    return attackers, defenders


def count_elements(seq) -> dict:
    """Tally elements from `seq`."""
    hist = {}
    for i in seq:
        hist[i] = hist.get(i, 0) + 1
    return hist


def ascii_histogram(seq) -> None:
    """A horizontal frequency-table/histogram plot."""
    counted = count_elements(seq)
    for k in sorted(counted):
        # print(f'{k}, {counted[k]} {"+" * counted[k]}')
        print(f'{k}, {counted[k]}')


def possibilities(attackers, defenders, iterations):
    ascii_histogram(war(attackers, defenders) for i in range(iterations))


possibilities(attackers=3, defenders=1, iterations=100000)
# ascii_histogram(die() for i in range(1000000))
