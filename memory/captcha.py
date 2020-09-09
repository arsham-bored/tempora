from .base_memory import BaseMemory
from datetime import datetime


class Captcha(BaseMemory):
    def __init__(self, internal_memory, attempts_memory: dict, time_memory: dict):
        super().__init__(internal_memory)
        self.attempts = attempts_memory
        self.time = time_memory

    def insert(self, userid):
        self.attempts[userid] += 1
        self.time[userid] = datetime.now()

    def record(self, event):
        userid = self.get_id(event)

        try:
            self.insert(userid)
        except:
            self.attempts[userid] = 0
            self.time[userid] = datetime.now()

    def raise_warn(self, event):
        userid = self.get_id(event)

        try:
            return self.attempts[userid] > 4

        except:
            return False

    def clear_by_time(self, event):
        userid = self.get_id(event)

        try:
            start_point = self.time[userid]
            now = datetime.now()

            difference = now - start_point

            if difference.total_seconds() > 60:
                print("dah")
                self.clear(event)

            print("nah")

        except:
            return

    def clear(self, event):
        userid = self.get_id(event)
        self.attempts[userid] = 0


memory = []
attempts = {}
time_memory = {}

bot_memory = Captcha(memory, attempts, time_memory)
