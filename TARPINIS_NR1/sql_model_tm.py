import datetime
import calendar
import os
from pathlib import Path
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey, Float
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

# Duombazes sukurimas
cwd = os.getcwd()
db_dir = Path(cwd + "//db//")
db_dir.mkdir(parents=True, exist_ok=True)
Base = declarative_base()
engine = create_engine("sqlite:///db//TM.db")
Base.metadata.create_all(engine)


class NaujasVartotojas(Base):
    __tablename__ = "VARTOTOJAI"
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    slaptazodis = Column(String)
    ivest_data_utc = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vardas: str, slaptazodis: str):
        self.vardas = vardas
        self.slaptazodis = slaptazodis


# Tabelio klasesAA
class TM_Irasas(Base):
    """ Tabelio įrašas """
    __tablename__ = "TABELIAI"
    id = Column(Integer, primary_key=True)
    vartotojo_id = Column(String)
    vardas = Column(String)
    proj_nr = Column(String)
    proj_vardas = Column(String)
    darb_kat = Column(String)
    start_dt = Column(DateTime)
    stop_dt = Column(DateTime)
    ivest_komentaras = Column(String)
    ivest_data_utc = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vartotojo_id, vardas, proj_nr, proj_vardas, darb_kat, start_dt, stop_dt, ivest_komentaras):
        self.vartotojo_id = vartotojo_id
        self.vardas = vardas
        self.proj_nr = proj_nr
        self.proj_vardas = proj_vardas
        self.darb_kat = darb_kat
        self.start_dt = start_dt
        self.stop_dt = stop_dt
        self.ivest_komentaras = ivest_komentaras


# Projekto klase
class Proj_Irasas(Base):
    __tablename__ = 'PROJEKTAI'
    id = Column(Integer, primary_key=True)
    pr_nr = Column(String)
    pr_vardas = Column(String)
    pr_aprasymas = Column(String)
    pr_pradzia = Column(DateTime)
    pr_pabaiga = Column(DateTime)
    pr_verte = Column(Float)
    pr_valiuta = Column(String)
    pr_statusas = Column(Integer)
    pr_ivest_data_utc = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, pr_nr, pr_vardas, pr_aprasymas, pr_pradzia, pr_pabaiga,
                 pr_verte, pr_valiuta="Eur.", pr_statusas=-1):
        self.pr_nr = pr_nr
        self.pr_vardas = pr_vardas
        self.pr_aprasymas = pr_aprasymas
        self.pr_pradzia = pr_pradzia
        self.pr_pabaiga = pr_pabaiga
        self.pr_verte = pr_verte
        self.pr_valiuta = pr_valiuta
        self.pr_statusas = pr_statusas


class Klasifikacija(Base):
    __tablename__ = 'KLASIFIKACIJA'
    id = Column(Integer, primary_key=True)
    kategoriju_grupe = Column(String)  # Pvz: PROJEKTAS
    kategorija = Column(String)  # pvz.: Programavimas, įranga, kelionė, dienpinigiai, višbutis,proj. valdymas

    def __init__(self, kategoriju_grupe, kategorija):
        self.kategoriju_grupe = kategoriju_grupe
        self.kategorija = kategorija


# Projekto medzio dedamosios
class Proj_Islaidos(Base):
    __tablename__ = 'PROJ_ISLAIDOS'
    id = Column(Integer, primary_key=True)
    pr_nr = Column(String)
    det_aprasymas = Column(String)
    det_verte = Column(Float)
    det_valiuta = Column(String)
    pr_ivest_data_utc = Column(DateTime, default=datetime.datetime.utcnow)
    parent_id = Column(Integer, ForeignKey('PROJ_ISLAIDOS.id'))
    parent = relationship("Proj_Islaidos", back_populates="children", remote_side=[id])  #
    children = relationship("Proj_Islaidos", back_populates="parent")

    def __init__(self, pr_nr, ded_aprasymas, ded_verte, parent=None, ded_valiuta="Eur."):
        self.pr_nr = pr_nr
        self.det_aprasymas = ded_aprasymas
        self.det_verte = ded_verte
        self.det_valiuta = ded_valiuta
        self.parent = parent


# ----------------------------------------------------------------
def default_vartotojai(sessionx: Session):
    if not sessionx.query(NaujasVartotojas).all():
        vart_01 = NaujasVartotojas("admin", "sadmin")
        vart_02 = NaujasVartotojas("user", "suser")
        sessionx.add_all([vart_01, vart_02])
        sessionx.commit()


