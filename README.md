# Determination of the optimal window size for the Spatial XOR filter

All the data is separated by ';'


---
# Data folders

`data/k` => Folder with the data of the experiments for the best value for `k`

`data/windo_size` => Folder with the data of the experiments for the best window size


---
# Files
## {folder}\exp_011_{T}.data
> File with the data of the experiments, where T is the size of the array.
> The sizes of the array size used in the experiments was: 
{ 12.5k, 50k, 75k, 150k, 250k, 500k, 1M, 1.5M, 2M, 2.5M, 3M, 3.5M, 4M, 4.5M, 5M, 5.5M, 6M, 6.5M, 7M, 7.5M, 8M, 8.5M, 9M, 9.5M, 10M, 10.5M, 11M, 11.5M, 12M, 12.M, 50M }.

Data => **{k};{alpha};{z};{S};{t};{etc}**

- k = Number of hash functions
- alpha = Load factor
- z = Window size
- S = Number of successful constructions
- t = Execution time of the experiment
- etc = Additional data for debugging purposes: ((MIN_WIN, MAX_WIN), (WIN_1Q, WIN_MID, WIN_2Q)) of the iteration


# To execute
First, install the required dependency:
> pip install mmh3==3.0.0

Then, run the `main.py` script:
> python main.py

# Cite us

```
@article{https://doi.org/10.1002/spe.70009,
	author = {Diogo Rodrigues Leão, Paulo and de Souza Oliveira, Fabiano and Eustaquio Duarte Pinto, Paulo},
	title = {Determination of the Optimal Window Size for the Spatial XOR Filter},
	journal = {Software: Practice and Experience},
	keywords = {optimal window size, spatial coupling, XOR filter},
	doi = {https://doi.org/10.1002/spe.70009},
	url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.70009},
	eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/spe.70009}
}
```


