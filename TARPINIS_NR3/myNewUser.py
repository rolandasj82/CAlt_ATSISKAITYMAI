import tkinter as tk
from tkinter import messagebox, BooleanVar
from testaidb_controller import naujas_vartotojas


class NaujasVartotojas:

    def __init__(self):
        self.master2 = tk.Tk()
        self.master2.title("Naujas vartotojas")
        self.master2.geometry("330x130")
        self.l_vartotojas = tk.Label(self.master2, text="Vartotojas:", font=("Courier New", 11, "bold"))
        self.l_slaptazodis = tk.Label(self.master2, text="Slpatažodis:", font=("Courier New", 11, "bold"))
        self.e_vartotojas = tk.Entry(self.master2, font=("Courier New", 11, "bold"))
        self.e_slaptazodis = tk.Entry(self.master2, show="*", font=("Courier New", 11, "bold"))
        self.admin_teis = BooleanVar()
        self.cbtn_admin = tk.Checkbutton(self.master2, variable=self.admin_teis, text="admin. teisės",
                                         font=("Courier New", 10, "bold"))
        self.btn_kurti = tk.Button(self.master2, text="Kurti", command=self.kurti, width=20,
                                   font=("Courier New", 11, "bold"))

        self.l_vartotojas.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.l_slaptazodis.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.e_vartotojas.grid(row=0, column=1, padx=0, pady=5)
        self.e_slaptazodis.grid(row=1, column=1, padx=0, pady=5)
        self.cbtn_admin.grid(row=2, column=1, columnspan=1, pady=1)
        self.btn_kurti.grid(row=3, column=1, columnspan=1, pady=1)
        self.master2.mainloop()

    def kurti(self):
        # Get values from entry widgets
        vartot = self.e_vartotojas.get()
        slpatazod = self.e_slaptazodis.get()
        teises = self.admin_teis.get()

        # butinas slaptazodis ir vartotojas
        if not vartot or not slpatazod:
            messagebox.showerror("Klaida", "Būtina įvesti vartotoją ir slaptažodį!")
            return
        stat = naujas_vartotojas(vardas=vartot, slaptazodis=slpatazod, admin_teises=teises)
        if not stat:
            messagebox.showerror("Klaida", "Toks vartotojas jau yra...!")
            return
        msg = f"Naujas vartotojas sukurtas: \nVartotojas: {vartot}\nSlaptažodis: {slpatazod}\nAdmin: {teises}"
        messagebox.showinfo("Sėkmingai", msg)

        self.e_vartotojas.delete(0, tk.END)
        self.e_slaptazodis.delete(0, tk.END)
        self.master2.destroy()


if __name__ == '__main__':
    pass

