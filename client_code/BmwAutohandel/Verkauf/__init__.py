from ._anvil_designer import VerkaufTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Verkauf(VerkaufTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    data_kunde = anvil.server.call('select_Kunde')
    self.repeating_panel_kunde.items = data_kunde
    # Any code you write here will run before the form opens.
    data_probe = anvil.server.call('select_Probefahrt')
    self.repeating_panel_Probefahrt.items = data_probe

  @handle("button_verkauf", "click")
  def button_verkauf_click(self, **event_args):
    open_form('BmwAutohandel.Verkaufsdaten')
    

  @handle("Button_back_to_main", "click")
  def Button_back_to_main_click(self, **event_args):
    open_form('BmwAutohandel')
    
