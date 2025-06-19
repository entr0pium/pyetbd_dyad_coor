import numpy as np
from pyetbd.organisms import ThreePopOrganism
from pyetbd.schedules import RandomIntervalSchedule


class CooperativeGame:
    def __init__(self, pop_size=100, low_pheno=0, high_pheno=1023, left_mean=60, right_mean=60):
        """
        Initialize the cooperative game.

        Args:
            pop_size (int): Population size for each population.
            low_pheno (int): Lower bound for phenotype values.
            high_pheno (int): Upper bound for phenotype values.
            left_mean (int): Mean interval for the Left-Left reinforcement schedule.
            right_mean (int): Mean interval for the Right-Right reinforcement schedule.
        """
        # Initialize two Artificial Organisms (AOs)
        self.AO1 = ThreePopOrganism(pop_size, low_pheno, high_pheno)
        self.AO2 = ThreePopOrganism(pop_size, low_pheno, high_pheno)

        # Initialize reinforcement schedules
        self.left_left_schedule = RandomIntervalSchedule(mean=left_mean)
        self.right_right_schedule = RandomIntervalSchedule(mean=right_mean)

    def coin_toss(self):
        """Randomly determine the first mover."""
        return np.random.choice([self.AO1, self.AO2])

    def evaluate_behavior(self, behavior):
        """Evaluate the emitted behavior."""
        if 471 <= behavior <= 511:
            return "Left-Move"
        elif 512 <= behavior <= 552:
            return "Right-Move"
        else:
            return "Non-Target Move"

    def update_populations(self, first_mover, second_mover, first_pop, second_pop, reinforced):
        """
        Update the populations of both organisms based on reinforcement.

        Args:
            first_mover (ThreePopOrganism): The first mover organism.
            second_mover (ThreePopOrganism): The second mover organism.
            first_pop (np.ndarray): The population of the first mover.
            second_pop (np.ndarray): The population of the second mover.
            reinforced (bool): Whether reinforcement was available.
        """
        if reinforced:
            # Apply midpoint fitness selection (placeholder logic)
            first_pop[:] = np.random.choice(first_pop, len(first_pop))
            second_pop[:] = np.random.choice(second_pop, len(second_pop))
        else:
            # Apply random selection
            first_pop[:] = np.random.choice(first_pop, len(first_pop))
            second_pop[:] = np.random.choice(second_pop, len(second_pop))

    def run_trial(self):
        """Run a single trial of the cooperative game."""
        # Coin toss to determine the first mover
        first_mover = self.coin_toss()
        second_mover = self.AO1 if first_mover == self.AO2 else self.AO2

        # First mover emits behaviors from POP1 until a target behavior is produced
        while True:
            first_behavior = first_mover.emit_from_pop(first_mover.POP1)
            first_move_type = self.evaluate_behavior(first_behavior)
            if first_move_type in ["Left-Move", "Right-Move"]:
                break

        # Determine the second mover's population based on the first mover's behavior
        if first_move_type == "Left-Move":
            second_behavior = second_mover.emit_from_pop(second_mover.POP2)
            second_move_type = self.evaluate_behavior(second_behavior)

            if second_move_type == "Left-Move":
                # Cooperation: Left-Left
                reinforced = self.left_left_schedule.run(first_behavior)
                self.update_populations(first_mover, second_mover, first_mover.POP1, second_mover.POP2, reinforced)
            else:
                # Non-cooperation: Left-Right
                self.update_populations(first_mover, second_mover, first_mover.POP1, second_mover.POP2, False)

        elif first_move_type == "Right-Move":
            second_behavior = second_mover.emit_from_pop(second_mover.POP3)
            second_move_type = self.evaluate_behavior(second_behavior)

            if second_move_type == "Right-Move":
                # Cooperation: Right-Right
                reinforced = self.right_right_schedule.run(first_behavior)
                self.update_populations(first_mover, second_mover, first_mover.POP1, second_mover.POP3, reinforced)
            else:
                # Non-cooperation: Right-Left
                self.update_populations(first_mover, second_mover, first_mover.POP1, second_mover.POP3, False)

        # Return trial results
        return {
            "first_move": first_move_type,
            "second_move": second_move_type,
            "reinforced": reinforced,
        }

    def run_game(self, gens=63000):
        """
        Run the cooperative game for a specified number of generations.

        Args:
            gens (int): Number of generations to run.

        Returns:
            list: A list of trial results.
        """
        results = []
        for _ in range(gens):
            trial_result = self.run_trial()
            results.append(trial_result)
        return results