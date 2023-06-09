"""
Find the Fastest Horses
 - You are given 25 horses, and your task is to determine the three fastest horses among them.
 - You can only race five horses at a time
 - There are no timers available.
 - The only information you can obtain from each race is the order in which the horses finish.

Your goal is to design an algorithm that can find the three fastest horses with the minimum number of races.
"""

import random
import argparse
import os
import matplotlib.pyplot as plt


def formatted_list(numbers):
    formatted_numbers = [f"{number:02d}" for number in numbers]
    return f"[{', '.join(formatted_numbers)}]"


def generate_horses():
    """
    Generate a list of 25 horses with different times to finish race
    :return: list of horses
    """
    horses = []
    for i in range(25):
        horses.append(i)
    random.shuffle(horses)
    return horses


def write_horses_to_file(horses, filename):
    """
    Write the list of horses to a text file
    :param horses: list of horses
    :param filename: name of the output file
    """
    try:
        with open("instances/"+filename, 'w') as file:
            for horse in horses:
                file.write(str(horse) + '\n')
    except IOError:
        # An error occurred while writing to the file
        print(f"An error occurred while writing to the file '{filename}'.")


def read_horses_from_file(filename):
    """
    Read the list of horses from a text file
    :param filename: name of the input file
    :return: list of horses
    """
    horses = []
    try:
        with open("instances/"+filename, 'r') as file:
            for line in file:
                horses.append(int(line.strip()))
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return horses


class HorseRanking:
    """
    A class depicting which horses are faster or slower that a given horse
    """

    def __init__(self, index):
        self.index = index
        self.complete = False
        self.faster = []
        self.slower = []

    def get_faster(self):
        return len(self.faster)

    def get_slower(self):
        return len(self.slower)

    def add_faster(self, index):
        """
        Add horse to faster list
        :param index: index of horse to add
        """
        if index == self.index:
            raise ValueError("A horse cannot be faster than itself.")
        else:
            if index not in self.faster:
                self.faster.append(index)

    def add_slower(self, index):
        """
        Add horse to slower list
        :param index: index of horse to add
        """
        if index == self.index:
            raise ValueError("A horse cannot be slower than itself.")
        else:
            if index not in self.slower:
                self.slower.append(index)

    def update_self_after_race(self, race):
        """
        Update faster and slower list after a race the horse took part on
        :param race: list of order
        """
        if self.index not in race:
            raise ValueError("This horse was not part of the race")
        else:
            own_rank = race.index(self.index)
            for horse in race[:own_rank]:
                self.add_slower(horse)
            for horse in race[own_rank+1:]:
                self.add_faster(horse)
        self.check_completion()

    def update_others(self):
        # add each slower horse to slower-list of each faster horse
        for slower_horse in self.slower:
            for faster_horse in self.faster:
                horse_rankings[faster_horse].add_slower(slower_horse)
        # add each faster horse to faster-list of each slower horse
        for faster_horse in self.faster:
            for slower_horse in self.slower:
                horse_rankings[slower_horse].add_faster(faster_horse)

    def check_completion(self):
        _progress = self.get_faster() + self.get_slower()
        if _progress == 24:
            self.complete = True
        return _progress


def race(horses, racers):
    """
    Get the order in which horses complete the race
    :param horses: list of all horses
    :param racers: indices of horses in the race
    :return: order at which horses finish race
    """

    if len(racers) != 5:
        raise ValueError("Exactly 5 horses must take part in a race.")

    # Sort the racers based on their corresponding horse times in ascending order
    sorted_racers = sorted(racers, key=lambda x: horses[x])

    # update ranks
    for horse in racers:
        horse_rankings[horse].update_self_after_race(sorted_racers)

    # Return the sorted racers list
    return sorted_racers


def check_overall_completion():
    """
    Checks overall completion over all horses
    :return: List of completion progress
    """
    # update others
    for i in range(25):
        horse_rankings[i].update_others()
    # create empty completion list
    completion_list = []
    # fill completion list
    for horse in range(25):
        completion_list.append(horse_rankings[horse].check_completion())
    return completion_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Horse Racing')
    parser.add_argument('filename', default='horses.txt', help='Name of the output file (default: horses.txt)')
    args = parser.parse_args()

    filename = args.filename
    if ".txt" not in filename:
        filename = filename+".txt"

    if not os.path.exists("instances/"+filename):
        print("Instance not found. Generating horses...")
        horses = generate_horses()
        print(f"Saving horses to instances/{filename}")
        write_horses_to_file(horses, filename)
    else:
        print("Instance found. Reading...")
        horses = read_horses_from_file(filename)

    # Create a list to hold the horse rankings
    horse_rankings = []

    # create horse ranking
    for i in range(len(horses)):
        _horse_ranking = HorseRanking(i)
        horse_rankings.append(_horse_ranking)

    # Conduct five races with non-overlapping sets of participating horses. Save the middle horse
    print(formatted_list(check_overall_completion()))
    for i in range(0, 24, 5):
        race(horses, list(range(i, i+5)))
    print(formatted_list(check_overall_completion()))

    # Conduct another race using one participant of each race
    race(horses, list(range(0, 25, 5)))

    # Update all horses using the faster and slower lists of each other
    print(formatted_list(check_overall_completion()))




    print()
