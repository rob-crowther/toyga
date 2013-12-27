#!/usr/bin/env python

import random
import ahkab
from ahkab import circuit, printing, devices
import scipy
import scipy.interpolate
import numpy
import math
import time
from pprint import pprint as pp

the_weights = [
    -1.3,   #   Maximum attenuation in the pass band
     1.0,   #   Minimum attenuation in the stop band
    -0.2,   #   Number of nodes
    -0.2,   #   Number of resistors
    -0.2,   #   Number of inductors
    -0.2    #   Number of capacitors
]

class Component(object):
    common  = list()
    value   = None
    name    = None

    def __init__(self, value=None):
        self.value = value if value else random.choice(self.common)

def Resistor(Component):
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

def Inductor(Component):
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

class Circuit(object):
    parameters  = None
    result      = None
    circuit     = None
    resistors   = None
    next_node   = 1

    def __init__(self, parameters=None):
        self.parameters             = dict()
        self.parameters['num_R']    = random.randint(1, 4)
        self.parameters['num_L']    = random.randint(1, 4)
        self.parameters['num_C']    = random.randint(1, 4)
        self.parameters['nodes']    = sum([
            self.parameters['num_R'],
            self.parameters['num_L'],
            self.parameters['num_C']])

        self.parameters['passives'] = list()

        #   Create a list of all the nodes to select from, emphasizing ground
        self.all_nodes = (['0'] * 3) + ["n%d" % i for i in range(1, self.parameters['nodes'])]

        for i in range(0, self.parameters['num_R']):
            a_resistor              = dict()
            a_resistor['name']      = "R%d" % random.randint(1, self.parameters['num_R'])
            a_resistor['ext_n1']    = random.choice(self.all_nodes)
            a_resistor['ext_n2']    = random.choice(self.all_nodes)
            a_resistor['value']     = random.choice(self.resistors)

            self.parameters['passives'].append(a_resistor)

        for i in range(0, self.parameters['num_L']):
            an_inductor             = dict()
            an_inductor['name']     = "L%d" % random.randint(1, self.parameters['num_L'])
            an_inductor['ext_n1']   = random.choice(self.all_nodes)
            an_inductor['ext_n2']   = random.choice(self.all_nodes)
            an_inductor['value']    = random.randint(0, 1000)/1000000.0

            self.parameters['passives'].append(an_inductor)

        for i in range(0, self.parameters['num_C']):
            a_capacitor             = dict()
            a_capacitor['name']     = "C%d" % random.randint(1, self.parameters['num_C'])
            a_capacitor['ext_n1']   = random.choice(self.all_nodes)
            a_capacitor['ext_n2']   = random.choice(self.all_nodes)
            a_capacitor['value']    = random.randint(0, 1000)/1000000000.0

            self.parameters['passives'].append(a_capacitor)

    #   Random correlation between parameters and simulation scores
    def simulate(self):
        if self.result: return self.result

        try:
            self.circuit = circuit.circuit(title=str(self.parameters))

            for i in range(0, self.parameters['nodes']):
                self.circuit.create_node("n%d" % self.next_node)
                self.next_node += 1
            
            for i in self.parameters['passives']:    
                if (i['name'][0] == 'R'):
                    self.circuit.add_resistor(i['name'], i['ext_n1'],  i['ext_n2'], R=i['value'])
                elif (i['name'][0] == 'L'):
                    self.circuit.add_inductor(i['name'], i['ext_n1'],  i['ext_n2'], L=i['value'])
                elif (i['name'][0] == 'C'):
                    self.circuit.add_capacitor(i['name'], i['ext_n1'],  i['ext_n2'], C=i['value'])

            voltage_step = devices.pulse(v1=0, v2=1, td=500e-9, tr=1e-12, pw=1, tf=1e-12, per=2)
            self.circuit.add_vsource(name="V1", ext_n1='n1', ext_n2='0', vdc=5, vac=1, function=voltage_step)

            ac_analysis = ahkab.new_ac(start=1e3, stop=1e5, points=100)
            self.result = ahkab.run(self.circuit, an_list=[ac_analysis])
        except:
            return None

        return self.result

    def score(self):
        print "\n\n"
        r = self.simulate()

        if not r:
            return -9000
        
        try:
            # Normalize the output to the low frequency value and convert to array
            norm_out = numpy.asarray(r['ac']['|Vn4|'].T/r['ac']['|Vn4|'].max())
            
            # Convert to dB
            norm_out_db = 20 * numpy.log10(norm_out)
            
            # Reshape to be scipy-friendly
            norm_out_db = norm_out_db.reshape((max(norm_out_db.shape),))
            
            # Convert angular frequencies to Hz and convert matrix to array
            frequencies = numpy.asarray(r['ac']['w'].T/2/math.pi)
            
            # Reshape to be scipy-friendly
            frequencies = frequencies.reshape((max(frequencies.shape),))
            
            # call scipy to interpolate
            norm_out_db_interpolated = scipy.interpolate.interp1d(frequencies, norm_out_db)
            
            max_attenuation_pass_band = (2e3, -1.0*norm_out_db_interpolated(2e3))
            min_attenuation_stop_band = (6.5e3, -1.0*norm_out_db_interpolated(6.5e3))
            
            print "Maximum attenuation in the pass band (0-%g Hz) is %g dB" % max_attenuation_pass_band
            print "Minimum attenuation in the stop band (%g Hz - Inf) is %g dB" % min_attenuation_stop_band
            
            #   Eliminate unusable results
            if (-1.0*norm_out_db_interpolated(2e3)) == -0:
                return -9000
            if (-1.0*norm_out_db_interpolated(6.5e3)) == -0:
                return -9000

            #   Form a draft of the final score
            a_score = [
                max_attenuation_pass_band[1], 
                min_attenuation_stop_band[1], 
                self.parameters['nodes'],
                self.parameters['num_R'],
                self.parameters['num_L'],
                self.parameters['num_C'],
            ]

            #   Weight the draft versions of the final scores
            return sum([a_weight * a_score for (a_weight, a_score) in zip(the_weights, a_score)])
        
        #   If ANYTHING goes wrong, we just mark the circuit as bad. Lazy. (Possibly bad. Probably bad.)
        except:
            return -9000

