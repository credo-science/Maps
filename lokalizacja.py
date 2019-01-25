#import bibliotek
import json   
import os
from os import listdir
from os.path import isfile, join
import datetime
import time

#okreslenie daty wczorajszej->[-datetime.timedelta(days=1)]
date = datetime.date.today() -datetime.timedelta(days=1)
rok = date.year #wyciągniecie roku z daty
miesiac=date.month #wyciągniecie miesiąca z daty
dzien=date.day #wyciągniecie dnia z daty
    
#**********************************************************************************************************************************************************************


#TWORZYMY PLIK Z USERAMI ich ID i nazwausera -> przyda sie jesli bedziech chcial pokazac gdzie konkretny user jest; Jesli nie usun ta czesc
name = 'user_mapping.json'
print("Tworzenie plikow z uzytkownikami: ")
with open(name) as f2:
    	json_from_file2 = json.load(f2)


fs = open('Lokalizacja/users.txt','w')#stworz nowy plik w folderze Lokalizacja o nazwie "users.txt" -> tu masz lokalny sposob tworzenia plikow (bez podania calej sciezki)
fs.close()
f3 = open('Lokalizacja/users.txt','a')#otworz dany plik i dopisuj na samym koncu

for user in json_from_file2['users']:
	nazwa = user['display_name']
	userID= user['id']
	f3.write(nazwa+';\t'+str(userID)+';\n')
			

#***********************************************************************************************************************************************************************
print (dzien)
#odkomentować po pierwszym uruchomieniu 4 ponizsze linie
#f = open('Lokalizacja/iloscplikow.txt', 'r') -> zakomentowane tylko przed 1 uruchomieniem
#for l in f:
	#zacznijod = int(l)-10#dla bezpieczenstwa czytamy wiecej cos bylo nie tak z nazwami -> odkomentuj pozniej
#f.close()
zacznijod = 30#zaczynamy od 30 pliku - przyspieszy dzialanie programu
#zmienna "zacznijod: decyduje ile plikow bierzemy pod uwage, jesli chcemy czytać pliki z 1 dnia, to bez sensu jest czytać wszystkie paczki, ustawione na 30 ponieważ nie wiem ile paczek jest u Ciebie

sciezka='/home/slawekstu/Pulpit/credo-data-export/' #sciezka do folderu "credo-data-export"
sciezka2 = sciezka+"Lokalizacja/"+str(rok)+"/"+str(miesiac)+"/"
sciezkalokalizacji = sciezka2+str(dzien)+"/"#sciezka dnia wczorajszego gdzie zapiszemy wyniki
if dzien == 28:
	os.mkdir(sciezka+"Lokalizacja/"+str(rok)+"/"+str(miesiac))#stworz nowy folder na zapas (na kolejny meisiac)
os.mkdir(sciezka2+str(dzien))
mypath = sciezka+'detections/'#sciezka do paczek z rozszerzeniem *.json
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
ilosc = len(onlyfiles)	
liczbauserow=14000#zmienna o wielkosci userow, by program sam ustalal ile jest użytkownikow, potrzeba wyszukać najwieksze ID w pliku user_mapping.json


print("wczytywanie plikow i podzial detekcji: ")
print(str(dzien)+"-"+str(miesiac))
start = int(datetime.datetime(rok, miesiac, dzien, 0, 0).strftime("%s")) * 1000 #data rozpoczecia pobierania detekcji ->ustawiona na date wczorajsza
start=str(start)#zamien na str -> usuwamy wtedy miejsca po przecinku: 147990.000 -> 147990
start=int(start)#zamiana z powrotem na int 
stop = int(datetime.datetime(rok, miesiac, dzien, 23, 59).strftime("%s")) * 1000 #data konca pobierania detekcji ->ustawiona na date wczorajsza
stop=str(stop)
stop=int(stop)

print(start)#czas unixowy
#deklaracja tablic, wspolrzednych geograficznych i czasu
array_latitude = []
array_longitude = []
array_height = []
array_time = []

#index tablicy to ID Usera. Uzupelniam tablice zerami
for i in range (0,liczbauserow):
	array_latitude.append(0)
	array_longitude.append(0)
	array_height.append(0)
	array_time.append(0)	
floc = open(sciezkalokalizacji+'lokalizacjausera.txt','w')#ilosc plikow detekcji
floc.close()

for i in range(zacznijod,ilosc):#petla po plikach ktore wczytujemy
	name = sciezka+'detections/'+str(onlyfiles[i])#wczytywanie konkretnej paczki detekcji
	with open(name) as f:
    		json_from_file = json.load(f)
	print("licze plik",i)
	
	for detection in json_from_file['detections']:
		stan = "True" #obraz widzialny na api.credo.science
		a=detection['user_id']
		index=int(a)#index to ID user
		latitude = detection['latitude']#zastepujemy w tablicy wartosc "0" na odpowiadajaca danemu uzytkownikowi - "a" to index/ID usera
		longitude = detection['longitude']
		height = detection['height']
		time=detection["timestamp"]
		wsp_latitude= 1#wymagane wspolzedna wieksza od -> mozesz tym ograniczyc zakres interesowanego cie regionu
		    #SPRAWDZMY CZY DANY REKORD MA CZAS i CZY DETEKCJA JEST WIDZIALNA NA STRONIE =>(TRUE) + warunek czy user istnieje np czy lat>0
		if int(time)<stop and int(time)>start and str(detection['visible'])==stan and int(latitude)> int(wsp_latitude):
			#wartosc tablicy uzupelniam tylko gdy jest spelniony warunek
			array_latitude[index]=latitude
			array_longitude[index]=longitude
			array_height[index]=height
			array_time[index]=time
			print("\nSpelniony warunek dla usera: "+str(index))
			    #zapis detekcji do pliku o nazwie ID usera np 1231.txt
			nazwa=str(index)+'.txt'
			f = open(sciezkalokalizacji+nazwa,'a')
			f.write(str(time)+';'+str(latitude)+';'+str(longitude)+';'+str(height)+';\n')#time;latitude;longitude;height
			f.close()
			floc1 = open(sciezkalokalizacji+'lokalizacjausera.txt','a')
			floc1.write(str(time)+'\n'+str(latitude)+'\n'+str(longitude)+'\n'+str(height)+'\n\n')
			floc1.close()

#INFORMACJA ILE BYLO DZIS ALL PACZEK
fsa = open(sciezka+'Lokalizacja/iloscplikow.txt','w')#ilosc plikow detekcji
fsa.write(str(ilosc))
fsa.close()
