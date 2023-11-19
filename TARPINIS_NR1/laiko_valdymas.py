import datetime
from pathlib import Path
from klases.sql_model_tm import (engine, Base, default_vartotojai, default_kategorijos, Klasifikacija,
                                 rodyti_visus_projektus, prisijungti, Proj_Irasas, default_projektai)
from sqlalchemy.orm import Session
from klases.demo_data import (generuoti_vartotojus, kurti_demo_projektus, kurti_demo_detalizacija, kurti_demo_TM_irasus)

Base.metadata.create_all(engine)
session = Session(engine)
# Default'iniai vartotojai
default_vartotojai(session)
# Defaultines kategorijos
default_kategorijos(session)
# Defaultiniai projektai
default_projektai(session)
# Prisijungimas
# esam_vartotojas=prisijungti(session)
# print(f"Sveiki prisijungę {esam_vartotojas.vardas} prie programos!")
# Pagrindinis meniu
# Tikriname ar yra duombaze
dbfile = Path(".//db//TM.db")
visi_proj = session.query(Proj_Irasas).all()
if len(visi_proj) <= 2:
    print(""
          "1 - paleisti programa\n"
          "2 - paleisti programą DEMO režimu\n"
          "q - baigti darbą")
    sel1 = input("Įveskite pasirinkimą: ")
    if sel1 == "q":
        exit(0)
    if sel1 == "1":

        pass
    elif sel1 == "2":
        test_table = session.query(Proj_Irasas).all()
        if len(test_table) <= 2:
            # Sugeneruojam atsitiktiniu vartotoju
            generuoti_vartotojus(session)
            # Sugeneruojam menamus projektus
            kurti_demo_projektus(session)
            kurti_demo_detalizacija(session)
            # Tabeliu užpildymas
            kurti_demo_TM_irasus(session)

#rodyti_visus_projektus(session)

session.commit()
