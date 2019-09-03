This is a collection of general tools that might be useful for various situations.  They are grouped into different categories:

* pandas_utils: utilities that help/automate working with Pandas
* plotting: plotting utilities and wrappers around matplotlib scripts

To use these tools, do the following:
* clone the repo to some local location: 
    * git clone git@f3eaipitcap01.statcan.ca:scriand/general_utils.git DESTINATION-FOLDER
* install the repo with pip:
    * pip install -e DESTINATION_FOLDER
    * (note pip install command might need the usual certificate/other info for pip install if you don't have all the dependencies for this package installed already?)
    * (note if installing to your root python instead of a virtual environment (not a good idea generally, but just in case...) add --user to the above pip call)

Once you have it installed you can keep it updated by going back to DESTINATION_FOLDER and doing a git pull (just like any other repo)

To actually use this once installed, do something like:

```python
import pandas as pd
import general_utils.pandas_utils as gup
df = pd.DataFrame([{'col1': "text", 'col2': "1"}, {'col1': "more text", 'col2': None},])
for i in range(2):
    print(f"col2 row {i} has value of {df['col2'].values[i]} (type = {type(df['col2'].values[i])})")
#(output) col2 row 0 has value of 1 (type = <class 'str'>)
#(output) col2 row 1 has value of None (type = <class 'NoneType'>)
df['col2'] = gup.safe_astype(df['col2'], int)
for i in range(2):
    print(f"col2 row {i} has value of {df['col2'].values[i]} (type = {type(df['col2'].values[i])})")
#(output) col2 row 0 has value of 1 (type = <class 'int'>)
#(output) col2 row 1 has value of None (type = <class 'NoneType'>)
```

Future work: 

* add examples
* add additional utilities
