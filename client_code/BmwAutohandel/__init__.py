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

    self.drop_down_mitarbeiter.items = anvil.server.call('select_Mitarbeiter')
 
  # def check_button_sign_in()

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

  @handle("button_singn_in", "click")
  def button_singn_in_click(self, **event_args):

    get_check_log_in_Kunde = anvil.server.call('check_login_kunde',
                                               int(self.text_box_id.text),
                                               self.text_box_vorname.text,
                                               self.text_box_nachname.text
                                              )

    get_check_log_in_Mitarbeiter = anvil.server.call('check_login_mitarbeiter',
                                                int(self.text_box_id.text),
                                               self.text_box_vorname.text,
                                               self.text_box_nachname.text,
                                               self.drop_down_mitarbeiter.selected_value
                                              )
  
    if self.radio_button_Mitarbeiter.selected:
      if get_check_log_in_Mitarbeiter is None :
        alert("Login falsch")
        return
      if get_check_log_in_Mitarbeiter["position"] == 'Verkäufer':
        print(get_check_log_in_Mitarbeiter)
        open_form('BmwAutohandel.Verkauf')
      elif get_check_log_in_Mitarbeiter["position"] == 'Serviceberater':
        open_form('BmwAutohandel.Service')

    if self.radio_button_Kunde.selected:
      if get_check_log_in_Kunde is None :
        print(get_check_log_in_Kunde)
        alert("Login falsch1")
        return
      open_form('BmwAutohandel.fahrzeuge')
    pass


