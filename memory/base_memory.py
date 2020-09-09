import logging


class BaseMemory:
    def __init__(self, memory):
        self.memory = memory

    ID_not_in_memory = ValueError

    @staticmethod
    def get_id(event):
        return event.from_id

    def add(self, event):
        userid = self.get_id(event)

        already_in_memory = self.check(event)

        if already_in_memory:
            return

        self.memory.append(userid)

    def remove(self, event):
        try:
            userid = self.get_id(event)
            self.memory.remove(userid)

        except self.ID_not_in_memory:
            return

    def check(self, event):
        userid = self.get_id(event)
        return userid in self.memory
