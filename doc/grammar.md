# Py-Dician's Grammar

## 1) Definitions

The Py-Dician language uses a few symbols to denote its values, operations and concepts. Those symbols are divided into three categories:
- signs;
- keywords;
- and literals.

The definitions are given in terms of regular expressions.

### 1.1) Signs

Signs are symbols made up of a single non-alphanumeric character. They represent delimiters and operators, such as mathematical symbols.

```
left_parenthesis  = (
right_parenthesis = )
plus              = +
minus             = -
multiply          = *
divide            = /
```

### 1.2) Keywords

Keywords are symbols made up of one or more alphanumeric characters — that is, _words_. They represent more complex operations and constructs or concepts. These words are reserved for use of the language.

```
die_tag = [dD]
```

### 1.3) Literals

Literals represent values that are expressed in an explicit manner, such as whole numbers.

```
integer = (0|[1-9][0-9]*)
```

## 2) Grammar

The language itself is described by _predicates_ that specify the syntactic components of the language, providing the rules for its expressions. These rules dictate the ways the symbols might be coherently arranged and therefore understood by the language. Think of these rules as the ways in which you can arrange words to formulate sentences in your language.

Each predicate is described as:

```
<name of the predicate> ::= rules
```

With `rules` being specified by one or more options separated by `|`.

```
first option | second option | ... | n-th option
```

Each of these options consists of a sequence of symbols and predicates, or the character `&`, indicating that the predicate is optional.

A complete set of predicates might look like this:

```
Definitions:
    plus    = +
    minus   = -
    integer = (0|[1-9][0-9]*)

Predicates:
    <evaluable_expression> ::= <sum_or_subtraction>

    <sum_or_subtraction>            ::= <value> <sum_or_subtraction_right_hand>
    <sum_or_subtraction_right_hand> ::= <plus_or_minus> <value> <sum_or_subtraction_right_hand> | &

    <value> ::= integer

    <plus_or_minus> ::= plus | minus
```

### 2.1) Specification

The Py-Dician language is specified by the following set of predicates, starting at `roll_expression`:

```
<roll_expression> ::= <math_expression>

<math_expression> ::= <add_or_subtract>

<add_or_subtract>            ::= <multiply_or_divide> <add_or_subtract_right_hand>
<add_or_subtract_right_hand> ::= <plus_or_minus> <multiply_or_divide> <add_or_subtract_right_hand> | &

<multiply_or_divide>            ::= <positive_or_negative> <multiply_or_divide_right_hand>
<multiply_or_divide_right_hand> ::= <multiply_or_divide> <positive_or_negative> <multiply_or_divide_right_hand> | &

<positive_or_negative> ::= <plus_or_minus> <dice_set> | <dice_set>

<dice_set>     ::= <value> <optional_die> | <die>
<optional_die> ::= <die> | &

<die> ::= die_tag <value>

<value> ::= <literal> | <parenthesized_expression>

<literal> ::= integer

<parenthesized_expression> ::= left_parenthesis <math_expression> right_parenthesis

<plus_or_minus>      ::= plus | minus
<multiply_or_divide> ::= multiply | divide
```
