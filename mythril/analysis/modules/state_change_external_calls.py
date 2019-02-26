from mythril.analysis.ops import Variable, VarType
from mythril.analysis.swc_data import REENTRANCY
from mythril.analysis.modules.base import DetectionModule
from mythril.analysis.report import Issue
from mythril.analysis.call_helpers import get_call_from_state
from mythril.analysis.analysis_module_helpers import CallIssue, ExternalCallsAnnotation
from mythril.laser.smt import symbol_factory, simplify
from mythril.laser.ethereum.state.global_state import GlobalState
from typing import List, cast
import logging

log = logging.getLogger(__name__)

DESCRIPTION = """

Check whether there is a state change of the contract after the execution of an external call
"""


class StateChange(DetectionModule):
    """This module searches for state change after low level calls (e.g. call.value()) that
    forward gas to the callee."""

    def __init__(self):
        """"""
        super().__init__(
            name="External calls",
            swc_id=REENTRANCY,
            description=DESCRIPTION,
            entrypoint="callback",
            pre_hooks=[
                "CALL",
                "SSTORE",
                "DELEGATECALL",
                "STATICCALL",
                "CREATE",
                "CALLCODE",
            ],
        )

    def execute(self, state: GlobalState):
        """

        :param state:
        :return:
        """
        self._issues.extend(self._analyze_state(state))
        return self.issues

    @staticmethod
    def _analyze_state(state) -> List[Issue]:
        """

        :param state:
        :return:
        """
        address = state.get_current_instruction()["address"]
        annotations = cast(
            List[ExternalCallsAnnotation],
            list(state.get_annotations(ExternalCallsAnnotation)),
        )
        if len(annotations) == 0:
            log.debug("Creating annotation for state")
            state.annotate(ExternalCallsAnnotation())
            annotations = cast(
                List[ExternalCallsAnnotation],
                list(state.get_annotations(ExternalCallsAnnotation)),
            )

        if state.get_current_instruction()["opcode"] in ("SSTORE", "CREATE", "CREATE2"):
            return StateChange._handle_state_change(
                state, address=address, annotation=annotations[0]
            )
        call = get_call_from_state(state)

        if call is None:
            return []

        if StateChange._balance_change(call.value):
            return StateChange._handle_state_change(
                state, address=address, annotation=annotations[0]
            )

        return []

    @staticmethod
    def _get_state_change_issues(
        callissues: List[CallIssue], state: GlobalState, address: int
    ) -> List[Issue]:
        issues = []
        for callissue in callissues:
            severity = "Medium" if callissue.user_defined_address else "Low"
            call = callissue.call
            logging.debug(
                "[EXTERNAL_CALLS] Detected state changes at addresses: {}".format(
                    address
                )
            )
            description_head = (
                "The contract account state is changed after an external call. "
            )
            description_tail = (
                "Consider that the called contract could re-enter the function before this "
                "state change takes place. This can lead to business logic vulnerabilities."
            )

            issue = Issue(
                contract=call.node.contract_name,
                function_name=call.node.function_name,
                address=address,
                title="State change after external call",
                severity=severity,
                description_head=description_head,
                description_tail=description_tail,
                swc_id=REENTRANCY,
                bytecode=state.environment.code.bytecode,
            )
            issues.append(issue)
        return issues

    @staticmethod
    def _handle_state_change(
        state: GlobalState, address: int, annotation: ExternalCallsAnnotation
    ) -> List[Issue]:
        calls = annotation.calls
        issues = StateChange._get_state_change_issues(calls, state, address)
        return issues

    @staticmethod
    def _balance_change(value: Variable) -> bool:
        if value.type == VarType.CONCRETE:
            return value.val > 0
        else:
            zero = symbol_factory.BitVecVal(0, 256)
            return simplify(value.val > zero)


detector = StateChange()
