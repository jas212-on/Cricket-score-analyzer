from collections import deque, defaultdict

class OverNode:
    def __init__(self, over_num, runs, wickets):
        self.over_num = over_num
        self.runs = runs
        self.wickets = wickets
        self.next = None

def cricket_analysis(runs, bowlers, batters):
    batter_queue = deque(batters)
    
    # batter & bowler stats
    batter_info = defaultdict(lambda: {"runs": 0, "balls": 0, "4s": 0, "6s": 0})
    bowler_info = defaultdict(lambda: {"overs": [], "runs": 0, "wickets": 0})
    extras = {"WD": 0, "NB": 0, "LB": 0, "B": 0}
    
    # initialize with two batters
    striker = batter_queue.popleft()
    non_striker = batter_queue.popleft()
    
    head = None
    prev = None
    ball_count = 0
    over_num = 1
    over_runs = 0
    over_wkts = 0
    
    i = 0
    while i < len(runs):
        run = str(runs[i]).upper()
        bowler = bowlers[(over_num - 1) % len(bowlers)]

        legal_delivery = False
        runs_scored = 0

        if ball_count == 0 :
            # At start of each over
            bowler = bowlers[(over_num - 1) % len(bowlers)]
            if over_num not in bowler_info[bowler]["overs"]:
                bowler_info[bowler]["overs"].append(over_num)


        if run == "W":  # Wicket
            batter_info[striker]["balls"] += 1
            bowler_info[bowler]["wickets"] += 1
            over_wkts += 1
            ball_count += 1
            legal_delivery = True

            if batter_queue:
                striker = batter_queue.popleft()
            else:
                break

        elif run.startswith("WD"):  # Wide
            extras["WD"] += 1
            bowler_info[bowler]["runs"] += 1
            over_runs += 1
            if len(run) > 2:
                addl = int(run[2:])
                extras["WD"] += addl
                bowler_info[bowler]["runs"] += addl
                over_runs += addl
            # no ball_count increment

        elif run.startswith("NB"):  # No-ball
            extras["NB"] += 1
            bowler_info[bowler]["runs"] += 1
            over_runs += 1
            if len(run) > 2:
                runs_scored = int(run[2:])
                batter_info[striker]["runs"] += runs_scored
                if runs_scored == 4:
                    batter_info[striker]["4s"] += 1
                elif runs_scored == 6:
                    batter_info[striker]["6s"] += 1
                bowler_info[bowler]["runs"] += runs_scored
                over_runs += runs_scored
                if runs_scored % 2 == 1:
                    striker, non_striker = non_striker, striker
            # no ball_count increment

        elif run.startswith("LB"):  # Leg Bye
            runs_scored = int(run[2:]) if len(run) > 2 else 1
            extras["LB"] += runs_scored
            bowler_info[bowler]["runs"] += runs_scored
            over_runs += runs_scored
            batter_info[striker]["balls"] += 1
            ball_count += 1
            legal_delivery = True
            if runs_scored % 2 == 1:
                striker, non_striker = non_striker, striker

        elif run.startswith("B"):  # Bye
            runs_scored = int(run[1:]) if len(run) > 1 else 1
            extras["B"] += runs_scored
            bowler_info[bowler]["runs"] += runs_scored
            over_runs += runs_scored
            batter_info[striker]["balls"] += 1
            ball_count += 1
            legal_delivery = True
            if runs_scored % 2 == 1:
                striker, non_striker = non_striker, striker

        else:  # Normal run
            runs_scored = int(run)
            batter_info[striker]["runs"] += runs_scored
            batter_info[striker]["balls"] += 1
            if runs_scored == 4:
                batter_info[striker]["4s"] += 1
            elif runs_scored == 6:
                batter_info[striker]["6s"] += 1
            bowler_info[bowler]["runs"] += runs_scored
            over_runs += runs_scored
            ball_count += 1
            legal_delivery = True
            if runs_scored % 2 == 1:
                striker, non_striker = non_striker, striker

        # End of over: every 6 legal balls
        if legal_delivery and ball_count == 6:
            node = OverNode(over_num, over_runs, over_wkts)
            if head is None:
                head = node
            else:
                prev.next = node
            prev = node

            over_num += 1
            ball_count = 0
            over_runs = 0
            over_wkts = 0
            striker, non_striker = non_striker, striker

        i += 1

    # Last incomplete over
    if ball_count > 0:
        node = OverNode(over_num, over_runs, over_wkts)
        if head is None:
            head = node
        else:
            prev.next = node


    
    return dict(batter_info), dict(bowler_info), extras, head






# Example Usage
runs = [0,4,0,0,1,2,"W",0,1,0,0,2,0,0,"W",0,1,1,1,1,2,0,4,"W",0,0,1,0,0,4,0,0,4,6,0,1,0,4,0,0,1,1,1,1,4,1,0,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,6,1,1,1,1,0,0,0,6,0,1,"W",0,0,1,0,1,1,1,0,1,1,4,1,4,1,1,6,6,"WD",1,1,0,1,1,1,1,0,2,1,1,1,"WD",1,1,2,1,6,1,1,1,4,0,"W",2,6,1,4]
bowlers = ["Shaheen Shah Afridi", "Faheem", "Shaheen Shah Afridi","Faheem","Shaheen Shah Afridi","Faheem","Nawaz","Haris Rauf","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Haris Rauf","Abrar Ahmed","Shaheen Shah Afridi","Haris Rauf","Faheem","Haris Rauf"]
batters = ["Abhishek Sharma","Shubman Gill","Suryakumar Yadav","Tilak Varma","Sanju Samson","Shivam Dube","Rinku Singh","Axar Patel","Kuldeep Yadav","Varun Chakaravarthy","Jasprit Bumrah"]

batters_data, bowlers_data,extras, overs_head = cricket_analysis(runs, bowlers, batters)

print("Batters Info:", batters_data)
print("Bowlers Info:", bowlers_data)
print("Extras:", extras)

# # Traverse linked list
# curr = overs_head
# while curr:
#     print(f"Over {curr.over_num}: Runs={curr.runs}, Wickets={curr.wickets}")
#     curr = curr.next
