# spei 추출 코드

import xarray as xr
import numpy as np 
import pandas
from scipy.interpolate import griddata
import rasterio as rio
import matplotlib.pyplot as plt 
import glob 

path = r"/share/drought-3/intern/jwlee/moved/Correlation_file"
flist = glob.glob("/share/drought-3/intern/jwlee/moved/Correlation_file/*_rVP.nc")
print(flist)

appenddata = []
z = np.zeros((708,1609))
# z[z==0]=-1

appenddata.append(z)

for i in range(len(flist)):
    data = xr.open_dataset(flist[i])
    data_arr = np.array(data['Correlation'])
    data_arr = np.nan_to_num(data_arr)
    appenddata.append(data_arr)

appenddata.append(z)

appendarray = abs(np.array(appenddata))
nanarray=np.nan_to_num(appendarray)

argm = np.argmax(abs(appendarray), axis=0)
nmax = np.nanmax(appendarray, axis=0)
appenddata

# argm의 자료형이 인데, nan은 float로 설정되어있기 때문에 타입을 바꿔야했음
argm = argm.astype(float)
argm[argm==0] = np.nan
nmax[nmax==0] = np.nan

plt.imshow(argm);plt.colorbar()
plt.imshow(nmax);plt.colorbar()
# 이제 nmax, argm, t, v, p weight의 데이터를 좌표와 함께 저장
# 문제는 어떻게 argm과 동일한 t, v, p의 값을 가져오느냐... 
# 먼저 모든 파일을 xr로 열어서 ~ = data['TCI~'] 와 같은 형태로 다 열어둬야함 
# 모든 것들을 1, ?의 형태로 순서 맞춰서 reshape한 다음에 
# for문으로 먼저 argm를 이용해서 if 문 거치게 한 뒤에 맞는 것을 갖고와서 append? or 걍 저장 >> 일단 먼저 동일한 크기의 배열을 만들어주자

result = np.zeros((5,708,1609))
reargm = argm.reshape(708*1609, order='C')
renmax = nmax.reshape(708*1609, order='C')

f01t_data = xr.open_dataset(flist[0])['TCI_weight']
f01v_data = xr.open_dataset(flist[0])['VCI_weight']
f01p_data = xr.open_dataset(flist[0])['PCI_weight']
f01c_data = xr.open_dataset(flist[0])['Correlation']

f03t_data = xr.open_dataset(flist[1])['TCI_weight']
f03v_data = xr.open_dataset(flist[1])['VCI_weight']
f03p_data = xr.open_dataset(flist[1])['PCI_weight']
f03c_data = xr.open_dataset(flist[1])['Correlation']

f06t_data = xr.open_dataset(flist[2])['TCI_weight']
f06v_data = xr.open_dataset(flist[2])['VCI_weight']
f06p_data = xr.open_dataset(flist[2])['PCI_weight']
f06c_data = xr.open_dataset(flist[2])['Correlation']

f09t_data = xr.open_dataset(flist[3])['TCI_weight']
f09v_data = xr.open_dataset(flist[3])['VCI_weight']
f09p_data = xr.open_dataset(flist[3])['PCI_weight']
f09c_data = xr.open_dataset(flist[3])['Correlation']

f12t_data = xr.open_dataset(flist[4])['TCI_weight']
f12v_data = xr.open_dataset(flist[4])['VCI_weight']
f12p_data = xr.open_dataset(flist[4])['PCI_weight']
f12c_data = xr.open_dataset(flist[4])['Correlation']

for j in range(708*1609):
    m = j //1609
    n = j % 1609
    if np.isnan(reargm[j]):
        if j%1000==0:
            print(j, end=' | ')
        result[:, m, n] = np.nan    
        continue
    elif reargm[j]==5:
        result[0, m, n] = f12t_data[m, n]
        result[1, m, n] = f12v_data[m, n]
        result[2, m, n] = f12p_data[m, n]
        result[3, m, n] = f12c_data[m, n]
        result[4, m, n] = 12
        if j%500==0:
            print(j)

    elif reargm[j]==4:
        result[0, m, n] = f09t_data[m, n]
        result[1, m, n] = f09v_data[m, n]
        result[2, m, n] = f09p_data[m, n]
        result[3, m, n] = f09c_data[m, n]
        result[4, m, n] = 9
        if j%500==0:
            print(j)

    elif reargm[j]==3:
        result[0, m, n] = f06t_data[m, n]
        result[1, m, n] = f06v_data[m, n]
        result[2, m, n] = f06p_data[m, n]
        result[3, m, n] = f06c_data[m, n]
        result[4, m, n] = 6
        if j%500==0:
            print(j)

    elif reargm[j]==2:
        result[0, m, n] = f03t_data[m, n]
        result[1, m, n] = f03v_data[m, n]
        result[2, m, n] = f03p_data[m, n]
        result[3, m, n] = f03c_data[m, n]
        result[4, m, n] = 3
        if j%500==0:
            print(j)

    elif reargm[j]==1:
        result[0, m, n] = f01t_data[m, n]
        result[1, m, n] = f01v_data[m, n]
        result[2, m, n] = f01p_data[m, n]
        result[3, m, n] = f01c_data[m, n]
        result[4, m, n] = 1
        if j%500==0:
            print(j)

    else : 
        print('out of prediction')

lon, lat = np.array(data['lon']), np.array(data['lat'])

TCI_weight = xr.DataArray(result[0],
                   dims=["y", "x"],
                   coords=dict(lat=(["y", "x"], lat), lon=(["y", "x"], lon))
                   )
VCI_weight = xr.DataArray(result[1],
                   dims=["y", "x"],
                   coords=dict(lat=(["y", "x"], lat), lon=(["y", "x"], lon))
                   )
PCI_weight = xr.DataArray(result[2],
                   dims=[ "y", "x"],
                   coords=dict(lat=(["y", "x"], lat), lon=(["y", "x"], lon))
                   )

Correlation = xr.DataArray(result[3],
                   dims=[ "y", "x"],
                   coords=dict(lat=(["y", "x"], lat), lon=(["y", "x"], lon))
                   )
Months = xr.DataArray(result[4],
                   dims=[ "y", "x"],
                   coords=dict(lat=(["y", "x"], lat), lon=(["y", "x"], lon))
                   )

_Result = xr.Dataset({'TCI_weight':TCI_weight,'VCI_weight':VCI_weight,'PCI_weight':PCI_weight,'Correlation':Correlation, 'Months':Months})

_Result.to_netcdf("/share/drought-3/intern/jwlee/moved/Correlation_file/Result.nc")


# tci, vci, pci weight들 여기서 저장 

# 마지막으로 이 아래에서 PPT에서 사용할 발표 자료 image로 만들어서 저장하기
# 어떤 자료들이 필요할지는 모름, plt 관련 코드 받은 것 가지고 만들어 보기 








