import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
from matplotlib import colors
from datetime import datetime
from pytz import timezone
from requests import get
from os.path import splitext, split
from os import remove, listdir
from re import match
import boto3
from calendar import monthrange

TIMEZONE = timezone('America/Sao_Paulo')

def get_name_file(date: str) -> str:
    return f'MERGE_CPTEC_{date}.grib2'

def download_cptec(date: str, year: int, month: str):
    file = get_name_file(date)
    url = f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{year}/{month}/{file}'
    r = get(url=url)
    r.raise_for_status()
    with open(file, 'wb') as f:
        f.write(r.content)
    return file

def process_cptec(file: str):
    # Open the GRIB2 file
    data = xr.open_dataset(file, engine='cfgrib')

    # Extract the precipitation data
    precipitation = data['prec']

    # Create a map of Brazil
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.coastlines()

    # Set the extent to cover Brazil
    ax.set_extent([-75, -35, -35, 5])  # [lon_min, lon_max, lat_min, lat_max]

    # Plot precipitation data
    # im = precipitation.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='Blues')

    # Add a colorbar and label
    # cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.005)
    # cbar.set_label('Precipitation (mm)')

    # Draw state boundaries
    states = NaturalEarthFeature(
            "cultural",
            "admin_1_states_provinces_lakes",
            "50m",
            edgecolor="black",
            facecolor="none",
        )
    ax.add_feature(states)

    schemes = {
        "colors": [
            "#FFFFFF", "#FFF9AE", "#FFDC78", "#FFAF20", "#C8CE4A",
            "#5DDA75", "#2FCB4D", "#23B52E", "#1A7A36", "#006E31",
            "#036331", "#4C9C95", "#96D2FD", "#72B3F1", "#5271F7",
            "#3327E0", "#1D1ED0", "#7070AD", "#4F4F4F",
        ],
        "bounds": [
            1, 3, 5, 7, 9,
            12, 15, 20, 25,
            30, 40, 50, 60, 80,
            100, 125, 150, 200,
        ]
    }
    COLOR_LIST = schemes.get("colors")
    BOUNDS = schemes.get("bounds")
    precipitation.plot.contourf(
            ax=ax,
            extend="both",
            cmap=colors.ListedColormap(COLOR_LIST),
            norm=colors.BoundaryNorm(
                boundaries=BOUNDS, ncolors=len(COLOR_LIST) - 2
            ),
            cbar_kwargs={
                "ticks": BOUNDS,
                "label": "Total Precipitação (mm)",
                "fraction": 0.05,
                "pad": 0.02,
                "shrink": 0.95,
            },
        )

    # Add a title
    plt.title('Precipitation in Brazil')

    # Show the plot
    file_name = f'{splitext(file)[0]}.jpeg'
    plt.savefig(file_name)
    plt.close()
    return file_name

def clean():
    for file in listdir():
        if match(r'^MERGE_CPTEC_.*', file):
            remove(file)

def upload_s3(file: str, bucket: str):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(file, bucket, split(file)[-1])

list_years = [y for y in range(2021, 2024)]
list_months = [f'{m:02d}' for m in range(1, 13)]

if __name__ == '__main__':
    BUCKET_RAW = 'raw-soybean-bucket'

    for year in list_years:
        for month in list_months:
            for day in range(1, monthrange(year, int(month))[1]):

                day = f'{day:02d}'
                date = datetime.strptime(f'{year}{month}{day}', '%Y%m%d').strftime('%Y%m%d')
                file = download_cptec(date, year, month)
                img = process_cptec(file)
                upload_s3(img, BUCKET_RAW)
                print(f'Uploaded {file} to {BUCKET_RAW} sucessfully!')
                clean()
# TODO: rodar a noite 2021 pra frente