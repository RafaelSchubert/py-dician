# Py-Dician

## What is Py-Dician?

This one is a little project of mine to practice and get used to working with the Python programming language.

I thought it could be fun to unite something useful (Python) with something which I enjoy (tabletop RPGs). So I decided to make a small, simple dice roll notation language — a _dice-language_ — with a Python interpreter — thus _Py-Dician_. As a bonus, I improve my understanding on interpreters and compilers — which are rather interesting, might I add.

## What is it comprised of?

So far, I've got:

- a **grammar** for the language — which you can read at `./doc/grammar.md`;
- a _**lexical module**_ for all the lexical stuff (symbols, keywords and token parsing and representation) in `./lexic.py`;
- a _**syntactical module**_ for all the syntactical stuff (syntactical parsing and validation) in `./syntactic.py`.

## What does the language feature?

- Describing dice rolls, of course — `mDn` means "roll _m_ dice, each numbered 1 through _n_";
- Arithmetical operations;
- Parenthesized expressions;
- Defining the number of dice and die faces through roll expressions (rolls within rolls within rolls...);

## What is next?

Of course, simply parsing and validating _roll expressions_ yields no meaningful results other than that you've got the grammar right.

The next steps aim for more practical applications:

- [ ] Semantical analysis;
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

## Suggestions

I would appreciate suggestions and reviews on ideas, mistakes and best practices. For that, you may mail me at rafael.schubert.campos@gmail.com.
