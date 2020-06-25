# Py-Dician's Grammar

## 1) Definitions

The Py-Dician language uses a few symbols to denote its values, operations and concepts. Those symbols are divided into three categories:
- signs;
- keywords;
- and literals.

The definitions are given in terms of regular expressions.

### 1.1) Signs

Signs are symbols composed of a single non-alphanumeric character. They represent delimiters and operators, such as mathematical symbols.

```
left_parenthesis  = (
right_parenthesis = )
plus              = +
minus             = -
multiply          = *
divide            = /
```

### 1.2) Keywords

Keywords are symbols composed of one or more alphanumeric characters — _words_, that is. They represent more complex operations and constructs or concepts. Those words are reserved for the language.

```
die_tag = [dD]
```

### 1.3) Literals

Literals represent values that are expressed in an explicit manner, such as whole numbers.

```
integer = (0 | [1-9] [0-9]*)
```

## 2) Grammar

The language per se is described by _predicates_: rules that dictate the way the symbols are coherently arranged. A predicate specifies a syntactical component of the language, providing the sequences of symbols that are understood by the language.

Each predicate is described as follows:

```
<name_of_the_predicate> ::= rule
```

Or:

```
<name_of_the_predicate> ::= first rule | second rule | ... | n-th rule
```

### 2.1) Predicates

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
