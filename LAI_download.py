

import credentials
from creds import *
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import requests
import getpass
import pandas as pd
from sentinelhub import (SHConfig, DataCollection, SentinelHubCatalog, SentinelHubRequest, BBox, bbox_to_dimensions, CRS, MimeType, Geometry)

# access token 얻는 함수 정의
def get_access_token(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Access token creation failed. Reponse from the server was: {r.json()}"
        )
    return r.json()["access_token"]

# copernicus 나의 로그인 정보 
access_token = get_access_token("sosyj0325@unist.ac.kr", "Liziwon1324!@")

access_token = get_access_token(
    getpass.getpass("Enter your username"),
    getpass.getpass("Enter your password"),
)





## 여기까지가 access token 얻는 과정, 이 밑에서 데이터를 검색하고, 다운받는 과정 코드 필요

start_date = "2022-06-01"
end_date = "2022-06-10"
data_collection = "SENTINEL-2"
aoi = "POLYGON((4.220581 50.958859, 4.521264 50.953236, 4.545977 50.906064, 4.541858 50.802029, 4.489685 50.763825, 4.23843 50.767734, 4.192435 50.806369, 4.189689 50.907363, 4.220581 50.958859))"

## 추가로 해야하는 것
# = 다운로드 url 리스트 가져오는 방법
# 패치로 지역 찾는 방법 > SRID?라는게 있는가봄
# cloud로 sort해서 리스트 가져오는 법
# id = MSIL1C가 포함된 데이터를 다운, Top Of Atmosphere(TOA)가 내가 다운 받는 데이터
# MSI = MultiSpectral Instrument
# id 는 OData의 Query by attributes 항목에서 다운 받을 수 있는 코드를 찾을 수 있다...



# download_granule 코드 ...?
url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products(acdd7b9a-a5d4-5d10-9ac8-554623b8a0c9)/$value"
# 요 url의 리스트를 어떻게 구하지? 
# > 예시 APIs>OData>filter option>query by name 에 있는 것이 파일 이름으로 구성된 url, 
# 위 형식의 url 리스트를 구름, tile 조건에 맞게 만들어야한다. 
# ID와 name을 가져와서 name안에 있는 타일 이름을 토대로 url 리스트를 sort하는과정이 필요할 듯

# 추가로 적절한 지역의 데이터인지 잘 확인하고 다운로드 진행 
# + tile 이라는 개념 자체를 사용하지 않도록 copernicus에서 유도하려고 한다?
# bbox는 뭔가 통일된 좌표 시스템인 듯? 이 정보를 가지고 쉽게 tile과 위치 정보를 정의할 수 있나봄

# 모르는 것 : aoi?, bbox?, 
# European Petroleum Survey Group, EPSG 코드란 좌표 변환 해주는 시스템?인듯
# http://bboxfinder.com/#0.000000,0.000000,0.000000,0.000000   요 사이트 들어가서 좌표 or tile정보를 뽑을 수 있을 듯


session = requests.Session()
session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products(8fc3f946-f617-5536-ba3a-1363547cbb04)/$value"
response = session.get(url, allow_redirects=False)
while response.status_code in (301, 302, 303, 307):
    url = response.headers['Location']
    response = session.get(url, allow_redirects=False)

file = session.get(url, verify=False, allow_redirects=True)

with open(f"product.zip", 'wb') as p:
    p.write(file.content)

# from utils import plot_image
config = SHConfig()
config.sh_client_id = "sh-f320c9e0-c8ff-4816-9a2a-90d5b27e2127"
config.sh_client_secret = "0SHUemrn1htl4nY1NBP0WOoCWVmgBdYz"
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
config.save()
# Saved config can be later accessed with config = SHConfig("cdse")
config = SHConfig()
aoi_coords_wgs84 = [4.20762, 50.764694, 4.487708, 50.916455]
resolution = 10
aoi_bbox = BBox(bbox=aoi_coords_wgs84, crs=CRS.WGS84)
aoi_size = bbox_to_dimensions(aoi_bbox, resolution=resolution)
print(f'Image shape at {resolution} m resolution: {aoi_size} pixels')
catalog = SentinelHubCatalog(config=config)
aoi_bbox = BBox(bbox=aoi_coords_wgs84, crs=CRS.WGS84)
time_interval = '2022-08-09', '2022-09-12'
search_iterator = catalog.search(
    DataCollection.SENTINEL2_L2A,
    bbox=aoi_bbox,
    time=time_interval,
    fields={"include": ["id", "properties.datetime"], "exclude": []},
)
results = list(search_iterator)
print("Total number of results:", len(results))
results