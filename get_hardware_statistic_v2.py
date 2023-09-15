## Скрипт для построения графиков статистики потребления ресурсов 
## Пример запуска на Linux: "python3 <имя файла>.py localhost 22-08-2022"
## Пример запуска на Windows: "py <имя файла>.py localhost 22-08-2022"
## Где localhost - имя папки где хранится БД с данными
## Где 22-08-2022 - дата (она же имя вложенной папки) за которую необходимо построить статистику
## Доработано с учетом особенностей Linux
import os
import logging
import json
import shelve
import sys
from sys import argv
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pprint import pprint
logging.basicConfig(level=logging.INFO, format='(%(asctime)s-%(levelname)s-%(message)s')

_,ip,date=argv

file_path=os.path.join('telemetry',ip,date,'db')

with shelve.open(file_path) as shelve_file:
    dataFrame=shelve_file["harware_state_history"]


x=dataFrame['time']

y_cpu=dataFrame['cpu_usage']
y_ram=dataFrame['ram_free']
y_ram=np.array(y_ram, dtype=float)
y_net_down=dataFrame['network_usage_down']
y_net_down=np.array(y_net_down, dtype=float)
y_net_up=dataFrame['network_usage_up']
y_net_up=np.array(y_net_up, dtype=float)
print("Построение графиков cpu_usage, ram_free и network_usage")

fig=plt.figure(figsize=(10,6) )
logging.info(f'date_label: {date}')
fig.suptitle(f'Ресурсы сервера {ip}\n за {date}')
plt.subplot(311)


#Набор инструкций для графиков "upload" в случае пересечения 
#plt.fill_between(x,y_net_up,y_net_down, where=(y_net_up>y_net_down), interpolate=True, label='upload',color = (0.95,0.6,0.6,1),alpha = 0.9)
plt.fill_between(x,y_net_up,y_net_down, where=None, interpolate=True, label='upload',color = (0.95,0.6,0.6,1),alpha = 0.5)
#plt.fill_between(x,y_net_up,0, where=(y_net_up<=2*y_net_down), interpolate=True,color = (0.95,0.6,0.6,1),alpha = 0.9)
plt.fill_between(x,y_net_up,0, where=(None), interpolate=True,color = (0.95,0.6,0.6,1),alpha = 0.5)
#plt.fill_between(x,y_net_up,0, where=(y_net_up==y_net_down), interpolate=True,color = (0.95,0.6,0.6,1),alpha = 0.9)
plt.fill_between(x,y_net_up,0, where=None, interpolate=True,color = (0.95,0.6,0.6,1),alpha = 0.5)
plt.plot(x,y_net_up,linewidth=1,color = (0.8,0.6,0.6,1))

#Набор инструкций для графиков "download" в случае пересечения
plt.fill_between(x,y_net_down,y_net_up, where=(y_net_down>y_net_up), interpolate=True, label='download',color = (0.3,0.62,0.83,1),alpha = 0.5)
#plt.fill_between(x,y_net_down,y_net_up, where=None, interpolate=True, label='download',color = (0.3,0.62,0.83,1),alpha = 0.1)
plt.fill_between(x,y_net_down,0, where=(y_net_down<=1.61*y_net_up), interpolate=True,color = (0.3,0.62,0.83,1),alpha = 0.5)
#plt.fill_between(x,y_net_down,0, where=None, interpolate=True,color = (0.3,0.62,0.83,1),alpha = 0.1)
plt.fill_between(x,y_net_down,0, where=(y_net_down==y_net_up), interpolate=True,color = (0.3,0.62,0.83,1),alpha = 0.5)
#plt.fill_between(x,y_net_down,0, where=None, interpolate=True,color = (0.3,0.62,0.83,1),alpha = 0.1)
plt.plot(x,y_net_down,linewidth=1,color = (0.2,0.62,0.83,1))






plt.legend(loc='upper left')
plt.grid(True)

plt.ylabel('network_usage, \nbytes per sec')
plt.ylim(0)

plt.subplot(312)
plt.fill_between(x,y_cpu,alpha = 0.5)
plt.plot(x,y_cpu,linewidth=1,color = (0.2,0.62,0.83,1))
plt.grid(True)
plt.ylim(0,100)
plt.ylabel('cpu, %')

plt.subplot(313)
plt.fill_between(x,y_ram,alpha = 0.5)
plt.plot(x,y_ram,linewidth=1,color = (0.2,0.62,0.83,1))
plt.grid(True)
plt.ylim(0,100)
plt.ylabel('ram_free, %')
plt.xlabel('Время')

plt.show()
