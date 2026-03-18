import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

@anvil.server.callable
def check_login_mitarbeiter(mid, vorname, nachname, position):
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    
    cur.execute("""
            SELECT Mid, Vorname, Nachname, Position
            FROM Mitarbeiter
            WHERE Mid = ? AND Vorname = ? AND Nachname = ? AND Position = ?
        """, (mid, vorname, nachname, position))

    mitarbeiter = cur.fetchone()

    if mitarbeiter:
      return {"rolle": "Mitarbeiter",
              "id": mitarbeiter[0],
              "vorname": mitarbeiter[1],
              "nachname": mitarbeiter[2],
              "position": mitarbeiter[3]}
  return None

@anvil.server.callable
def check_login_kunde(kid, vorname, nachname):
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    cur.execute("""
            SELECT Kid, Vorname, Nachname
            FROM Kunde
            WHERE Kid = ? AND Vorname = ? AND Nachname = ? 
        """, (kid, vorname, nachname))

    kunde = cur.fetchone()

    if kunde:
      return {"rolle": "Kunde",
              "id": kunde[0],
              "vorname": kunde[1],
              "nachname": kunde[2]}
  return None

@anvil.server.callable
def select_Mitarbeiter():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Position FROM Mitarbeiter")
    result = cur.fetchall()
  return [row[0] for row in result]

@anvil.server.callable
def select_Kunde():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Kunde")
    rows = cur.fetchall()
    return [dict(row) for row in rows]



@anvil.server.callable
def select_Probefahrt():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  cur.execute("""
    SELECT 
          p.Datum,
          p.WIN,
          p.Kid,
          k.Vorname,
          k.Nachname,
          m.Modellname
      FROM Probefahrt p
      LEFT JOIN Kunde k
          ON p.Kid = k.Kid
      LEFT JOIN Fahrzeug f
          ON p.WIN = f.WIN
      LEFT JOIN Modellreihe m
          ON f.ModellId = m.ModellId;
  """)
  rows_p = cur.fetchall()
  return [dict(row) for row in rows_p]

@anvil.server.callable
def get_verkaeufer():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
            SELECT Mid, Vorname || ' ' || Nachname AS Name
            FROM Mitarbeiter
            WHERE Position = 'Verkäufer'
        """)
    rows = cur.fetchall()
    return [dict(row) for row in rows]

@anvil.server.callable
def get_verkaeufe_for_mid(Mid):
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
            SELECT f.WIN, f.Preis, v.Datum
            FROM Verkauf v
            JOIN Fahrzeug f ON v.WIN = f.WIN
            WHERE v.Mid = ?
            ORDER BY v.Datum
        """, (Mid,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]


@anvil.server.callable
def get_verkaufssumme(Mid):
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    cur.execute("""
            SELECT SUM(f.Preis) 
            FROM Verkauf v
            JOIN Fahrzeug f ON v.WIN = f.WIN
            WHERE v.Mid = ?;
        """, (Mid,))
    result = cur.fetchone()[0]
    # Falls der Verkäufer noch keine Verkäufe hat, Summe = 0
    return result if result is not None else 0



@anvil.server.callable
def get_alle_verkaufssummen():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    cur.execute("""
            SELECT m.Vorname || ' ' || m.Nachname, SUM(f.Preis)
            FROM Verkauf v
            JOIN Mitarbeiter m ON v.Mid = m.Mid
            JOIN Fahrzeug f ON v.WIN = f.WIN
            WHERE m.Position='Verkäufer'
            GROUP BY m.Mid
        """)
    rows = cur.fetchall()

    namen = [row[0] for row in rows]
    summen = [row[1] for row in rows]

    return namen, summen

@anvil.server.callable
def get_wartung_daten():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Datum FROM Wartung")
    return [row[0] for row in cur.fetchall()]

@anvil.server.callable
def get_wartung(datum):
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
            SELECT *
            FROM Wartung
            WHERE Datum = ?
        """, (datum,))
    rows = cur.fetchall()
    return [dict(row) for row in rows]

@anvil.server.callable
def get_reparatur_pie_data():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    # Zähle, wie oft jede Reparatur vorkommt
    cur.execute("""
            SELECT Reparatur, COUNT(*) as Anzahl
            FROM Wartung
            WHERE Reparatur IS NOT NULL AND Reparatur != ''
            GROUP BY Reparatur
        """)
    rows = cur.fetchall()
    # Listen für Labels und Werte zurückgeben
    labels = [row[0] for row in rows]
    values = [row[1] for row in rows]
    return labels, values

@anvil.server.callable
def get_modellreihen_tabelle():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Modellreihe")
    rows = cur.fetchall()
    return [dict(row) for row in rows]

@anvil.server.callable
def get_fahrzeug_tabelle():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Fahrzeug")
    rows = cur.fetchall()
    return [dict(row) for row in rows]

