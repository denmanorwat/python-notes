from Instruction_hierarchy import SingleNoteInstruction, FilterNoteInstruction


class Executer:

    def __init__(self, database):
        self.database = database

    def execute(self, instruction):
        print("Received instruction: {}".format(instruction.instruction))
        answer = None
        log = None

        if isinstance(instruction, SingleNoteInstruction):
            if instruction.instruction == "CREATE":
                log = self.database.create_entry(instruction.text,
                                                    instruction.tags, instruction.datetime)
            if instruction.instruction == "DELETE":
                log = self.database.delete_entry(instruction.id)
            if instruction.instruction == "EDIT":
                log = self.database.edit_entry(instruction.id, instruction.text,
                                                  instruction.tags, instruction.datetime)
            print(log)
            answer = self.database.get_entries()

        if isinstance(instruction, FilterNoteInstruction):
            if instruction.instruction == "GET":
                filter_tags, datetime_interval = instruction.tags, instruction.datetime_interval
                answer = self.database.get_entries(filter_tags, datetime_interval)
            print(answer)

        return answer
