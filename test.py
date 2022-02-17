import subprocess

def run_stupid():
    print("Testing Stupid AI")
    count_p1 = 0
    count_p2 = 0
    # Stupid AI
    # print line break
    for i in range(1, 6):
        print("Testing Stupid AI seed: " + str(i))
        output = subprocess.check_output(
            "python main.py -p1 minimaxAI -p2 stupidAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  1  has won" in output.decode("utf-8"):
            count_p1 += 1
            print("Our Player wins")
        else:
            print("Our Player loses")

        output = subprocess.check_output(
            "python main.py -p2 minimaxAI -p1 stupidAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  2  has won" in output.decode("utf-8"):
            count_p2 += 1
            print("Our Player wins")
        else:
            print("Our Player loses")

    print("Wins As Player 1: " + str(count_p1))
    print("Wins As Player 2: " + str(count_p2))
    print("\n\n")

# Random AI
def run_random():
    print("Testing Random AI")
    count_p1 = 0
    count_p2 = 0
    for i in range(1, 6):
        print("Testing Random AI seed: " + str(i))
        output = subprocess.check_output(
            "python main.py -p1 minimaxAI -p2 randomAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  1  has won" in output.decode("utf-8"):
            count_p1 += 1
            print("Our Player wins")
        else:
            print("Our Player loses")

        output = subprocess.check_output(
            "python main.py -p2 minimaxAI -p1 randomAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  2  has won" in output.decode("utf-8"):
            count_p2 += 1
            print("Our Player wins")
        else:
            print("Our Player loses")

    print("Wins As Player 1: " + str(count_p1))
    print("Wins As Player 2: " + str(count_p2))
    print("\n\n")

# MonteCarlo AI
def run_monte():
    print("Testing Monte Carlo AI")
    count_p1 = 0
    count_p2 = 0
    for i in range(1, 11):
        output = subprocess.check_output(
            "python main.py -p1 minimaxAI -p2 monteCarloAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  1  has won" in output.decode("utf-8"):
            count_p1 += 1
            print("Our Player wins")
        else:
            print("Our Player loses")

        output = subprocess.check_output(
            "python main.py -p2 minimaxAI -p1 monteCarloAI -limit_players 1,2 -visualize False -seed "+str(i), shell=True)
        if "Player  2  has won" in output.decode("utf-8"):
            count_p2 += 1
            print("Our Player wins")
        else:
            print("Our Player loses")

    print("Wins As Player 1: " + str(count_p1))
    print("Wins As Player 2: " + str(count_p2))
    
run_stupid()
