import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
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

@anvil.server.callable
def select_Mitarbeiter():
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Position FROM Mitarbeiter")
    result = cur.fetchall()
  return [row[0] for row in result]

@anvil.server.callable
def select_Kunde(query: str):
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM Kunde")
    rows = cur.execute(query).fetchall()
    # In Liste von Dictionaries umwandeln
    return [dict(row) for row in rows]

