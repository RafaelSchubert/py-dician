# Py-Dician

## 1) What is Py-Dician?

This one is a little project of mine to practice and get used to working with the Python programming language.

I thought it would be fun to combine something useful (Python) with something which I enjoy (tabletop RPGs). So I decided to make a small, simple dice roll notation language — a _dice-language_ — with a Python interpreter — thus _Py-Dician_. As a bonus, I improve my understanding of interpreters and compilers — which are quite interesting, might I add.

## 2) What is it comprised of?

### 2.1) Grammar

Py-Dician has a grammar: a set of lexic and syntactic rules that all sentences in this language must follow. It details all the symbols of the language and their meaning, how a sentence can be structured and in what order its operations are solved. The complete Py-Dician grammar can be found at `./doc/grammar.md`.

### 2.2) Free Functions

The user can quickly process Py-Dician expressions using either the `parse()` or `roll()` free functions.

The `parse()` function takes an expression as a string argument, parses it and returns the resulting operation tree. This operation tree may then be executed as many times as needed. It may raise an exception if the expression is inconsistent.

```Python
import pydician

# Subtracts the roll of a six-sided die
# from the roll of another six-sided die.
# Results range from [-5, 5].
roll_op = pydician.parse("1d6 - 1d6")

few_rolls = [roll_op.run() for _ in range(10)]

print(", ".join(str(roll) for roll in few_rolls))

# Possible output:
#
# 1, 0, 2, -1, 5, -4, 3, -3, -3, 1
```

The `roll()` function takes an expression as a string argument, parses it and immediately runs it, returning its result. As with `parse()`, it may raise an exception if the expression is inconsistent.

```Python
import pydician

# Adds the roll of a eight-sided die
# to the roll of a twelve-sided die.
# Results range from [2, 20].
few_rolls = [pydician.roll("1d12 + 1d8") for _ in range(10)]

print(", ".join(str(roll) for roll in few_rolls))

# Possible output:
#
# 9, 15, 13, 16, 9, 6, 12, 6, 16, 10
```

### 2.3) Lexic Components

There's also components for lexic analysis. Using the `Tokenizer` class, the language's tokens can be extracted from a string by sequentially calling the `.next_token()` method until the _end_ token is found (`TokenType.END` type) or an exception is raised. Each token is represented by a `Token` object, which contains the token's type (`.type`), value (`.value`) and position in the string (`.line` and `.column`).

```Python
import pydician

tk_fetcher = pydician.Tokenizer()

# Adds three to the roll of two six-sided dice.
tk_fetcher.set_input_string("2d6 + 3")

# Or just:
# tk_fetcher = pydician.Tokenizer("2d6 + 3")

fetched_tokens = []
while True:
  tk = tk_fetcher.next_token()
  if tk.type is pydician.TokenType.END:
    break
  fetched_tokens.append(tk)

for tk in fetched_tokens:
  print(f'Fecthed: {tk} ({tk.type.name: <10}, Ln {tk.line:02}, Col {tk.column:02})')

# Output
#
# Fecthed: 2 (INTEGER   , Ln 01, Col 01)
# Fecthed: d (DIE       , Ln 01, Col 02)
# Fecthed: 6 (INTEGER   , Ln 01, Col 03)
# Fecthed: + (PLUS      , Ln 01, Col 05)
# Fecthed: 3 (INTEGER   , Ln 01, Col 07)
```

### 2.4) Syntactic Components

The syntactic analysis is made by the `Parser` class, which also translates a Py-Dician sentence into a tree of executable operations. All you need to do is to call `.parse()` providing the sentence as a string argument for the method.

```Python
import pydician

parser = pydician.Parser()
dice_roll = parser.parse("2d6 + 3")

for i in range(10):
  print(f'{i}th roll: {dice_roll.run()}')

# Possible output:
#
# 0th roll: 13
# 1th roll: 13
# 2th roll: 9
# 3th roll: 11
# 4th roll: 12
# 5th roll: 7
# 6th roll: 8
# 7th roll: 10
# 8th roll: 13
# 9th roll: 11
```

## 3) What does the language feature?

- Describing dice rolls, of course — `mDn` means "roll _m_ dice, each numbered 1 through _n_";
- Arithmetic operations;
- Parenthesized expressions;
- Defining the number of dice and die faces through roll expressions (rolls within rolls within rolls...);

## 4) What is next?

Possible features:

- More complex roll operations, such as:
  - Exploding rolls (may result in rolls higher than the die's maximum):
    - Exploding at a given threshold;
  - Exploding dice (additional dice):
    - Also exploding at a given threshold;
  - Drop lowest/highest roll;
  - Success counting;
  - Result-set operations;
  - Any other ideas that may eventually come into mind...
- Perhaps a dice library as a _sibling-project_;

## 5) Suggestions

I would appreciate suggestions and reviews on ideas, mistakes and best practices. For that, you may mail me at rafael.schubert.campos@gmail.com.
