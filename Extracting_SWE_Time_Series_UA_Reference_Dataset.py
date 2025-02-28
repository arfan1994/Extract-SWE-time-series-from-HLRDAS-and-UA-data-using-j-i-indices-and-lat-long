# -*- coding: utf-8 -*-

import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

## For HRLDAS
# Path to the HRLDAS SNEQV NetCDF file
hrldas_file = '/glade/derecho/scratch/aarshad/HRLDASOUT/SNEQV_Nov2017Oct2018_controlrun.nc'
wrfinput_file = '/glade/work/aarshad/CONUS404_data/wrfinput_d01.oct011979_WUS.nc'

# Open the HRLDAS dataset
hrldas_ds = xr.open_dataset(hrldas_file)

# Open the WRF input file to get XLAT and XLONG
with xr.open_dataset(wrfinput_file) as wrf_ds:
    xlat = wrf_ds['XLAT'][0, :, :]
    xlon = wrf_ds['XLONG'][0, :, :]

# Define target latitude and longitude
lat0, lon0 = 48.8, -121.9
# Find nearest i, j indices
a = np.abs(xlat - lat0) + np.abs(xlon - lon0)
j, i = np.unravel_index(a.argmin(), a.shape)

# Extract the SNEQV time series at the closest grid point
SNEQV_timeseries = hrldas_ds['SNEQV'].isel(south_north=j, west_east=i)

# Ensure time is properly sorted
SNEQV_timeseries = SNEQV_timeseries.sortby('time')  # Ensure chronological order
time_values_sneqv = SNEQV_timeseries['time'].values  # Extract time values

# Convert to Pandas DataFrame for CSV export
df_sneqv = pd.DataFrame({'Time': time_values_sneqv, 'SNEQV (mm)': SNEQV_timeseries.values})
csv_path_sneqv = "/glade/derecho/scratch/aarshad/AllCodes/SNEQV_timeseries_HRLDAS.csv"
df_sneqv.to_csv(csv_path_sneqv, index=False)
print(f"HRLDAS Time series data exported to: {csv_path_sneqv}")

## For UA Snow Data
# Path to the UA reference NetCDF file
ua_file = '/glade/derecho/scratch/aarshad/ReffSnowData/UA_SWE_Regridded_to_HRLDAS.nc'

# Open the dataset
ua_ds = xr.open_dataset(ua_file)

# Select the time series at the specified latitude and longitude
SWE_timeseries = ua_ds['SWE_regridded'].isel(south_north=j, west_east=i)

# Ensure time is properly converted
SWE_timeseries = SWE_timeseries.sortby('time')  # Ensure chronological order
time_values_ua = SWE_timeseries['time'].values  # Extract time values

# Convert to Pandas DataFrame for CSV export
df_ua = pd.DataFrame({'Time': time_values_ua, 'SWE (mm)': SWE_timeseries.values})
csv_path_ua = "/glade/derecho/scratch/aarshad/AllCodes/SWE_timeseries_UA.csv"
df_ua.to_csv(csv_path_ua, index=False)
print(f"UA Time series data exported to: {csv_path_ua}")

## **Plot both time series on the same graph**
plt.figure(figsize=(10, 5))

# Plot UA SWE data
plt.plot(time_values_ua, SWE_timeseries, label='UA SWE (mm)', color='blue')

# Plot HRLDAS SNEQV data
plt.plot(time_values_sneqv, SNEQV_timeseries, label='HRLDAS SNEQV (mm)', color='red')

# Formatting the x-axis with date labels
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotating and aligning the date labels
plt.gcf().autofmt_xdate()

# Adding titles and labels
plt.title('Comparison of UA SWE and HRLDAS SNEQV Time Series`')
plt.xlabel('Time')
plt.ylabel('Snow Equivalent (mm)')
plt.legend()
plt.grid()
plt.tight_layout()

# Save the plot as a PNG file
plot_path = "/glade/derecho/scratch/aarshad/AllCodes/UA_SWE_vs_HRLDAS_SNEQVv1.png"
plt.savefig(plot_path, format='png')
plt.close()

print(f"Plot saved at: {plot_path}")
