"""
Finite Automaton (DFA) simulator for simplified email addresses.

Alphabet:
  letters a-z and digits 0-9 plus '@' and '.'

Language accepted:
  username@d1.d2[.d3...]
  - username, each domain label: one or more alnum
  - at least one dot in the domain part (=> at least two domain names)
  - last domain (TLD) length is exactly 2 or 3 (alnum)
No regex is used. This is a DFA simulation.
"""

from enum import Enum, auto
import sys


class State(Enum):
    Q0 = auto()  # start
    Q1 = auto()  # reading username (seen at least 1 alnum)
    Q2 = auto()  # just read '@', need first domain char
    Q3 = auto()  # reading a domain label before a dot
    Q4 = auto()  # just read '.', need first char after dot
    Q5 = auto()  # TLD length = 1 (since last dot)
    Q6 = auto()  # TLD length = 2 (ACCEPT)
    Q7 = auto()  # TLD length = 3 (ACCEPT)
    QD = auto()  # dead


def is_alnum(ch: str) -> bool:
    return ('a' <= ch <= 'z') or ('0' <= ch <= '9')


def delta(state: State, ch: str) -> State:
    """Transition function δ(state, ch) -> next_state"""
    # Dead state loops
    if state == State.QD:
        return State.QD

    # Q0: must start with alnum
    if state == State.Q0:
        if is_alnum(ch):
            return State.Q1
        else:
            return State.QD

    # Q1: username continues on alnum, then '@' goes to Q2
    if state == State.Q1:
        if is_alnum(ch):
            return State.Q1
        elif ch == '@':
            return State.Q2
        else:  # '.' or anything else
            return State.QD

    # Q2: first char of first domain label must be alnum
    if state == State.Q2:
        if is_alnum(ch):
            return State.Q3
        else:
            return State.QD

    # Q3: reading domain label (before dot). '.' starts "after dot" region.
    if state == State.Q3:
        if is_alnum(ch):
            return State.Q3
        elif ch == '.':
            return State.Q4
        else:  # '@' or anything else
            return State.QD

    # Q4: first char after dot must be alnum (start counting TLD length)
    if state == State.Q4:
        if is_alnum(ch):
            return State.Q5
        else:
            return State.QD

    # Q5: after dot, length 1 so far; next alnum makes length 2 (Q6)
    if state == State.Q5:
        if is_alnum(ch):
            return State.Q6
        else:
            return State.QD

    # Q6: TLD length 2 (accepting). Another alnum makes length 3 (Q7).
    # A dot means: that label wasn't final; start a new "after dot" label.
    if state == State.Q6:
        if is_alnum(ch):
            return State.Q7
        elif ch == '.':
            return State.Q4
        else:
            return State.QD

    # Q7: TLD length 3 (accepting). Another alnum => too long => dead.
    # Dot means: this 3-length label becomes not-final; start new label.
    if state == State.Q7:
        if is_alnum(ch):
            return State.QD
        elif ch == '.':
            return State.Q4
        else:
            return State.QD

    # Fallback
    return State.QD


def accepts(s: str, trace: bool = False) -> bool:
    """Run DFA on input string s. Return True if accepted."""
    s = s.strip().lower()  # enforce [a-z0-9] only, treat uppercase as lowercase
    state = State.Q0
    if trace:
        print(f"start: {state.name}")

    for i, ch in enumerate(s):
        state = delta(state, ch)
        if trace:
            print(f" read '{ch}' -> {state.name}")
        if state == State.QD and trace:
            # still keep reading for full simulation; DFA stays dead anyway
            pass

    # Accepting states are Q6 or Q7 (meaning final label length is 2 or 3)
    return state in (State.Q6, State.Q7)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 email_fa.py <email_string> [--trace]")
        print("  python3 email_fa.py --file <path_to_test_file> [--trace]")
        sys.exit(1)

    trace = "--trace" in sys.argv

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Error: missing file path after --file")
            sys.exit(1)
        path = sys.argv[2]
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                x = line.strip()
                if not x:
                    continue
                ok = accepts(x, trace=trace)
                print(f"{x} => {'ACCEPT' if ok else 'REJECT'}")
    else:
        email = sys.argv[1]
        ok = accepts(email, trace=trace)
        print("ACCEPT" if ok else "REJECT")


if __name__ == "__main__":
    main()
