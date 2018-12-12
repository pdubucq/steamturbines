# Optimization Models for Steam Turbines lecture at TUHH

The files in this library are used in the lecture "Steam Turbine" at Hamburg University of Technology.

## Getting Started

You can use the models in this repository on Azure Notebooks or on a local machine using a Python distribution like Anaconda.

### Running the code using Azure Notebooks

To work with the files in this library using [Azure Notebooks](https://notebooks.azure.com/pascal-dubucq/libraries/tuhh) only a Webbrowser and a Microsoft Account is needed. To install the libraries required to run the code, first you need to open and run the setup.ipynb Notebook, then you are good to go.

Alternatively, go to console, start ipython and run
'''
conda install -c conda-forge pulp
'''

### Running the code locally

To run the models with anaconda install the dependencies using the environment.yml.

```python
conda env create -f environment.yml
conda activate steamturbines
```
## Authors

Pascal Dubucq

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The optimzation models are all using PuLP and pandas. Thanks for the great work to the developers.
