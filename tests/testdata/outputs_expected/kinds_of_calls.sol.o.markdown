# Analysis results for test-filename.sol

## Unchecked CALL return value
- SWC ID: 104
- Type: Informational
- Contract: Unknown
- Function name: `_function_0x141f32ff`
- PC address: 618
- Estimated Gas Usage: 1113 - 35865

### Description

The return value of an external call is not checked. Note that execution continue even if the called contract throws.

## Use of callcode
- SWC ID: 111
- Type: Warning
- Contract: Unknown
- Function name: `_function_0x141f32ff`
- PC address: 618
- Estimated Gas Usage: 389 - 1141

### Description

The function `_function_0x141f32ff` uses callcode. Callcode does not persist sender or value over the call. Use delegatecall instead.

## Unchecked CALL return value
- SWC ID: 104
- Type: Informational
- Contract: Unknown
- Function name: `_function_0x9b58bc26`
- PC address: 849
- Estimated Gas Usage: 1170 - 35922

### Description

The return value of an external call is not checked. Note that execution continue even if the called contract throws.

## External call to user-supplied address
- SWC ID: 107
- Type: Warning
- Contract: Unknown
- Function name: `_function_0xeea4c864`
- PC address: 1038
- Estimated Gas Usage: 471 - 1223

### Description

The contract executes a function call with high gas to a user-supplied address. Note that the callee can contain arbitrary code and may re-enter any function in this contract. Review the business logic carefully to prevent unanticipated effects on the contract state.

## Unchecked CALL return value
- SWC ID: 104
- Type: Informational
- Contract: Unknown
- Function name: `_function_0xeea4c864`
- PC address: 1038
- Estimated Gas Usage: 1195 - 35947

### Description

The return value of an external call is not checked. Note that execution continue even if the called contract throws.
