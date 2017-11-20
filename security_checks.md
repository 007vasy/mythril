# Smart Contract Security Issues

| Issue | Description | Mythril Detection Module(s) | References |
|------:|-------------|------------|----------|
|Unprotected functions| Critical functions such as sends with non-zero value or suicide() calls are callable by anyone, or msg.sender is compared against an address in storage that can be written to. E.g. Parity wallet bugs. | [unchecked_suicide](mythril/analysis/modules/unchecked_suicide.py), [ether_send](mythril/analysis/modules/ether_send.py)          | |
|Missing check on CALL return value|  | [unchecked_retval](mythril/analysis/modules/unchecked_retval.py) | [Handle errors in external calls](https://consensys.github.io/smart-contract-best-practices/recommendations/#use-caution-when-making-external-calls) |
|Re-entrancy|                        | [call to untrusted contract with gas](mythril/analysis/modules/call_to_dynamic_with_gas.py) | |
|Multiple sends in a single transaction| External calls can fail accidentally or deliberately. Avoid combining multiple send() calls in a single transaction. |           |   [Favor pull over push for external calls¶](https://consensys.github.io/smart-contract-best-practices/recommendations/#favor-pull-over-push-for-external-calls) |
|Function call to untrusted contract|             |           [call to untrusted contract with gas](mythril/analysis/modules/call_to_dynamic_with_gas.py) | |
|Delegatecall or callcode to untrusted contract|                   | [delegatecall_forward](mythril/analysis/modules/delegatecall_forward.py), [delegatecall_to_dynamic.py](mythril/analysis/modules/delegatecall_to_dynamic.py) |  |
|Integer overflow/underflow|                        | [integer_underflow](mythril/analysis/modules/integer_underflow.py)          |  |
|Type confusion|                        |           |  |
|Predictable RNG|                        |           |  |
|Transaction order dependence|             |           |           |  |
|Timestamp dependence|                        |           |  |
|Information exposure|                        |           |   |
|Payable transaction does not revert in case of failure | | |   |
|Call depth attack|                        |           |   |
