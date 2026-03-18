from ._anvil_designer import fahrzeugeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class fahrzeuge(fahrzeugeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Modellreihe-Tabelle füllen
    modellreihen = anvil.server.call("get_modellreihen_tabelle")
    self.repeating_panel_modell.items = modellreihen

    # Fahrzeug-Tabelle füllen
    fahrzeuge = anvil.server.call("get_fahrzeug_tabelle")
    self.repeating_panel_Fahrzeug.items = fahrzeuge
    # Any code you write here will run before the form opens.

  @handle("button_back_to_main", "click")
  def button_back_to_main_click(self, **event_args):
    open_form('BmwAutohandel')
    pass



