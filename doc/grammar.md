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
<roll_expression> ::= <arithmetic_expression>

<arithmetic_expression>            ::= <term> <arithmetic_expression_right_hand>
<arithmetic_expression_right_hand> ::= <plus_or_minus> <term> <arithmetic_expression_right_hand>
                                     | &

<term>            ::= <factor> <term_right_hand>
<term_right_hand> ::= <multiply_or_divide> <factor> <term_right_hand>
                    | &

<factor> ::= <plus_or_minus> <dice_set>
           | <dice_set>

<dice_set> ::= <value> <optional_die>
             | <die>

<die>          ::= die_tag <value>
<optional_die> ::= <die>
                 | &

<value> ::= <parenthesized_expression>
          | <literal_expression>

<parenthesized_expression> ::= left_parenthesis <arithmetic_expression> right_parenthesis

<literal_expression> ::= integer

<plus_or_minus>      ::= plus | minus
<multiply_or_divide> ::= multiply | divide
```
