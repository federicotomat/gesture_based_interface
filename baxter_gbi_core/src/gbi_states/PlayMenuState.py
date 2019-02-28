# -*- coding: latin-1 -*-
## @package PlayMenuState
## This package describes the structure of the play menu state 

from FileMenuState import FileMenuState

#   PlayMenuState
#   inerithed form MenuState
class PlayMenuState(FileMenuState):
    #  constructor
    #  @param trigger_event istance of FsmEvent class
    def __init__(self, trigger_event):
        outcomes = ['back',
                    'remove']

        FileMenuState.__init__(self,
                               outcomes,
                               trigger_event,
                               'Playback menu',
                               fixed_options=['back', 'remove'])