if __name__ == "__main__":
    desired_score   = 20
    population_size = 10
    the_population  = [Circuit() for i in range(0, population_size)]
    the_generation  = 0

    #   Loop until greated than `desired_score` 
    while True:
        the_scores = []

        #   Simulate and score each member of the population
        for a_member in the_population:
            the_scores.append((a_member.score(), a_member))

        #   Remove unusable results and sort the remainder
        the_scores = filter(lambda x: not math.isnan(x[0]), the_scores)
        the_scores = filter(lambda x: x[0] != -9000, the_scores)
        the_scores.sort(key=lambda x: -x[0])

        #   Print out the remaining circuits
        print "\n\n"
        pp(the_scores)
        print "\n"

        try:
            top_score = the_scores[0]

        #   Take a mulligan
        except IndexError:
            the_population = [Circuit() for i in range(0, population_size)]
            continue

        #   Print the top score
        print "Top Score (generation %d): score: %s\n\n" % (the_generation, top_score[0])
        printing.print_circuit(top_score[1].circuit)
        top_score[1].score()
        the_generation += 1

        #   Good Enough answer found
        if top_score[0] > desired_score:
            break

        #   Keep up to the first 3 and generate up to 97 new ones
        the_population =  [a_score[1] for a_score in the_scores[:3]]
        the_population += [Circuit() for i in range(0, 100 - len(the_population))]

        print "\n"

        #   Pause for humans to read post-generation results (Optional)
        time.sleep(10)
