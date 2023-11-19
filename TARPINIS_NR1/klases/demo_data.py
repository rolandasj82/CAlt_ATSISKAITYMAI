import datetime
from dateutil.relativedelta import relativedelta
import calendar
import random
from TARPINIS_NR1.klases.sql_model_tm import NaujasVartotojas, Proj_Irasas, Proj_Islaidos, TM_Irasas, Session


class MazaDetalizacija:
    def __init__(self, root_prj: Proj_Irasas, data_inp: list, sessionx: Session):
        """ dataInp=[
                    [Įranga,[[SQL serveris,12000],[serverių spinta,3000]]],
                    [Programavimas,[[SQL migracija,20000],[Naujų duomenų įvedimas,10000]]]
                      ]"""
        self.root_prj = root_prj
        self.data_inp = data_inp
        self.sessionx = sessionx

    def rasytiSQL(self):
        prj_medis = []
        p_000 = Proj_Islaidos(self.root_prj.pr_nr, self.root_prj.pr_vardas, self.root_prj.pr_verte)
        prj_medis.append(p_000)
        k = 1
        for el in self.data_inp:
            p_num = 100 * k
            p_x0x = Proj_Islaidos(self.root_prj.pr_nr + f"_{p_num}", el[0], 0, p_000)
            prj_medis.append(p_x0x)
            ded_sum = 0
            for el2 in el[1]:
                p_num += 10
                p_xxx = Proj_Islaidos(self.root_prj.pr_nr + f"_{p_num}", el2[0], el2[1], p_x0x)
                prj_medis.append(p_xxx)
                try:
                    if el2[1] != None:
                        ded_sum += el2[1]
                except TypeError:
                    pass

            p_x0x.ded_verte = ded_sum
            k += 1
        self.sessionx.add_all(prj_medis)


def generuoti_vartotojus(sessionx: Session):
    demo_vart = ["Vaida", "Eimantas", "Domas", "Aivaras", "Živilė", "Petras", "Jokūbas"]
    for v in demo_vart:
        userx = NaujasVartotojas(v, "s" + v.lower())
        sessionx.add(userx)
    sessionx.commit()
    print("Vartotojai sukurti...")
    return demo_vart


def kurti_demo_projektus(sessionx: Session):
    t1 = datetime.datetime(2023, 9, 18)
    t2 = datetime.datetime(2023, 12, 15)
    proj_01 = Proj_Irasas("T2365", "Vilniaus alėja", "Gatvių apšvietimo automatika", t1, t2, 40_000, "Eur.", 0)
    t1 = datetime.datetime(2023, 2, 3)
    t2 = datetime.datetime(2023, 9, 16)
    proj_02 = Proj_Irasas("T2564", "Nauja statyba", "Gyvenamųjų namų statyba", t1, t2, 2_000_000, "Eur.", 0)
    t1 = datetime.datetime(2020, 5, 3)
    t2 = datetime.datetime(2021, 10, 20)
    proj_03 = Proj_Irasas("T2003", "Europos parama mokykloms", "Klasės kompiuterių atnaujinimas", t1, t2, 60_000,
                          "Eur.", 1)
    t1 = datetime.datetime(2022, 11, 20)
    t2 = datetime.datetime(2023, 6, 2)
    proj_04 = Proj_Irasas("T2063", "Auto logistika", "Duombazes atnaujinimo darbai", t1, t2, 67_000, "Eur.", 0)
    t1 = datetime.datetime(2023, 12, 10)
    t2 = datetime.datetime(2024, 4, 7)
    proj_05 = Proj_Irasas("T2883", "Kaunos Statistika", "Informacinė sistemos atnaujinimas ", t1, t2, 200_000, "Eur.",
                          0)
    t1 = datetime.datetime(2023, 10, 1)
    t2 = datetime.datetime(2024, 2, 1)
    proj_06 = Proj_Irasas("T3569", "Vilniaus Statistika", "SQL duombazės migracija ", t1, t2, 100_000, "Eur.", 0)
    t1 = datetime.datetime(2023, 9, 6)
    t2 = datetime.datetime(2024, 3, 14)
    proj_07 = Proj_Irasas("T2578", "Telekomunikacija AG", "Interaktyvios televizijos paslaugos", t1, t2, 55_000,
                          "Eur.", 0)
    t1 = datetime.datetime(2023, 12, 2)
    t2 = datetime.datetime(2024, 7, 5)
    proj_08 = Proj_Irasas("T2238", "Baldų gamyba", "ERP valdymo sistema ", t1, t2, 360_000,
                          "Eur.", -1)
    sessionx.add_all([proj_01, proj_02, proj_03, proj_04, proj_05, proj_06, proj_07, proj_08])
    sessionx.commit()
    print("Projektai sukurti...")


