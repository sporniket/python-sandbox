# Finite State Machine from a list of words

## Abstract

```python
# items of the list of words = {word:string,tag:integer}
# * word : the actual word to be recognized by the fsm
# * tag : the strictly positive integer identifying the word. The same tag MAY be attached to different words seen as equivalent/synonyms/aliases.
# NOTE : A word MAY be an illegal key, thus we don't use a dictionnary {word->tag}.
fsm = fsmFromWordlist([
    {word:"foo",tag:1},
    {word:"bar",tag:2}
])

assert(fsm.scan("foo") == 1)
assert(fsm.scan("bar") == 2)
assert(fsm.scan("fooo") == 0)
assert(fsm.scan("whatever") == 0)
```

## Principle of the generated state machine

### About the characters

* Only characters stored in one byte, and only the US-ASCII part (0 to 127), are supported.
* The list of acceptable characters, and the case sensitivity, allow to build an encoding function `psi` that convert a byte into
an integer code, starting from 1 to K (the size of the list of acceptable characters). The mapping is ordered like the source bytes, meaning that for each `i`,`j` in the range [0..127], if `i < j` then `psi(i) < psi(j)`, and if `i == j` then `psi(i) == psi(j)`.
A code of 0 mean that the source character is invalid for this machine.

The encoding function is modelized as a list of 128 bytes, each one being a value in the [0..K] range.

If the machine is case insensitive, for each `i` in the range [a-z], `psi(i) = psi(i-32)`.

### About the state machine

* A state machine is an ordered list of states, identified by their indexes in the list. The state 0 is the initial state.
* Each state of the state machine is described by :
  * A tag (strictly positive integer), meaning that reaching this state with the last character to scan is a match ; or 0 (zero), meaning no match
  * For each acceptable character, a relative value that points to the next state, relative to the current state (meaning that this character is valid from this state), or 0 (meaning that this character is not valid, thus not a match).
* States are ordered so that next valid states are **always** after the current state, meaning that the relative value is always positive.

As a result, a state can be modelized as a list `s` of `K+1` unsigned integers :
  * `s[0]` stores the tag or 0
  * `s[psi(char)]` stores the offset to the next state or 0

## Making of the finite state machine

### First pass

* The list of words is sorted alphabetically
* Prepare a list of 127 integer values (psi), initialized to 0
* for each word, scan each char `c` : 
  * if the char is out of the [0..127] range, **raise an error** ("out of range")
  * if `psi(c)` is zero, change this value to 1.
* K = 0  
* for each `c` in range [0..127]:
  * if `psi(c)` is not zero
    * if case sensitive or `c` not in range [a-z] : increment K, and change the value `psi(c)` to K
    * else (`c` in range [a-z]) : change the value of `psi(c)` to the same value as `psi(c-32)`

> Also, assess `lambda` as the maximum length of the words of the list.

### Second pass

* current state = 0, target = 0
* for each length from 1 to `lambda` as `l`
  * reset previous prefix.
  * for each word of the sorted list as `w`
    * if the prefix (`w[1..l-1]`) is different, advance one state, decrement the next target value, reset previous char, update previous prefix.
    * if the last char (`w[l]`) is different, increment target, then `state[current][psi(w[l])] = target`

The machine size (number of states) is `current state + 1`.
