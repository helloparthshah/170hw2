
Command
python main.py -p1 minimaxAI -p2 stupidAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p1 stupidAI -p2 minimaxAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p1 minimaxAI -p2 randomAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p1 randomAI -p2 minimaxAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p1 minimaxAI -p2 monteCarloAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p1 monteCarloAI -p2 minimaxAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p1 alphaBetaAI -p2 monteCarloAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p1 monteCarloAI -p2 alphaBetaAI -limit_players 1,2 -visualize False -verbose True -seed 0
python main.py -p2 alphaBetaAI -limit_players 2 -visualize True -verbose True
python main.py -p1 alphaBetaAI -limit_players 1 -visualize True -verbose True