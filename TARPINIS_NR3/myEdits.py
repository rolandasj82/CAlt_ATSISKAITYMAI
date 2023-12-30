import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from testaidb_controller import *
from myWidgets import MButton01, MEntry02, MLable05


class TemuRedagavimas:
    def __init__(self):
        self.e_tekstas01 = None
        self.text_VarStr = None
        self.balas_VarStr = None
        self.e_balas01 = None
        self.btn_trinti = None
        self.btn_redaguot = None
        self.treev = None
        self.tema = None
        self.master = tk.Toplevel()
        self.master.title("Temų redaktorius")
        self.master.geometry("1090x580")

        self.fr_klausim = None
        # self.master.option_add("*Font", ("Courier New", 12))

        self.fr_temos = tk.Frame(self.master)
        self.fr_temos.pack()

        self.lbox_temos = tk.Listbox(self.fr_temos, justify=tk.LEFT, width=90, height=20, font=("Courier New", 12))
        self.btn_delete = tk.Button(self.fr_temos, text="Trinti",
                                    width=15, command=self.trinti_tema, font=("Courier New", 13, "bold"))
        self.btn_rename = tk.Button(self.fr_temos, text="Pervadinti",
                                    width=15, command=self.pervardinti, font=("Courier New", 13, "bold"))
        self.btn_klausimai = tk.Button(self.fr_temos, text="Klausimai", width=15,
                                       command=self.klausimu_redag, font=("Courier New", 13, "bold"))
        self.lbox_temos.pack()
        self.btn_delete.pack(side=tk.RIGHT, pady=10, padx=10)
        self.btn_rename.pack(side=tk.LEFT, pady=10, padx=10)
        self.btn_klausimai.pack(side=tk.LEFT, pady=10, padx=10)
        temos_l = nuskaityti_temas()
        for tem in temos_l:
            self.lbox_temos.insert(tk.END, tem)
        self.master.mainloop()

    def trinti_tema(self):
        try:
            tema_str = self.lbox_temos.selection_get()
            orm_trinti_tema(tema_str=tema_str)
            messagebox.showinfo("Trinimas", "Tema ištrinta!")
            self.lbox_temos.delete(0, tk.END)
            self.atnaujinti_listBox()
        except tk.TclError:
            pass

    def trinti_klausima_atsakyma(self):
        ind = self.treev.selection()[0]
        parent_id = self.treev.parent(ind)
        datax = self.treev.item(ind).get("values")
        if parent_id != "":
            # ------- ORM
            orm_trinti_atsakyma(ats_id=datax[0])
            self.atnaujint_treeview()
        else:
            # ------- ORM
            orm_trinti_klausima(kl_id=datax[0])
            self.atnaujint_treeview()

    def pervardinti(self):
        esam_pavad = self.lbox_temos.selection_get()
        nauj_pavad = simpledialog.askstring("TEMA", "Naujas pavadin.:", initialvalue=esam_pavad)
        orm_pervadinti_tema(esam_pavad, nauj_pavad)
        self.atnaujinti_listBox()

    def atnaujinti_listBox(self):
        self.lbox_temos.delete(0, tk.END)
        temos_l = nuskaityti_temas()
        for tem in temos_l:
            self.lbox_temos.insert(tk.END, tem)

    def klausimu_redag(self):
        self.tema = self.lbox_temos.selection_get()
        self.fr_temos.destroy()
        self.fr_klausim = tk.Frame(self.master)
        self.fr_klausim.grid(row=0, column=0)

        ttk.Style().configure("mtreev.Treeview", highlightthickness=0, bd=0, font=("Courier new", 12))
        ttk.Style().configure("mtreev.Treeview.Heading", font=('Calibri', 14, 'bold'))
        self.treev = ttk.Treeview(self.fr_klausim, columns=["id", "klausimx", "balas"],
                                  style="mtreev.Treeview", height=20)
        vert_sb = ttk.Scrollbar(self.fr_klausim, orient="vertical", command=self.treev.yview)

        self.treev.configure(yscrollcommand=vert_sb.set)
        self.treev.heading('#0', text='')
        self.treev.heading('id', text='ID')
        self.treev.heading('klausimx', text='Klausimai')
        self.treev.heading('balas', text='Balai')
        self.treev.column('#0', width=20, minwidth=20, anchor=tk.W)
        self.treev.column('id', width=60, minwidth=60, anchor=tk.N)
        self.treev.column('klausimx', width=900, minwidth=900, anchor=tk.W)
        self.treev.column('balas', width=90, minwidth=90, anchor=tk.W)
        vert_sb.grid(row=0, column=3, sticky=tk.NS + tk.E)
        self.treev.grid(row=0, column=0, sticky=tk.NSEW, columnspan=4)
        self.treev.bind('<<TreeviewSelect>>', lambda e: self.pazymeta_eilut())
        self.atnaujint_treeview()

        l_tekstas01 = MLable05(self.fr_klausim, text="Klausimai/atsakymai:")
        l_tekstas01.grid(row=1, column=0, padx=10, sticky=tk.W)

        self.text_VarStr = tk.StringVar()
        self.e_tekstas01 = MEntry02(self.fr_klausim, textvariable=self.text_VarStr)
        self.e_tekstas01.grid(row=2, column=0, sticky=tk.W, padx=10, pady=2, columnspan=4)
        self.e_tekstas01['state'] = "disabled"

        l_balai01 = MLable05(self.fr_klausim, text="Balai:")
        l_balai01.grid(row=3, column=0, padx=10, sticky=tk.W)

        self.balas_VarStr = tk.StringVar()
        self.e_balas01 = MEntry02(self.fr_klausim, textvariable=self.balas_VarStr, width=15)
        self.e_balas01.grid(row=4, column=0, sticky=tk.W, padx=10, pady=2, columnspan=2)
        self.e_balas01['state'] = "disabled"

        # Mygtukai
        self.btn_redaguot = MButton01(self.fr_klausim, text="Redaguoti", command=self.redaguoti_irasa)
        self.btn_redaguot.grid(row=5, column=0, sticky=tk.E, padx=10, )

        btn_saugot = MButton01(self.fr_klausim, text="Išsaugoti", command=self.isaugoti_irasa)
        btn_saugot.grid(row=5, column=1, sticky=tk.W, padx=10, )

        self.btn_trinti = MButton01(self.fr_klausim, text="Trinti", command=self.trinti_klausima_atsakyma)
        self.btn_trinti.grid(row=5, column=3, sticky=tk.W, padx=10, )

    def pazymeta_eilut(self):
        try:
            ind = self.treev.selection()[0]
        except IndexError:
            return
        datax = self.treev.item(ind).get("values")
        if len(datax) > 2:
            self.text_VarStr.set(datax[1])
            self.balas_VarStr.set(datax[2])
        else:
            self.text_VarStr.set(datax[1])
            self.balas_VarStr.set("")

    def redaguoti_irasa(self):
        ttk.Style().configure("treev_edit.Treeview", background="gray", font=("Courier new", 12))
        self.e_tekstas01["state"] = "normal"
        self.e_balas01["state"] = "normal"
        self.treev["selectmode"] = "none"
        self.treev["style"] = "treev_edit.Treeview"
        self.btn_redaguot["state"] = "disabled"
        self.btn_trinti["state"] = "disabled"
        # selectmode = 'browse'
        # selectmode = 'none'

    def isaugoti_irasa(self):
        ind = self.treev.selection()[0]
        parent_id = self.treev.parent(ind)
        datax = self.treev.item(ind).get("values")
        if parent_id != "":
            redag_tekst = self.e_tekstas01.get().strip()
            redag_balas = float(self.e_balas01.get().strip())
            # ------- ORM
            orm_redaguoti_atsakyma(ats_id=datax[0], nauj_vardas=redag_tekst, baslas=redag_balas)
            self.atnaujint_treeview()
        else:
            redag_tekst = self.e_tekstas01.get().strip()
            # ------- ORM
            orm_redaguoti_klausima(kl_id=datax[0], nauj_pavadinimas=redag_tekst)
            self.atnaujint_treeview()

        self.e_tekstas01["state"] = "disabled"
        self.e_balas01["state"] = "disabled"
        self.treev["selectmode"] = "browse"
        self.treev["style"] = "mtreev.Treeview"
        self.btn_redaguot["state"] = "normal"
        self.btn_trinti["state"] = "normal"

    def atnaujint_treeview(self):
        self.treev.delete(*self.treev.get_children())
        # duomenu ikelimas
        tema_df = nuskaityti_klausimus(tema=self.tema)
        klausimai = tema_df.get(self.tema).keys()
        for klx in list(klausimai):
            klx_l = klx.split("||")
            klx_o = self.treev.insert("", tk.END, values=klx_l)
            ats_l = tema_df.get(self.tema).get(klx)
            for a in ats_l:
                self.treev.insert(klx_o, tk.END, values=(a[0], a[1], a[2]))


if __name__ == '__main__':
    pass
