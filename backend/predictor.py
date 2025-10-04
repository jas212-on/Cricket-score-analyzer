def adjusted_probs_for_batter(batter, bowler,skill,batter_bowler_probs):
    """
    Return a new probs dict shifted by batter skill:
    - If skill < 1, move some mass from scoring outcomes into 'W'.
    - Keeps the distribution normalized.
    """
    base = batter_bowler_probs[batter][bowler].copy()
    s = skill.get(batter, 1.0)
    # scoring outcomes
    run_keys = [0,1,2,3,4,6]
    shifted_mass = 0.0
    newp = {}
    for r in run_keys:
        newp[r] = base[r] * s
        shifted_mass += base[r] * (1.0 - s)
    # add shifted mass to wicket probability
    newp['W'] = base['W'] + shifted_mass
    # normalize (in case rounding)
    total = sum(newp.values())
    for k in list(newp.keys()):
        newp[k] /= total
    return newp

# DFS using adjusted probs (no final multiplicative wicket factor)
def dfs_win_prob(runs_left, balls_left, wickets_left, striker_idx, non_striker_idx, bowler_idx,bowlers,batters,batter_bowler_probs,skill,memo):
    if runs_left <= 0:
        return 1.0
    if balls_left == 0 or wickets_left == 0:
        return 0.0

    key = (runs_left, balls_left, wickets_left, striker_idx, non_striker_idx, bowler_idx)
    if key in memo:
        return memo[key]

    prob = 0.0
    striker = batters[striker_idx]
    bowler = bowlers[bowler_idx % len(bowlers)]
    probs = adjusted_probs_for_batter(striker, bowler,skill,batter_bowler_probs)

    for outcome, p in probs.items():
        next_runs_left = runs_left
        next_wickets_left = wickets_left
        next_striker = striker_idx
        next_non_striker = non_striker_idx
        next_balls_left = balls_left - 1

        if outcome == 'W':
            next_wickets_left -= 1
            if next_wickets_left > 0 and striker_idx + 1 < len(batters):
                next_striker = striker_idx + 1
        else:
            next_runs_left = max(0, runs_left - outcome)
            if outcome % 2 == 1:
                next_striker, next_non_striker = next_non_striker, next_striker

        next_bowler_idx = bowler_idx  # keep same in-DFS; rotation handled outside

        prob += p * dfs_win_prob(next_runs_left, next_balls_left, next_wickets_left,
                                 next_striker, next_non_striker, next_bowler_idx,bowlers,batters,batter_bowler_probs,skill,memo)

    memo[key] = prob
    return prob


# Function to get run value and balls consumed
def parse_ball(run):
    """
    Returns (runs_scored, balls_consumed)
    """
    if isinstance(run,int):
        return run,1
    run = str(run)
    if run.startswith("LB"):
        # Leg bye or bye, counts as runs but ball is counted
        return int(run[2:]),1
    if run.startswith("B"):
        return int(run[1:]),1
    if run == "WD":
        return 1,0  # wide: +1 run, ball not counted
    if run == "NB":
        return 1,0  # no ball: +1 run, ball not counted
    if run == "W":
        return 0,1  # wicket, ball counted
    return int(run),1  # fallback for numeric string


# ------------------------------
# Simulate match ball by ball and print after each over
# ------------------------------



