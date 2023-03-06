# ntcrypy
This is a Python module implementing algorithms taught in MAT4930 - Number Theory &amp; Cryptography.

## Setup

1. Install Python. There are many ways to do this. I personally prefer creating an [Anaconda](https://www.anaconda.com/products/individual) environment, but any up-to-date Python installation should work.

2. Clone the repository:

	```
	git clone https://github.com/butakow/ntcrypy
	```

3. To call the algorithms, include `ntcrypy` in the same directory as your Python scripts and import the relevant submodule, for example:

	```py
	from ntcrypy import numt
	solutions = numt.solve_congruence(114, 33, 18)
	```
