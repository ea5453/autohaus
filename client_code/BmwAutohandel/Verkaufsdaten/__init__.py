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
    get_data_verkauf = anvil.server.call('select_Verkauf',self.drop_down_verkaufer.selected_value)
    self.repeating_panel_verkauf.items = get_data_verkauf

    # Any code you write here will run before the form opens.

  @handle("button_back_to_Verkauf", "click")
  def button_back_to_Verkauf_click(self, **event_args):
    open_form('BmwAutohandel.Verkauf')
    pass
