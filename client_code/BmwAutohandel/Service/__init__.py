from ._anvil_designer import ServiceTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Service(ServiceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    daten = anvil.server.call("get_wartung_daten")
    self.drop_down_wartung.selected_value = daten
    self.drop_down_wartung.items = [(d, d) for d in daten]

    labels, values = anvil.server.call("get_reparatur_pie_data")

    fig = go.Figure(
      data=[go.Pie(labels=labels, values=values, hole=0)]
    )

    fig.update_layout(title_text="Reparaturen - Übersicht")

    # plot_1 = Plot-Komponente auf dem Form
    self.plot_service.figure = fig

  @handle("drop_down_wartung", "change")
  def drop_down_wartung_change(self, **event_args):

    get_date = self.drop_down_wartung.selected_value
    daten = anvil.server.call("get_wartung", get_date)
    self.repeating_panel_wartung.items = daten
    pass

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    open_form('BmwAutohandel')
    pass
