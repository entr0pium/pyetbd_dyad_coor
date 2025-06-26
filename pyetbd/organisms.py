from dataclasses import dataclass, field
import numpy as np
from pyetbd.defaults import DEFAULTS


@dataclass
class Organism:
    pop_size: int = field(default_factory=lambda: DEFAULTS["pop_size"])
    low_pheno: int = field(default_factory=lambda: DEFAULTS["low_pheno"])
    high_pheno: int = field(default_factory=lambda: DEFAULTS["high_pheno"])

    def __post_init__(self) -> None:
        self.bin_length = len(bin(self.high_pheno)[2:])
        self.init_population()
        # used for keeping track of the fitness values of the population
        self.fitness_values = np.ndarray(self.pop_size)
        # used for keeping track of parents as the algorithm progresses
        self.parents = np.ndarray([self.pop_size, 2])
        # used for keeping track of offspring as the algorithm progresses
        self.offspring_genos = np.ndarray([self.pop_size, self.bin_length])

    def emit(self) -> None:
        self.emitted = np.random.choice(self.population)

    def emit_from_pop(self, population):
        """Emit a behavior sampled from the provided population."""
        self.emitted = np.random.choice(population)
        return self.emitted

    def init_population(self) -> None:
        self.population = np.random.randint(
            self.low_pheno, self.high_pheno, self.pop_size
        )

@dataclass
class ThreePopOrganism(Organism):
    """
    An Artificial Organism endowed with three distinct populations of
    potential behaviors for use in social or context-dependent simulations.

    This class extends the base Organism to support experiments where an
    organism's available actions depend on a specific context (e.g., being a 
    first- or second-mover). It replaces the single population with three
    distinct, independently evolving populations.

    Attributes:
        pop1 (np.ndarray): The first population of behaviors (first-mover).
        pop2 (np.ndarray): The second population of behaviors (second-mover after left).
        pop3 (np.ndarray): The third population of behaviors (second-mover after right).
    """
    def __post_init__(self) -> None:
        """
        Overrides the parent __post_init__ to create three populations
        instead of one.
        """
        self.bin_length = len(bin(self.high_pheno)[2:])
        self.init_populations()
        
        # These attributes are required by the algorithm class for processing
        self.fitness_values = np.ndarray(self.pop_size)
        self.parents = np.ndarray([self.pop_size, 2])
        self.offspring_genos = np.ndarray([self.pop_size, self.bin_length])

        # We set the original population attribute to pop1 by default.
        # The game logic will be responsible for swapping this out as needed.
        self.population = self.pop1


    def init_populations(self) -> None:
        """Initialize three distinct populations for the organism."""
        self.pop1 = np.random.randint(
            self.low_pheno, self.high_pheno, self.pop_size
        )
        self.pop2 = np.random.randint(
            self.low_pheno, self.high_pheno, self.pop_size
        )
        self.pop3 = np.random.randint(
            self.low_pheno, self.high_pheno, self.pop_size
        )

    def set_active_population(self, pop_name: str) -> None:
        """
        Sets the organism's main 'population' attribute to point to one
        of the three context-specific populations. The Algorithm class
        operates on `self.organism.population`, so this method is the key
        to directing the evolutionary process to the correct set of behaviors.

        Args:
            pop_name (str): The name of the population to set as active 
                            ('pop1', 'pop2', or 'pop3').
        """
        if pop_name == 'pop1':
            self.population = self.pop1
        elif pop_name == 'pop2':
            self.population = self.pop2
        elif pop_name == 'pop3':
            self.population = self.pop3
        else:
            raise ValueError(f"Unknown population name for ThreePopOrganism: {pop_name}")