from Pd import *

# mains method
if __name__ == '__main__':

    # creates an instance of Pd
    pd = Pd()

    # initializes Pyata
    pd.init()

    # creates an object dac~ in 10, 10 on the patch
    dac = Object(10, 10, "dac~")

    # moves the dac to 300, 300
    dac.move(200, 200)

    # creates an object osc~ in 200, 100 on the patch
    osc = Object(200, 150, "osc~")

    # connects the outlet 0 from osc to the inlet 0 from dac
    connect(osc, 0, dac, 0)

    # edits the osc object from "osc~" to "osc~ 220"
    osc.edit("osc~ 220")

    sleep(2)

    # creates an number in 200, 10 on the patch
    n1 = Number(osc.x, osc.y - 50)

    # connects the outlet 0 from osc to the inlet 0 from dac
    connect(n1, 0, osc, 0)

    # sets the value from the number to 440
    n1.set(440)

    sleep(2)

    # increments n1 120 times
    for i in range(0, 220):
        n1.increment()
    sleep(2)

    # prints n1 value
    print(n1.get_value())

    # prints all objects available in memory
    print(pd.get_box_list())

    # prints all connections available in memory
    print(pd.get_connection_list())

    # sleep(2)

    # finishes Pyata
    pd.quit()
