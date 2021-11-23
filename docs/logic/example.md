# Example

In this chapter you will learn how to set up `universal-data-catalog` and configure the associated `catalog.yml` configuration file. To do this, we use the widely used titanic dataset as an example. The steps are as follows:

* Download the Titanic dataset.
* Register the dataset using the `catalog.yml` file.
* Read the dataset from Python using the `DataCatalog` interface.
* Save the dataset in Python using the `DataCatalog` interface.


## 1. Get Data

In this example, we use the Titanic dataset. You can download it from [here](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv). Create a folder `data` and download the dataset into this folder. Also create an empty `catalog.yml` and a `main.py`. We will discuss their contents later. Your file structure should look like this.

```
├── catalog.yml
├── data
│   └── titanic.csv
└── main.py
```

## 2. Register the dataset in `catalog.yml`

You must first register your record in a `catalog.yml` so that it can later be loaded by the `DataLoader`. For each dataset you need to add a named entry in the `catalog.yml`. The entry should contain the file path, type of record and any other required arguments. Below is an example of a configuration file for a `.csv` file.

```yaml
titanic:
  filepath: data/titanic.csv
  type: pandas.CSVDataSet
  load_args:
    sep: ","
  save_args:
    index: False
```

## 3. Load the titanic dataset from the data catalog

To load the dataset, you must first create a `DataCatalog` object that serves as the interface for all read and write operations.
This has the advantage that the load logic for the csv file is completely decoupled from the load interface. We can load the file under `data/titianic.csv` by simply calling the `.load()` method of the `DataCatalog` class. Under the hood, `pd.read_csv` is used to load the file. This was specified in the `type` key in `catalog.yml`. All arguments under `load_args` in `catalog.yml` are passed as additional arguments to `pd.read_csv`. This allows you to customize the loading behavior via the configuration file, rather than relying on hard-coded values. To load the dataset, execute:


```python
from universal_data_catalog.data_catalog import DataCatalog

catalog = DataCatalog("catalog.yml", conf)
df = catalog.load("titanic")
```

Verify that you have successfully loaded the Titanic record by running the following command. It should return the first five lines of passenger information from Titanic.

```
df.head(5)
```

## 3. Save a modified dataset back to the data catalog

Next we want to change the loaded record and save the result in a csv file. You can easily do this with the `.save` method. Under the hood all arguments that are specified in the `save_args` keys are passed to the `pd.DataFrame.to_csv()` function. In this case this is just `index=False`.
Run the following command and make sure you have saved a modified version of the dataset by looking at the file at `data/titianic.csv`.

```python
df_queried = df.query("Embarked == 'S'")
catalog.save("titanic", df_queried)
```
