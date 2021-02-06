#!/usr/bin/env python3

import numpy as np
import random

class SelectionOperators:
    
    @staticmethod
    def random(population, k):
        return np.random.choice(len(population), size=k, replace=False)

    @staticmethod
    def k_best(population, fitness, k, maximize):
        return population[np.argsort(fitness)[::-1 if maximize else 1][:k]]

    @staticmethod
    def tournament(population, fitness, k, maximize, tournsize):
        chosen = []

        for i in range(k):
            aspirants = SelectionOperators.sel_random(population, tournsize)
            if maximize:
                chosen.append(population[np.argmax(fitness[aspirants], axis=0)])
            else:
                chosen.append(population[np.argmin(fitness[aspirants], axis=0)])

        return chosen

    @staticmethod
    def roulette(population, fitness, k, maximize):
        s_inds = sorted(list(zip(fitness, population)), reverse=maximize, key=lambda x: x[0])
        sum_fits = sum(fitness)
        chosen = []

        for i in range(k):
            u = random.random() * sum_fits
            partial_sum = 0
            for fit, ind in s_inds:
                partial_sum += fit
                if partial_sum > u:
                    chosen.append(ind)
                    break

        return chosen

class CrossoverOperators:

    def _crossover_assertions(parents):
        assert type(parents) == np.ndarray, f"type(parents) must be <class 'numpy.ndarray'>, found {type(parents)} instead"
        assert parents.shape[0] == 2, f"parents.shape must be (2, x), found {parents.shape} instead"

    def _are_permutations(parents):
        dc = dict()

        for i in parents[0,:]:
            if i not in dc:
                dc[i] = 1
            else:
                dc[i] += 1
        
        for i in parents[1,:]:
            if i not in dc or dc[i] == 0:
                return False
            else:
                dc[i] -= 1
        
        return True

    def _map_to_indexes(parents):
        mapped = np.zeros_like(parents)
        indexes = [0] * parents.shape[1]
        map = {}

        for i in range(parents.shape[1]):
            mapped[0, i] = i
            indexes[i] = parents[0, i]
            map[parents[0, i]] = i

        for i in range(parents.shape[1]):
            mapped[1, i] = map[parents[1, i]]

        return mapped, indexes

    def _unmap_from_indexes(individuals, indexes):
        unmapped = np.zeros_like(individuals)

        for i in range(individuals.shape[0]):
            for j in range(individuals.shape[1]):
                unmapped[i, j] = indexes[individuals[i, j]]

        return unmapped

    @staticmethod
    def single_point(parents, make_assert=True):
        if make_assert:
            CrossoverOperators._crossover_assertions(parents)

        point = random.randint(1, parents.shape[1] - 1)
        children = np.copy(parents)
        children[0, point:] = parents[1, point:]
        children[1, point:] = parents[0, point:]

        return children

    @staticmethod
    def k_point(parents, k):
        CrossoverOperators._crossover_assertions(parents)
        assert k > 0, f"k must be greater than 0, found k = {k} instead"
        assert k < parents.shape[1], f"k must be lesser than parents.shape[1] = {parents.shape[1]}, found k = {k} instead"
        
        for i in range(k):
            children = CrossoverOperators.single_point(parents, make_assert=False)
            parents = children

        return children

    @staticmethod
    def uniform(parents, rate=0.5):
        CrossoverOperators._crossover_assertions(parents)
        children = np.copy(parents)

        for i in range(parents.shape[1]):
            if random.random() < rate:
                children[0,i] = parents[1,i]
                children[1,i] = parents[0,i]

        return children

    @staticmethod
    def pmx(parents):
        '''
        Code adapted from DEAP: https://github.com/DEAP/deap/blob/master/deap/tools/crossover.py
        Unlike code from DEAP, this code works for non-index like representations.
        To do that, we index the representation and then un-do it.
        '''
        CrossoverOperators._crossover_assertions(parents)
        assert CrossoverOperators._are_permutations(parents), f"PMX operator expects parents to be permutations of themselves"
        children, indexes = CrossoverOperators._map_to_indexes(parents)
        p = np.zeros_like(parents)

        for i in range(children.shape[1]):
            p[0, children[0, i]] = i
            p[1, children[1, i]] = i

        cxpoint1 = random.randint(0, parents.shape[1])
        cxpoint2 = random.randint(0, parents.shape[1] - 1)

        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:  
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        for i in range(cxpoint1, cxpoint2):
            temp1 = children[0, i]
            temp2 = children[1, i]
            
            children[0, i], children[0, p[0, temp2]] = temp2, temp1
            children[1, i], children[1, p[1, temp1]] = temp1, temp2
            
            p[0, temp1], p[0, temp2] = p[0, temp2], p[0, temp1]
            p[1, temp1], p[1, temp2] = p[1, temp2], p[1, temp1]

        return CrossoverOperators._unmap_from_indexes(children, indexes)

class MutationOperators:

    @staticmethod
    def uniform_integers(individual, lower, upper, mutation_rate):
        new_ind = np.copy(individual)
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                new_ind[i] = random.randint(lower, upper)
        return new_ind

    @staticmethod
    def flip_bit(individual, mutation_rate):
        new_ind = np.copy(individual)
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                new_ind[i] = not new_ind[i]
        return new_ind

    @staticmethod
    def swap(individual, mutation_rate):
        new_ind = np.copy(individual)
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                swap_index = i
                while swap_index == i:
                    swap_index = random.randint(0, len(individual) - 1)
                new_ind[i] = individual[swap_index]
                new_ind[swap_index] = individual[i]
        return new_ind
        