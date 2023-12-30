from tkinter import ttk
import tkinter as tk


class MButton01(ttk.Button):
    """ Meniu mygtukai"""

    def __init__(self, parent, text="", width=None, **kwargs):
        stylex = ttk.Style()
        stylex.configure('meniu.TButton', font=('Courier New', 16, "bold"))
        mykwargs = {"style": "meniu.TButton", "text": text, "width": width}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MButton02(ttk.Button):
    """ Meniu nustatymų mygtukas"""

    def __init__(self, parent, **kwargs):
        stylex = ttk.Style()
        stylex.configure('settings.TButton', font=('Courier New', 10))
        mykwargs = {"style": "settings.TButton"}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MButton03(ttk.Button):
    """ Login mygtukas """

    def __init__(self, parent, **kwargs):
        stylex = ttk.Style()
        stylex.configure('myButton03.TButton', font=('Helvetica', 14, "bold"))
        mykwargs = {"style": "myButton03.TButton"}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MLable01(ttk.Label):
    """ Klausimai """

    def __init__(self, parent, text="", **kwargs):
        style001 = ttk.Style()
        style001.configure("myLable01.TLabel", font=("Courier New", 14, "bold"))

        mykwargs = {"text": text,
                    "style": "myLable01.TLabel"}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MLable02(ttk.Label):
    """ Klausimo verte """

    def __init__(self, parent, text="", **kwargs):
        ttk.Style().configure("myLable02.TLabel", font=("Courier New", 12, "normal"), foreground="green")

        mykwargs = {"text": text,
                    "style": "myLable02.TLabel"}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MLable03(ttk.Label):
    """ Rezultatas taskų"""

    def __init__(self, parent, taskai, text="", **kwargs):
        if taskai >= 50:
            ttk.Style().configure("myLable03.TLabel", font=("Courier New", 16, "bold"), foreground="green")
        else:
            ttk.Style().configure("myLable03.TLabel", font=("Courier New", 16, "bold"), foreground="red")

        mykwargs = {"text": text,
                    "style": "myLable03.TLabel"}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MLable04(ttk.Label):
    """ Laiko informacija"""

    def __init__(self, parent, text="", textvariable=None, **kwargs):
        ttk.Style().configure("myLable04.TLabel", font=("Courier New", 14, "bold"), foreground="black")

        mykwargs = {"text": text,
                    "style": "myLable04.TLabel",
                    "textvariable": textvariable}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MLable05(ttk.Label):
    """ Redagavimo langas """

    def __init__(self, parent, text="", **kwargs):
        style001 = ttk.Style()
        style001.configure("myLable05.TLabel", font=("Courier new", 14, "bold"))

        mykwargs = {"text": text,
                    "style": "myLable05.TLabel"}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MCheckbutton01(ttk.Checkbutton):
    """ Atsakymai """

    def __init__(self, parent, **kwargs):
        style001 = ttk.Style()
        style001.configure("customx.TCheckbutton", font=("Courier New", 12, "normal"))

        mykwargs = {"onvalue": True, "offvalue": False,
                    "style": "customx.TCheckbutton"}
        mykwargs.update(kwargs)

        super().__init__(parent, **mykwargs)


class MLableInfoBar(tk.Label):
    def __init__(self, parent, text="", textvariable=None, **kwargs):
        mykwargs = {"text": text,
                    "font": ("Courier New", 12, "bold"),
                    "relief": tk.SUNKEN, "bd": 1, "height": 1,
                    "textvariable": textvariable}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MEntry01(ttk.Entry):
    """ Login ivestis"""

    def __init__(self, parent, **kwargs):
        ttk.Style().configure("myEntry01.TEntry")
        mykwargs = {"style": "myEntry01.TEntry",
                    "font": ("Courier New", 14, "normal")}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)


class MEntry02(ttk.Entry):
    """ Testu redagavimas """

    def __init__(self, parent, width=100, **kwargs):
        ttk.Style().configure("myEntry02.TEntry")
        mykwargs = {"style": "myEntry02.TEntry",
                    "font": ("Courier New", 12, "normal"),
                    "width": width}
        mykwargs.update(kwargs)
        super().__init__(parent, **mykwargs)
