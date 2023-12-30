import datetime
import os
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Time, ForeignKey, create_engine, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///db/testu.db")
Base = declarative_base()


class Vartotojas(Base):
    __tablename__ = 'vartotojas'
    id = Column(Integer, primary_key=True)
    vardas = Column(String, unique=True)
    slaptazodis = Column(String)
    admin_teises = Column(Boolean, default=False)
    statistika = relationship("VartotojoStatistika", back_populates="vartotojas",
                              cascade="all, delete-orphan", uselist=False)
    sesijos = relationship("Sesija", back_populates="vartotojas")


class VartotojoStatistika(Base):
    __tablename__ = 'vartotojo_statistika'
    id = Column(Integer, primary_key=True)
    atlikti_testai = Column(Integer, default=0)
    testu_vidurkis_proc = Column(Float, default=0.0)
    pradeti_testai = Column(Integer, default=0)
    bendri_balai = Column(Float, default=0.0)
    vartotojas_id = Column(Integer, ForeignKey("vartotojas.id"))
    vartotojas = relationship("Vartotojas", back_populates="statistika")  # uselist=False


class Sesija(Base):
    __tablename__ = 'sesija'
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default=datetime.datetime.utcnow())
    vartotojas_id = Column(Integer, ForeignKey("vartotojas.id"))
    vartotojas = relationship("Vartotojas", back_populates="sesijos")
    rezultatas = relationship("Rezultatas", back_populates="sesija")
    vartot_atsakymai = relationship("VartotojoAtsakymas", back_populates="sesija")


class Rezultatas(Base):
    __tablename__ = 'rezultatas'
    id = Column(Integer, primary_key=True)
    pateikta = Column(Boolean, default=False)
    balai = Column(Float, default=0.0)
    laikas = Column(Time)
    sesija_id = Column(Integer, ForeignKey("sesija.id"))
    sesija = relationship("Sesija", back_populates="rezultatas")


class Tema(Base):
    __tablename__ = 'tema'
    id = Column(Integer, primary_key=True)
    pavadinimas = Column(String)
    klausimai = relationship("Klausimas", back_populates="tema",cascade="all, delete-orphan")


class Klausimas(Base):
    __tablename__ = 'klausimas'
    id = Column(Integer, primary_key=True)
    pavadinimas = Column(String)
    tema_id = Column(Integer, ForeignKey("tema.id"))
    tema = relationship("Tema", back_populates="klausimai")
    atsakymai = relationship("Atsakymas", back_populates="klausimas", cascade="all, delete-orphan")

# association_table=Table('association', Base.metadata,
#                        Column('tevas_id', Integer, ForeignKey('tevas.id')),
#                        Column('vaikas_id', Integer, ForeignKey('vaikas.id')))

class Atsakymas(Base):
    __tablename__ = 'atsakymas'
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    teisingas = Column(Boolean, default=False)
    balas = Column(Float, default=0.0)
    klausimas_id = Column(Integer, ForeignKey("klausimas.id"))
    klausimas = relationship("Klausimas", back_populates="atsakymai")
    vart_atsakymai = relationship("VartotojoAtsakymas", back_populates="atsakymas")



class VartotojoAtsakymas(Base):
    __tablename__ = 'vartot_atsakymas'
    id = Column(Integer, primary_key=True)
    atsakymas_id = Column(Integer, ForeignKey("atsakymas.id"))
    sesija_id = Column(Integer, ForeignKey("sesija.id"))
    sesija = relationship("Sesija", back_populates="vartot_atsakymai")
    atsakymas = relationship("Atsakymas",back_populates="vart_atsakymai")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
# ------------------------------------------------------------------------------------------

# # sukuria defaultini useri
# db_file = './db/testu.db'
# if not os.path.exists(db_file):
#     # Naujas vartotojas
#     admin_vart_o = Vartotojas(vardas="admin", slaptazodis="admin")
#     statistika_o = VartotojoStatistika()
#     admin_vart_o.statistika = statistika_o
#     session.add(admin_vart_o)
#     session.commit()
#
# # False True
# NaujasVartotojas = False
# Nauja_temaF = False
# Nauja_sesijaF = False
#
# if NaujasVartotojas:
#     # Naujas vartotojas
#     vartot_o = Vartotojas(vardas="Tomas", slaptazodis="AAAA")
#     statistika_o = VartotojoStatistika()
#     vartot_o.statistika = statistika_o
#     session.add(vartot_o)
#     session.commit()
#
# if Nauja_temaF:
#     tema01_o = Tema(pavadinimas="Python testas I d.")
#     klausimas01_o = Klausimas(pavadinimas="Kaip inicijuoti sąraša?")
#     atsak1_1o = Atsakymas(vardas="...[]", teisingas=True, balas=1.0)
#     atsak1_2o = Atsakymas(vardas="...{}", balas=0)
#     atsak1_3o = Atsakymas(vardas="...<>", balas=0)
#     ats = [atsak1_1o, atsak1_2o, atsak1_3o]
#     klausimas01_o.atsakymai = ats
#     tema01_o.klausimai.append(klausimas01_o)
#     session.add(tema01_o)
#     session.commit()
#
# sesijax_o = Sesija()
# userx_o = session.query(Vartotojas).get(1)
# sesijax_o.vartotojas = userx_o
#
# if Nauja_sesijaF:
#     # vart_ats_o = VartotojoAtsakymas()
#     # vart_ats_o.sesija = sesijax_o
#
#     # Esamas klausimas
#     klaus = session.query(Klausimas).filter(Klausimas.id == 1).all()
#     # pasirinktas atsakymas
#     atsx = session.query(Atsakymas).filter(Atsakymas.klausimas_id == klaus[0].id).all()
#     pasirinkimas = atsx[1]
#     vatsak = VartotojoAtsakymas()
#     vatsak.sesija = sesijax_o
#     vatsak.atsakymas = pasirinkimas
#     session.add(vatsak)
#     # rezultatas
#     rezultats_o = Rezultatas()
#     rezultats_o.sesija = sesijax_o
#     rezultats_o.balai = vatsak.atsakymas.balas
#     session.add(rezultats_o)
#     session.commit()
#
# # vart_o=Vartotojas(vardas="Rolka2",slaptazodis= "aa")
# # statistika_o=VartotojoStatistika(atlikti_testai=5,testu_vidurkis_proc=23.3,pradeti_testai=1,bendri_balai=80)
# # vart_o.statistika=statistika_o
# # session.add(vart_o)
# # session.commit()
#
# # vart_db = session.query(Vartotojas).all()
# # for x in vart_db:
# #     print(x.id, x.vardas)
# # userx1 = session.query(Vartotojas).get(1)
# # # session.delete(delet_ob)
# # # session.commit()
# # # print('trinsim', delet_ob.id, delet_ob.vardas)
# # sesijax_o = Sesija()
# # sesijax_o.vartotojas = userx1
# # session.add(sesijax_o)
# # print(sesijax_o.vartotojas.vardas)
