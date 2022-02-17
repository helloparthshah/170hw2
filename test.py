import subprocess


def run_stupid(player="minimaxAI"):
    print("Testing Stupid AI")
    count_p1 = 0
    count_p2 = 0
    # Stupid AI
    # print line break
    for i in range(1, 6):
        output = subprocess.check_output(
            "python main.py -p1 "+player + " -p2 stupidAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  1  has won" in output.decode("utf-8"):
            count_p1 += 1
            print("Our Player wins as p1 at seed: " + str(i))
        else:
            print("Our Player loses as p1 at seed: " + str(i))

        output = subprocess.check_output(
            "python main.py -p2 " + player + " -p1 stupidAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  2  has won" in output.decode("utf-8"):
            count_p2 += 1
            print("Our Player wins as p2 at seed: " + str(i))
        else:
            print("Our Player loses as p2 at seed: " + str(i))

    print("Wins As Player 1: " + str(count_p1))
    print("Wins As Player 2: " + str(count_p2))

# Random AI


def run_random(player="minimaxAI"):
    print("Testing Random AI")
    count_p1 = 0
    count_p2 = 0
    for i in range(1, 6):
        output = subprocess.check_output(
            "python main.py -p1 "+player+" -p2 randomAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  1  has won" in output.decode("utf-8"):
            count_p1 += 1
            print("Our Player wins as p1 at seed: " + str(i))
        else:
            print("Our Player loses as p1 at seed: " + str(i))

        output = subprocess.check_output(
            "python main.py -p2 "+player+" -p1 randomAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  2  has won" in output.decode("utf-8"):
            count_p2 += 1
            print("Our Player wins as p2 at seed: " + str(i))
        else:
            print("Our Player loses as p2 at seed: " + str(i))

    print("Wins As Player 1: " + str(count_p1))
    print("Wins As Player 2: " + str(count_p2))

# MonteCarlo AI


def run_monte(player="minimaxAI"):
    print("Testing Monte Carlo AI")
    count_p1 = 0
    count_p2 = 0
    for i in range(1, 11):
        output = subprocess.check_output(
            "python main.py -p1 "+player+" -p2 monteCarloAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  1  has won" in output.decode("utf-8"):
            count_p1 += 1
            print("Our Player wins as p1 at seed: " + str(i))
        elif "The game has tied" in output.decode("utf-8"):
            print("The game has tied as p1 at seed: " + str(i))
        else:
            print("Our Player loses as p1 at seed: " + str(i))

        output = subprocess.check_output(
            "python main.py -p2 "+player+" -p1 monteCarloAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  2  has won" in output.decode("utf-8"):
            count_p2 += 1
            print("Our Player wins as p2 at seed: " + str(i))
        elif "The game has tied" in output.decode("utf-8"):
            print("The game has tied as p2 at seed: " + str(i))
        else:
            print("Our Player loses as p2 at seed: " + str(i))

    print("Wins As Player 1: " + str(count_p1))
    print("Wins As Player 2: " + str(count_p2))


# run_stupid()
# run_random()
run_monte()
run_monte("alphaBetaAI")
