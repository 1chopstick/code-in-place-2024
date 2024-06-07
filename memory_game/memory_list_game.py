import random

NUM_PAIRS = 4

def main():
    """
    You should write your code here. Make sure to delete 
    the 'pass' line before starting to write your own code.
    """
    # Milestone #1: Create the truth list
    truth = []
    for i in range(NUM_PAIRS):
        truth.append(i)
        truth.append(i)

    # Milestone #2: Shuffle the list
    random.shuffle(truth)
    print(truth)

    # Milestone #3: Create a displayed list
    display = ['*' for _ in range(NUM_PAIRS*2)]
    print(display)
    
    # Milestone #4: Get a valid index from the user
    matches = 0
    while matches != NUM_PAIRS:
        first = input("Enter an index: ")
        second = input("Enter an index: ")

        # Milestone #5: Check correct
        if first == second:
            print("You entered the same index twice. Try again.")
        elif get_valid_index(display, first) and get_valid_index(display, second):
            first = int(first)
            second = int(second)
            print("Value at index {} is {}".format(first, truth[first]))
            print("Value at index {} is {}".format(second, truth[second]))
            if truth[first] == truth[second]:
                pytho
                print("Match!")
                display[first] = truth[first]
                display[second] = truth[second]
                matches += 1
                print(display)
            else:
                print("No match. Try again.")

    print("Congratulations! You won!")


def get_valid_index(display, index):
    
    if not index.isnumeric():
        print("Not a number. Try again.")
        return False

    index = int(index)

    if index < 0 or index > len(display):
        print("This number is invalid index. Try again.")
        return False

    if display[index] != '*':
        print("This number has already been matched. Try again.")
        return False

    return True



def clear_terminal():
    for i in range(20):
      print('\n')

if __name__ == '__main__':
    main()
