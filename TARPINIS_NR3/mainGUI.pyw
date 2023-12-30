import copy
from tkinter import Menu, filedialog
from myWidgets import *
from myNewUser import *
from myEdits import TemuRedagavimas
import time
from testaidb_controller import *


class MainWindows:
    __geometry01 = "600x500"
    __geometry02 = "1200x500"

    def __init__(self, master):
        # Kintamuju inicializacija
        self._testo_visi_klausimai = None
        self.__isr_tema = None
        self.fr_meniu = None
        self.frm_temos = None
        self.listBox = None
        self.fr_infobar = None
        self.fr_klausim_navig = None
        self.fr_klausimai = None
        self._aktyvus_klausimas = None
        self.l1_infobar = None
        self.fr_login = None
        self.e_user = None
        self.e_passw = None
        self.fr_klausimo_istor = None
        self.s = None
        self.prisijung_ses = None
        self.sql_temos = None
        self.temos_df = None
        self.orm_vart_atsakymu_istor = None
        self.df_vart_atsakymu_istor = None
        self.vart_atsakymu_istor = None
        self.fr_temu_istor = None
        self.klaus_istor_z = {}
        self.istorija_index01 = 0
        self._kl_index = 0
        self._kl_kiekis = 0
        self._kl_taskai = 0
        self._testo_taskai = 0
        self._testo_rezultatas = 0
        self._temos_klausimai_atsakymai = {}
        self.laikas_dabar = None
        self.file_menu = None
        self.sql_menu = None
        # self.praejes_laikas = None
        self.after_id = None
        self.praejes_laik_varSTr = tk.StringVar()
        self.praejes_laik_varSTr.set("0:00")
        self._sesij_pateikta = False
        self.btn_pateikti = None

        style_teising = ttk.Style()
        style_teising.configure("teisingas.TCheckbutton",
                                font=("Courier New", 12, "normal"), background="lime", foreground="black")
        style_blog = ttk.Style()
        style_blog.configure("blogas.TCheckbutton",
                             font=("Courier New", 12, "normal"), background="#f2cac9", foreground2="black")

        self.master = master
        self.master.title("Testų žaidimas")
        self.master.geometry(self.__geometry01)
        self.meniu_juosta()
        self.init_login()
        admin_vartotojas()
        self.master.mainloop()

    @staticmethod
    def redaguoti_temas():
        TemuRedagavimas()

    @staticmethod
    def sukurti_vartotoja():
        NaujasVartotojas()

    @staticmethod
    def importuoti_testa():

        f_testas = filedialog.askopenfilename(
            title="Pasirinkite testo failą", filetypes=(("Text failai", "*.txt"),
                                                        ("Visi failai", "*.*")), initialdir="./")
        test_df = nuskaityti_importa(failas=f_testas)
        import_test_to_sql(test_df)

    def init_login(self):
        self.fr_login = tk.Frame(self.master)
        self.fr_login.pack(expand=True)
        l_user = MLable01(self.fr_login, text="Vartotojas:")
        l_passw = MLable01(self.fr_login, text="Slaptažodis:")
        self.e_user = MEntry01(self.fr_login)
        self.e_passw = MEntry01(self.fr_login, show="*")
        btn_login = MButton03(self.fr_login, text="Prisijugti", command=self.login_ok)
        self.e_user.insert(tk.END, "admin")  # ----------------------
        self.e_passw.insert(tk.END, "admin")  # ---------------------

        l_user.grid(row=0, column=0, sticky=tk.E)
        l_passw.grid(row=1, column=0, sticky=tk.E)
        self.e_user.grid(row=0, column=1)
        self.e_passw.grid(row=1, column=1)
        btn_login.grid(row=2, column=1, pady=10, sticky=tk.E)

    def login_ok(self):
        self.prisijung_ses = nauja_prisijung_sesija(vardas=self.e_user.get(), slaptazodis=self.e_passw.get())
        if self.prisijung_ses[0]:
            self.fr_login.destroy()
            if self.prisijung_ses[1].admin_teises:
                self.tesises_on()
            self.mainmeniu()
        else:
            messagebox.showerror("KLAIDA", "Blogi prisijungimo duomenys!")

    def exit_wind(self):
        self.master.quit()

    def mainmeniu(self):
        if self.frm_temos is not None:
            self.frm_temos.destroy()
        if self.fr_temu_istor is not None:
            self.fr_temu_istor.destroy()
        self.fr_meniu = tk.Frame(self.master)
        self.fr_meniu.pack(expand=True)
        btn_atlikti = MButton01(self.fr_meniu, text="Peržiūreti atliktus testus",
                                command=self.perziureti_atliktus_testus, width=30)
        btn_temos = MButton01(self.fr_meniu, text="Rinktis temą", command=self.temusar, width=30)
        btn_atsijungti = MButton01(self.fr_meniu, text="Atsijungti", command=self.atjungti_sesija)
        btn_iseiti = MButton01(self.fr_meniu, text="Išeiti", command=self.exit_wind)
        btn_atlikti.pack(side=tk.TOP)
        btn_temos.pack(fill=tk.X)
        btn_atsijungti.pack(fill=tk.X)
        btn_iseiti.pack(fill=tk.X)

    def perziureti_atliktus_testus(self):
        self.orm_vart_atsakymu_istor = orm_atlikti_testai(self.prisijung_ses[1])
        self.df_vart_atsakymu_istor = []
        for vart, ses, vats, ats, kl, tem in self.orm_vart_atsakymu_istor:
            # 0.v.id 1.vardas 2.ses.id 3.tem.id 4.tem.pavadin 5.kl.id 6.kl.pavadin 7atsakym[]
            self.df_vart_atsakymu_istor.append([vart.id, vart.vardas, ses.id, tem.id, tem.pavadinimas,
                                                kl.id, kl.pavadinimas,
                                                [ats.id, ats.vardas, ats.balas, vats.atsakymas_id]])
        self.fr_meniu.destroy()
        self.istorija_temu()

    def istorija_temu(self):
        self.fr_temu_istor = tk.Frame(self.master)
        self.fr_temu_istor.pack(expand=True)
        self.listBox = tk.Listbox(self.fr_temu_istor, width=50, height=20, font=("Courier New", 12))
        self.listBox.pack()
        btn_perziuret = MButton01(self.fr_temu_istor, text="Peržiūrėti", command=self.istorija_klausimu)
        btn_perziuret.pack(fill=tk.X)
        btn_gryzt = MButton01(self.fr_temu_istor, text="Grįžti", command=self.mainmeniu)
        btn_gryzt.pack(fill=tk.X)
        temos_l = []
        for el1 in self.df_vart_atsakymu_istor:
            temp_tema = str(el1[2]) + "||" + el1[4]
            if temp_tema not in temos_l:
                temos_l.append(temp_tema)
        for tem2 in temos_l:
            str1 = tem2.split("||")
            self.listBox.insert(tk.END, f'{str1[0]}|' + str1[1])

    def istorija_klausimu(self):
        """ tema[0]=id, tema[1]=pavadinimas"""
        isrinkta = self.listBox.selection_get().split("|")
        klausimai_l = []
        klausid_l = []
        self.klaus_istor_z = {}
        atsid_l = []
        atsak_l = []
        for el in self.df_vart_atsakymu_istor:
            if int(isrinkta[0]) == el[2]:
                if el[5] not in klausid_l:
                    atsak_l = []
                    klausid_l.append(el[5])
                    klausimai_l.append(el[6])
                    atsak_l.append(
                        [el[7][0], el[7][1], el[7][2], el[7][3]])  # ats.id, ats.vardas, ats.balas, vartot.ats_id
                    atsid_l.append(el[7][1])
                    r = str(el[5]) + "||" + el[6]
                    self.klaus_istor_z.update({r: atsak_l})
                else:
                    atsak_l.append([el[7][1], el[7][2]])
                    atsid_l.append(el[7][1])
                    r = str(el[5]) + "||" + el[6]
                self.klaus_istor_z.update({r: atsak_l})

        self.istorija_index01 = 0
        self.istorija_naujas_klausimo_langas(self.istorija_index01, self.klaus_istor_z)

    def istorija_naujas_klausimo_langas(self, index, klaus_z):
        self.master.geometry(self.__geometry02)
        if self.fr_klausimo_istor is not None:
            self.fr_klausimo_istor.destroy()
        tem_klausimai = list(klaus_z.keys())
        if index >= len(tem_klausimai):
            self.master.geometry(self.__geometry01)
            self.istorija_temu()
            return
        atss = orm_gauti_atsakymus_pagal_klid(tem_klausimai[index].split("||")[0])
        self.fr_temu_istor.destroy()
        self.fr_klausimo_istor = tk.Frame(self.master)
        self.fr_klausimo_istor.pack(expand=True)#grid(row=0, column=0, pady=10, sticky=tk.S)
        temp_kl = f"{self.istorija_index01 + 1}. " + tem_klausimai[index].split("||")[1]
        l_klausim01 = MLable01(self.fr_klausimo_istor, text=temp_kl)
        l_klausim01.grid(row=0, column=0, pady=10, sticky="ew")
        i = 1
        offsx = 0
        for i, ats_x in enumerate(atss, 1):
            cbxname = f"ats_{i + offsx - 1}"
            vcbxname = f"kint_{i + offsx - 1}"

            bool_var = globals()[vcbxname] = tk.BooleanVar(name=vcbxname)
            bool_var.set(False)
            globals()[cbxname] = MCheckbutton01(self.fr_klausimo_istor, text=ats_x[1],
                                                variable=bool_var, name=cbxname)
            cbtnx = globals()[cbxname]
            cbtnx["state"] = "disabled"
            vart_ats = klaus_z.get(tem_klausimai[index])
            print("vart_ats", vart_ats)
            print("ats_x", ats_x)
            if vart_ats[0][0] == ats_x[0]:
                bool_var.set(True)
                cbtnx.configure(style="blogas.TCheckbutton")

            if ats_x[2] > 0.0:
                cbtnx.configure(style="teisingas.TCheckbutton")

            cbtnx.grid(row=i, column=0, pady=10, sticky="ew")
            offsx == 50

        btn_klausim01 = MButton01(self.fr_klausimo_istor, text="Sekantis klausimas", command=self.istorija_kitas)
        btn_klausim01.grid(row=i + 1, column=0, pady=10, sticky="S")

    def istorija_kitas(self):
        self.istorija_index01 += 1
        self.istorija_naujas_klausimo_langas(self.istorija_index01, self.klaus_istor_z)

    def atjungti_sesija(self):
        self.fr_meniu.destroy()
        self.init_login()
        self.tesises_off()
        self.prisijung_ses = None

    def temusar(self):
        self.fr_meniu.destroy()
        self.frm_temos = tk.Frame(self.master)
        self.frm_temos.pack(expand=True)  # expand=True  side=tk.TOP, anchor=tk.W side=tk.CENTER

        # saraso variantas
        self.listBox = tk.Listbox(self.frm_temos, width=50, height=20, font=("Courier New", 12))
        self.listBox.pack()
        self.sql_temos = nuskaityti_temas()
        for i, tem in enumerate(self.sql_temos, 0):
            self.listBox.insert(tk.END, f"{i + 1}. " + tem)
        btn_start = MButton01(self.frm_temos, text="Pradėti", command=self.start_test)
        btn_gryzt = MButton01(self.frm_temos, text="Grįžti", command=self.mainmeniu)
        btn_start.pack(fill=tk.X)
        btn_gryzt.pack(fill=tk.X)

    def start_test(self):
        self._kl_index = 0
        self._testo_taskai = 0
        self._kl_taskai = 0
        self._testo_rezultatas = 0
        self._sesij_pateikta = False
        indx = self.listBox.curselection()
        if indx == ():
            messagebox.showinfo("Nepasirinkote", "Pasirinkite temą!")
            return
        self.__isr_tema = self.listBox.selection_get()
        self.__isr_tema = self.__isr_tema.replace(f"{indx[0] + 1}. ", "")
        self.master.geometry(self.__geometry02)
        self.temos_df = nuskaityti_klausimus(tema=self.__isr_tema)
        self._testo_visi_klausimai = copy.deepcopy(self.temos_df.get(self.__isr_tema))
        self._kl_kiekis = len(self._testo_visi_klausimai.keys())
        self.frm_temos.destroy()
        self.naujas_klausimas(self._sesij_pateikta)
        self.start_laikm()
        self.s = nauja_testo_sesija(self.prisijung_ses[1])

    def naujas_klausimas(self, pateikta):

        self.fr_klausimai = tk.Frame(self.master)
        self.fr_klausimai.pack(expand=True)
        l_klausimas = MLable01(self.fr_klausimai)
        l_kl_vert = MLable02(self.fr_klausimai)
        l_klausimas.grid(row=0, column=0, sticky="ew")
        l_kl_vert.grid(row=1, column=0, sticky="ew")
        klausimai = list(self._testo_visi_klausimai.keys())
        self._aktyvus_klausimas = klausimai[self._kl_index]
        l_klausimas["text"] = f"{self._kl_index + 1}. " + self._aktyvus_klausimas.split("||")[1]
        self._temos_klausimai_atsakymai = {}
        kl_verte = 0
        for i, ats in enumerate(self._testo_visi_klausimai.get(self._aktyvus_klausimas), 2):
            kl_verte += ats[2]
            cbxname = f"ats_{i - 1}"
            vcbxname = f"kint_{i - 1}"
            self._temos_klausimai_atsakymai[cbxname] = [vcbxname, ats[2], ats[3]]
            bool_var = globals()[vcbxname] = tk.BooleanVar(name=vcbxname)
            bool_var.set(ats[3])
            globals()[cbxname] = MCheckbutton01(self.fr_klausimai, text=ats[1], command=self.zymeti_ats,
                                                variable=bool_var, name=cbxname)
            cbtnx = globals()[cbxname]
            cbtnx.grid(row=i, column=0, pady=10, sticky="ew")
            if pateikta:
                cbtnx["state"] = "disabled"
                if ats[3] > 0:
                    cbtnx.configure(style="blogas.TCheckbutton")
                if ats[2] > 0:
                    cbtnx.configure(style="teisingas.TCheckbutton")
        l_kl_vert["text"] = f"({kl_verte} bal.)"
        self.init_infobar()
        self.init_navigac_mygt()

    def zymeti_ats(self):
        wdgx = self.fr_klausimai.focus_get().winfo_name()
        wdgx_var = self._temos_klausimai_atsakymai.get(wdgx)
        i = int(wdgx.replace("ats_", "")) - 1
        kl_atsakymai = self._testo_visi_klausimai.get(self._aktyvus_klausimas)
        kl_atsakymai[i][3] = self.fr_klausimai.getvar(wdgx_var[0])
        self._testo_visi_klausimai.update({self._aktyvus_klausimas: kl_atsakymai})

    def atgal(self):
        self._kl_index -= 1
        if self._kl_index <= 0:
            self._kl_index = 0
        self.fr_klausimai.destroy()
        self.fr_klausim_navig.destroy()
        self.fr_infobar.destroy()
        self.naujas_klausimas(self._sesij_pateikta)

    def pirmyn(self):
        self._kl_index += 1
        self.fr_klausimai.destroy()
        self.fr_klausim_navig.destroy()
        self.fr_infobar.destroy()
        if self._kl_index + 1 > self._kl_kiekis:
            self.fr_klausimai = tk.Frame(self.master)
            self.fr_klausimai.pack(expand=True)
            self.btn_pateikti = MButton01(self.fr_klausimai, text="Pateikti", command=self.pateikti_testa)
            self.btn_pateikti.pack()
            self.init_infobar()
            self.init_navigac_mygt()
            if self._sesij_pateikta:
                self.testo_uzrakinimas()
            else:
                self.btn_pateikti["state"] = "normal"

        else:
            self.naujas_klausimas(self._sesij_pateikta)

    def pateikti_testa(self):
        self.skaiciuoti_taskus()
        laik_str = self.praejes_laik_varSTr.get().replace('Laikas:', '')
        laik_l = laik_str.split(':')
        if len(laik_l) == 3:
            valand, minut, sekund = map(int, laik_l)
            laik = datetime.time(hour=valand, minute=minut, second=sekund)
        else:
            minut, sekund = map(int, laik_l)
            laik = datetime.time(minute=minut, second=sekund)
        orm_pateikti_rezultata(testo_sesij=self.s, pateikta=True, balai=self._testo_rezultatas, laikas=laik)
        self.visi_orm_klaus_ats()
        self.testo_uzrakinimas()

    def visi_orm_klaus_ats(self):
        df = self._testo_visi_klausimai
        for rakt in df.keys():
            atsx_l = df.get(rakt)
            for atsx in atsx_l:
                ats_obj = orm_gauti_atsakyma(ats_id=atsx[0])
                orm_vartotoj_atsakym(testo_ses=self.s, atsakymas_o=ats_obj)
                # if atsx[3] > 0:
                #     ats_obj = orm_gauti_atsakyma(ats_id=atsx[0])
                #     orm_vartotoj_atsakym(testo_ses=self.s, atsakymas_o=ats_obj)

    def testo_uzrakinimas(self):
        self.stop_laikm()
        self._sesij_pateikta = True
        self.btn_pateikti["state"] = "disabled"
        self.btn_pateikti.destroy()
        l_taskai = MLable03(self.fr_klausimai, taskai=self._testo_rezultatas)
        l_laikas = MLable04(self.fr_klausimai)
        l_taskai.pack(pady=20)
        l_laikas.pack()
        l_taskai["text"] = f"Viso surinkote {self._testo_rezultatas} %"
        l_laikas["text"] = f"Jusų laikas {self.praejes_laik_varSTr.get().replace('Laikas:', '')}"
        btn_baigti = MButton01(self.fr_klausimai, text="Uždaryti testą", command=self.testo_uzdarymas)
        btn_baigti.pack(pady=10)

    def testo_uzdarymas(self):
        self.fr_klausimai.destroy()
        self.fr_klausim_navig.destroy()
        self.fr_infobar.destroy()
        self.mainmeniu()
        self.master.geometry(self.__geometry01)

    def init_navigac_mygt(self):
        self.fr_klausim_navig = tk.Frame(self.master)
        self.fr_klausim_navig.pack(side=tk.BOTTOM)  # expand=True
        btn_kitas = MButton01(self.fr_klausim_navig, text="Sekantis", command=self.pirmyn)
        btn_atgal = MButton01(self.fr_klausim_navig, text="Atgal", command=self.atgal)
        btn_kitas.grid(row=1, column=1, padx=100, pady=100)
        btn_atgal.grid(row=1, column=0, padx=100, pady=100)
        if self._kl_index == self._kl_kiekis:
            btn_kitas['state'] = 'disabled'
        if self._kl_index == 0:
            btn_atgal['state'] = 'disabled'

    def init_infobar(self):
        self.fr_infobar = tk.Frame(self.master)
        self.fr_infobar.pack(side=tk.BOTTOM, fill=tk.X)
        self.l1_infobar = MLableInfoBar(self.fr_infobar, textvariable=self.praejes_laik_varSTr, anchor=tk.E, padx=20)
        self.l1_infobar.pack(fill=tk.X)

    # ----------- LAIKMATIS ----------------------
    def start_laikm(self):
        self.laikas_dabar = time.time()
        self.atnaujint_laikm()

    def stop_laikm(self):
        self.master.after_cancel(self.after_id)

    def atnaujint_laikm(self):
        viso_sek = int(time.time() - self.laikas_dabar)
        minut = viso_sek // 60
        sekund = viso_sek % 60
        self.praejes_laik_varSTr.set(f"Laikas: {minut}:{sekund:02d}")
        # atnaujina laikmacio verte, kas 1000 ms
        self.after_id = self.master.after(500, self.atnaujint_laikm)

    # ------------------------------------------------

    def meniu_juosta(self):
        self.file_menu = Menu(self.master, tearoff=0, font=("Courier New", 11))
        self.sql_menu = Menu(self.master, tearoff=0, font=("Courier New", 11))
        view_menu = Menu(self.master, tearoff=0, font=("Courier New", 11))

        menubar = Menu(self.master)
        menubar.add_cascade(
            label="File",
            menu=self.file_menu
        )
        menubar.add_cascade(
            label="Įrankiai",
            menu=self.sql_menu
        )
        menubar.add_cascade(
            label="View",
            menu=view_menu
        )
        self.master.config(menu=menubar)
        self.sql_menu.add_command(
            label="Naujas vartotojas",
            command=self.sukurti_vartotoja
        )
        self.sql_menu.add_command(
            label="Redaguoti temas",
            command=self.redaguoti_temas
        )
        self.file_menu.add_command(
            label='Importuoti testą',
            command=self.importuoti_testa,
        )
        self.file_menu.add_command(
            label='Uždaryti',
            command=self.master.destroy,
        )
        view_menu.add_command(
            label="Per visą ekraną",
            command=self.fullscreen
        )
        self.tesises_off()

    def tesises_off(self):
        self.sql_menu.entryconfigure(0, state='disabled')
        self.sql_menu.entryconfigure(1, state='disabled')
        self.file_menu.entryconfigure(0, state='disabled')

    def tesises_on(self):
        self.sql_menu.entryconfigure(0, state='normal')
        self.sql_menu.entryconfigure(1, state='normal')
        self.file_menu.entryconfigure(0, state='normal')

    def fullscreen(self):
        stat = self.master.attributes('-fullscreen')
        if stat == 0:
            self.master.attributes('-fullscreen', True)
        else:
            self.master.attributes('-fullscreen', False)

    def skaiciuoti_taskus(self):
        for klaus in self._testo_visi_klausimai.keys():
            atsakymai = self._testo_visi_klausimai.get(klaus)
            temp_task = 0
            for atsx in atsakymai:
                self._kl_taskai += atsx[2]
                if atsx[3] > 0 and atsx[2] > 0:
                    temp_task += atsx[2]
                if atsx[3] > 0 and atsx[2] == 0:
                    temp_task = 0.0
                    break
            self._testo_taskai += temp_task

        self._testo_rezultatas = round(self._testo_taskai / self._kl_taskai * 100)


#
#
# # pack: -after, -anchor, -before, -expand, -fill, -in, -ipadx, -ipady, -padx, -pady, or -side
# # grid: -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
#
# # # Pack the buttons with different fill options
# #         button1.pack(fill=tk.X)
# #         button2.pack(fill=tk.Y)
# #         button3.pack(fill=tk.BOTH)
mainw = tk.Tk()
MainWindows(mainw)
