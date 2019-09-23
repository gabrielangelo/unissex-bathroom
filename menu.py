# builtin imports
import os

# internal imports
from unissex_bathroom import UnissexBathroom


if __name__ == "__main__":
    args_choices = {
        '1': {'num_people': 5, 'num_boxes': 1},
        '2': {'num_people': 150, 'num_boxes': 3},
        '3': {'num_people': 300, 'num_boxes': 5}
    }

    while 1:
        print('choice the problem bellow:')
        print(60 * '*')
        print('1: Problem 1 -> 60 people to one box in the bathroom')
        print('2: Problem 2 -> 150 people to 3 boxes')
        print('3: Problem 3 -> 300 people to 5 boxes')
        print(60 * '*')
        choice = input('Choice:')

        try:
            args = args_choices[choice]
        except KeyError:
            print('Invalid option, try again')

        UnissexBathroom.run(**args)
        os.system('cls')
