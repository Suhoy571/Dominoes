import random


def get_highest_domino(player: list, computer: list):
    player.sort()
    computer.sort()
    max_player = player[-1]
    max_computer = computer[-1]
    if max_player > max_computer:
        player.remove(max_player)
        return max_player
    else:
        computer.remove(max_computer)
        return max_computer


def check_move(type_of_player, player: list, piece_id: int, list_dominoes: list):
    if type_of_player == 'human':
        lst = player[abs(piece_id) - 1]
    else:
        lst = player[abs(piece_id) - 1]
    if piece_id >= 0:
        if lst[0] == list_dominoes[-1][1]:
            end = True
            begin = False
            reorient = False
            return end, begin, reorient
        elif lst[1] == list_dominoes[-1][1]:
            end = True
            begin = False
            reorient = True
            return end, begin, reorient
        else:
            end = False
            begin = False
            reorient = False
            return end, begin, reorient
    else:
        if lst[0] == list_dominoes[0][0]:
            end = False
            begin = True
            reorient = True
            return end, begin, reorient
        elif lst[1] == list_dominoes[0][0]:
            end = False
            begin = True
            reorient = False
            return end, begin, reorient
        else:
            end = False
            begin = False
            reorient = False
            return end, begin, reorient


def make_move(player: list, piece_id: int, list_dominoes: list):
    end, begin, reorient = check_move('human', player, piece_id, list_dominoes)
    if piece_id == 0 and stock_pieces:
        random.shuffle(stock_pieces)
        player.append(stock_pieces[0])
        stock_pieces.remove(stock_pieces[0])
    else:
        if end == True and begin == False and reorient == False:
            list_dominoes.append(player[abs(piece_id) - 1])
        elif end == True and begin == False and reorient == True:
            list_dominoes.append(player[abs(piece_id) - 1][::-1])
        elif end == False and begin == True and reorient == False:
            list_dominoes.insert(0, player[abs(piece_id) - 1])
        elif end == False and begin == True and reorient == True:
            list_dominoes.insert(0, player[abs(piece_id) - 1][::-1])
        else:
            return 'Illegal move. Please try again', player, list_dominoes
        player.pop(abs(piece_id) - 1)
    if stock_pieces == 0:
        return '', player, list_dominoes
    else:
        return '', player, list_dominoes


def computer_move(computer: list, list_dominoes: list):
    all_dominoes = computer + list_dominoes
    # Count the number of 0's, 1's, 2's, etc., in your hand, and in the snake.
    count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, }
    for i, value in enumerate(all_dominoes):
        count[all_dominoes[i][0]] = count[all_dominoes[i][0]] + 1
        count[all_dominoes[i][1]] = count[all_dominoes[i][1]] + 1
    domino_scores = {}
    for i in computer:
        domino_scores[tuple(i)] = int(count[i[0]]) + int(count[i[1]])
    # Сортировка по максимальному значение value
    domino_scores = {k: v for k, v in sorted(domino_scores.items(), key=lambda item: item[1])}
    # print(domino_scores)
    computer.clear()
    for i in domino_scores:
        computer.append(list(i))
    # print(computer)

    for i in range(-len(computer), len(computer)):
        end, begin, reorient = check_move('computer', computer, i, list_dominoes)
        if end == True and begin == False and reorient == False:
            list_dominoes.append(computer[abs(i) - 1])
            computer.pop(i)
            break
        elif end == True and begin == False and reorient == True:
            list_dominoes.append(computer[abs(i) - 1][::-1])
            computer.pop(i)
            break
        elif end == False and begin == True and reorient == False:
            list_dominoes.insert(0, computer[abs(i) - 1])
            computer.pop(i)
            break
        elif end == False and begin == True and reorient == True:
            list_dominoes.insert(0, computer[abs(i) - 1][::-1])
            computer.pop(i)
            break
    else:
        if stock_pieces == 0:
            return computer, list_dominoes
        else:
            random.shuffle(stock_pieces)
            computer.append(stock_pieces[0])
            stock_pieces.remove(stock_pieces[0])
    return computer, list_dominoes


