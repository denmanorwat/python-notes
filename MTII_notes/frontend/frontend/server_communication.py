import socket
import pickle
from Instruction_hierarchy import FilterNoteInstruction
from forms.entry_manager import get_tags_and_dates


class RemoteDB:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_instruction(self, instruction):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            binary_instruction = pickle.dumps(instruction)
            s.sendall(binary_instruction)
            answer = pickle.loads(s.recv(1024))
        s.close()
        return answer

    def get_all_items(self):
        tags, date_interval = get_tags_and_dates()
        instruction = FilterNoteInstruction("GET", tags, date_interval)
        answer = self.send_instruction(instruction)
        return answer
