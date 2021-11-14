# Example

In this section we exaplain how to set up `universal-data-catalog` and configure the associated `catalog.yml` config file. For that we will use the commonly used titanic dataset as an example. The steps are as follows:

* Download the titanic dataset
* Register the data set using the `catalog.yml`
* Read the dataset from python using the `DataCatalog` interface
* Save the dataset from python using the `DataCatalog` interface

## 1. Get Data

In this example we use the titanic dataset. You can download it from [here](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv). Create a `data` folder and download the dataset into it. In addition create a empty `catalog.yml` and a `main.py`. We will disscuss their contents later. You file structure should look like this.

```
├── catalog.yml
├── data
│   └── titanic.csv
└── main.py
```

## 2. Register the dataset in `catalog.yml`

You need to register you dataset first in a `catalog.yml` so that it can later by loaded by the `DataLoader`. For each dataset you need to add a named entry into the `catalog.yml`. The entry should contain the file path, type of dataset and any other required arguments. The following is a example config file for a `.csv` file.


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

To load the dataset you first have to create a `DataCatalog` object that acts as an interface for all data read and writes.
The advantage of that is that the load logic for the csv file is complely uncoupled from the loading interface. We can load the file under `data/titianic.csv` by simply calling the `.load()` method form the `DataCatalog` class. Under the hood `pd.read_csv` is used to load the file. This was specified in the `type` key in `catalog.yml`. All the arguments under `load_args` in `catalog.yml` are passed as extra argments to `pd.read_csv`. With that you can customize the loading behaviour form the config file instead of relying on hard coded values. To load the dataset run:

```python
from universal_data_catalog.data_catalog import DataCatalog

catalog = DataCatalog("catalog.yml", conf)
df = catalog.load("titanic")
```

Verify that you sucessfully loaded the titanic dataset by running the following command. It should return the first five rows containing passanger information from the titianic.

```
df.head(5)
```

## 3. Save a modified dataset back to the data catalog

Next we want to modify the loaded dataset and save the result back into a csv. This can be done just by simply using the `.save` method.
Run the following command and verify that you saved a modifies version of the dataset by looking at the file under `data/titianic.csv`.

```python
df_queried = df.query("Embarked == 'S'")
catalog.save("titanic", df_queried)
```
