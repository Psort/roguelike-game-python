from ast import While
import util
import engine
import ui
import inventory as inv
import players
import test
import items
import characters
import keys

def get_player():
    player = players.create_player()
    util.clear_screen()
    choice = input("Select boards 1-4: ")
    return play(player,choice)


def play(player,choice):
    add_info = {}
    position_player = players.Position_player(player['icon'])
    test.start_thread(player,add_info)
    number_board,board, hiden_board = ui.choosing_a_board(choice)
    how_many_item = 20
    how_many_hiden_item = 10
    if choice == 3:
        characters.put_mob_to_map(hiden_board)
        how_many_item = 6
        how_many_hiden_item = 3
    
    items.put_medicines_to_map(hiden_board,how_many_item)
    items_list = items.create_hidden_item(hiden_board,how_many_hiden_item)
    is_running = True
    check = "no"
    while is_running:
        function_board(hiden_board,board,position_player,check, add_info)
        key = util.key_pressed()
        if key == 'q':
            is_running = False
            return False
        elif key == 'i':
            print(inv.display_inventory(player["inventory"]))
            util.key_pressed()
        elif key == 'p':
            players.player_statistic(player)
            util.key_pressed()
        if engine.position_player_is_free(board,position_player,key):
            position_player = engine.move(key,position_player)
            if board[position_player['y']] [position_player['x']] == "H":
                hiden_board = board
            if position_player['y'] == 0:
                util.clear_screen()
                print("Congratulation, you esceped from the shelted!")
                util.key_pressed()
                return False
        check = check_play(hiden_board,position_player,board,player,items_list,number_board,choice)
        util.clear_screen()


def function_board(hiden_board,board,position_player,check, add_info):
        if check != "Run":
            engine.put_position_player_on_board(hiden_board, position_player)
            engine.put_position_player_on_board(board, position_player)

            ui.display_board(hiden_board,position_player, add_info)
            engine.remove_position_player_on_board(hiden_board, position_player)
            engine.remove_position_player_on_board(board, position_player)
        else:
            ui.display_board(hiden_board,position_player, add_info)

def check_play(hiden_board,position_player,board,player,items_list,number_board,choice):
    if player["health"]<1:
        play(players.take_player(player["name"]),choice)
    if hiden_board[position_player['y']] [position_player['x']] == "i":
        items.loot_medicine(player)
    if {"y":position_player['y'],"x": position_player['x']} in items_list:
        items.loot_sickness(player)
        items_list.remove({"y":position_player['y'],"x": position_player['x']})
    if hiden_board[position_player['y']] [position_player['x']] in ["¶","."]:
        keys.open_door(number_board,hiden_board,position_player)
        keys.open_door(number_board,board,position_player)
    if board[position_player['y']] [position_player['x']] == "B":
        characters.fight_with_boss(player, characters.choose_mob(hiden_board[position_player['y']] [position_player['x']]), board, position_player,choice)
    if board[position_player['y']] [position_player['x']] in ["G","S","F"]:
        return characters.fight_with_mob(characters.choose_mob(hiden_board[position_player['y']] [position_player['x']]), player,choice)