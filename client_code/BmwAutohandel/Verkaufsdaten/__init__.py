from ._anvil_designer import VerkaufsdatenTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Verkaufsdaten(VerkaufsdatenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    verkaeufer = anvil.server.call("get_verkaeufer")
    self.drop_down_verkaufer.items = [(v["Name"], v["Mid"]) for v in verkaeufer]

  
   

  @handle("button_back_to_Verkauf", "click")
  def button_back_to_Verkauf_click(self, **event_args):
    open_form('BmwAutohandel.Verkauf')
    pass

  @handle("drop_down_verkaufer", "change")
  def drop_down_verkaufer_change(self, **event_args):
    selected_mid = self.drop_down_verkaufer.selected_value
    verkaufsliste = anvil.server.call("get_verkaeufe_for_mid", selected_mid)
    self.repeating_panel_verkauf.items = verkaufsliste

    
    get_sum_verkauf = anvil.server.call('get_verkaufssumme',self.drop_down_verkaufer.selected_value )
    self.label_summe.text = f"{get_sum_verkauf} €"