def default_kategorijos(sessionx: Session):
    if len(sessionx.query(Klasifikacija).all()) > 0:
        return
    visos_klasifik = []
    kg01 = "Projektas"
    data_in = [
        [kg01, "Įranga"],
        [kg01, "Programavimas"],
        [kg01, "Derininmo darbai"],
        [kg01, "Projekto valdymas"],
        [kg01, "Projektavimas"],
        [kg01, "Instaliacija"],
        [kg01, "Dienpinigiai"],
        [kg01, "Kelionės"],
    ]
    n = 1
    for data in data_in:
        kint_vard = f"kat{n}"
        objx = globals()[kint_vard] = Klasifikacija(data[0], data[1])
        visos_klasifik.append(objx)
        n += 1
    sessionx.add_all(visos_klasifik)
    sessionx.commit()


def default_projektai(sessionx: Session):
    test_pr = sessionx.query(Proj_Irasas).all()
    t1 = datetime.datetime.utcnow()
    t2 = datetime.datetime.utcnow()
    if len(test_pr) == 0:
        proj_Bendr = Proj_Irasas("T0001", "Bendros", "Ne projektinės valandos", t1, t2, 0, "Eur.", 0)
        proj_Mokym = Proj_Irasas("T0002", "Mokymai", "Valandos mokymams", t1, t2, 0, "Eur.", 0)
        sessionx.add_all([proj_Bendr, proj_Mokym])
        sessionx.commit()


def rodyti_visus_projektus(sessionx: Session):
    # visi ivesti projektai
    lent_pl = 125
    print("-" * lent_pl)
    visprojektaitxt = "VISI PROJEKTAI"
    k_visprj = lent_pl // 2 - len(visprojektaitxt) // 2
    print(" " * k_visprj, visprojektaitxt, " " * k_visprj)
    print("-" * lent_pl)
    proj_all = sessionx.query(Proj_Irasas).all()
    for pr in proj_all:
        tarp0 = " " * (3 - len(str(pr.id)))
        tarp1 = " " * (26 - len(pr.pr_vardas))
        tarp2 = " " * (40 - len(pr.pr_aprasymas))
        tarp3 = " " * (12 - len(str(pr.pr_verte)))
        if pr.pr_nr == "T0001" or pr.pr_nr == "T0002":
            print(tarp0, pr.id, ".", pr.pr_nr, pr.pr_vardas, tarp1, pr.pr_aprasymas)
        else:
            print(tarp0, pr.id, ".", pr.pr_nr, pr.pr_vardas, tarp1, pr.pr_aprasymas, tarp2,
                  pr.pr_pradzia.strftime("%Y-%m-%d"), "-->", pr.pr_pabaiga.strftime("%Y-%m-%d"), tarp3, pr.pr_verte,
                  pr.pr_valiuta)
    print("\n")


def rodyti_proj_detalizacija(sessionx: Session, raktas=None, tiksliai=False):
    plot_k = 100
    print()
    uzras_txt = "PROJEKTŲ IŠLAIDŲ DETALIZACIJA"
    k_visprj = plot_k // 2 - len(uzras_txt) // 2
    print("*" * k_visprj, uzras_txt, "*" * k_visprj)
    print()
    if raktas is None:
        visos_eilutes = sessionx.query(Proj_Islaidos).all()
    else:
        if not tiksliai:
            visos_eilutes = sessionx.query(Proj_Islaidos).filter(Proj_Islaidos.pr_nr.ilike(f"%{raktas}%")).all()
        else:
            visos_eilutes = sessionx.query(Proj_Islaidos).filter(Proj_Islaidos.pr_nr.ilike(f"{raktas}%")).all()
            if len(visos_eilutes) == 0:
                print(f"Projekto nr.:{raktas} nerastas. Pasitikrinkite ar teisingai įvedėte projekto nr.? ")
                return

    kof1 = 65
    kof2 = 8

    print("-" * plot_k)
    for r in visos_eilutes:
        detalizac_sum = 0
        if r.parent_id is None:
            tarp1 = "." * (kof1 - len(r.det_aprasymas) + 6) + " suma:"
            tarp2 = " " * (kof2 - len(str(r.det_verte)))
            print("", r.pr_nr, r.det_aprasymas, tarp1, r.det_verte, tarp2, r.det_valiuta)
            print("-" * plot_k)
            for l1 in visos_eilutes:
                if l1.parent_id == r.id and r.parent_id is None:
                    tarp1 = "." * (kof1 - len(l1.det_aprasymas) + 2)
                    tarp2 = " " * (kof2 - len(str(l1.det_verte)) + 4)
                    print(" -", l1.pr_nr, l1.det_aprasymas, tarp1, l1.det_verte, tarp2, l1.det_valiuta)
                    for l2 in visos_eilutes:
                        if l2.parent_id == l1.id and l1.parent_id == r.id and r.parent_id is None:
                            detalizac_sum += l2.det_verte
                            tarp1 = "." * (kof1 - len(l2.det_aprasymas))
                            tarp2 = " " * (kof2 - len(str(l2.det_verte)) + 2)
                            print("     -", l2.pr_nr, l2.det_aprasymas, tarp1, l2.det_verte, tarp2, l2.det_valiuta)
            sum_msg1 = f"Detalizacijos suma :{detalizac_sum} Eur."
            sum_msg2 = f"Balansas :{r.det_verte - detalizac_sum} Eur."
            print("\n", " " * (plot_k - len(sum_msg1)) + sum_msg1)
            print(" " * (plot_k - len(sum_msg2)) + sum_msg2)
            print("\n\n", "-" * plot_k)


