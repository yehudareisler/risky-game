import random

from agent import Agent
from enum import Enum

PlanStage = Enum("PlanStage", "REINFORCE ATTACK FORTIFY")


class Plan:
    def __init__(self):
        self.reinforce = []
        self.attack = []
        self.fortify = None
        self.stage = PlanStage.REINFORCE
        self.substep = 0

    def set_stage(self, new_stage):
        self.stage = new_stage
        self.substep = 0


class PlannerAgent(Agent):
    """
    An agent that plans.
    """

    def __init__(self, number_of_branches):
        self.plan = None
        self.number_of_branches = number_of_branches
        self.best_plan = None
        self.best_plan_score = float("-inf")
        self.new_plan = None
        self.new_plan_score = 0
        self.get_plan = False

    def make_plan(self, state):
        player = state.player_to_move
        self.best_plan = None
        self.best_plan_score = float("-inf")
        for branch in range(self.number_of_branches):
            state.board.start_simulation()
            self.simulate_turn_with_plan(state)
            if self.new_plan_score > self.best_plan_score:
                self.best_plan_score = self.new_plan_score
                self.best_plan = self.new_plan
            else:
                self.new_plan = None
            state.board.end_simulation()

    def simulate_turn_with_plan(self, state):
        self.get_plan = True
        self.new_plan = Plan()
        state.player_to_move.take_turn(state)

        self.get_plan = False

    @staticmethod
    def get_state_value(state, player):

    # overriding abstract method
    def reinforce_owned_territory(self, state):
        if self.get_plan:
            assert self.new_plan
            territory = self.planner_reinforce_owned_territory(state)
            self.new_plan.reinforce.append(territory)
            return territory
        if not self.plan:
            self.make_plan(state)
        if self.plan and self.plan.stage == PlanStage.REINFORCE:
            territory = self.plan.reinforce[self.plan.substep]
            self.plan.substep += 1
            if self.plan.substep == len(self.plan.reinforce):
                self.plan.set_stage(PlanStage.ATTACK)
            return territory
        territories = state.board.border_territories(state.player_to_move)
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def reinforce_neutral_territory(self, state):
        # DONE
        territories = state.board.neutral_territories()
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def defend_territory(self, state, attacked_territory):
        # DONE
        troop_count = 1
        if attacked_territory.troops > 1:
            troop_count = 2
        return troop_count

    # overriding abstract method
    def wants_to_attack(self, state):
        if self.get_plan:
            wants_to_attack = self.planner_wants_to_attack(state)
            if wants_to_attack:
                assert self.new_plan
                self.new_plan.attack.append((None, None))
            return wants_to_attack
        territories_to_attack_from = state.board.territories_to_attack_from(state.player_to_move)
        if self.plan:
            if not (self.plan.stage == PlanStage.ATTACK and territories_to_attack_from):
                return False
            source, target = self.plan.attack[self.plan.substep]
            while target.ruler == state.player_to_move or source not in territories_to_attack_from:
                self.plan.substep += 1
                if self.plan.substep == len(self.plan.attack):
                    self.plan.set_stage(PlanStage.FORTIFY)
                    return False
            return True
        return random.random() < 0.9

    # overriding abstract method
    def select_attack_source(self, state):
        if self.get_plan:
            source = self.planner_select_attack_source(state)
            assert self.new_plan and (None, None) == self.new_plan.attack[-1]
            self.new_plan.attack[-1] = (source, None)
            return source
        territories = list(state.board.territories_to_attack_from(state.player_to_move))
        if self.plan:
            source, target = self.plan.attack[self.plan.substep]
            if source in territories:
                return source
            else:
                self.plan.set_stage(PlanStage.FORTIFY)
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def select_attack_target(self, state, source):
        if self.get_plan:
            target = self.planner_select_attack_target(state, source)
            assert self.new_plan and self.new_plan.attack[-1][1] is None
            source = self.new_plan.attack[-1][0]
            self.new_plan.attack[-1] = (source, target)
            return target
        territories = list(source.enemy_neighbors())
        if self.plan:
            source, target = self.plan.attack[self.plan.substep]
            if target in territories:
                return target
            else:
                self.plan.set_stage(PlanStage.FORTIFY)
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def select_attack_count(self, state, source):
        # TODO this doesn't make sense at the moment
        if self.get_plan:
            ret_val = self.planner_select_attack_count(state, source)
            return ret_val
        if self.plan and self.plan.stage == PlanStage.ATTACK:
            return source.troops - 1
        return random.randint(1, source.troops - 1)

    # overriding abstract method
    def wants_to_fortify(self, state):
        if self.get_plan:
            wants_to_fortify = self.planner_wants_to_fortify(state)
            if wants_to_fortify:
                assert self.new_plan
                self.new_plan.fortify = (None, None)
            return wants_to_fortify
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        if self.plan and self.plan.stage == PlanStage.FORTIFY:
            if not self.plan.fortify:
                return False
            source, target = self.plan.fortify
            if target not in territories or source not in target.friendly_fortifiers():
                return False
            return True
        return random.random() < 0.9

    # overriding abstract method
    def select_fortify_source(self, state, target):
        if self.get_plan:
            source = self.planner_select_fortify_source(state, target)
            assert self.new_plan and self.new_plan.fortify[0] is None
            target = self.new_plan.fortify[1]
            self.new_plan.fortify = (source, target)
            return source
        if self.plan and self.plan.stage == PlanStage.FORTIFY:
            source, target = self.plan.fortify
            return source
        source = random.choice(target.friendly_fortifiers())
        return source

    # overriding abstract method
    def select_fortify_target(self, state):
        if self.get_plan:
            target = self.planner_select_fortify_target(state)
            assert self.new_plan and self.new_plan.fortify == (None,None)
            self.new_plan.fortify = (None, target)
            return target
        if self.plan and self.plan.stage == PlanStage.FORTIFY:
            source, target = self.plan.fortify
            return target
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        target = random.choice(territories)
        return target

    # overriding abstract method
    def select_fortify_count(self, state, source):
        if self.get_plan:
            ret_val = self.planner_select_fortify_count(state, source)
            return ret_val
        if self.plan and self.plan.stage == PlanStage.FORTIFY:
            return source.troops - 1
        troop_count = random.randint(1, source.troops - 1)
        return troop_count

    # overriding abstract method
    def planner_reinforce_owned_territory(self, state):
        territories = state.board.border_territories(state.player_to_move)
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def planner_reinforce_neutral_territory(self, state):
        # DONE
        territories = state.board.neutral_territories()
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def planner_defend_territory(self, state, attacked_territory):
        # DONE
        troop_count = 1
        if attacked_territory.troops > 1:
            troop_count += 1
        return troop_count

    # overriding abstract method
    def planner_wants_to_attack(self, state):
        return random.random() < 0.9

    # overriding abstract method
    def planner_select_attack_source(self, state):
        territories = list(state.board.territories_to_attack_from(state.player_to_move))
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def planner_select_attack_target(self, state, source):
        territories = list(source.enemy_neighbors())
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def planner_select_attack_count(self, state, source):
        return random.randint(1, source.troops - 1)

    # overriding abstract method
    def planner_wants_to_fortify(self, state):
        return random.random() < 0.9

    # overriding abstract method
    def planner_select_fortify_source(self, state, target):
        source = random.choice(target.friendly_fortifiers())
        return source

    # overriding abstract method
    def planner_select_fortify_target(self, state):
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        target = random.choice(territories)
        return target

    # overriding abstract method
    def planner_select_fortify_count(self, state, source):
        troop_count = random.randint(1, source.troops - 1)
        return troop_count
