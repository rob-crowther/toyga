toyga
=====

This was originally posted as an entry on 
[longchute](https://longchute.heroku.com/2013/12/27/toy-genetic-algorithm-part-2/). It uses the
`simulate` function of a `Circuit` to drive a circuit simulator 
([Ahkab](https://ahkab.github.com/ahkab/)) with a `Population` of random `Circuit`s made of random 
`Component`s (`Resistor`, `Inductor`. and `Capacitor`) representing low-pass filters. It runs an 
AC analysis and minimizes the maximum attenuation in the pass band and maximizes the minimum 
attenuation in the stop band. If `pre_seed` is altered to `pre_seed = True`, the population will 
be seeded with two pre-existing circuits found during earlier runs.

The `score` code in `Circuit` is largely derived from 
[this example](https://github.com/ahkab/ahkab/wiki/Example:-Python-API). A `Population` holds 
`population_size` `Circuit`s. When the `simulate` generator of a `Population` is iterated over, 
the `score` and `simulate` methods of each `Circuit` in the `Population` are called. Circuits that 
fail to simulate correctly are removed from the scoring before being returned. 

In each generation:

* the best `top_n` are copied unmutated, 
* the top 3 are copied `top_n` times and mutated, 
* the `top_n` are copied and mutated, 
* the top 3 are copied `top_n` times and recombined, 
* the `top_n` are copied and recombined, 
* and the rest are regenerated randomly. 

`mutate` has a random chance of `mutate_add`, `mutate_delete`, `mutate_value`, `mutate_node`, or 
no effect. Recombination selects randomly from the pool of potential circuits and selects random 
components from the two circuits to form a new circuit of the average size of the parent circuits. 
All circuits being `recombine`d are done in a single pass. If no viable scores exist in a 
generation, the population is `repopulate`d.

 **Note**: This expects a folder (`ramdisk`) within the current directory. Ahkab uses this as a 
 scratch pad for simulation results. Ahkab's `cvslib` expects a string for `filename`, so passing 
 a `tempfile.SpooledTemporaryFile` isn't possible. You should consider mounting a ramdisk at 
 `ramdisk` for increased speed and reduced wear on your drive. For example:

>
    $ mkdir ramdisk
    $ sudo mount -t tmpfs none ramdisk

If you want to see the raw results of Ahkab's analysis, you can `cat ramdisk/sim.ac`, or for 
near-realtime viewing, you can `watch -n0.1 cat ramdisk/sim.ac`. You can set `debug = True` to
increase the simulation verbosity and include mutation and recombination details.

 This is tested on Python 2.7.6 with 
 [Ahkab fbd9777e7a](https://github.com/ahkab/ahkab/commit/fbd9777e7ad1a8afbdef18d68c2b2be827d61a8c), SciPy 0.12.1, NumPy 1.7.1, and SymPy 0.7.2. 

**Usage**: `./toyga.py`

**Sample Output**:

>
    [(60.202476256287355,
      [<__main__.Resistor object at 0x3925e90> R3 0 n4 100000,
       <__main__.Resistor object at 0x3925ed0> R4 n5 0 300,
       <__main__.Resistor object at 0x3925450> R5 n2 n3 330,
       <__main__.Resistor object at 0x3925f90> R6 n8 n6 160,
       <__main__.Inductor object at 0x39256d0> L0 n8 n5 6.2e-08,
       <__main__.Inductor object at 0x3925690> L1 n4 n6 3.3e-07,
       <__main__.Inductor object at 0x3929c90> L2 n1 n3 1.3e-08,
       <__main__.Capacitor object at 0x3929fd0> C1 n2 n7 8.2e-08,
       <__main__.Capacitor object at 0x3929ed0> C2 n7 n5 6.8e-06,
       <__main__.Capacitor object at 0x3929e10> C3 n6 0 3.9e-07]),
>
    ...
>
    Top Score (generation 55): 60.2024762563
>
    * TITLE: Untitled
    R3 0 n4 100000
    R4 n5 0 300
    R5 n2 n3 330
    R6 n8 n6 160
    L0 n8 n5 6.2e-08
    L1 n4 n6 3.3e-07
    L2 n1 n3 1.3e-08
    C1 n2 n7 8.2e-08
    C2 n7 n5 6.8e-06
    C3 n6 0 3.9e-07
    V1 n1 0 type=vdc vdc=5 vac=1 arg=0 type=pulse v1=0 v2=1 td=5e-07 per=2 tr=1e-12 tf=1e-12 pw=1
    (models and analysis directives are omitted)
    log((MASB / MAPB), 10) = 4.961829
    Maximum attenuation in the pass band (0-2000 Hz) is 3.33976e-05 dB
    Minimum attenuation in the stop band (6500 Hz - Inf) is 3.05875 dB