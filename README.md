# CWL Examples and Tutorials

This repository provides some guides on how to use cwl-eval and the framework for performing information retrieval evaluations.


## Installation

To install `cwl-eval` you need Python 3+, and run `pip install cwl-eval`, otherwise you can download it from github to get the latest: https://github.com/ireval/cwl.git


## Guides

- For a tutorial on how to use `cwl-eval` and its differences with `trec_eval` see USING-CWL-EVAL.md


## Notebook Examples

In *notebooks/*, we have provided examples in Jupyter Notebooks Using the CWL Evaluation Framework are in the notebooks directory.

- *SIGIR2019-Demo-CWL-Plots.ipynb*: shows how the CWL framework can be used to inspect the internal continuation, weight and likelihood of stopping vectors
- *SIGIR2019-Demo-Measurement-Plots*: shows the different measurements from the CWL framework provide different insights into how rankings are scored.

Assumes that the cwl framework is installed.

## Compatiability Tests

In *compatiability/*, we have provided a number of bash scripts that compare the ranking of TREC_EVAL and INST_EVAL against CWL_EVAL.

Assumes that TREC_EVAL and INST_EVAL have been installed.





