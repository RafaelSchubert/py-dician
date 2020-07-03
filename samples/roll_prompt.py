import pydician


def main():
    print('Input a Py-Dician roll expression to be parsed ("q" to exit):')

    last_roll_expr = None

    while True:
        try:
            roll_expr = input('Roll >> ').strip()

            if not roll_expr:
                if last_roll_expr:
                    roll_expr = last_roll_expr
                else:
                    continue

            if roll_expr.lower()=='q':
                break

            result = pydician.roll(roll_expr)
            last_roll_expr = roll_expr

            print(f'{roll_expr} = {result}')
        except pydician.PyDicianError:
            print(f'"{roll_expr}" is not recognized as a roll expression.')


if __name__ == "__main__":
    main()
