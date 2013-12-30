#!/usr/bin/env python

import random
import ahkab
from ahkab import circuit, printing, devices
import scipy
import scipy.interpolate
import numpy
import math
import time
import copy
from pprint import pprint as pp

debug = True

if debug:
    print "Using `ahkab` %s" % ahkab.ahkab.__version__

class Component(object):
    def __init__(self, value=None, part_id=None, n1=None, n2=None):
        self.value      = value
        self.part_id    = part_id
        self.n1         = n1
        self.n2         = n2

    def __repr__(self):
        return '<%s.%s object at %s> %s %s %s %s' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
            self.part_id,
            self.n1,
            self.n2,
            self.value)

class Resistor(Component):
    common = [  #   In ohms
        10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82,
        91, 100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 390, 430, 470, 
        510, 560, 620, 680, 750, 820, 910, 1000, 1100, 1200, 1300, 1500, 1600, 1800, 2000, 2200, 
        2400, 2700, 3000, 3300, 3600, 3900, 4300, 4700, 5100, 5600, 6200, 6800, 7500, 8200, 9100, 
        10000, 11000, 12000, 13000, 15000, 16000, 18000, 20000, 22000, 24000, 27000, 30000, 33000,
        36000, 39000, 43000, 47000, 51000, 56000, 62000, 68000, 75000, 82000, 91000, 100000, 
        110000, 120000, 130000, 150000, 160000, 180000, 200000, 220000, 240000, 270000, 300000, 
        330000, 360000, 390000, 430000, 470000, 510000, 560000, 620000, 680000, 750000, 820000, 
        910000, 1000000, 1100000, 1200000, 1300000, 1500000, 1600000, 1800000, 2000000, 2200000, 
        2400000, 2700000, 3000000, 3300000, 3600000, 3900000, 4300000, 4700000, 5100000, 5600000, 
        6200000, 6800000, 7500000, 8200000, 9100000, 10000000, 11000000, 12000000, 13000000, 
        15000000, 16000000, 18000000, 20000000, 22000000, 24000000, 27000000, 30000000, 33000000, 
        36000000, 39000000, 43000000, 47000000, 51000000, 56000000, 62000000, 68000000, 75000000, 
        82000000, 91000000]

class Inductor(Component):
    common = [  #   In henries
        1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 1e-09, 1.1e-08, 1.1e-07, 1.1e-06, 1.1e-05, 1e-09, 
        1.2e-08, 1.2e-07, 1.2e-06, 1.2e-05, 1e-09, 1.3e-08, 1.3e-07, 1.3e-06, 1.3e-05, 2e-09, 
        1.5e-08, 1.5e-07, 1.5e-06, 1.5e-05, 2e-09, 1.6e-08, 1.6e-07, 1.6e-06, 1.6e-05, 2e-09, 
        1.8e-08, 1.8e-07, 1.8e-06, 1.8e-05, 2e-09, 2e-08, 2e-07, 2e-06, 2e-05, 2e-09, 2.2e-08, 
        2.2e-07, 2.2e-06, 2.2e-05, 2e-09, 2.4e-08, 2.4e-07, 2.4e-06, 2.4e-05, 3e-09, 2.7e-08, 
        2.7e-07, 2.7e-06, 2.7e-05, 3e-09, 3e-08, 3e-07, 3e-06, 3e-05, 3e-09, 3.3e-08, 3.3e-07, 
        3.3e-06, 3.3e-05, 4e-09, 3.6e-08, 3.6e-07, 3.6e-06, 3.6e-05, 4e-09, 3.9e-08, 3.9e-07, 
        3.9e-06, 3.9e-05, 4e-09, 4.3e-08, 4.3e-07, 4.3e-06, 4.3e-05, 5e-09, 4.7e-08, 4.7e-07, 
        4.7e-06, 4.7e-05, 5e-09, 5.1e-08, 5.1e-07, 5.1e-06, 5.1e-05, 6e-09, 5.6e-08, 5.6e-07, 
        5.6e-06, 5.6e-05, 6e-09, 6.2e-08, 6.2e-07, 6.2e-06, 6.2e-05, 7e-09, 6.8e-08, 6.8e-07, 
        6.8e-06, 6.8e-05, 8e-09, 7.5e-08, 7.5e-07, 7.5e-06, 7.5e-05, 8e-09, 8.2e-08, 8.2e-07, 
        8.2e-06, 8.2e-05, 9e-09, 8.7e-08, 8.7e-07, 8.7e-06, 8.7e-05, 9e-09, 9.1e-08, 9.1e-07, 
        9.1e-06, 9.1e-05]

