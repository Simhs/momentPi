from lib.core import Machine

machine = Machine(480,320)
while True:
    machine.displayFlip()
    cmd = machine.getCommand()
    machine.changeState(cmd)
