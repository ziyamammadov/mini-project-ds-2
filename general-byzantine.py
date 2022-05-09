import rpyc
import sys
from rpyc.utils.server import ThreadedServer
from threading import Thread
from general import General

generals = {}
primary_gid = 0

class GB(rpyc.Service):
    def __init__(self, n):
        self.is_accessible = True
        self.initializeGenerals(n)

    def initializeGenerals(self, N):
        for id in range(N):
            createGeneral(id+1)
        selectPrimary(1)

    def exposed_verify_order(self, id):
        ids = generals.keys()
        responses = []
        n_faulty = 0
        id = primary_gid + 1
        while primary_gid + 1 <= len(ids) + 1:
            if id in generals:
                if generals[id].state == "F":
                    n_faulty += 1
                responses.append(generals[id].majority)
            else:
                break
            id += 1
        return responses, n_faulty


def createGeneral(id):
    general = General(id)
    general.daemon = True
    general.start()
    generals[id] = general


def selectPrimary(id):
    global primary_gid
    generals[id].type = "primary"
    primary_gid = id


def broadcastOrder(order):
    for general in generals.values():
        general.majority = order


def sendOrder(order):
    if len(generals) <= 3:
        failures = [g for g in generals.values() if g.state == "F"]
        generals[primary_gid].majority = order
        for g in generals.values():
            print(f"G{g.id}, {g.type}, majority={g.majority}, state={g.state}")
        print(f"Execute order: cannot be determined – not enough generals in the system! {len(failures)} faulty node in the system - {len(generals)-1} out of {len(generals)} quorum not consistent")
    else:
        generals[primary_gid].majority = order
        broadcastOrder(order)
        responses, n_failure = generals[primary_gid].verifyOrder()
        c_ans = 0
        for ans in responses:
            if ans == order:
                c_ans += 1
        count_verified_responses = c_ans
        for g in generals.values():
            print(f"G{g.id}, {g.type}, majority={g.majority}, state={g.state}")
        if n_failure == 0:
            print(f"Execute order: {order}! Non-faulty nodes in the system – {count_verified_responses} out of {len(generals)} quorum suggest {order}")
        else:
            print(f"Execute order: {order}! {n_failure} faulty nodes in the system – {count_verified_responses - n_failure} out of {len(generals)} quorum suggest {order}")
    broadcastOrder("undefined")


def initializeGenerals(N):
    for id in range(1, N + 1):
        createGeneral(id)
    selectPrimary(1)

def run_server(server):
    server.start()


if __name__ == "__main__":
    number_of_processes = int(sys.argv[1])
    if number_of_processes < 1:
        print("Number of generals should be greater than 0")
        sys.exit()

    ts = ThreadedServer(GB(number_of_processes), port=23456)
    server_thread = Thread(target=run_server, args=(ts,), daemon=True)
    server_thread.start()

    while True:
        inpt = input("Input the command: ")
        command = inpt.lower().split(" ")
        if "actual-order" in command[0]:
            if len(command) > 0:
                if command[1] == "attack" or command[1] == "retreat":
                    sendOrder(command[1])
                else:
                    print("USAGE: actual-order attack/retreat")
        elif "exit" in command:
            print("Program exited")
            sys.exit()