class Capacitor(Component):
    common = [  #   In farads
        1e-11, 1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1.2e-11, 1.2e-10, 1.2e-09, 1.2e-08, 1.2e-07, 
        1.2e-06, 1.5e-11, 1.5e-10, 1.5e-09, 1.5e-08, 1.5e-07, 1.5e-06, 1.8e-11, 1.8e-10, 1.8e-09, 
        1.8e-08, 1.8e-07, 1.8e-06, 2.2e-11, 2.2e-10, 2.2e-09, 2.2e-08, 2.2e-07, 2.2e-06, 2.7e-11, 
        2.7e-10, 2.7e-09, 2.7e-08, 2.7e-07, 2.7e-06, 3.3e-11, 3.3e-10, 3.3e-09, 3.3e-08, 3.3e-07, 
        3.3e-06, 3.9e-11, 3.9e-10, 3.9e-09, 3.9e-08, 3.9e-07, 3.9e-06, 4.7e-11, 4.7e-10, 4.7e-09, 
        4.7e-08, 4.7e-07, 4.7e-06, 5.6e-11, 5.6e-10, 5.6e-09, 5.6e-08, 5.6e-07, 5.6e-06, 6.8e-11, 
        6.8e-10, 6.8e-09, 6.8e-08, 6.8e-07, 6.8e-06, 8.2e-11, 8.2e-10, 8.2e-09, 8.2e-08, 8.2e-07, 
        8.2e-06]

