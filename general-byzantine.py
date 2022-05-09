import rpyc
import sys
from rpyc.utils.server import ThreadedServer
from threading import Thread
from general import General

supported_commands = ["actual-order attack", "actual-order retreat",
                      "g-state ID STATE(Faulty/Non-faulty)", "g-state", "g-kill ID", "g-add K"]
generals = {}
primary_gid = 0


class GB(rpyc.Service):
    def __init__(self, n):
        self.is_accessible = True
        self.initializeGenerals(n)

    def initializeGenerals(self, N):
        for id in range(N):
            createGeneral(id + 1)
        selectPrimary(1)

    def exposed_verify_order(self, id):
        ids = generals.keys()
        responses = []
        n_faulty = 0
        id = primary_gid + 1
        while primary_gid <= len(ids):
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
        print(
            f"Execute order: cannot be determined – not enough generals in the system! {len(failures)} faulty node in the system - {len(generals) - 1} out of {len(generals)} quorum not consistent")
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
            print(
                f"Execute order: {order}! Non-faulty nodes in the system – {count_verified_responses} out of {len(generals)} quorum suggest {order}")
        else:
            print(
                f"Execute order: {order}! {n_failure} faulty nodes in the system – {count_verified_responses - n_failure} out of {len(generals)} quorum suggest {order}")
    broadcastOrder("undefined")


def deleteGeneral(id):
    if id in generals:
        if generals[id].type != "primary":
            del generals[id]
        else:
            del generals[id]
            selectPrimary(id + 1)
    else:
        print("Please enter the correct general id.")
    for general in generals.values():
        print(f"G{general.id}, state={general.state}")


def addGenerals(K):
    last_gid = list(generals.keys())[-1]
    for n in range(K + 1):
        createGeneral(last_gid + n)
    for general in generals.values():
        print(f"G{general.id}, {general.type}")


def initializeGenerals(N):
    for id in range(1, N + 1):
        createGeneral(id)
    selectPrimary(1)


def changeState(id, state):
    if state == "faulty":
        generals[id].state = "F"
    elif state == "non-faulty":
        generals[id].state = "NF"
    else:
        print("State can only be Faulty or Non-faulty")
    for general in generals.values():
        print(f"G{general.id}, state = {general.state}")


def listGenerals():
    for general in generals.values():
        print(f"G{general.id}, {general.type}, state={general.state}")


def run_server(server):
    server.start()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("USAGE: general-byzantine.py <number_of_processes>")
        sys.exit()

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
        elif "g-state" in command[0]:
            try:
                id = int(command[1])
                state = command[2]
                changeState(id, state)
            except:
                listGenerals()
        elif "g-kill" in command[0]:
            try:
                id = int(command[1])
                deleteGeneral(id)
            except:
                print("Argument should be numeric. For example <g-kill 2>")
        elif "g-add" in command[0]:
            try:
                k = int(command[1])
                addGenerals(k)
            except:
                print("Argument should be numeric. For example <g-add 2>")
        elif "exit" in command:
            print("Program exited")
            sys.exit()
        else:
            print(f"Not supported command. Please use following commands {supported_commands}")
