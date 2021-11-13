# What is universal-data-catalog ?

The goal of `universal-data-catalog` is to act as abstaction layer on data IO targeted at small to medium sized data science projects. 
Instead of hard codeding data interface in `pandas`, the configuration is instead loaded from a config file which acts as a data catalog. The concept is borrowed from [kedro](https://github.com/quantumblacklabs/kedro) data catalogs.

# Getting Started

See [Example](logic/example.md) for a minimal example of how to set up the data catalog.

# Code Documentation

See [Code Documentation](code/data_catalog.md).