class Circuit(list):       
    def __init__(self, title="Untitled", num_nodes=0, outfile='ramdisk/sim.ac', sim_verbosity=0, weights=None, random=None):
        self.title          = title             #   Title of the circuit
        self.num_nodes      = num_nodes         #   Number of connection nodes
        self.outfile        = outfile           #   The filename for Ahkab's scratchpad
        self.sim_verbosity  = sim_verbosity     #   Simulation verbosity for Ahkab
        self.weights        = weights if weights else [
             10.0,  #   log 10 (Minimum attenuation in the stop band / Maximum attenuation in the pass band)
            -100.0, #   Maximum attenuation in the pass band
             10.0,  #   Minimum attenuation in the stop band
            -2.0,   #   Number of nodes
            -2.0    #   Number of parts
        ]
        
        self.circuit                    = None  #   An Ahkab circuit object
        self.max_attenuation_pass_band  = None  #   Tuple of (pass band upper frequency, maximum attenuation)
        self.min_attenuation_stop_band  = None  #   Tuple of (stop band lower frequency, minimum attenuation)

        #   Table of `Component` types to lists of [subclass, init method for Ahkab, subclass count]
        self.component_types = {     
            'R': [Resistor,     'add_resistor',     0],   
            'L': [Inductor,     'add_inductor',     0],    
            'C': [Capacitor,    'add_capacitor',    0]
        }

        #   Populate the `Circuit` with random `Component`s
        if random: self.random()

    #   Creates many random `Component`s
    def random(self):
        self.num_nodes = random.randint(3, 8)

        for i in range(0, random.randint(4, 20)):
            #   Make sure to append to self (a `Circuit`) instead of overwriting with a basic `list`
            self.append(self.random_part())
            
    #    Creates a random `Component`
    def random_part(self):
        #   Create a list of all the nodes to select from, emphasizing ground
        all_nodes = (['0'] * 3) + ["n%d" % i for i in range(1, self.num_nodes)]

        a_type                  = random.choice(self.component_types.keys())
        a_class, an_init, an_id = self.component_types[a_type]
        a_part                  = a_class()
        a_part.value            = random.choice(a_part.common)
        a_part.part_id          = "%s%d" % (a_type, an_id)
        a_part.n1               = random.choice(all_nodes)
        a_part.n2               = random.choice(all_nodes)

        #   Increment per-subclass counter (for next `an_id`)
        self.component_types[a_type][2] += 1

        return a_part

    #   Mutations to fine-tune the `top_n` solutions
    def mutate(self):
        mutation = random.randint(0, 1000)

        if debug:
            print "Mutating (from):"
            pp(self)

        if  mutation < 400:     self.mutate_delete()
        elif mutation < 500:    self.mutate_add()
        elif mutation < 800:    self.mutate_value()
        elif mutation < 900:    self.mutate_node()

        if debug:
            print "Mutating (to):"
            pp(self)
            print "\n"

    #   Deletes a `Component`
    def mutate_delete(self):
        if debug:
            print "Mutate 'delete'"

        size = len(self)
        if size > 1:
            del self[random.randint(0, size-1)]

    #   Adds a `Component`
    def mutate_add(self):
        if debug:
            print "Mutate 'add'"

        self.append(self.random_part())

    #   Selects a new `value` for a random `Component`
    def mutate_value(self):
        if debug:
            print "Mutate 'value'"

        a_part          = self[random.randint(0, len(self)-1)]
        a_part.value    = random.choice(a_part.common)

    def mutate_node(self):
        if debug:
            print "Mutate 'node'"

        #   Create a list of all the nodes to select from, emphasizing ground
        all_nodes = (['0'] * 3) + ["n%d" % i for i in range(1, self.num_nodes)]

        #   Choose a random `Component`
        a_part = self[random.randint(0, len(self)-1)]

        #   Choose a random connection node to swap
        if random.randint(0, 1):
            a_part.n1 = random.choice(all_nodes)
        else:
            a_part.n2 = random.choice(all_nodes)

    #   Drive the Ahkab circuit simulator
    def simulate(self):
        #   Build a copy of the circuit for Ahkab
        self.circuit = circuit.circuit(title=self.title)

        #   Create nodes
        for i in range(0, self.num_nodes):
            self.circuit.create_node("n%d" % i)

        #   Create passive components
        for i in self:
            #   Call the init method of the current component type
            getattr(self.circuit, self.component_types[i.part_id[0]][1])(
                i.part_id, 
                i.n1,
                i.n2,
                value=i.value)

        #   Add a voltage source
        voltage_step = devices.pulse(v1=0, v2=1, td=500e-9, tr=1e-12, pw=1, tf=1e-12, per=2)
        self.circuit.add_vsource(part_id='V1', n1='n1', n2='0', value=5, vac=1, function=voltage_step)

        #   Simulate the circuit with an AC analysis
        return ahkab.ac.ac_analysis(self.circuit, 1e3, 100, 1e5, 'LOG', outfile=self.outfile, verbose=self.sim_verbosity)

    def score(self):
        r = self.simulate()

        #   Didn't simulate
        if not r: return None
        
        try:
            # Normalize the output to the low frequency value and convert to array
            norm_out = numpy.asarray(r['|Vn4|'].T/r['|Vn4|'].max())
            
            # Convert to dB
            norm_out_db = 20 * numpy.log10(norm_out)
            
            # Reshape to be scipy-friendly
            norm_out_db = norm_out_db.reshape((max(norm_out_db.shape),))
            
            # Convert angular frequencies to Hz and convert matrix to array
            frequencies = numpy.asarray(r['w'].T/2/math.pi)
            
            # Reshape to be scipy-friendly
            frequencies = frequencies.reshape((max(frequencies.shape),))
            
            # call scipy to interpolate
            norm_out_db_interpolated = scipy.interpolate.interp1d(frequencies, norm_out_db)
            
            self.max_attenuation_pass_band = (2e3, -1.0*norm_out_db_interpolated(2e3))
            self.min_attenuation_stop_band = (6.5e3, -1.0*norm_out_db_interpolated(6.5e3))
        #   If ANYTHING goes wrong, we just mark the circuit as bad. Lazy. (Possibly bad. Probably bad.)
        except: return None

        #   Eliminate unusable results
        if (self.max_attenuation_pass_band[1] == -0) or math.isnan(self.max_attenuation_pass_band[1]):
            return None
        if (self.min_attenuation_stop_band[1] == -0) or math.isnan(self.min_attenuation_stop_band[1]):
            return None

        if debug:
            printing.print_circuit(self.circuit)
            print "\nlog((MASB / MAPB), 10) = %f" % math.log((self.min_attenuation_stop_band[1] / self.max_attenuation_pass_band[1]), 10)
            print "Maximum attenuation in the pass band (0-%g Hz) is %g dB" % self.max_attenuation_pass_band
            print "Minimum attenuation in the stop band (%g Hz - Inf) is %g dB\n\n" % self.min_attenuation_stop_band

        #   Form a draft of the final score
        a_score = [
            math.log((self.min_attenuation_stop_band[1] / self.max_attenuation_pass_band[1]), 10),
            self.max_attenuation_pass_band[1], 
            self.min_attenuation_stop_band[1], 
            self.num_nodes,
            len(self)
        ]

        #   Weight the draft version of the final score
        return sum([a_weight * a_score for (a_weight, a_score) in zip(self.weights, a_score)])

