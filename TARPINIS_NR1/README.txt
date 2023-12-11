
Programos vardas: "Time Management"
        Autorius: Rolandas Jonušys

    Tai supaprastinta laiko apskaitos valdymo programa. Per šią programą vartotojai (pvz.: įmonės darbuotojai) gali
suvedinėti valandas, kur ir kada prie kokio projekto dirbo, peržiūreti projketus ir jų išlaidas.
    Paleidus pirmą karta programą, ji automatiškai sukuria SQLite3 duombazė ""./db/TM.db" į kurią įrašo
administartoriaus vartotoją admin (slaptažodis:sadmn) ir du objektus/projektus (Bendros valandos, Mokymai).
    Pati programa susideda iš trijų moduliu:
       1. TimeManagement - tai pagrindinis (main) programos kodas.
       2. sql_model_tm - tai pagalbinis modulis, kuriame yra aprašytos SQL duombazė, per SQLAlchemy klases.
       3. demo_data - tai modulis skirtas programos pasibandymui, t.y., jo viduje yra sukurtas kodas, kuris generuoja
          duomenis į SQL duombazę.  Sukuria najų vartotojų, naujų menamų projektų ir jų detalizacijų. Demo duomenų
          generavimas veikia tik, kai duombazė yra tuščia. Jei duombazė yra pradėta pildyti, DEMO režimo meniu
          praleidžiams automatiškai.
