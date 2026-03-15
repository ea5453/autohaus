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
def check_login(Kid,Mid,Vorname,Nachname):
  with sqlite3.connect(data_files["autohaus.db"]) as conn:
    cur = conn.cursor()
    
    cur.execute("""
    SELECT Mid,Vorname,Nachname FROM Mitarbeiter
    WHERE Mid = ? AND Vorname = ? AND Nachname = ?
    """,(Mid,Vorname,Nachname))
    Mitarbeiter = cur.fetchone()

    if Mitarbeiter:
      return Mitarbeiter[0],Mitarbeiter[1],Mitarbeiter[2]

      cur.execute("""
      SELECT Mid,Vorname,Nachname FROM Kunde
      WHERE Kid = ? AND Vorname = ? AND Nachname = ?
      """,(Kid,Vorname,Nachname))
      Kunde = cur.fetchone()

    elif Kunde:
      return Kunde[0],Kunde[1],Kunde[2]

    else:
      return None
    

    

