# Py-Dician's Grammar

## Definitions

Signs, keywords and literals of the language.

```
# Signs
left_parenthesis  = "("
right_parenthesis = ")"
plus              = "+"
minus             = "-"
multiply          = '*'
divide            = '/'

# Keywords
die_tag = [dD]

# Literals
integer = ("0" | [1-9] [0-9]*)
```

Only things worthy of note are:

- `die_tag`: used in conjunction with numerical expressions to describe a _dice set_, i.e. one or more dice rolled together;
- `integer`: describes a non-negative whole number, i.e. a number equal to or greater than 0 (zero).

## Grammar

The predicates and production rules of the language.

```
<roll_expression> ::= <addition_or_subtraction>

<addition_or_subtraction>            ::= <product_or_division> <addition_or_subtraction_right_hand>
<addition_or_subtraction_right_hand> ::= <plus_or_minus> <product_or_division> <addition_or_subtraction_right_hand>
                                       | &

<product_or_division>            ::= <positive_or_negative> <product_or_division_right_hand>
<product_or_division_right_hand> ::= <multiply_or_divide> <positive_or_negative> <product_or_division_right_hand>
                                   | &

<positive_or_negative> ::= <plus_or_minus> <dice_set_or_value>
                         | <dice_set_or_value>

<dice_set_or_value> ::= <value> <optional_die>
                      | <die>

<optional_die> ::= <die>
                 | &

<die> ::= die_tag <value>

<value> ::= <parenthesized_expression>
          | <literal>

<parenthesized_expression> ::= left_parenthesis <roll_expression> right_parenthesis

<literal> ::= <numeric_literal>

<numeric_literal> ::= integer

<plus_or_minus> ::= plus
                  | minus

<multiply_or_divide> ::= multiply
                       | divide
```