def prisijungti(sessionx: Session):
    b = 0
    while True:
        vard = input("Įveskite vardą: ")
        slapt = input("Įveskite slaptažodį: ")
        rasti_vard = sessionx.query(NaujasVartotojas).filter_by(vardas=vard).all()
        for v in rasti_vard:
            if v.vardas == vard and v.slaptazodis == slapt:
                return v
        b += 1
        print("Blogis prisijungimo duomenys. Bandykite dar karta.")
        if b > 2:
            if input("Jei norite išeiti spauskite 'q': ") == "q":
                exit(-9)
    return None


def tabelio_ataskaita(sessionx: Session, esam_vart: NaujasVartotojas = None):
    # Jeigu admin prisijunge
    print("\n\n")
    if esam_vart.vardas == "admin":
        # spausdinami visi vartotojai
        visi_vart = sessionx.query(NaujasVartotojas).all()
        print("Visi programos vartotojai:")
        print("-------------------------:")
        for v in visi_vart:
            print("id:", v.id, " vardas:", v.vardas)
        try:
            sel_var = int(input("Pasirinkite vartotoją, pagal ID, kurio duomenis norite matyti: "))
        except ValueError:
            print("KLAIDA: įvedėte ne skaičių!")
            return
        for v in visi_vart:
            if v.id == sel_var:
                esam_vart = v
    try:
        sel_met = int(input("Įveskite metus, iš kurių norite gauti ataskaitą (pvz.: 2023): "))
        sel_men = int(input("Įveskite menesį, kurio ataskaitą norite gauti (pvz.: 9): "))
        if sel_men not in range(1, 13):
            print(f"Tokio mėnesio {sel_men} nėra...")
            return
    except ValueError:
        print("Blogai įvedėte mėnesį arba metus. Turi būti skaičiai.")
        print("\n\n")
    key_dt1 = datetime.datetime.strptime(f"{sel_met}-{sel_men}", "%Y-%m")
    key_dt2 = datetime.datetime.strptime(f"{sel_met}-{sel_men + 1}", "%Y-%m")
    visi_tm_irasai = sessionx.query(TM_Irasas).filter(TM_Irasas.vardas.ilike(esam_vart.vardas)).filter(
        TM_Irasas.start_dt >= key_dt1).filter(TM_Irasas.start_dt < key_dt2).all()
    visi_proj_nr = [pr.proj_nr for pr in visi_tm_irasai]
    visi_skirtingi_tm_irasai = []
    # Perrenkam visus įrašus
    ds_num = calendar.monthrange(sel_met, sel_men)
    print("\n\n")
    # unikaliu proj nr. paieska
    for tm in visi_proj_nr:
        if tm not in visi_skirtingi_tm_irasai:
            visi_skirtingi_tm_irasai.append(tm)
    print(f"{sel_met}m. {sel_men} men.", " " * 60, f"vardas:{esam_vart.vardas}, id={esam_vart.id}")
    print("-" * 100)
    # Spausdinimas kiek prie kiekvieno projekto išdirbta
    projekt_val_l = []
    for nr in visi_skirtingi_tm_irasai:
        sumx = []
        print_obj = None
        for x in visi_tm_irasai:
            if x.proj_nr == nr:
                print_obj = x
                dt = x.stop_dt - x.start_dt
                # print(dt)
                sumx.append((dt.seconds) / 3600)
        sumx = sum(sumx)
        if print_obj.proj_nr != "T0001" and print_obj.proj_nr != "T0002":
            projekt_val_l.append(sumx)
        tarp1 = "." * (50 - len(print_obj.darb_kat))
        tarp1_1 = " " * (26 - len(print_obj.proj_vardas))
        print(print_obj.proj_nr, print_obj.proj_vardas, tarp1_1, print_obj.darb_kat, tarp1, round(sumx, 1), "val.")
    print("")
    txt1 = "Į projektus nurašytos valandos:"
    tarp1 = "." * (50 - len(txt1) - len(str(round(sum(projekt_val_l), 1))))
    print(txt1, tarp1, round(sum(projekt_val_l), 1), "val.")
    # Šis menuo turi darbo valandu
    d_num = calendar.monthrange(sel_met, sel_men)[1]
    dd = [d for d in range(1, d_num + 1)
          if datetime.datetime(sel_met, sel_men, d).isoweekday() != 6 and
          datetime.datetime(sel_met, sel_men, d).isoweekday() != 7]
    viso_darb_val = len(dd) * 8
    txt2 = "Bendrosios valandos:"
    bendrosios_men_val = viso_darb_val - sum(projekt_val_l)
    tarp2 = "." * (50 - len(txt2) - len(str(round(bendrosios_men_val, 1))))
    print(txt2, tarp2, round(bendrosios_men_val, 1), "val.")
    txt3 = "Vartotojo apkrovimas:"
    darb_ur = round((sum(projekt_val_l) / viso_darb_val) * 100, 2)
    tarp3 = "." * (50 - len(txt3) - len(str(darb_ur)))
    print(txt3, tarp3, darb_ur, "%")
    txt4 = f"Viso {sel_men} mėn. turėjo darbo valandų:"
    tarp4 = "." * (50 - len(txt4) - len(str(round(float(viso_darb_val), 1))))
    print(txt4, tarp4, round(float(viso_darb_val), 1), "val.")
    print("\n\n")
    input("Jei norite testi spauskyte ENTER>>>")


