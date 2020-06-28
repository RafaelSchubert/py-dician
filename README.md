# Py-Dician

## 1) What is Py-Dician?

This one is a little project of mine to practice and get used to working with the Python programming language.

I thought it would be fun to combine something useful (Python) with something which I enjoy (tabletop RPGs). So I decided to make a small, simple dice roll notation language — a _dice-language_ — with a Python interpreter — thus _Py-Dician_. As a bonus, I improve my understanding of interpreters and compilers — which are quite interesting, might I add.

## 2) What is it comprised of?

### 2.1) Grammar

Py-Dician has a grammar: a set of lexic and syntactic rules that all sentences in this language must follow. It details all the symbols of the language and their meaning, how a sentence can be structured and in what order its operations are solved. The complete Py-Dician grammar can be found at `./doc/grammar.md`.

As an example, `2d6 + 3` means _roll two six-sided dice, add their results and add three to that_, which can be broken as:

```
2d6 + 3

    +
   / \
  d   3
 / \
2   6
```

### 2.2) Lexic Components

There's also components for lexic analysis. Using the `Tokenizer` class, the language's tokens can be extracted from a string by sequentially calling the `.next_token()` method until the _end_ token is found (`TokenType.END` type) or an exception is raised. Each token is represented by a `Token` object, which contains the token's type (`.type`), value (`.value`) and position in the string (`.line` and `.column`).

```Python
import pydician

tk_fetcher = pydician.Tokenizer()
tk_fetcher.set_input_string("2d6 + 3")

# Or just:
# tk_fetcher = pydician.Tokenizer("2d6 + 3")

tk = tk_fetcher.next_token()
while not tk.type is pydician.TokenType.END:
  print(f'Fecthed: {tk} ({tk.type.name: <7}, Ln {tk.line:02}, Col {tk.column:02})')
  tk = tk_fetcher.next_token()

# Output
#
# Fecthed: 2 (INTEGER, Ln 01, Col 01)
# Fecthed: d (DIE    , Ln 01, Col 02)
# Fecthed: 6 (INTEGER, Ln 01, Col 03)
# Fecthed: + (PLUS   , Ln 01, Col 05)
# Fecthed: 3 (INTEGER, Ln 01, Col 07)
```

Use the `TokenType` enum to reference the language's token types.

```Python
import pydician

for tt in pydician.TokenType:
  print(f'{tt.name: <20}: {tt.symbol}')

# Output
#
# END                 : None
# PLUS                : +
# MINUS               : -
# MULTIPLY            : *
# DIVIDE              : /
# LEFT_PARENTHESIS    : (
# RIGHT_PARENTHESIS   : )
# DIE                 : d
# INTEGER             : None
```

- a _**syntactic module**_ for all the syntactic stuff (syntactic parsing and validation) in `./syntactic.py`.

## 3) What does the language feature?

- Describing dice rolls, of course — `mDn` means "roll _m_ dice, each numbered 1 through _n_";
- Arithmetic operations;
- Parenthesized expressions;
- Defining the number of dice and die faces through roll expressions (rolls within rolls within rolls...);

## 4) What is next?

Of course, simply parsing and validating _roll expressions_ yields no meaningful results other than that you've got the grammar right.

The next steps aim for more practical applications:

- [ ] Semantic analysis;
- [ ] Parsing resulting in executable operation trees;
  - Perhaps a dice library as a _sibling-project_;
- More complex roll-operations, such as:
  - [ ] Exploding rolls (may result in rolls higher than the die's maximum):
    - [ ] Exploding at a given threshold;
  - [ ] Exploding dice (additional dice):
    - [ ] Also exploding at a given threshold;
  - [ ] Drop lowest/highest roll;
  - [ ] Success counting;
  - [ ] Result-set operations;
  - Any other ideas that may eventually come into mind...

## 5) Suggestions

I would appreciate suggestions and reviews on ideas, mistakes and best practices. For that, you may mail me at rafael.schubert.campos@gmail.com.
