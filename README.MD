# Differentiable Inductive Logic Programming

Python and TensorFlow implementation of the paper "Learning Explanatory Rules from Noisy Data." Evans Richard and Edward Grefenstette. Journal of Artificial Intelligence Research 61 (2018): 1-64.

Paper: https://arxiv.org/pdf/1711.04574.pdf

DeepMind blog: https://deepmind.com/blog/learning-explanatory-rules-noisy-data/

To run the code you create a folder. In our case the folder `example/`. It has three files.

- `facts.ilp` : contains the facts
- `negative.ilp`: contains the negative examples
- `positive.ilp`: contains the positive examples

You can run the code by:

```
python run.py example
```

### Note

We have restricted the facts predicates to arity 1 and the iron producing predicates should adhere to the following rules:

The code currently only supports one predicate learning at a time

This is a code in progress. Please raise issues and suggestions to improve it
