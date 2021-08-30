import random
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
        attackers += attack_attempters
        defenders += defense_attempters
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
    print(1000 - (sum(k[0] * counted[k] for k in sorted(counted)) / 10000))


def possibilities(attackers, defenders, iterations):
    ascii_histogram(war(attackers, defenders) for i in range(iterations))


# possibilities(attackers=1000, defenders=20, iterations=10000)


# ascii_histogram(die() for i in range(1000000))

def chain_war(initial_attackers, defenders_list, iterations):
    fail = 0
    sum_remaining_attackers = 0
    mn, mx = float("inf"), 0
    for i in range(iterations):
        a = initial_attackers
        for d in defenders_list:
            a, d = war(a, d)
            if a == 1:
                fail += 1
                break
            a -= 1
        a += 1
        mn = min(mn, a)
        mx = max(mx, a)
        sum_remaining_attackers += a
    return fail, sum_remaining_attackers / iterations, mn, mx


def get_n_random_integers_sum_to_m(n, m):
    while True:
        limits = [0]
        for i in range(n - 1):
            limits.append(random.randint(1, m - 1))
        limits.append(m)
        limits.sort()
        nums = [limits[i + 1] - limits[i] for i in range(n)]
        if 0 not in nums:
            return nums


def random_chain_war(attackers, defenders, chains, iterations, chain_length):
    mx, mn, sm = 0, float("inf"), 0
    sum_of_mins, sum_of_maxs = 0, 0
    for i in range(chains):
        c = chain_war(attackers, get_n_random_integers_sum_to_m(chain_length, defenders),
                      iterations)
        if c[1] > mx:
            mx = c[1]
        if c[1] < mn:
            mn = c[1]
        sm += c[1]
        sum_of_mins += c[2]
        sum_of_maxs += c[3]
    sm = sm / chains
    return round(attackers - mx, 2), round(attackers - mn, 2), round(attackers - sm, 2), \
           round(attackers - sum_of_mins / chains, 2), round(attackers - sum_of_maxs / chains, 2)


# initial_attacking_soldiers = 100
# for j in range(5, 70):
#     print(j, round(initial_attacking_soldiers -
#                    chain_war(initial_attacking_soldiers, get_n_random_integers_sum_to_m(7, j),
#                              1000)[1], 2))

"""
This seems to prove that with large numbers, the spread of defenders doesn't seem to matter that 
much, the number of attackers left in the last country, is very similar to the number of soldiers 
started with minus the number of attackers.
"""
for i in range(5, 101, 5):
    print(i, random_chain_war(attackers=1000, defenders=i, chains=20, iterations=500,
                              chain_length=4))
