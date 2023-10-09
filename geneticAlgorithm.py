import math
import random


def genetic_algorithm(population, max_generations):
    for iterations in range(max_generations):
        # returns a selection in the population if that selection has a fitness score of 1024
        for selection in population:
            if fitness(selection) == 1024:
                return selection

        # generate a new population if none of them are up to spec.
        population_2 = []
        print(population)
        for i in range(len(population)):
            parents = weighted_random_choice(population, 2)
            child = mutate(reproduce(parents[0], parents[1]))
            print(f"{parents} -> {to_decimal(child)}")
            population_2.append(to_decimal(child))
        population = population_2.copy()
        population_2.clear()


def reproduce(parent_1, parent_2):
    parent_1_binary = to_binary(parent_1)
    parent_2_binary = to_binary(parent_2)

    if len(parent_1_binary) < len(parent_2_binary):
        parent_1_binary = lengthen_binary(parent_1_binary, len(parent_2_binary))
    elif len(parent_1_binary) > len(parent_2_binary):
        parent_2_binary = lengthen_binary(parent_2_binary, len(parent_1_binary))

    split_point = random.randint(0, len(parent_1_binary))
    child = []
    for i in range(split_point):
        child.append(parent_1_binary[i])
    for i in range(split_point, len(parent_1_binary)):
        child.append(parent_2_binary[i])
    return child


def weighted_random_choice(pop, count):
    population = pop.copy()
    if count > len(population):
        return population
    selections = []
    while count >= 1:
        weighted_list = []
        total_weight = 0
        for selection in population:
            current_weight = fitness(selection)
            total_weight += current_weight
            weighted_list.append(total_weight)
        random_pick = random.random()*total_weight
        for index, selection in enumerate(population):
            if weighted_list[index] >= random_pick:
                selections.append(population.pop(index))
                break
        count -= 1
    return selections


def fitness(selection):
    """Returns the distance from 0 an item is, divided by 10"""
    val = func(selection)
    if val < 1024:
        return 1024 - val
    else:
        return 0


def lengthen_binary(binary_arr: list, length):
    """Converts a binary_arr of length n to length s, where s > n"""
    if length <= len(binary_arr):
        return binary_arr
    else:
        iterations = length - len(binary_arr)
        for i in range(iterations):
            binary_arr.insert(0, 0)
        return binary_arr


def to_binary(num: int):
    """Converts an integer number into binary"""
    max_pow = 0
    while pow(2, max_pow) <= num:
        max_pow += 1
    max_pow -= 1

    current_pow = max_pow
    current_num_value = num
    binary_arr = []
    while current_pow >= 0:
        if pow(2, current_pow) <= current_num_value:
            current_num_value -= pow(2, current_pow)
            binary_arr.append(1)
        else:
            binary_arr.append(0)
        current_pow -= 1
    return binary_arr


def to_decimal(binary_arr: list):
    max_pow = len(binary_arr) - 1
    val = 0
    for i in binary_arr:
        val += i*(2**max_pow)
        max_pow -= 1
    return val


def mutate(binary_arr: list):
    """Receives a binary array, and mutates some members of it depending on the mutation probability"""
    mutation_probability = 0.02
    mutated_child = []
    for i in binary_arr:
        if random.random() <= mutation_probability:
            mutated_child.append(int(not i))
        else:
            mutated_child.append(i)
    return mutated_child


def func(x):
    return pow(x, 2) + 2*x


def generate_population(num_population: int, min_val: int, max_val: int):
    """Returns an array of length num_population, whose members are values between min_val and max_val"""
    population = []
    for i in range(num_population):
        population.append(random.randint(min_val, max_val))
    return population


print(genetic_algorithm(generate_population(4, 0, 31), 10))
