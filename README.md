## Demo app ernestas_biblioteka

https://ernestasbiblioteka.streamlit.app/

## Informacija

1. paleidimas su streamlit, iš failo ernestas_biblioteka/streamlit/app.py
2. demo prisijungimai, Bibliotekininkas ({vardas: 'Onute', password: seacret123})
3. prisijungus galima pažiūrėti visus skitytojus ir kortelių nr., su kuriais galima prisijungti prie skaitytojų.

## Papildomai atlikta

1. Registracija naujo skaitytojo (išvesta projekte)
2. Naujo Bibliotekininko pridėjimas (neišvesta)
3. Sąrašai su platesne informacija, pagal juos galima išvesti įvairios info

- skaitytojo: paimtų ir gražintų knygų laikai ir istorija.
- bibliotekininko: įkeltų ir pašalintų knygų sąrašas su laikais.
- visi skaitytojai: prie jų pradelstos knygos, jei tokios yra.
- pradelstų knygų sąrašas iškarto su skaitytoju.

4. Sukurtas fakeris, kuris sukuria knygas, įkelia sukurdamas įrašus bibliotekininkui, sukuria skaitytojus ir jiems priskiria papimtas knygas su įvairiais paėmimo laikais ir sukuria įrašus apie tai.
5. Knygų grąžinimas į biblioteką

## Pagrindinės užduotys

Įsivaizduokite, kad buvote pasamdyti sukurti paprastą bibliotekos valdymo python programą, ši programa turėtų galėti atlikti šias funkcijas:

###############################

Turėtų būti galima pridėti naują į knygą į biblioteką (knyga, privalo turėti bent, autorių pavadinimą išleidimo metus ir žanrą . #atlikta

Turėtų būti galima pašalinti senas/nebenaudojamas knygas, galima daryti pagal išleidimo metus, jeigu senesnis nei x išmetam. #atlikta

Skaitytojai turėtų galėti pasiimti knygą išsinešimui (knygų kiekis ribotas) #atlikta

Turėtų būti galimybė ieškoti knygų bibliotekoje, pagal knygos pavadinimą arba autorių. #atlikta

Knygos išduodamos tik tam tikram laikui, jeigu knygos negrąžinamos iki išduotos datos, jos skaitomos vėluojančiomis (angl. Overdue). #atlikta

Turi būti galima peržiūrėti visas bibliotekos knygas #atlikta

Turi būti galima peržiūrėti visas vėluojančias knygas #atlikta

Turi būti neleidžiama pasiimti knygos, jeigu skaitytojas turi vėluojančią knygą ir jis turi būti įspėtas, kad knyga vėluoja #atlikta

####################################

Bonus Balai (neprivaloma padaryti)

Knygas galima pasiimti tik su skaitytoje kortele, skaitytojo korteles reikia galėti užregistruoti ir priskirti naudotojui. #atlikta

Turėtų būti galimybė išvesti statistiką, koks yra vidutinis vėluojančių knygų kiekis ir kitus aktualius rodiklius, tokius kaip, kokio žanro knygų yra daugiausiai, kokio žanro knygas, dažniausiai ima skaitytojai ir t.t #atlikta

Dvi rolės bibliotekininkas ir skaitytojas, bibliotekininkas prisijungia įvedę naudotojo vardą ir slaptažodį, o skaitytojas savo skaitytojo kortelės numerį. Skaitytojas negali pridėti/išimti knygų. #atlikta

Paleiskite programą per streamlit #atlikta

Naudojama virtuali aplinka viso darbo metu (tinka tiek venv tiek poetry) #atlikta

Galite pamėginti padaryti grafinę sąsają ir per įrankius, kaip tkinter.

######################################

Būtinos sąlygos

Nerašome visko viename faile (turi būti laikomasi, bent minimalios struktūros) #atlikta

Programa turi veikti tol, kol bus išjungta, naudotojo pageidavimu #atlikta

Pridėtos/pašalintos knygos, turi išlikti tarp programos paleidimų (vadinasi viskas saugoma faile) #atlikta

Informacija saugome pkl/csv/json/txt failuose #atlikta

Programa negali "nulūžti" (už kiekvieną vietą, kurioje lūžta, minus balai)

Programoje viskas turi būti funkcijose/metoduose klasėse. Globaliai jie gali būti tik kviečiami, bet visi skaičiavimai būtent šiose struktūrose. #atlikta

Privaloma naudota GitHub ir turėti logiškus commit pavadinimus, bent 3 šakas sukurtas projekto metu ir bent 5 commitai (commitai neturėtų būti labai dideli, po vieną funkcionalumą vienas commitas) #atlikta

#####################################

Taip pat prisekite word failą, kuriame bus tokie dalykai.

1. Įsivertinti save, kažkokiu tai pažymiu iki 10
2. Parašyti, kas patiko ar nepatiko darbo metu
3. Kas buvo naujo, ko išmokote
4. Ar turite kokių pastebėjimų
