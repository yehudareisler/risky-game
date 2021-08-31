import random

from agent import Agent
from enum import Enum
from logger import Logger
planner_number_of_branches = 20

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

    def __repr__(self):
        return f"PLAN: reinforce:{[territory.name for territory in self.reinforce]}, attack" \
               f":{[(source.name, target.name) for source, target in self.attack]}, fortify" \
               f":{self.fortify}, " \
               f"stage:{self.stage}, substep:{self.substep}"

class PlannerAgent(Agent):
    """
    An agent that plans.
    """

    def __init__(self):
        self.plan = None
        self.number_of_branches = planner_number_of_branches
        self.best_plan = None
        self.best_plan_score = float("-inf")
        self.new_plan = None
        self.new_plan_score = 0
        self.get_plan = False

    def make_plan(self, state):
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
        self.plan = self.best_plan
        self.best_plan = None
        self.best_plan_score = float("-inf")

    def simulate_turn_with_plan(self, state):
        player = state.player_to_move
        self.get_plan = True
        self.new_plan = Plan()
        state.player_to_move.take_turn(state)
        self.new_plan_score = self.get_state_value(state, player)
        self.get_plan = False

    @staticmethod
    def get_state_value(state, player):
        other_player = state.player_to_move if player != state.player_to_move else \
            state.player_to_wait
        player.receive_troops(state)
        other_player.receive_troops(state)
        state_value = player.available_troops - other_player.available_troops
        player.available_troops = 0
        other_player.available_troops = 0
        return state_value

    # overriding abstract method
    def reinforce_owned_territory(self, state):
        if self.get_plan:
            assert self.new_plan
            territory = self.planner_reinforce_owned_territory(state)
            self.new_plan.reinforce.append(territory)
            return territory

        if state.player_to_move.available_troops == \
                state.player_to_move.number_of_troops_to_reinforce_with(state)[0]:
            Logger.log("making new plan", state.verbose)
            self.make_plan(state)

        if self.plan and self.plan.stage == PlanStage.REINFORCE:
            Logger.log(self.plan.__repr__(),state.verbose)
            Logger.log("reinforce according to plan", state.verbose)
            territory = self.plan.reinforce[self.plan.substep]
            self.plan.substep += 1
            if self.plan.substep == len(self.plan.reinforce):
                self.plan.set_stage(PlanStage.ATTACK)
            return territory

        Logger.log(f"reinforce not according to plan ", state.verbose)
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
        territories_to_attack_from = state.board.territories_to_attack_from(state.player_to_move)
        if self.get_plan:
            assert self.new_plan
            if not self.new_plan.attack and territories_to_attack_from:
                self.new_plan.attack.append((None, None))
                return True
            wants_to_attack = self.planner_wants_to_attack(state)
            if wants_to_attack:
                self.new_plan.attack.append((None, None))
            return wants_to_attack

        if self.plan:
            Logger.log("wants_to_attack according to plan", state.verbose)
            if not (self.plan.stage == PlanStage.ATTACK and territories_to_attack_from):
                Logger.log(f"self.plan.stage={self.plan.stage}, bool(terr_to_attk_from)="
                           f"{bool(territories_to_attack_from)}",
                           state.verbose)
                return False
            if not self.plan.attack:
                Logger.log("attacker empty", state.verbose)
                raise Exception("attacker empty")
            source, target = self.plan.attack[self.plan.substep]
            while target.ruler == state.player_to_move or source not in territories_to_attack_from:
                self.plan.substep += 1
                if self.plan.substep == len(self.plan.attack):
                    self.plan.set_stage(PlanStage.FORTIFY)
                    return False
                source, target = self.plan.attack[self.plan.substep]
            return True

        Logger.log("wants_to_attack not according to plan", state.verbose)
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
                Logger.log("select_attack_source according to plan", state.verbose)
                return source
            else:
                self.plan.set_stage(PlanStage.FORTIFY)

        territory = random.choice(territories)
        Logger.log("select_attack_source not according to plan", state.verbose)
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
                Logger.log("select_attack_target according to plan", state.verbose)
                return target
            else:
                self.plan.set_stage(PlanStage.FORTIFY)

        Logger.log("select_attack_target not according to plan", state.verbose)
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
            Logger.log("want_to_fortify according to plan", state.verbose)
            if not self.plan.fortify:
                self.plan = None
                return False
            source, target = self.plan.fortify
            if target not in territories or source not in target.friendly_fortifiers():
                self.plan = None
                return False
            return True

        Logger.log("want_to_fortify not according to plan", state.verbose)
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
            Logger.log("select_fortify_source according to plan", state.verbose)
            source, target = self.plan.fortify
            self.plan = None
            return source

        Logger.log("select_fortify_source not according to plan", state.verbose)
        source = random.choice(target.friendly_fortifiers())
        self.plan = None
        return source

    # overriding abstract method
    def select_fortify_target(self, state):
        if self.get_plan:
            target = self.planner_select_fortify_target(state)
            assert self.new_plan and self.new_plan.fortify == (None, None)
            self.new_plan.fortify = (None, target)
            return target

        if self.plan and self.plan.stage == PlanStage.FORTIFY:
            Logger.log("select_fortify_target according to plan", state.verbose)
            source, target = self.plan.fortify
            return target

        Logger.log("select_fortify_target not according to plan", state.verbose)
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
