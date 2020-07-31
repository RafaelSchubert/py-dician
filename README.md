# Py-Dician

## What is Py-Dician?

This one is a little project of mine to practice and get used to working with the Python programming language.

I thought it would be fun to combine something useful (Python) with something which I enjoy (tabletop RPGs). So I decided to make a small, simple dice roll notation language — a _dice-language_ — with a Python interpreter — thus _Py-Dician_. As a bonus, I improve my understanding of interpreters and compilers — which are quite interesting, might I add.

### Samples

Check the available samples at `./samples/` for usage examples.

## What does Py-Dician feature?

### Dice rolls, of course

You can describe the roll of multiple dice with the `NdF` notation, where `N` is the number of dice, and `F` the maximum value of the die. (or number of _faces_, numbered 1 through `F`) You can also ommit the number of dice for a roll of single die.

For instance, `3d6` means _"roll three six-sided dice"_, `1d10` means _"roll a single ten-sided die"_, and `1d100` means _"roll a single 100-sided die."_ (also known as a percentile die)

That same notation is regularly used by tabletop games that require some different dice rolls, especially RPGs.

### Arithmetic operations

You can use any of the four main arithmetic operations (sum, subtraction, multiplication and division) with the results of the dice rolls, mixed with fixed numbers. That lets you apply modifiers to these rolls and/or make basic math with them. Indeed, many tabletop RPG rules require adding modifiers to dice rolls.

The available operations are sum, subtraction, multiplication and division, represented by the symbols `+`, `-`, `*` and `/`, respectively.

For instance, `1d6 + 2` means _"roll a single six-sided die and add two to the result"_, while `5 * 1d10` mean _"roll a single ten-sided die and multiply the result by five."_

The operations follow the same precedence as their mathematic counterparts: operations are solved left to right, multiplications and divisions first, sums and subtractions after. You can change this order by surrounding an expression with parentheses (`( expression )`).

Suppose we need to roll a number ranging from 25 to 50, stepping 5 at a time. (25, 30, 35, 40, 45 and 50) We could do so by rolling a single six-sided die, adding four to the result and multiplying it by five. If we write that literally, we get `1d6 + 4 * 5`, which actually doesn't meet our description. The multiplication would be solved before the sum, resulting in 21, 22, 23, 24, 25 or 26 instead. So we change the operation precedence by enclosing the sum in parentheses: `(1d6 + 4) * 5`.

### Logical comparisons

You can compare two values to determine whether one is less than the other, or both are equal or different. The comparison yields `1` if true, or `0` if false. The compared values can be any combination of values and expressions, as long as they're comparable.

The available operations are:
- smaller than (`a < b`);
- greater than (`a > b`);
- equals to (`a = b`);
- smaller than or equal to (`a <= b`);
- greater than or equal to (`a >= b`);
- not equal to (`a <> b`);

The logical comparison operators have a higher precedence than any of the arithmetical operations. For instance, `1 + 1 = 2` means _"is `1 + 1` equals to `2`?"_, and is executed as `(1 + 1) = 2`. On the other hand, `2 < 3 + 1 = 0` is executed as `(2 < (3 + 1)) = 0`.

## What is Py-Dician comprised of?

### Grammar

Py-Dician has a grammar: a set of lexic and syntactic rules that all sentences in this language must follow. It details all the symbols of the language and their meaning, how a sentence can be structured and in what order its operations are solved. The complete Py-Dician grammar can be found at `./doc/grammar.md`.

### Free Functions

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

### Lexic Components

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

### Syntactic Components

The syntactic analysis is made by the `Parser` class, which also translates a Py-Dician sentence into a tree of executable operations. All you need to do is to call `.parse()` providing the sentence as a string argument for the method.

```Python
import pydician

roll_expr = "2d6 + 3"
parser = pydician.Parser()

# Add three to the roll of two six-sided dice.
dice_roll = parser.parse(roll_expr)

for i in range(10):
  print(f'{i}: {roll_expr} = {dice_roll.run()}')

# Possible output:
#
# 0: 2d6 + 3 = 13
# 1: 2d6 + 3 = 13
# 2: 2d6 + 3 = 9
# 3: 2d6 + 3 = 11
# 4: 2d6 + 3 = 12
# 5: 2d6 + 3 = 7
# 6: 2d6 + 3 = 8
# 7: 2d6 + 3 = 10
# 8: 2d6 + 3 = 13
# 9: 2d6 + 3 = 11
```

## What is next?

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

## Suggestions

I would appreciate suggestions and reviews on ideas, mistakes and best practices. For that, you may mail me at rafael.schubert.campos@gmail.com.
