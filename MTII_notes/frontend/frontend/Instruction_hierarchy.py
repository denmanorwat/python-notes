class Instruction:
    def __init__(self, instruction):
        self.instruction = instruction


class SingleNoteInstruction(Instruction):
    def __init__(self, instruction, id=None, text=None, tags=None, datetime=None):
        super().__init__(instruction)
        self.id = id
        self.text = text
        self.tags = tags
        self.datetime = datetime


class FilterNoteInstruction(Instruction):
    def __init__(self, instruction, tags=None, datetime_interval=None):
        super().__init__(instruction)
        self.tags = tags
        self.datetime_interval = datetime_interval
