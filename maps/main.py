import cfgrib
import xarray

# Import data
cptec_daily = cfgrib.open_datasets('./MERGE_CPTEC_20230922.grib2')[0]

x = cptec_daily.prec
x.plot()
