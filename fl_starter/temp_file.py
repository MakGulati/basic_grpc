from time import sleep

from pyrsistent import s
from chain_code import *

# eventUpdate("7", "2", "f_sun", register_member())
if __name__ == "__main__":
    for i in range(3):

        uploadLocalModelExperimentRelated(
            f"fmoon__11_{2*i+5}_{i}", "7", i, register_member(), "f_sun"
        )
        sleep(1)