def predict(runs, batters, bowlers, target_runs, total_overs,batter_bowler_probs,skill,memo):
    balls_bowled = 0
    current_score = 0
    wickets_fallen = 0
    striker_idx = 0
    non_striker_idx = 1
    bowler_idx = 0
    predictingData=[]

    print("Over\tScore\tWickets\tWinProb%")
    for run in runs:
        run_value, ball_count = parse_ball(run)
        
        if run=="W":
            wickets_fallen +=1
            if striker_idx+1 < len(batters):
                striker_idx +=1
        else:
            current_score += run_value
            if run_value %2 ==1:
                striker_idx, non_striker_idx = non_striker_idx, striker_idx
        
        balls_bowled += ball_count
        
        # after each over
        if balls_bowled %6 ==0 or balls_bowled>114:
            balls_left = total_overs*6 - balls_bowled
            wickets_left = 10 - wickets_fallen
            runs_left = target_runs - current_score
            memo.clear()
            prob = dfs_win_prob(runs_left, balls_left, wickets_left, striker_idx, non_striker_idx, bowler_idx,bowlers,batters,batter_bowler_probs,skill,memo)
            data={
            "over": balls_bowled//6,
            "teamBScore": current_score,
            "teamBWickets": wickets_fallen,
            "teamBWinProb": prob*100,
            "teamAWinProb": 100-prob*100
            }
            if balls_bowled>114:
                data["over"] = float(str(balls_bowled//6)+"."+str(balls_bowled%6))
            predictingData.append(data)
            print(f"{balls_bowled//6}\t{current_score}\t{wickets_fallen}\t{prob*100:.2f}%")
            bowler_idx +=1  # rotate bowler each over
    return predictingData
    


# runs=[0,0,0,0,4,0,"LB1",0,0,2,4,0,1,1,1,1,0,4,4,0,6,1,"B1",1,0,1,0,2,1,1,0,0,1,2,1,4,1,1,1,0,2,6,1,2,0,4,1,0,"WD",1,6,"B1",2,1,1,0,1,6,"W",1,2,1,1,4,0,4,1,1,4,0,1,1,2,"WD",0,1,"WD",2,1,"W",0,0,1,"W",1,1,2,2,0,6,"W",1,1,2,1,"W",0,1,1,"W",0,"WD",0,"W",0,"W",1,4,0,2,"W",0,2,0,0,1,1,1,"W"]
# bowlers=["Shivam Dube","Jasprit Bumrah","Shivam Dube","Jasprit Bumrah","Varun Chakaravarthy","Axar Patel","Kuldeep Yadav","Axar Patel","Kuldeep Yadav","Varun Chakaravarthy","Shivam Dube","Tilak Varma","Kuldeep Yadav","Axar Patel","Varun Chakaravarthy","Axar Patel","Kuldeep Yadav","Jasprit Bumrah","Varun Chakaravarthy","Jasprit Bumrah"]
# batters=["Sahibzada Farhan","Fakhar Zaman","Saim Ayub","Mohammad Haris","Salman Ali Agha","Hussain Talt","Mohammad Nawaz","Shaheen Afridi","Faheem Ashraf","Haris Rauf","Abrar Ahmed"]
# target_runs = 150
# total_overs = 20

runs = [0,4,0,0,1,2,"W",0,1,0,0,2,0,0,"W",0,1,1,1,1,2,0,4,"W",0,0,1,0,0,4,0,0,4,6,0,1,0,4,0,0,1,1,1,1,4,1,0,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,6,1,1,1,1,0,0,0,6,0,1,"W",0,0,1,0,1,1,1,0,1,1,4,1,4,1,1,6,6,"WD",1,1,0,1,1,1,1,0,2,1,1,1,"WD",1,1,2,1,6,1,1,1,4,0,"W",2,6,1,4]
bowlers = ["Shaheen Shah Afridi", "Faheem", "Shaheen Shah Afridi","Faheem","Shaheen Shah Afridi","Faheem","Nawaz","Haris Rauf","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Haris Rauf","Abrar Ahmed","Shaheen Shah Afridi","Haris Rauf","Faheem","Haris Rauf"]
batters = ["Abhishek Sharma","Shubman Gill","Suryakumar Yadav","Tilak Varma","Sanju Samson","Shivam Dube","Rinku Singh",]
target_runs=146
total_overs=20

# ------------------------------
# Batter vs Bowler Probabilities
# ------------------------------


# batter_bowler_probs = {
#     "Sahibzada Farhan": {
#         "Shivam Dube": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.28,1:0.27,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Axar Patel": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Fakhar Zaman": {
#         "Shivam Dube": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.10,'W':0.06},
#         "Jasprit Bumrah": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Axar Patel": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.30,6:0.05,'W':0.08},
#         "Kuldeep Yadav": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.10,'W':0.06},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Saim Ayub": {
#         "Shivam Dube": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.25,2:0.05,3:0.02,4:0.30,6:0.05,'W':0.08},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Mohammad Haris": {
#         "Shivam Dube": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Salman Ali Agha": {
#         "Shivam Dube": {0:0.28,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.07},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     # You can continue in this same pattern for remaining batters:
#     "Hussain Talt": {
#         "Shivam Dube": {0:0.28,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.07},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Mohammad Nawaz": {
#         "Shivam Dube": {0:0.28,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.07},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Shaheen Afridi": {
#         "Shivam Dube": {0:0.28,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.07},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Faheem Ashraf": {
#         "Shivam Dube": {0:0.28,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.07},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Haris Rauf": {
#         "Shivam Dube": {0:0.28,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.07},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     },
#     "Abrar Ahmed": {
#         "Shivam Dube": {0:0.28,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.07},
#         "Jasprit Bumrah": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Varun Chakaravarthy": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Axar Patel": {0:0.25,1:0.28,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.10},
#         "Kuldeep Yadav": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
#         "Tilak Varma": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08}
#     }
# }


# ------------------------------
# DFS + Memoization Function
# ------------------------------
# Example skill (1.0 = normal, <1 weaker)


# skill = {
#     # Top order
#     "Sahibzada Farhan": 0.90,   # opener, decent hitter
#     "Fakhar Zaman": 1.0,        # senior opener, aggressive, strong
#     "Saim Ayub": 0.90,          # young top-order, good stroke player
#     "Mohammad Haris": 0.95,     # attacking wicketkeeper-batter

#     # Middle order
#     "Salman Ali Agha": 0.85,    # reliable but less explosive
#     "Hussain Talt": 0.80,       # utility batter, moderate hitter
#     "Mohammad Nawaz": 0.75,     # all-rounder, can bat but inconsistent

#     # Lower order / bowlers
#     "Shaheen Afridi": 0.60,     # tail-ender, can hit a few but unreliable
#     "Faheem Ashraf": 0.70,      # bowling all-rounder, a bit better than Shaheen
#     "Haris Rauf": 0.55,         # mostly bowler, weak batting
#     "Abrar Ahmed": 0.50         # pure bowler, tail-end
# }


# print(predict(runs,batters,bowlers,target_runs,20,batter_bowler_probs,skill,{}))