def print_snake(list_dominoes: list):
    if len(list_dominoes) >= 6:
        return print(
            f"{''.join([str(k) for k in list_dominoes[0:3]])}...{''.join([str(k) for k in list_dominoes[len(list_dominoes) - 3:len(list_dominoes)]])}")
    else:
        return print(''.join([str(k) for k in list_dominoes]))


def check_condition(player_pieces: list, computer_pieces: list, high_element: list):
    if len(stock_pieces) == 0:
        return
    if len(player_pieces) == 0 or len(computer_pieces) == 0:
        if len(player_pieces) == 0:
            return "Status: The game is over. You won!"
        else:
            return "Status: The game is over. The computer won!"
    if high_element[0][0] == high_element[-1][1]:
        counter = 1
        for i in high_element:
            if high_element[0][0] in i:
                counter += 1
                if counter == 8:
                    return "Status: The game is over. It's a draw!"


stock_pieces = [
    [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
    [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 2],
    [2, 3], [2, 4], [2, 5], [2, 6], [3, 3], [3, 4], [3, 5],
    [3, 6], [4, 4], [4, 5], [4, 6], [5, 5], [5, 6], [6, 6]
]

Domino_snake = []
random.shuffle(stock_pieces)

player_pieces = stock_pieces[0:7]
[stock_pieces.remove(k) for k in player_pieces]
computer_pieces = stock_pieces[0:7]
[stock_pieces.remove(k) for k in computer_pieces]

high_element = [get_highest_domino(player_pieces, computer_pieces)]

status = True
iteration = 0
command = ''

while True:
    print(70 * "=")
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}")
    # print(f"Computer pieces: {computer_pieces}")
    print()
    print_snake(high_element)
    print()
    if iteration == 0:
        if len(computer_pieces) > len(player_pieces):
            status = True
            print("Your pieces:")
            for i, value in enumerate(player_pieces):
                print(f"{i + 1}:{value}")
            print()
            print("Status: Computer is about to make a move. Press Enter to continue...")
            while True:
                if input() == "":
                    computer_pieces, high_element = computer_move(computer_pieces, high_element)
                    iteration += 1
                    break
                else:
                    print("Invalid input. Please try again.")
        else:
            status = False
            print("Your pieces:")
            for i, value in enumerate(player_pieces):
                print(f"{i + 1}:{value}")
            print()
            print("Status: It's your turn to make a move. Enter your command.")
            while True:
                command = input()
                if command.lstrip('-').isdigit() and abs(int(command)) <= len(player_pieces):
                    result, player_pieces, high_element = make_move(player_pieces, int(command), high_element
                                                                    )
                    if result:
                        print(result)
                    else:
                        iteration += 1
                        break
                    iteration += 1
                else:
                    print("Invalid input. Please try again.")
    else:
        condition = check_condition(player_pieces, computer_pieces, high_element)
        if condition:
            print("Your pieces:")
            for i, value in enumerate(player_pieces):
                print(f"{i + 1}:{value}")
            print(condition)
            print()
            break
        else:
            if not status:
                status = True
                print("Your pieces:")
                for i, value in enumerate(player_pieces):
                    print(f"{i + 1}:{value}")
                print()
                print("Status: Computer is about to make a move. Press Enter to continue...")
                while True:
                    if input() == "":
                        computer_pieces, high_element = computer_move(computer_pieces, high_element)
                        break
                    else:
                        print("Invalid input. Please try again.")
                continue
            else:
                status = False
                print("Your pieces:")
                for i, value in enumerate(player_pieces):
                    print(f"{i + 1}:{value}")
                print()
                print("Status: It's your turn to make a move. Enter your command.")
                while True:
                    command = input()
                    if command.lstrip('-').isdigit() and abs(int(command)) <= len(player_pieces):
                        result, player_pieces, high_element = make_move(player_pieces, int(command), high_element)
                        if result:
                            print(result)
                        else:
                            break
                    else:
                        print("Invalid input. Please try again.")
                continue
    iteration += 1