class Population(list):
    def __init__(self, population=None, population_size=200, top_n=5, generation=0):
        self.population_size    = population_size
        self.top_n              = top_n
        self.generation         = generation

        self.repopulate(population=population, population_size=self.population_size)

    def repopulate(self, population=None, population_size=None):
        if population_size: self.population_size = population_size

        #   Make sure to append to self (a `Population`) instead of overwriting with a basic `list`
        del self[:]
        if population:
            self += population
        else:
            self += [Circuit(random=True) for i in range(0, self.population_size)]

    def recombine(self, a, b):
        a_circuit = Circuit()

        #   Create a circuit with the mean number of components of `a` and `b`, choosing 
        #   components randomly from either `a` or `b`. Renumber the components to avoid overlaps.
        for i in range(0, ((len(a) + len(b)) / 2)):
            a_part          = copy.deepcopy(random.choice(random.choice([a, b])))
            a_part.part_id  = "%s%d" % (a_part.part_id[0], a_circuit.component_types[a_part.part_id[0]][2])
            a_circuit.append(a_part)
            a_circuit.component_types[a_part.part_id[0]][2] += 1

        return a_circuit

    def simulate(self):
        while True:
            scores = []

            #   Simulate and score each member of the population
            for a_member in self:
                a_score = a_member.score()
                if a_score: scores.append((a_score, a_member))

            #   Sort the results
            scores.sort(key=lambda x: -x[0])

            #   No surviving circuits in this generation
            if not scores:
                self.repopulate()
                print "Generation %d: mulligan" % self.generation
                self.generation += 1

                #   Pause for humans to read post-generation results (Optional)
                time.sleep(1)
                continue

            #   Return a tuple of (last simulated generation, [(score, circuit)...])
            yield (self.generation, scores)
            self.generation += 1

            #   Pristine copies of the `top_n`
            new_population          =   [copy.deepcopy(a_score[1]) for a_score in scores[:self.top_n]]

            #   Select subpopulations for mutation and recombination
            mutated_population      =   (copy.deepcopy([scores[0][1]]) * self.top_n)   + \
                                        (copy.deepcopy([scores[1][1]]) * self.top_n)   + \
                                        (copy.deepcopy([scores[2][1]]) * self.top_n)   + \
                                        [copy.deepcopy(a_score[1]) for a_score in scores[:self.top_n]]
            recombined_population   = copy.deepcopy(mutated_population)

            #   Mutate copies of the `top_n`
            for a_member in mutated_population:
                a_member.mutate()

            new_population += mutated_population

            #   Recombine copies of the `top_n`
            for i in range(0, len(recombined_population) * 2):
                a_member    = random.choice(recombined_population)
                b_member    = random.choice(recombined_population)
                new_member  = self.recombine(a_member, b_member)
                
                if debug:
                    print "\nCircuit A\n---------"
                    pp(a_member)
                    print "\nCircuit B\n---------"
                    pp(b_member)
                    print "\nNew Circuit\n---------"
                    pp(new_member)
                    print

                new_population.append(new_member)

            #   Random new population
            new_population += [Circuit(random=True) for i in range(0, self.population_size - len(new_population))]

            #   Make sure to append to self (a `Population`) instead of overwriting with a basic `list`
            del self[:]
            self += new_population

