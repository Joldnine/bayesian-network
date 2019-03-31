# bayesian-network
A python implemention for checking D-separation in a Bayesian Networks (BN).
The main algorithm follows
```
Koller and Friedman (2009), "Probabilistic Graphical Models: Principles and Techniques" (page 75)
```

# Input and Ouput
## Example
### Input
#### graph.txt
```
4
1 2
1 4
2 3
2 4
3 4
```
which implies a graph:
```
4<--------
^    |    |
|    |    |
1 -> 2 -> 3
```
#### queries.txt
```
{1} {3} {2}
{1} {2} {}
```
which implies queries to be checked:
```
{1} ⊥ {3} | {2}
{1} ⊥ {2} |  ∅
```
#### Run:
```
$ python d-sep.py graph.txt queries.txt
```

### Output
```
True
False
```
