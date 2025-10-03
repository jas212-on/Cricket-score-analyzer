import networkx as nx
from collections import deque

def batter_vs_bowler_graph(runs, bowlers, batters):
    """
    Build batter vs bowler analysis graph with cricket rules:
      - Batters stored in queue (FIFO)
      - Bowlers rotate sequentially after each over
      - Handles extras: W, WD, NB, LB, B
    """
    G = nx.DiGraph()
    batter_q = deque(batters)
    striker = batter_q.popleft() if batter_q else None
    non_striker = batter_q.popleft() if batter_q else None

    bowler_idx = 0
    balls_in_over = 0
    current_bowler = bowlers[bowler_idx]

    extras = {"WD": 0, "NB": 0, "LB": 0, "B": 0}

    for ball in runs:
        if striker is None or current_bowler is None:
            break

        # add nodes
        if not G.has_node(striker):
            G.add_node(striker, role="batter")
        if not G.has_node(current_bowler):
            G.add_node(current_bowler, role="bowler")

        # add edge if not exist
        if not G.has_edge(striker, current_bowler):
            G.add_edge(striker, current_bowler, runs=0, balls=0, wickets=0)

        ball_str = str(ball).upper()

        legal_ball = True  # whether this counts towards balls_in_over

        # --- Handle extras and wickets ---
        if ball_str == "W":  # wicket
            G[striker][current_bowler]["balls"] += 1
            G[striker][current_bowler]["wickets"] += 1
            striker = batter_q.popleft() if batter_q else None

        elif ball_str.startswith("WD"):  # wide
            extras["WD"] += 1
            extra_runs = int(ball_str[2:]) if len(ball_str) > 2 else 1
            extras["WD"] += extra_runs - 1
            # Add only to bowler, not batter
            G[striker][current_bowler]["runs"] += 0  # batter gets 0
            legal_ball = False

        elif ball_str.startswith("NB"):  # no-ball
            extras["NB"] += 1
            extra_runs = int(ball_str[2:]) if len(ball_str) > 2 else 0
            if extra_runs > 0:  # runs scored off the bat on NB
                G[striker][current_bowler]["runs"] += extra_runs  # only runs from bat
                if extra_runs % 2 == 1:
                    striker, non_striker = non_striker, striker
            legal_ball = False 

        elif ball_str.startswith("LB"):  # leg bye
            runs_scored = int(ball_str[2:]) if len(ball_str) > 2 else 1
            extras["LB"] += runs_scored
            G[striker][current_bowler]["balls"] += 1
            if runs_scored % 2 == 1:
                striker, non_striker = non_striker, striker

        elif ball_str.startswith("B"):  # bye
            runs_scored = int(ball_str[1:]) if len(ball_str) > 1 else 1
            extras["B"] += runs_scored
            G[striker][current_bowler]["balls"] += 1
            if runs_scored % 2 == 1:
                striker, non_striker = non_striker, striker

        else:  # normal run
            runs_scored = int(ball_str)
            G[striker][current_bowler]["runs"] += runs_scored
            G[striker][current_bowler]["balls"] += 1
            if runs_scored % 2 == 1:
                striker, non_striker = non_striker, striker

        # increment legal balls
        if legal_ball:
            balls_in_over += 1

        # --- Check over end ---
        if balls_in_over == 6:
            bowler_idx = (bowler_idx + 1) % len(bowlers)
            current_bowler = bowlers[bowler_idx]
            balls_in_over = 0
            # swap strike
            striker, non_striker = non_striker, striker

    return G, extras





# runs = ["1", "2", "W", "WD", "NB4", "LB1", "B2", "6", "W"]
# bowlers = ["A", "B", "C"]
# batters = ["D", "E", "F", "G"]

# G, extras = batter_vs_bowler_graph(runs, bowlers, batters)

# print("Extras:", extras)
# for u, v, data in G.edges(data=True):
#     print(f"{u} vs {v} → {data}")