if __name__ == "__main__":
    desired_score   = 1000
    top_score       = None
    a_population    = Population(population_size=20, top_n=1)
    pre_seed        = False

    if pre_seed:
        #   Create a seed circuit
        a_circuit = Circuit()
        a_circuit.component_types['R'][2] = 5
        a_circuit.component_types['L'][2] = 5
        a_circuit.component_types['C'][2] = 7
        a_circuit += [
            Resistor(   part_id='R0',   n1='n5',    n2='n3',    value=62000000),
            Resistor(   part_id='R1',   n1='n4',    n2='n5',    value=620000),
            Resistor(   part_id='R2',   n1='n3',    n2='n4',    value=680000),
            Resistor(   part_id='R3',   n1='n2',    n2='n6',    value=22),
            Resistor(   part_id='R4',   n1='n6',    n2='n1',    value=15),
            Inductor(   part_id='L0',   n1='n7',    n2='n7',    value=1.6e-06),
            Inductor(   part_id='L1',   n1='n7',    n2='n7',    value=9.1e-06),
            Inductor(   part_id='L2',   n1='0',     n2='n1',    value=3e-09),
            Inductor(   part_id='L3',   n1='0',     n2='n7',    value=3e-05),
            Inductor(   part_id='L4',   n1='0',     n2='0',     value=1e-09),
            Capacitor(  part_id='C0',   n1='n7',    n2='n2',    value=1.5e-09),
            Capacitor(  part_id='C1',   n1='0',     n2='n6',    value=5.6e-07),
            Capacitor(  part_id='C2',   n1='0',     n2='n3',    value=3.3e-10),
            Capacitor(  part_id='C3',   n1='n6',    n2='0',     value=2.7e-07),
            Capacitor(  part_id='C4',   n1='n5',    n2='n1',    value=6.8e-11),
            Capacitor(  part_id='C5',   n1='n7',    n2='n7',    value=2.2e-08),
            Capacitor(  part_id='C6',   n1='0',     n2='n4',    value=6.8e-09)
        ]

        #   Append the seed circuit to the population
        a_population.append(a_circuit)
        a_population.population_size += 1

    for (generation, scores) in a_population.simulate() :
        #   Print out the remaining circuits
        top_score = scores[0]
        print "Scores\n------\n"
        pp(sorted(scores, key=lambda x: x[0]))  #   Print scores in reverse order for easier viewing
        print "\n"        

        #   Print the top score
        print "Top Score (generation %d): %s\n\n" % (generation, top_score[0])
        printing.print_circuit(top_score[1].circuit)
        print "\nlog((MASB / MAPB), 10) = %f" % math.log((top_score[1].min_attenuation_stop_band[1] / top_score[1].max_attenuation_pass_band[1]), 10)
        print "Maximum attenuation in the pass band (0-%g Hz) is %g dB" % top_score[1].max_attenuation_pass_band
        print "Minimum attenuation in the stop band (%g Hz - Inf) is %g dB\n\n" % top_score[1].min_attenuation_stop_band

        #   Good Enough answer found
        if top_score[0] > desired_score:
            break

        #   Pause for humans to read post-generation results (Optional)
        time.sleep(2)
