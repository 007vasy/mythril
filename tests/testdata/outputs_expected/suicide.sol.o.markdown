# Analysis results for test-filename.sol

## Unchecked SUICIDE
- SWC ID: 106
- Type: Warning
- Contract: Unknown
- Function name: `kill(address)`
- PC address: 146
- Estimated Gas Usage: 168 - 263

### Description

The contract can be killed by anyone and the attacker can withdraw its balance.
