import sqlalchemy.exc

from testaidb_modelis import *
import hashlib


def orm_gauti_atsakymus_pagal_klid(kl_id, sess=session):
    result = sess.query(Klausimas, Atsakymas).join(Atsakymas, Klausimas.id == Atsakymas.klausimas_id).filter(
        Klausimas.id == kl_id).all()
    atsak_l = []
    for kl, ats in result:
        atsak_l.append([ats.id, ats.vardas, ats.balas])
    return atsak_l


def orm_visi_klausimai_pagal_temos_id(tem_id):
    pass
    rez = session.query(Tema, Klausimas, Atsakymas) \
        .join(Klausimas, Tema.id == Klausimas.tema_id) \
        .join(Atsakymas, Klausimas.id == Atsakymas.klausimas_id).filter(Tema.id == tem_id)
    zodynas = {}
    kl_id_l = []
    ats_l = []
    for tem, kl, ats in rez:
        if kl.id not in kl_id_l:
            kl_id_l.append(kl.id)
            ats_l = []
            ats_l.append([ats.id, ats.vardas, ats.balas])
        else:
            ats_l.append([ats.id, ats.vardas, ats.balas])
        zodynas.update({f"{kl.id}||{kl.pavadinimas}": ats_l})
    return zodynas


def orm_sesiju_istorija_pagal_vart_id(vart_id):
    pass
    rez = session.query(Vartotojas, Sesija, VartotojoAtsakymas, Atsakymas, Klausimas, Tema) \
        .join(Sesija, Vartotojas.id == Sesija.vartotojas_id) \
        .join(VartotojoAtsakymas, Sesija.id == VartotojoAtsakymas.sesija_id) \
        .join(Atsakymas, VartotojoAtsakymas.atsakymas_id == Atsakymas.id) \
        .join(Klausimas, Atsakymas.klausimas_id == Klausimas.id) \
        .join(Tema, Klausimas.tema_id == Tema.id).filter(Vartotojas.id == vart_id).group_by(Sesija.id)
    visi_ses_atsak = []
    for vart, ses, vats, ats, kl, tem in rez:
        # 0-sesid, 1-temid, 2-tempav
        visi_ses_atsak.append([ses.id, tem.id, tem.pavadinimas])
    return visi_ses_atsak


def orm_visi_vartot_atsakym_pagal_ses_id(ses_id):
    pass
    rez = session.query(VartotojoAtsakymas).filter(VartotojoAtsakymas.sesija_id == ses_id).all()
    vatsakym_l = []
    for va in rez:
        vatsakym_l.append([va.sesija_id, va.atsakymas_id])
    return vatsakym_l


# def orm_atlikti_testai(vartotoj_sess, sess=session):
#     if vartotoj_sess.admin_teises:
#         result = sess.query(Vartotojas, Sesija, VartotojoAtsakymas, Atsakymas, Klausimas, Tema).outerjoin(Sesija,
#                                                                                                           Vartotojas.id == Sesija.vartotojas_id).join(
#             VartotojoAtsakymas, Sesija.id == VartotojoAtsakymas.sesija_id).join(Atsakymas,
#                                                                                 VartotojoAtsakymas.atsakymas_id == Atsakymas.id).join(
#             Klausimas, Atsakymas.klausimas_id == Klausimas.id).join(Tema, Klausimas.tema_id == Tema.id).all()
#     else:
#         result = sess.query(Vartotojas, Sesija, VartotojoAtsakymas, Atsakymas, Klausimas, Tema).outerjoin(Sesija,
#                                                                                                           Vartotojas.id == Sesija.vartotojas_id).join(
#             VartotojoAtsakymas, Sesija.id == VartotojoAtsakymas.sesija_id).join(Atsakymas,
#                                                                                 VartotojoAtsakymas.atsakymas_id == Atsakymas.id).join(
#             Klausimas, Atsakymas.klausimas_id == Klausimas.id).join(Tema, Klausimas.tema_id == Tema.id).filter(
#             Vartotojas.id == vartotoj_sess.id).all()
#     return result


def orm_vartotoj_atsakym(testo_ses, atsakymas_o, sess=session):
    vart_ats_o = VartotojoAtsakymas()
    vart_ats_o.sesija = testo_ses
    vart_ats_o.atsakymas = atsakymas_o
    session.add(vart_ats_o)
    sess.commit()


def orm_gauti_atsakyma(ats_id, sess=session):
    atsakymas_o = sess.query(Atsakymas).get(ats_id)
    return atsakymas_o


def orm_pateikti_rezultata(testo_sesij, pateikta, balai, laikas, sess=session):
    rezultat_o = Rezultatas(pateikta=pateikta, balai=balai, laikas=laikas)
    rezultat_o.sesija = testo_sesij
    sess.add(rezultat_o)
    sess.commit()


def orm_trinti_atsakyma(ats_id, sess=session):
    atsakymas_o = sess.query(Atsakymas).get(ats_id)
    sess.delete(atsakymas_o)
    sess.commit()


def orm_trinti_klausima(kl_id, sess=session):
    klausymas_o = sess.query(Klausimas).get(kl_id)
    sess.delete(klausymas_o)
    sess.commit()


