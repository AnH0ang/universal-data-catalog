# Config File

The keys that are currently available in the configuration file are:

* `type` - **string** - Specifies the provider used to load/save the record. You can either select one of the existing providers or one of your own custom providers.
* `file_path` - **string** - Specifies the path to the dataset.
* `read_only` - **bool** - Specifies whether the record is read-only. If this key is set to true, all operations to save the dataset are prohibited.
* `transformers` - **list[object]** - Lists one or more transformers that are executed before reading from / writing to the dataset.
