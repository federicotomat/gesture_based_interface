## @package MacroMenuState
## This package describes the general structure of the macro menu state

from MenuState import MenuState

##  MacroMenuState
#   inerithed form BlockingState
class MacroMenuState(MenuState):
    ## constructor
    #  @param trigger_event istance of FsmEvent class
    def __init__(self, trigger_event):
        outcomes = ['play',
                    'back']
        MenuState.__init__(self,
                           outcomes,
                           trigger_event,
                           'Macro menu',
                           input_keys=['macro_idx', 'macro_filename'])
        self.macro_slots = [None, None, None, None, None]

    ## method update_variable_options
    #  @param userdata 
    #  
    #  override of MenuState.update_variable_options
    #  updates the variable options of the menu
    def update_variable_options(self, userdata):
        if userdata.macro_idx:  # TODO: check if it works
            if userdata.macro_filename:
                self.macro_slots[userdata.macro_idx] = userdata.macro_filename
        return self.macro_slots


    ## method on_variable_selection
    #  @param userdata 
    #  @param index
    #  @param item 
    #
    #  override of MenuState.update_variable_options
    #  updates the variable options of the menu
    def on_variable_selection(self, index, item, userdata):
        userdata.selection = index
        return 'selection'


    # FIXME: 'play' outcome does not outputs macro configuration