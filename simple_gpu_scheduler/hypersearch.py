"""Tool for generating hyperparameter search commands."""
import argparse
from collections import OrderedDict
import itertools
import random
import sys


class HyperparameterSearch:
    """Represenation of a hyperparameter search."""

    def __init__(self, command_pattern, sampling_mode, n_samples, parameters):
        """Initialize hyperparameter search object.

        Args:
            command_pattern: Command pattern containing placeholders such as
                `my_program -paramter1 {parameter1}`.
            sampling_mode: Either grid or shuffled_grid.
            n_samples: Number of commands to generate.
            parameters: Dictionary mapping parameter names to a list of
                possible values.

        """
        self.command_pattern = command_pattern
        self.sampling_mode = sampling_mode
        self.n_samples = n_samples
        self.parameters = parameters

    def get_commands(self):
        """Get commands according to the hyperparameter search.

        Returns: List of commands where the parameter placeholders were filled.

        """
        # Build a list of dicts containing {parameter_name: sampled_value}
        parameter_combinations = [
            dict(zip(self.parameters.keys(), values))
            for values in itertools.product(*self.parameters.values())
        ]
        if self.sampling_mode == 'shuffled_grid':
            random.shuffle(parameter_combinations)

        if self.n_samples is not None:
            parameter_combinations = parameter_combinations[:self.n_samples]

        commands = [
            self.command_pattern.format_map(parameters)
            for parameters in parameter_combinations
        ]
        return commands


def build_hyperparameter_search():
    """Build HyperparameterSearch object from commandline parameters."""
    parser = argparse.ArgumentParser(
        description='Convenience tool to generate hyperparameter search '
                    'commands from a command pattern and parameter ranges.',
        epilog='Usage example:\n'
               '    %(prog)s "my_program --param1 {param1} --param2 {param2}" '
               '-p param1 0 1 -p param2 2 3\n'
               '    will generate the output:\n'
               '    my_program --param1 0 --param2 2\n'
               '    my_program --param1 0 --param2 3\n'
               '    my_program --param1 1 --param2 2\n'
               '    my_program --param1 1 --param2 3',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'command_pattern', type=str,
        help='Command pattern where placeholders with {parameter_name} should '
             'be replaced.'
    )
    parser.add_argument(
        '--sampling-mode', type=str,
        choices=['shuffled_grid', 'grid'],
        default='grid',
        help='Determine how to sample commands. Either in the '
             'grid order [grid] or in a shuffled order '
             '[shuffled_grid, default].'
    )
    parser.add_argument(
        '--n-samples', type=int, default=None,
        help='Number of samples to draw. '
             'If not provided use all possible combinations.'
    )
    parser.add_argument(
        '--seed', type=int, default=None,
        help='Random seed to ensure reproducability when using randomized '
             'order of the grid.'
    )
    parser.add_argument(
        '-p', '--parameter', nargs='+', action='append',
        metavar=('NAME', 'VALUES'),
        help='Name of parameter followed by values that should be considered '
             'for hyperparameter search. Example: `-p lr 0.01 0.001 0.0001`'
    )
    args = parser.parse_args()

    random.seed(args.seed)
    # Build a dictionary with {name: possible_values} for each parameter
    parameter_range_mapping = OrderedDict(
        ((param[0], param[1:]) for param in args.parameter)
    )
    hypersearch = HyperparameterSearch(
        args.command_pattern,
        args.sampling_mode,
        args.n_samples,
        parameter_range_mapping
    )
    return hypersearch


def generate_commands():
    """Command line tool to generate hyperparameter search commands."""
    hypersearch = build_hyperparameter_search()
    for command in hypersearch.get_commands():
        sys.stdout.write(command)
        sys.stdout.write('\n')
        sys.stdout.flush()
