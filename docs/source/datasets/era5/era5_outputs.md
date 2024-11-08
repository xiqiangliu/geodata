# Generating Outputs with ERA5 Data

<!-- We may need to overhaul this section after the model module becomes stable! -->

**geodata** currently supports the following wind outputs using ERA5 data from the [Copernicus Data Store](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview).

* Wind generation time-series (`wind`)
* Wind speed time-series (`windspd`)
* Solar photovoltaic generation time-series (`pv`)

## Supported ERA5 Outputs

### Wind Generation Time-series

Convert wind speeds for turbine to wind energy generation.

```python
cutout.wind(turbine: str | dict[str, str], smooth: bool = False)
```

#### Parameters

* `cutout` - `Cutout` -  A cutout created by `geodata.Cutout()`
* `turbine` - `str | dict` - Name of a turbine known by the reatlas client or a turbineconfig dictionary with the keys 'hub_height' for the hub height and 'V', 'POW' defining the power curve.  For a full list of currently supported turbines, see [the list of turbines here.](https://github.com/GeodataTools/geodata/tree/master/src/geodata/resources/windturbine)
* `smooth` - `bool | dict` - If `True`, smooth power curve with a gaussian kernel as determined for the Danish wind fleet to Delta_v = 1.27 and sigma = 2.29. A dict allows to tune these values.

*Note*: You can also specify all of the general conversion arguments documented in the `convert_and_aggregate` function (e.g. `var_height='lml'`).

#### Example Code

```python
ds_wind = cutout.wind(turbine="Suzlon_S82_1.5_MW", smooth=True)
ds_wind.to_dataframe(name="wind")
```

### Wind Speed Time-series

Extract wind speeds at given height (ms-1)


```
geodata.convert.windspd(cutout: geodata.Cutout, **params)
```

#### Parameters

* `cutout` - `str` -  A cutout created by `geodata.Cutout()`
* `**params` - Must have 1 of the following:
    - `turbine` - `str | dict` - Name of a turbine known by the reatlas client or a turbineconfig dictionary with the keys 'hub_height' for the hub height and 'V', 'POW' defining the power curve.  For a full list of currently supported turbines, [the list of turbines here.](https://github.com/GeodataTools/geodata/tree/master/src/geodata/resources/windturbine)
    - `hub-height` - `int` - Extrapolation height (m)
*Note*: You can also specify all of the general conversion arguments documented in the `convert_and_aggregate` function (e.g. `var_height='lml'`).
#### Example Code

```python
ds_windspd = cutout.windspd(turbine='Vestas_V66_1750kW')
ds_windspd.to_dataframe(name = 'windspd')
```


### Solar photovoltaic generation time-series

Convert downward-shortwave, upward-shortwave radiation flux and ambient temperature into a pv generation time-series.

```python
cutout.pv(panel, orientation, clearsky_model)
```

#### Parameters

* `cutout` - **string** -  A cutout created by `geodata.Cutout()`
* `panel` - string - Specify a solar panel type on which to base the calculation.  **geodata** contains an internal solar panel dictionary with keys defining several solar panel characteristics used for the time-series calculation.  For a complete list of included panel types, see [the list of panel types here.](https://github.com/east-winds/geodata/tree/master/geodata/resources/solarpanel)
* `orientation` - str, dict or callback - Panel orientation can be chosen from either `latitude_optimal`, a constant orientation such as `{'slope': 0.0,'azimuth': 0.0}`,  or a callback function with the same signature as the callbacks generated by the `geodata.pv.orientation.make_*` functions.
* (optional) clearsky_model - string or None - 	Either the `simple` or the `enhanced` Reindl clearsky model. The default choice of None will choose dependending on data availability, since the `enhanced` model also incorporates ambient air temperature and relative humidity.

#### Example Code and Result

```python
ds_pv = geodata.convert.pv(panel="KANEKA", orientation = "latitude_optimal")
ds_pv.to_dataframe(name = 'pv')
```

## Example Output

With the full list of supported ERA5 outputs above, we can see an example of generating output ERA5 data from the [Copernicus Data Store](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview).


### Setup

Let's assume we've created an ERA5 cutout along the following lines:

```python
cutout = geodata.Cutout(name="era5-europe-example",
    module="era5",
    weather_data_config="era5_monthly",
    xs=slice(30, 41.56244222),
    ys=slice(33.56459975, 35),
    years=slice(2011, 2011),
    months=slice(1,1)
)
```

Note that unlike datasets, we don't need explicitly prepare a cutout. Geodata will prepare the cutout automatically if it's not ready. We can now use this cutout to generate datasets.

### Creating a Solar photovoltaic (pv) generation time-series

To create a pv generation time-series, we can use the following code with our ERA5 cutout:


```python
ds = cutout.pv(panel="KANEKA", orientation="latitude_optimal")
```

Some information about the parameters:
* `panel` - string - Specify a solar panel type on which to base the calculation.  **geodata** contains an internal solar panel dictionary with keys defining several solar panel characteristics used for the time-series calculation.  For a complete list of included panel types, see [the list of panel types here.](https://github.com/east-winds/geodata/tree/master/geodata/resources/solarpanel)
* `orientation` - str, dict or callback - Panel orientation can be chosen from either `latitude_optimal`, a constant orientation such as `{'slope': 0.0,'azimuth': 0.0}`,  or a callback function with the same signature as the callbacks generated by the `geodata.pv.orientation.make_*` functions.
* (optional) clearsky_model - string or None - 	Either the `simple` or the `enhanced` Reindl clearsky model. The default choice of None will choose dependending on data availability, since the `enhanced` model also incorporates ambient air temperature and relative humidity.


The convert function returns an xarray dataset, which is an in-memory representation of a NetCDF file:

```
<xarray.DataArray 'AC power' (y: 5, time: 744, x: 47)>
array([[[0., 0., 0., ..., 0., 0., 0.],
        [0., 0., 0., ..., 0., 0., 0.],
        [0., 0., 0., ..., 0., 0., 0.],

Coordinates:
    lon      (x) float32 30.0 30.25 30.5 30.75 31.0 ... 40.75 41.0 41.25 41.5
    lat      (y) float32 34.815 34.565 34.315 34.065 33.815
  * x        (x) float32 30.0 30.25 30.5 30.75 31.0 ... 40.75 41.0 41.25 41.5
  * y        (y) float32 34.815 34.565 34.315 34.065 33.815
  * time     (time) datetime64[ns] 2011-01-01 ... 2011-01-31T23:00:00
```

To convert this array to a more conventional dataframe, we can run:

```python
df = ds.to_dataframe(name='pv')
```

which converts the xarray dataset into a pandas dataframe.


The result is a dataset with an observation for each time period (in this ERA5 case, hourly) and geographic point with the calculated pv generation for each observation.

Finally, we can run something like:

```python
df.to_csv('era5_pv_data.csv')
```

to output the data to csv for use in other applications.
