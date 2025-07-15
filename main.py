# misc support: multiple dice roll (example: 2d6 instead of d6 twice), humor, etc.
# effect support: advantage, modifiers (+, -, /, *)
# dice support: d1, d3, d4, d6, d10, d12, d20, d100, percentile (or whatever you want rolled?)
# resistance and vulnerability (half damage and double damage respectively)
# help, manual, error handling
# critical hits
# re-roll mechanics?
# humor?
# gtk4 ui eventually

import random
import re
import math

roll_history = []


def dice_roller(dice_quantity_str, dice_type_str):
    # initialize dice result list
    dice_quantity = int(dice_quantity_str)
    dice_type = int(dice_type_str)
    raw_dice_roll_results = []
    # main dice rolling logic
    for _ in range(dice_quantity):
        current_roll = random.randint(1, dice_type)
        raw_dice_roll_results.append(current_roll)
    # sum & return dice results
    sum_of_dice = sum(raw_dice_roll_results)
    return sum_of_dice, raw_dice_roll_results


def add_to_history(user_input, raw_dice_rolls, final_result):
    roll_history.append(user_input)
    roll_history.append(raw_dice_rolls)
    roll_history.append(final_result)


def display_history():
    # displays the last 10 rolls, thinking a list system?
    if not roll_history:
        print("You haven't rolled anything this session, you should get to that\n")
    else:
        for i in range(0, len(roll_history), 3):
            print(roll_history[i:i + 3])
        print("\n")


def help_func():
    # this code is really simple
    print("Welcome to the help program. type 'exit' at any time to exit the help program.")
    # the while loop works, but wasn't written the best
    the_input = "poopy"
    while the_input != "exit":
        the_input = input("(type exit or help): ")
        if the_input == "help":
            print("~~~")
            print("This program supports several functions, including:")
            print(
                "* Rolling multiple types of dice (d1, d2, d3, d4, d6, d10, d12, d20, d100, and percentile; d%)")
            print("* Rolling multiple dice at a time (2d6, 4d12, etc)")
            print("* Rolling dice with modifiers (d10 + 5, 2d12 - 5, etc)")
            print("* Rolling d20s with advantage/disadvantage (d20a, d20d, d20a + 3)")
            print("* Rolling dice with vulnerability and resistance (d12v, 6d6d, etc)")
            print("* Combinations of what was just said (4d12+1vc, 12d12/6r, etc)")
            print("~~~")
            print(
                "supported effects: critical hits (c), resistance (r), vulnerability (v), advantage (a), disadvantage (d)")
            print("~~~")
            print("This program supports several commands, including:")
            print("<help> - you know what this does, and how you got here presumably")
            print("<history> - print last 10 rolls")
            print("<exit> - exit whatever program you're in")
            print("~~~")
        if the_input == "exit":
            print("\n")
            break


def exit_func():
    # this is the exit function
    print("\nBye")
    exit(0)


def error_func():
    print("That's not a valid roll or command, please try again.\n")
    return 1


def input_func():
    # example input: d20a, 3d12 + 6, d3, coinflip, 8d6 - 1, d20d + 5
    dice_input_str = input("What do you want rolled?: ").lower().strip().replace(" ", "")
    pattern = re.compile(r"(\d+)?d(\d+|%)([ad])?([+\-*/])?(\d+)?([vrc]*)?")
    if dice_input_str == "exit":
        return "exited"
    if dice_input_str == "help":
        return "needs_help"
    if dice_input_str == "history":
        return "history"
    # Regex is really useful but also confusing
    # 1st bit: (\d+)? - group 1: allows for numbers in front of the roll; how many dice
    # 2nd bit: d - literally matches the d character
    # 3rd bit: (\d+|%) - group 2: the dice type, e.g. d20, d6, d%, etc
    # 4th bit: ([ad])? - group 3: optional advantage or disadvantage
    # 5th bit: ([+\-*/])? - group 4: optional modifier operator, e.g. +, -, *, /
    # 6th bit: (\d+)? - group 5: optional modifier value
    # 7th bit: ([vrc]*)? - group 6: optional vulnerability, resistance, critical hit, in any combo
    # Handle '%' before converting to int
    match = pattern.match(dice_input_str)
    if not match:
        return "failed"
    how_many_dice_str, dice_type_str, adv_dis, mod_type, mods_str, vul_res_crit = match.groups()
    if not match:
        return "failed"
    if dice_type_str == '%':
        dice_type_str = 100
    return how_many_dice_str, dice_type_str, adv_dis, mod_type, mods_str, vul_res_crit, dice_input_str


