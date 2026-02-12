
# Email DFA Simulator (No Regex)

This program simulates a deterministic finite automaton (DFA) that recognizes simplified valid email addresses.

## Language definition (what it accepts)
- username is one or more letters/digits: [a-z0-9]+
- then '@'
- then a list of at least two domain names separated by '.'
- each domain name is [a-z0-9]+
- the last domain name (TLD) has length exactly 2 or 3

Examples accepted:
- abc@dsu.edu
- abc@pluto.dsu.edu
- 11@123.com

Examples rejected:
- a.b.ab      (no '@')
- ab@ab       (no '.' in domain => not at least two domain names)
- ab@ab.abcd  (TLD length is 4)

## Files
- email.py  (source code)

## How to run
Requires Python 3.

Run on one input:
```bash
python3 email.py abc@dsu.edu

```
Run on multiple input: 
```bash
python email.py --file test.txt
