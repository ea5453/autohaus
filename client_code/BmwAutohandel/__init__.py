from ._anvil_designer import BmwAutohandelTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class BmwAutohandel(BmwAutohandelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    return_value = anvil.server.call('select_Mitarbeiter','SELECT DISTINCT Position FROM Mitarbeiter')
    return_value = [entry[0] for entry in return_value]
    self.drop_down_mitarbeiter.items = return_value

  def check_button_sign_in()

  @handle("text_box_id", "pressed_enter")
  def text_box_id_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  @handle("radio_button_Kunde", "clicked")
  def radio_button_Kunde_clicked(self, **event_args):
    self.drop_down_mitarbeiter.visible = False
    pass

  @handle("radio_button_Mitarbeiter", "clicked")
  def radio_button_Mitarbeiter_clicked(self, **event_args):
    self.drop_down_mitarbeiter.visible = True
    pass