def orm_redaguoti_atsakyma(ats_id, nauj_vardas, baslas, sess=session):
    atsakymas_o = sess.query(Atsakymas).get(ats_id)
    atsakymas_o.vardas = nauj_vardas
    atsakymas_o.balas = baslas
    sess.commit()


def orm_redaguoti_klausima(kl_id, nauj_pavadinimas, sess=session):
    klausymas_o = sess.query(Klausimas).get(kl_id)
    klausymas_o.pavadinimas = nauj_pavadinimas
    sess.commit()


def orm_trinti_tema(tema_str, sess=session):
    temax_o = sess.query(Tema).filter(Tema.pavadinimas == tema_str).first()
    if temax_o is not None:
        sess.delete(temax_o)
        sess.commit()


def orm_pervadinti_tema(tema_esam, tema_nauj, sess=session):
    temax_o = sess.query(Tema).filter(Tema.pavadinimas == tema_esam).first()
    if temax_o is not None:
        temax_o.pavadinimas = tema_nauj
        sess.commit()


def nuskaityti_importa(failas=""):
    tema_simb = "##"
    klausimas_simb = "@@"
    atsakymas_simb = "[]"
    ln = 1
    klausimas = None
    tema_df = None
    tema = None
    a_l = []

    with open(failas, 'r', encoding="utf-8") as file:
        for line in file:
            data_l = line.strip().split("|")
            # tema
            if ln == 1:
                tema_df = {tema: {}}
                if data_l[0] == tema_simb:
                    tema = data_l[1]
                    continue
            # Klausimas
            if data_l[0] == klausimas_simb:
                klausimas = data_l[1]
                a_l = []
            # atsakymai
            else:
                if data_l[0] == atsakymas_simb:
                    a_l.append([data_l[1], data_l[2]])
            tema_df[tema].update({klausimas: a_l})
            ln += 1
    return tema_df


def import_test_to_sql(test_df, sess=session):
    tema = list(test_df.keys())[0]
    klausimai_l = list(test_df.get(tema).keys())
    # Sukuriam tema, klausimus ir atsakymus
    tema_o = Tema(pavadinimas=tema)
    for kl in klausimai_l:
        kl_o = Klausimas(pavadinimas=kl)
        ats_l = test_df.get(tema).get(kl)
        for a in ats_l:
            ats_o = Atsakymas(vardas=a[0], balas=a[1])
            kl_o.atsakymai.append(ats_o)
        tema_o.klausimai.append(kl_o)
    sess.add(tema_o)
    sess.commit()


def nuskaityti_temas(sess=session):
    sql_temos = sess.query(Tema).all()
    temos_l = []
    for t in sql_temos:
        temos_l.append(t.pavadinimas)
    return temos_l


def nuskaityti_klausimus(tema="", sess=session):
    klausimai = {tema: {}}
    sql_klausimai = (sess.query(Tema, Klausimas, Atsakymas).join(Klausimas, Tema.id == Klausimas.tema_id).
                     join(Atsakymas, Klausimas.id == Atsakymas.klausimas_id).filter(
        Tema.pavadinimas == tema).all())
    k_l = []
    a_l = []
    for t, k, a in sql_klausimai:
        if k.pavadinimas not in k_l:
            a_l = []
            k_l.append(k.pavadinimas)
            a_l.append([a.id, a.vardas, a.balas, 0])
        else:
            a_l.append([a.id, a.vardas, a.balas, 0])
        klausimai[tema].update({str(k.id) + "||" + k.pavadinimas: a_l})
    return klausimai


def nauja_prisijung_sesija(vardas, slaptazodis, sess=session) -> tuple:
    vartotojai = sess.query(Vartotojas).all()
    for vard in vartotojai:
        if vard.vardas == vardas:
            sys_vart = sess.query(Vartotojas).filter(Vartotojas.vardas == vardas).first()
            if sys_vart.slaptazodis == slapt_hash(slaptazodis):
                return True, sys_vart
    return False, None


def nauja_testo_sesija(vart_sesij, sess=session):
    sesijax_o = Sesija()
    sesijax_o.vartotojas = vart_sesij
    sess.add(sesijax_o)
    sess.commit()
    return sesijax_o


def naujas_vartotojas(vardas, slaptazodis, admin_teises=False, sess=session):
    vartot_o = Vartotojas(vardas=vardas, slaptazodis=slapt_hash(slaptazodis), admin_teises=admin_teises)
    statistika_o = VartotojoStatistika()
    vartot_o.statistika = statistika_o
    try:
        sess.add(vartot_o)
        sess.commit()
    except sqlalchemy.exc.IntegrityError:
        sess.rollback()
        return False
    return True


def slapt_hash(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    h_slpataz = sha256.hexdigest()
    return h_slpataz


def admin_vartotojas(sess=session):
    visi_vart = sess.query(Vartotojas).all()
    if len(visi_vart) == 0:
        naujas_vartotojas("admin", "admin", True)
        sess.flush()


if __name__ == '__main__':
    pass
    orm_visi_klausimai_pagal_temos_id(1)
