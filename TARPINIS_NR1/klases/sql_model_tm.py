import datetime
from pathlib import Path
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey, Float
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

# Duombazes sukurimas
db_dir = Path("db")
db_dir.mkdir(parents=True, exist_ok=True)
Base = declarative_base()
engine = create_engine("sqlite:///db//TM.db")
Base.metadata.create_all(engine)


# class Vartotojas:
#     def __init__(self, vardas, slaptazodis):
#         self.vardas = vardas
#         self.slaptazodis = slaptazodis


class NaujasVartotojas(Base):
    __tablename__ = "VARTOTOJAI"
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    slaptazodis = Column(String)
    ivest_data_utc = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vardas: str, slaptazodis: str):
        self.vardas = vardas
        self.slaptazodis = slaptazodis


# Tabelio klases
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
    ded_aprasymas = Column(String)
    ded_verte = Column(Float)
    ded_valiuta = Column(String)
    pr_ivest_data_utc = Column(DateTime, default=datetime.datetime.utcnow)
    parent_id = Column(Integer, ForeignKey('PROJ_ISLAIDOS.id'))
    parent = relationship("Proj_Islaidos", back_populates="children", remote_side=[id])  #
    children = relationship("Proj_Islaidos", back_populates="parent")

    def __init__(self, pr_nr, ded_aprasymas, ded_verte, parent=None, ded_valiuta="Eur."):
        self.pr_nr = pr_nr
        self.ded_aprasymas = ded_aprasymas
        self.ded_verte = ded_verte
        self.ded_valiuta = ded_valiuta
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


def rodyti_proj_detalizacija(sessionx: Session, raktas=None):
    plot_k = 100
    print()
    uzras_txt = "PROJEKTŲ IŠLAIDŲ DETALIZACIJA"
    k_visprj = plot_k // 2 - len(uzras_txt) // 2
    print("*" * k_visprj, uzras_txt, "*" * k_visprj)
    print()
    if raktas is None:
        visos_eilutes = sessionx.query(Proj_Islaidos).all()
    else:
        visos_eilutes = sessionx.query(Proj_Islaidos).filter(Proj_Islaidos.pr_nr.ilike(f"%{raktas}%")).all()

    kof1 = 65
    kof2 = 8

    print("-" * plot_k)
    for r in visos_eilutes:
        detalizac_sum = 0
        if r.parent_id is None:
            tarp1 = "." * (kof1 - len(r.ded_aprasymas) + 6) + " suma:"
            tarp2 = " " * (kof2 - len(str(r.ded_verte)))
            print("", r.pr_nr, r.ded_aprasymas, tarp1, r.ded_verte, tarp2, r.ded_valiuta)
            print("-" * plot_k)
            for l1 in visos_eilutes:
                if l1.parent_id == r.id and r.parent_id is None:
                    tarp1 = "." * (kof1 - len(l1.ded_aprasymas) + 2)
                    tarp2 = " " * (kof2 - len(str(l1.ded_verte)) + 4)
                    print(" -", l1.pr_nr, l1.ded_aprasymas, tarp1, l1.ded_verte, tarp2, l1.ded_valiuta)
                    for l2 in visos_eilutes:
                        if l2.parent_id == l1.id and l1.parent_id == r.id and r.parent_id is None:
                            detalizac_sum += l2.ded_verte
                            tarp1 = "." * (kof1 - len(l2.ded_aprasymas))
                            tarp2 = " " * (kof2 - len(str(l2.ded_verte)) + 2)
                            print("     -", l2.pr_nr, l2.ded_aprasymas, tarp1, l2.ded_verte, tarp2, l2.ded_valiuta)
            sum_msg1 = f"Detalizacijos suma :{detalizac_sum} Eur."
            sum_msg2 = f"Balansas :{r.ded_verte - detalizac_sum} Eur."
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
