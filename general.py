import rpyc
from threading import Thread


class General(Thread):
    def __init__(self, id, type="secondary", majority="undefined", state="NF"):
        Thread.__init__(self)
        self.id = id
        self.type = type
        self.majority = majority
        self.state = state

    def verifyOrder(self):
        conn = rpyc.connect('localhost', 23456)
        return conn.root.verify_order(id)
