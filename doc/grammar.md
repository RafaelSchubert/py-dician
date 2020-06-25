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
<roll_expression> ::= <math_expression>

<math_expression> ::= <add_or_subtract>

<add_or_subtract>            ::= <multiply_or_divide> <add_or_subtract_right_hand>
<add_or_subtract_right_hand> ::= <plus_or_minus> <multiply_or_divide> <add_or_subtract_right_hand>
                               | &

<multiply_or_divide>            ::= <positive_or_negative> <multiply_or_divide_right_hand>
<multiply_or_divide_right_hand> ::= <multiply_or_divide> <positive_or_negative> <multiply_or_divide_right_hand>
                                  | &

<positive_or_negative> ::= <plus_or_minus> <dice_set>
                         | <dice_set>

<dice_set>     ::= <value> <optional_die>
                 | <die>
<optional_die> ::= <die>
                 | &

<die> ::= die_tag <value>

<value> ::= <literal>
          | <parenthesized_expression>

<literal> ::= integer

<parenthesized_expression> ::= left_parenthesis <math_expression> right_parenthesis

<plus_or_minus>      ::= plus | minus
<multiply_or_divide> ::= multiply | divide
```