def advantage_disadvantage(sum_of_output, how_many_dice, dice_type, adv_dis):
    if adv_dis == "d":
        if dice_type != 20:
            return "error"
        else:
            roll_again = dice_roller(how_many_dice, dice_type)
            sum_of_output_two = roll_again[0]
            list_of_vantage_rolls = [sum_of_output_two, sum_of_output]
            if sum_of_output_two >= sum_of_output:
                return sum_of_output, list_of_vantage_rolls
            else:
                return sum_of_output_two, list_of_vantage_rolls
    if adv_dis == "a":
        if dice_type != 20:
            return "error"
        else:
            roll_again = dice_roller(how_many_dice, dice_type)
            sum_of_output_two = roll_again[0]
            list_of_vantage_rolls = [sum_of_output_two, sum_of_output]
            if sum_of_output_two <= sum_of_output:
                return sum_of_output, list_of_vantage_rolls
            else:
                return sum_of_output_two, list_of_vantage_rolls
    if adv_dis is None:
        list_of_vantage_rolls = "nothing"
        return sum_of_output, list_of_vantage_rolls
    else:
        list_of_vantage_rolls = "nothing"
        return sum_of_output, list_of_vantage_rolls


def modifiers(premod_output, mod_type, mods_str):
    if mod_type == "*":
        modded_output = int(premod_output) * int(mods_str)
        modded_output = math.floor(modded_output)
        return modded_output
    elif mod_type == "+":
        modded_output = int(premod_output) + int(mods_str)
        return modded_output
    elif mod_type == "-":
        modded_output = int(premod_output) - int(mods_str)
        return modded_output
    elif mod_type == "/":
        modded_output = int(premod_output) // int(mods_str)
        modded_output = math.floor(modded_output)
        return modded_output
    return None


def vulner_resist_critical(modded_output, vul_res_crit, how_many_dice, dice_type):
    crit_results = []
    if "v" in vul_res_crit:
        modded_output = modded_output * 2
    if "r" in vul_res_crit:
        modded_output = modded_output // 2
        modded_output = math.floor(modded_output)
    if "c" in vul_res_crit:
        # critical hits make you roll double dice, so I have to deal with that, grr
        raw_second_crit_roll = dice_roller(how_many_dice, dice_type)
        # this returns sum of rolls, and list of rolls, I want to return both.
        crit_results = [raw_second_crit_roll[0], raw_second_crit_roll[1]]
    return modded_output, crit_results


def main():
    # main function
    print("Welcome to the dice roller")
    print(f"Type 'exit', 'history, or 'help', to get their respective actions\n")
    while True:
        input_results = input_func()
        if input_results == "failed":
            error_func()
            continue
        if input_results == "exited":
            exit_func()
            break
        if input_results == "needs_help":
            help_func()
            continue
        if input_results == "history":
            display_history()
            continue
        how_many_dice_str = input_results[0]
        dice_type_str = input_results[1]
        adv_dis = input_results[2]
        mod_type = input_results[3]
        mods_str = input_results[4]
        vul_res_crit = input_results[5]
        dice_input_str = input_results[6]
        if how_many_dice_str is None:
            how_many_dice_str = "1"
        if dice_type_str is None:
            error_func()
        if mod_type is None:
            mod_type = "+"
            mods_str = 0
        # calls first dice roll
        how_many_dice = int(how_many_dice_str)
        if how_many_dice > 1000:
            print("That can't possibly be a real d&d roll, please roll again\n")
            continue
        dice_type = int(dice_type_str)
        if dice_type > 150:
            print("That's not a real dnd dice, please roll again\n")
            continue
        roll_output = dice_roller(how_many_dice, dice_type)
        sum_of_output = roll_output[0]
        list_of_rolls = roll_output[1]
        # calls advantage and disadvantage stuff next
        second_stage = advantage_disadvantage(sum_of_output, how_many_dice, dice_type, adv_dis)
        if second_stage == "error":
            print("Advantage/Disadvantage only applies to d20 rolls\n")
            error_func()
            continue
        second_stage_winner = second_stage[0]
        vantage_rolls = second_stage[1]
        # now we call any applicable modifiers
        modded_output = modifiers(second_stage_winner, mod_type, mods_str)
        # now we call the last stage with vul resit, crit
        final_effect_result = vulner_resist_critical(modded_output, vul_res_crit, how_many_dice, dice_type)
        final_result = final_effect_result[0]
        crit_results = final_effect_result[1]
        if "c" in vul_res_crit:
            crit_sum = crit_results[0]
            crit_list = crit_results[1]
            if adv_dis is None:
                # if crit happened, I need to add the two lists of rolls, and add the sums
                final_result = crit_sum + final_result
                list_of_rolls = crit_list + list_of_rolls
            else:
                print("You can't roll a critical attack with with advantage or disadvantage (I think?)")
                error_func()
                continue
        print("\nYou rolled:", dice_input_str)
        if how_many_dice > 25:
            print("That's too many raw dice to display, results will display as normal\n")
        else:
            if adv_dis is not None:
                print("Raw rolls:", vantage_rolls)
            else:
                print("Raw rolls:", list_of_rolls)
            print("Final Result:", final_result, "\n")
        if adv_dis is not None:
            add_to_history(dice_input_str, vantage_rolls, final_result)
        else:
            add_to_history(dice_input_str, list_of_rolls, final_result)


if __name__ == "__main__":
    main()
