# Climate Change Visualization

This is a data analysis project for CS-106 at Calvin University. The purpose is to use processed data from credible sources like Berkeley Earth and World Bank to demostrate the fact that global warming has been existing and is getting severe.

## Dataset
The CO2 emission dataset is found from [World Bank](http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=csv) and processed by *peter-stuart-turner* on [his Github](https://github.com/peter-stuart-turner/time-series-analyses-and-climate-change/blob/master/processed_data/global_co2_emissions_per_capita.csv). The rest of processed global temperature datasets are from [Kaggle](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data) and was originally from [Berkeley Earth](http://berkeleyearth.org/data/).

## Guide
The user has to install **dash**, a Python package, to successfully run the climate_change.py in App_climate folder. Both conda and pip should work. The code is below.
```python
conda install -c conda-forge dash
```

Or

```python
pip install dash==1.7.0
```

Once all packages are installed, use *git clone* to download the repository. Then,the user can simply run climate_change.py to acquire a local link to the dashboard. 

## Reference

* http://berkeleyearth.org/data/
* https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
* https://towardsdatascience.com/interactive-dashboards-for-data-science-51aa038279e5
* http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=csv