def valandu_ivedimas(sessionx: Session, esam_vart: NaujasVartotojas):
    print("\n")
    print("*********** VALANDŲ VEDIMAS **************************:")
    rodyti_visus_projektus(sessionx)
    rakt = input("Pasirinkite projektą iš sarašo, pagal PROJEKTO NR.")
    root_pr_obj = sessionx.query(Proj_Irasas).filter(Proj_Irasas.pr_nr == rakt).first()
    print("AAAA", root_pr_obj.pr_vardas)
    rodyti_proj_detalizacija(sessionx, rakt, tiksliai=True)
    # Projekto išrinkimas
    while True:
        proj_ded_nr = input("Pasirinkite projekto dedamąją iš sarašo, pagal PROJEKTO NR.: ")
        try:
            isld_obj = sessionx.query(Proj_Islaidos).filter(Proj_Islaidos.pr_nr == proj_ded_nr).first()
            print("Projekto eilutė: '", isld_obj.pr_nr, " ", isld_obj.det_aprasymas, "' rasta")
            if not "_" in isld_obj.pr_nr:
                print(f"Toks projektas '{isld_obj.pr_nr}' yra, bet blogai nurodėte jo detalizaciją...")
                continue
            break
        except:
            print("Tokio projekto nėra...")
    # Laiku sudeliojimas:
    while True:
        start_dt = input("Iveskite datą ir laiką, kada pradėjote darbus (yyyy-mm-dd HH:MM):")
        stop_dt = input("Iveskite datą ir laiką, kada baigėte darbus (yyyy-mm-dd HH:MM):")
        try:
            start_dt = datetime.datetime.strptime(start_dt, "%Y-%m-%d %H:%M")
            stop_dt = datetime.datetime.strptime(stop_dt, "%Y-%m-%d %H:%M")
            break
        except:
            print("Blogai įvedėte laiką!")
            continue

    komentaras = input("Įveskite eilutės komentarą:")
    tm_obj = TM_Irasas(esam_vart.id, esam_vart.vardas, isld_obj.pr_nr, root_pr_obj.pr_vardas, isld_obj.det_aprasymas,
                       start_dt, stop_dt, komentaras)
    sessionx.add(tm_obj)
    sessionx.commit()
    print("\n\n")
