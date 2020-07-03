# Samples

In this folder, you'll find some practical usage examples of the Py-Dician module. You can run them from the console/terminal from inside the repository folder as is, like so:

```
/my/pydician/folder> python -m samples.sample_name
```

## 1) Roll Prompt

The `roll_prompt.py` example shows how you can easily set an interactive prompt for making dice rolls. To run it, you can simply execute the script from inside the repository folder.

```
/my/pydician/folder> python -m samples.roll_prompt
```

### How does it work?
It's simple: input a roll expression, press `[Enter]` and that's it.

```
Input a Py-Dician roll expression to be parsed ("q" to exit):
Roll >> 2d6
2d6 = 7
Roll >>
```

It'll request and execute roll expressions until you input `q` to exit.

```
/my/pydician/folder/> python -m samples.roll_prompt
Input a Py-Dician roll expression to be parsed ("q" to exit):
Roll >> d4
d4 = 3
Roll >> d6
d6 = 1
Roll >> d8
d8 = 8
Roll >> d10
d10 = 1
Roll >> d12
d12 = 2
Roll >> q

/my/pydician/folder/>
```

You can also run the last successfully parsed roll expression by providing no input.

```
Input a Py-Dician roll expression to be parsed ("q" to exit):
Roll >> 2d10 + 5
2d10 + 5 = 22
Roll >>
2d10 + 5 = 13
Roll >>
2d10 + 5 = 12
Roll >>
```
