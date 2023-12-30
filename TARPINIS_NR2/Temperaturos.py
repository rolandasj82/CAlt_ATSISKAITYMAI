import tkinter as tk
from tkinter import colorchooser
import matplotlib.pyplot as plt
import requests


class PasaulioTemper:
    def __init__(self, master):
        self.HOST = "https://api-temperaturos.run-eu-central1.goorm.site"
        self.ENDPOINT = "/v1/temperaturos"
        self.master = master
        self.fonosp = "#7cc58e"
        self.txt_font12 = ("Helvetica", 12, "normal")
        self.txt_font12b = ("Helvetica", 12, "bold")
        self.txt_font10i = ("Helvetica", 10, "italic")
        self.infe_bcolor = '#c0c5c0'
        master.configure(bg=self.fonosp)
        # master.resizable(False, False)

        # print(colorchooser.askcolor())

        self.l_top = tk.Label(master, text="Temperatūros pasaulyje", bg=self.fonosp, height=2)
        self.l_top.configure(font=("Helvetica", 16, "bold"), foreground="blue")
        self.l_top.grid(row=0, column=2, padx=0, pady=0)

        m_pos = (1, 0)
        self.l_miestas = tk.Label(master, text="Miestas:", bg=self.fonosp, font=self.txt_font12)
        self.l_miestas.grid(row=m_pos[0], column=m_pos[1], padx=10, pady=10)
        self.e_miestas = tk.Entry(master, font=self.txt_font12)
        self.e_miestas.insert(0, "Vilnius")
        self.e_miestas.configure(state="normal")
        self.e_miestas.grid(row=m_pos[0], column=m_pos[1] + 1, padx=10, pady=10, sticky=tk.W)

        self.l_start = tk.Label(master, text="Data nuo:", bg=self.fonosp, font=self.txt_font12)
        self.l_start.grid(row=m_pos[0] + 1, column=m_pos[1], padx=10, pady=10)
        self.e_start = tk.Entry(master, font=self.txt_font12)
        self.e_start.insert(0, "2019-05-01")
        self.e_start.grid(row=m_pos[0] + 1, column=m_pos[1] + 1, padx=10, pady=10, sticky=tk.W)

        self.l_end = tk.Label(master, text="Data iki:", bg=self.fonosp, font=self.txt_font12)
        self.l_end.grid(row=m_pos[0] + 2, column=m_pos[1], padx=10, pady=10)
        self.e_end = tk.Entry(master, font=self.txt_font12)
        self.e_end.insert(0, "2019-05-12")
        self.e_end.grid(row=m_pos[0] + 2, column=m_pos[1] + 1, padx=10, pady=10, sticky=tk.W)

        self.btn_ieskot = tk.Button(master, text="Ieškoti", command=self.get_api_data, font=self.txt_font12)
        self.btn_ieskot.grid(row=m_pos[0] + 3, column=m_pos[1] + 1, columnspan=2, pady=0, sticky=tk.W)

        self.btn_plot = tk.Button(master, text="Kreivė", command=self.draw_plot, font=self.txt_font12, state="disabled")
        self.btn_plot.grid(row=m_pos[0] + 3, column=m_pos[1] + 2, columnspan=2, pady=0, sticky=tk.W)

        # ----informaciniai laukai:
        i_pos = (1, 2)

        self.li_miestas = tk.Label(master, text="Miestas:", bg=self.fonosp, font=self.txt_font12, width=7)
        self.li_miestas.grid(row=i_pos[0], column=i_pos[1], sticky=tk.E)
        self.li_miestas_v = tk.Entry(master)
        self.li_miestas_v.grid(row=i_pos[0], column=i_pos[1] + 1, sticky=tk.W)
        self.li_miestas_v.config(font=self.txt_font12, bg=self.infe_bcolor)

        self.li_salis = tk.Label(master, text="Šalis:", bg=self.fonosp, font=self.txt_font12, width=6)
        self.li_salis.grid(row=i_pos[0] + 1, column=i_pos[1], sticky=tk.E)
        self.li_salis_v = tk.Entry(master)
        self.li_salis_v.grid(row=i_pos[0] + 1, column=i_pos[1] + 1, sticky=tk.W)
        self.li_salis_v.config(font=self.txt_font12, bg=self.infe_bcolor)

        self.li_sk = tk.Label(master, text="Šalies kodas:", bg=self.fonosp, font=self.txt_font12, width=12)
        self.li_sk.grid(row=i_pos[0] + 2, column=i_pos[1], sticky=tk.E)
        self.li_sk_v = tk.Entry(master)
        self.li_sk_v.grid(row=i_pos[0] + 2, column=i_pos[1] + 1, sticky=tk.W)
        self.li_sk_v.config(font=self.txt_font12, bg=self.infe_bcolor)

        self.li_gyvent = tk.Label(master, text="Gyventojai:", bg=self.fonosp, font=self.txt_font12, width=9)
        self.li_gyvent.grid(row=i_pos[0] + 3, column=i_pos[1], sticky=tk.E)
        self.li_gyvent_v = tk.Entry(master)
        self.li_gyvent_v.grid(row=i_pos[0] + 3, column=i_pos[1] + 1, sticky=tk.W)
        self.li_gyvent_v.config(font=self.txt_font12, bg=self.infe_bcolor)

        self.li_plat = tk.Label(master, text="Platuma:", bg=self.fonosp, font=self.txt_font12, width=8)
        self.li_plat.grid(row=i_pos[0] + 4, column=i_pos[1], sticky=tk.E)
        self.li_plat_v = tk.Entry(master)
        self.li_plat_v.grid(row=i_pos[0] + 4, column=i_pos[1] + 1, sticky=tk.W)
        self.li_plat_v.config(font=self.txt_font12, bg=self.infe_bcolor)

        self.li_ilg = tk.Label(master, text="Ilguma:", bg=self.fonosp, font=self.txt_font12, width=8)
        self.li_ilg.grid(row=i_pos[0] + 5, column=i_pos[1], sticky=tk.E)
        self.li_ilg_v = tk.Entry(master)
        self.li_ilg_v.grid(row=i_pos[0] + 5, column=i_pos[1] + 1, sticky=tk.W)
        self.li_ilg_v.config(font=self.txt_font12, bg=self.infe_bcolor)

    def status_infoe(self, stat="normal"):
        self.li_miestas_v.config(state=stat)
        self.li_salis_v.configure(state=stat)
        self.li_sk_v.config(state=stat)
        self.li_gyvent_v.config(state=stat)
        self.li_plat_v.config(state=stat)
        self.li_ilg_v.config(state=stat)

    def na_values(self):
        self.li_miestas_v.insert(0, "n/a")
        self.li_salis_v.insert(0, "n/a")
        self.li_sk_v.insert(0, "n/a")
        self.li_gyvent_v.insert(0, "n/a")
        self.li_plat_v.insert(0, "n/a")
        self.li_ilg_v.insert(0, "n/a")

    def get_api_data(self):
        self.status_infoe("normal")
        self.li_miestas_v.delete(0, "end")
        self.li_salis_v.delete(0, "end")
        self.li_sk_v.delete(0, "end")
        self.li_gyvent_v.delete(0, "end")
        self.li_plat_v.delete(0, "end")
        self.li_ilg_v.delete(0, "end")

        self.miestas = self.e_miestas.get()
        self.start = self.e_start.get()
        self.end = self.e_end.get()
        print(f"Miestas: {self.miestas}, Nuo: {self.start}, Iki:{self.end}")
        self.arguments = {"miestas": self.miestas,
                          "start": self.start,
                          "end": self.end}
        r = requests.get(self.HOST + self.ENDPOINT, params=self.arguments)

        try:
            self.req_data = r.json()
        except requests.exceptions.JSONDecodeError:
            self.na_values()
            return

        if not r.ok:
            return
        if self.req_data.get('Informacija 001', None) == None:
            self.miestas = list(self.req_data)[0]
            self.r_gyventojai = self.req_data.get(self.miestas).get('Informacija').get('gyventojai')
            self.r_platuma = self.req_data.get(self.miestas).get('Informacija').get('koordinatės').get('platuma')
            self.r_ilguma = self.req_data.get(self.miestas).get('Informacija').get('koordinatės').get('ilguma')
            self.r_miestas = self.req_data.get(self.miestas).get('Informacija').get('miestas')
            self.r_sk = self.req_data.get(self.miestas).get('Informacija').get('šalies kodas iso3')
            self.r_salis = self.req_data.get(self.miestas).get('Informacija').get('šalis')
            self.r_datos = self.req_data.get(self.miestas).get('Temperatūros').get('data')
            self.r_temper = self.req_data.get(self.miestas).get('Temperatūros').get('vertės')

            self.li_miestas_v.insert(0, self.r_miestas)
            self.li_salis_v.insert(0, self.r_salis)
            self.li_sk_v.insert(0, self.r_sk)
            self.li_gyvent_v.insert(0, self.r_gyventojai[:-2])
            self.li_plat_v.insert(0, self.r_platuma)
            self.li_ilg_v.insert(0, self.r_ilguma)
            # aktyvuojam mygtuką
            self.btn_plot.configure(state="normal")
            print(f"Viso rasta {len(self.r_temper)} temperatūros matavimų")
        else:
            self.na_values()

    # ------------------------------------------------------------------------------------------------------------

    def draw_plot(self):
        x = self.r_datos
        y = self.r_temper

        # Sukuriam figure ir asis
        fig, ax = plt.subplots()

        # Plot data
        ax.plot(x, y, label=f'{self.r_miestas}\n{self.r_datos[0]} - {self.r_datos[-1]}\nmetų temperatūros')
        ax.set_xlabel('Datos')
        ax.set_ylabel('°C')
        ax.set_title('Temperatūros')
        ax.legend()
        plt.show()


main_form = tk.Tk()

main_form.title("Pasaulio temperatūros")
main_form.geometry('800x320')

myapp = PasaulioTemper(main_form)
main_form.mainloop()
