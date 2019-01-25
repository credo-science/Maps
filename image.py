#dodanie bibliotek
import json   
import os
from os import listdir
from os.path import isfile, join
import datetime
import time
import base64
#okreslenie daty o 2 wstecz ->[-datetime.timedelta(days=2)]
date = datetime.date.today() -datetime.timedelta(days=2)
rok = date.year
miesiac=date.month
dzien=date.day

zacznijod = 70 #od ktorej paczki ma zaczac badac - jesli mamy 80 i chcemy tylko z dzis czy wczoraj wystarczy zaczac od 70
sciezka = '/media/slawekstu/Gry i Programy/Praca/Api/od12 do 26/credo-data-export/'
mypath = '/media/slawekstu/Gry i Programy/Praca/Api/od12 do 26/credo-data-export/detections/'#name where is file with detections *.json
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
ilosc = len(onlyfiles)	

date = datetime.date.today()
start = int(datetime.datetime(rok, miesiac, dzien-1, 0, 0).strftime("%s")) * 1000 #data rozpoczecia pobieranie detekcji ->ustawiona na date wczorajsza
start=str(start)#zamien na str -> usuwamy wtedy miejsca po przecinku: 147990.000 -> 147990
start=int(start)#zamiana z powrotem na int 


for i in range(zacznijod,ilosc):#petla po plikach ktore wczytujemy
	name = sciezka+'detections/'+str(onlyfiles[i])#wczytywanie konkretnej paczki detekcji
	with open(name) as f:
    		json_from_file = json.load(f)
	print("licze plik",i)
	
	for detection in json_from_file['detections']:
		stan = "True" #obraz widzialny na api.credo.science
		a=detection['user_id']
		index=int(a)#index to ID user
		time=detection["timestamp"]
		image=detection["frame_content"].encode('ascii')

		if int(time)>start and str(detection['visible'])==stan:
			print("\nSpelniony warunek dla usera: "+str(index))
			    #zapis detekcji do pliku o nazwie ID usera np 1231.txt
			nazwa=str(index)+'_'+str(time)+'.png'
			with open("Image/"+nazwa, "wb") as fh:
    				fh.write(base64.decodebytes(image))

