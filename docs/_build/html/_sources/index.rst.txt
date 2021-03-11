.. Quantum Computing Project documentation master file, created by
   sphinx-quickstart on Sat Mar  6 18:43:57 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Quantum Computing Project's documentation!
=====================================================

This is the documentation for the Quantum Computing Project Course at the University of Edinburgh. 
In this project, we create two different implementations of quantum circuits which we use to explore 
Grover’s Algorithm. 

The two implementations were created in order to test diifferent techniques of creating this 
quantum algorithm and to test across each other for parts that make the algorithm more efficient.
We decided to include both in our project because they employ different techniques and helped 
us understand the algorithm from two different perspectives.

The first implementation --NAME--, is allowing the User to build their own circuit on the go, 
create custom circuits and manually code the algorithm needed. It explores the Grover’s 
algorithm both numrically and geometrically as it can plot visually the results on a given 
axis of rotation. It is using a SparseMatrix program that we created in order to make the 
computations as efficient as possible. 

Usage:

--Add  usage--

The second implementation --NAME--, has predefined circuits for the Grover algorithm 
and an example of the use of Quantum Teleportation. It can visually show the probabilities 
of finding a state as an animation and allows the User through prompts to explore Quantum 
Teleportation by defining Alice’s and Bob’s states. It is not using a SparseMatrix Implementation, 
instead it uses the numpy.kchron library and numpy.dot for its computations.

Usage:

--Add  usage--

Sample Results:

--Add results--

A comparison between the two implementations in their quest of finding the 
required state through a Grover’s algorithm has shown …

Trial equation:

.. math::

   \frac{ \sum_{t=0}^{N}f(t,k) }{N}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules2
   modules





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
