import os
import re
import sys
import json
import random
import getpass
import datetime
import rasterio
import requests
import credentials
import numpy as np
import pandas as pd
import matplotlib.image
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

from creds import *
from pathlib import Path
from rasterio.windows import Window
from sentinelhub import (SHConfig, DataCollection, SentinelHubCatalog, SentinelHubRequest, BBox, bbox_to_dimensions, CRS, MimeType, Geometry)
from utils import plot_image


config = SHConfig()
config.sh_client_id = getpass.getpass("Enter your SentinelHub client id")
config.sh_client_secret = getpass.getpass("Enter your SentinelHub client secret")
config.sh_client_id = 'sosyj0325@unist.ac.kr'
config.sh_client_secret = 'Liziwon1324!@'
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
# config.save("cdse")
config = SHConfig()
config.instance_id = "my-instance-id"
config.save("my-profile")



config = SHConfig()
config.sh_client_id = 'sosyj0325@unist.ac.kr'
config.sh_client_secret = 'Liziwon1324!@'
config.sh_base_url = 'https://sh.dataspace.copernicus.eu'
config.sh_token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'

betsiboka_coords_wgs84 = (126.562497,37.718592,127.968747,38.822593 )

resolution = 60
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")

################################################################################
from sentinelhub import DataCollection
from sentinelhub import CRS, BBox, MimeType, SentinelHubRequest, SHConfig

DataCollection.SENTINEL2_L1C

# Write your credentials here if you haven't already put them into config.toml
CLIENT_ID = "sosyj0325@unist.ac.kr"
CLIENT_SECRET = "Liziwon1324!@"

config = SHConfig()
if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET


# Columbia Glacier, Alaska
glacier_bbox = BBox((126.562497,37.718592,127.968747,38.822593), crs=CRS.WGS84)
glacier_size = (700, 466)
time_interval = "2020-07-15", "2020-07-16"

evalscript_true_color = """
//VERSION=3

function setup() {
    return {
        input: [{
            bands: ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B11', 'B12']
        }],
        output: {
            bands: 12
        }
    };
}

function evaluatePixel(sample) {
    return [3];
}
"""

request = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=time_interval,
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    bbox=glacier_bbox,
    size=glacier_size,
    config=config,
)

image = request.get_data()[0]
plt.imshow(image)

# The following is not a package. It is a file utils.py which should be in the same folder as this notebook.
from utils import plot_image

plot_image(image, factor=3.5 / 255, clip_range=(0, 1))


