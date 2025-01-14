"""
TODO: Write some docs here.
"""
from __future__ import annotations

import asyncio

from tqdm import tqdm

from .evaluator.poke_env import PokeEnv
from .stats.team_recorder import TeamRecorder
from .teams.builder import Builder

N_generations = 50  # Number of generations to run
N_teams = 2  # Number of teams to generate per generation
N_battles = 3  # Number of battles to run per team
RECORD = True


async def main_loop():
    builder = Builder(N_seed_teams=N_teams)
    builder.build_N_teams_from_poke_pool(N_teams)
    curr_gen = 0  # Current generation
    evaluator = PokeEnv(n_battles=N_battles)
    recorder = TeamRecorder()

    # Main expected loop
    print("Starting main loop and running on Generation: ")
    for _ in tqdm(range(N_generations)):
        if RECORD:
            recorder.record_teams(builder.get_teams(), curr_gen)
        await evaluator.evaluate_teams(builder.get_teams())
        builder.generate_new_teams()
        curr_gen += 1


def main():
    asyncio.get_event_loop().run_until_complete(main_loop())


if __name__ == "__main__":
    main()
