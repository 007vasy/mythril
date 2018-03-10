from mythril.analysis.report import Issue
from mythril.exceptions import UnsatError
from mythril.analysis import solver
from z3 import simplify
import logging


'''
MODULE DESCRIPTION:

Check for constraints on tx.origin (i.e., access to some functionality is restricted to a specific origin).
'''


def execute(statespace):

    logging.debug("Executing module: ASSERT_VIOLATION")

    issues = []

    for k in statespace.nodes:
        node = statespace.nodes[k]

        for state in node.states:

            instruction = state.get_current_instruction()

            if(instruction['opcode'] == "ASSERT_FAIL"):

                logging.debug("Opcode 0xfe detected.")

                try:
                    model = solver.get_model(node.constraints)
                    logging.debug("[ASSERT_VIOLATION ASSERT] MODEL: " + str(model))

                    address = state.get_current_instruction()['address']

                    description = "Invalid opcode reached (0xfe). This can be caused by a type error, out-of-bounds array access, or assert violation.\n\n"

                    description += "The following input and state variables trigger the invalid instruction:\n\n"

                    for d in model.decls():

                        try:
                            condition = hex(model[d].as_long())
                        except:
                            condition = str(simplify(model[d]))

                        description += ("%s: %s\n" % (d.name(), condition))

                    description += "\nNote that assert() should only be used to check invariants. Use require() for regular input checking.\n"

                    issues.append(Issue(node.contract_name, node.function_name, address, "Assertion violation", description))

                except UnsatError:
                    logging.debug("[FAILED ASSERT] no model found")

    return issues