def kurti_demo_detalizacija(sessionx: Session):
    root_projs = sessionx.query(Proj_Irasas).all()
    data0 = [["Bendros", [["Bendros valandos", 0]]]]
    data1 = [["Mokymai", [["Mokymų valandos", 0]]]]
    data2 = [
        ["Įranga", [["Lempos", 10000], ["Metalo konstrukcijos", 30000], ["Automatikos komponentai", 16000]]],
        ["Projektavimo darbai", [["Konstrukcijų projektavimas", 10000], ["Automatikos projektavimas", 12000]]],
        ["Programavimas", [["PLV programavimas", 10000], ["Duomenų perdavimas", 12000]]],
        ["Projekto valdymas", [["Projokto vadovo kaštai", 15000]]],
        ["Instaliacijos darbai", [["Mechanikos instaliacija", 15000], ["Automatikos instaliacija", 8500]]],
    ]
    data3 = [
        ["Medžiagos", [["Statybinės medžiagos", 600000], ["Armatūros", 70000]]],
        ["Statyba", [["Statyba", 200000]]],
    ]
    data4 = [
        ["Įranga", [["Kompiuteriai", 50000], ["IT papildoma įranga", 6000]]],
        ["Instaliacijos darbai", [["Kompiuterių instaliacija klasėse", 20000], ["Elektros instaliacija", 1000]]],
    ]
    data5 = [
        ["Įranga", [["SQL serveris", 15000], ["Serverių spinta", 3000]]],
        ["Programavimas", [["SQL migracija", 20000], ["SQL naujų duomenų suvedimas", 12000]]],
    ]
    data6 = [
        ["Įranga", [["DELL serveriai", 15000], ["Serverių spinta", 3000]]],
        ["Instaliacijos darbai", [["Senos įrangos išmontavimas", 5000], ["Naujos įrangos montavimas", 8520]]],
        ["Programavimas", [["SQL migracija", 20000], ["SQL nauju duomenu suvedimas", 12000]]],
    ]
    data7 = [
        ["Įranga", [["Serveriai", 15000], ["Serverių spinta", 3200]]],
        ["Instaliacijos darbai", [["Serverių instaliacija", 2300]]],
        ["Programavimas", [["SQL migracija", 15200], ["SQL nauju duomenu suvedimas", 21586]]],
    ]
    data8 = [
        ["Įranga", [["HPE Serveriai", 48200], ["Serverių spinta", 9600]]],
        ["Projektavimo darbai", [["IT architekturos projektavimas", 13200], ["Skydų projektavimas", 15156]]],
        ["Programavimas", [["Serverių paruošimas", 25630], ["Vartotojo programos kūrimas", 86520],
                           ["Komunikacijų programavimas", 25300]]],
        ["Projekto valdymas", [["Projekto vadovo valandos", 13200]]],
    ]
    data9 = [
        ["Įranga", [["Serveriai", 23500], ["Komunikacinė įranga", 45000]]],
        ["Instaliacijos darbai", [["Komunikacijos konverterių instaliacija gamyboje", 16300]]],
        ["Programavimas", [["Gamybos duomenų surinkimas", 56000], ["Statistikos programavimas", 34300]]],
        ["Projekto valdymas", [["Projekto vadovo valandos", 33200]]],
        ["Dienpinigiai", [["Dienpinigiai", 30000]]],
        ["Keliones", [["Lektuvo bilietai", 10000], ["Apgyvendinimas", 56420]]],
    ]
    all_data = [data0, data1, data2, data3, data4, data5, data6, data7, data8, data9]
    n = 0
    for rootx in root_projs:
        kint_vard = f"data{n}"
        datax = globals()[kint_vard] = all_data[n]
        objx = MazaDetalizacija(rootx, datax, sessionx)
        objx.rasytiSQL()
        n += 1
    sessionx.commit()
    print("Projektų detalizacijos sukurtos...")


def kurti_demo_TM_irasus(sesionx: Session):
    komentarai = ["Nebaigti darbai.", "Negalima testi darbų, nes rangovas neatliko savųjų.", "Mano dalis jau padaryta",
                  "Dėl tolimesnių darbų, reikia daryti komandos susirinkimą",
                  "Trūksta resursų, farbai laiku nebus baigti", "Darbams užbaigti liko viena diena",
                  "Darbų metu įvyko sistemos lūžimas. Bus pretenzija iš kliento", "Viskas padaryta", " "]
    visi_prj = sesionx.query(Proj_Irasas).all()
    visi_vart = sesionx.query(NaujasVartotojas).all()
    # Išrenkamas mėnesis
    dabar_dt = datetime.datetime.now()
    men_1 = dabar_dt - relativedelta(months=2)
    men_2 = dabar_dt - relativedelta(months=1)
    men_l=[men_1,men_2]
    visi_irasai = []
    for men_x in men_l:
        d_num = calendar.monthrange(men_x.year, men_x.month)[1]
        for asmuo in visi_vart:
            if asmuo.vardas != "admin" and asmuo.vardas != "user":
                for dd in range(1, d_num + 1):
                    savait_diena = datetime.datetime(men_x.year, men_x.month, dd).isoweekday()
                    if savait_diena != 6 and savait_diena != 7:
                        dirb_val = random.randint(1, 5)
                        start_val = random.randint(8, 16)
                        if start_val + dirb_val > 17:
                            dirb_val = 17 - start_val
                        start_dt = datetime.datetime(men_x.year, men_x.month, dd, start_val, 0)
                        end_dt = datetime.datetime(men_x.year, men_x.month, dd, start_val + dirb_val, 0)
                        esam_proj = random.choice(visi_prj)
                        proj_visos_isl = sesionx.query(Proj_Islaidos).filter(
                            Proj_Islaidos.pr_nr.ilike(f"%{esam_proj.pr_nr}%")).all()
                        proj_visos_isl2 = [isl for isl in proj_visos_isl if len(isl.pr_nr) > 5]
                        esam_proj_kategor = random.choice(proj_visos_isl2)
                        komentaras = random.choice(komentarai)
                        tm_1 = TM_Irasas(asmuo.id, asmuo.vardas, esam_proj.pr_nr, esam_proj.pr_vardas,
                                         esam_proj_kategor.ded_aprasymas,
                                         start_dt, end_dt, komentaras)
                        visi_irasai.append(tm_1)
    sesionx.add_all(visi_irasai)
    sesionx.commit()
    print("Praito mėnesio tabelis užpildytas...")
