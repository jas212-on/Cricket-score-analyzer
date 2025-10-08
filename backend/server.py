from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Cricket_analyzer import analyze
from predictor import predict
from cric import analyze_bowling_stats
from dsa import batter_vs_bowler_graph
from dsa_info import cricket_analysis
from batting_sort import sort_batting_stats

# Import all DSA 2.0 functions
from dsa2 import (
    find_weakest_bowler_per_batter,
    find_strongest_bowler_per_batter,
    calculate_bowler_centrality,
    optimal_bowler_assignment,
    OverAnalyzer,
    PlayerStatsBST,
    PlayerTrie,
    optimal_bowling_allocation,
    detect_scoring_patterns,
    detect_duplicate_overs,
    cluster_batters_by_common_dismissals,
    BowlerScheduler
)

# create app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "FastAPI backend is running!"}


# root endpoint
@app.post("/cricket-analysis")
def cricket_analysis_api():
    runs = [0,4,0,0,1,2,"W",0,1,0,0,2,0,0,"W",0,1,1,1,1,2,0,4,"W",0,0,1,0,0,4,0,0,4,6,0,1,0,4,0,0,1,1,1,1,4,1,0,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,6,1,1,1,1,0,0,0,6,0,1,"W",0,0,1,0,1,1,1,0,1,1,4,1,4,1,1,6,6,"WD",1,1,0,1,1,1,1,0,2,1,1,1,"WD",1,1,2,1,6,1,1,1,4,0,"W",2,6,1,4]
    bowlers = ["Shaheen Shah Afridi", "Faheem", "Shaheen Shah Afridi","Faheem","Shaheen Shah Afridi","Faheem","Nawaz","Haris Rauf","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Haris Rauf","Abrar Ahmed","Shaheen Shah Afridi","Haris Rauf","Faheem","Haris Rauf"]
    batters = ["Abhishek Sharma","Shubman Gill","Suryakumar Yadav","Tilak Varma","Sanju Samson","Shivam Dube","Rinku Singh","Axar Patel","Kuldeep Yadav","Varun Chakaravarthy","Jasprit Bumrah"]

    runsB=[0,0,0,0,4,0,"LB1",0,0,2,4,0,1,1,1,1,0,4,4,0,6,1,"B1",1,0,1,0,2,1,1,0,0,1,2,1,4,1,1,1,0,2,6,1,2,0,4,1,0,"WD",1,6,"B1",2,1,1,0,1,6,"W",1,2,1,1,4,0,4,1,1,4,0,1,1,2,"WD",0,1,"WD",2,1,"W",0,0,1,"W",1,1,2,2,0,6,"W",1,1,2,1,"W",0,1,1,"W",0,"WD",0,"W",0,"W",1,4,0,2,"W",0,2,0,0,1,1,1,"W"]
    bowlersB=["Shivam Dube","Jasprit Bumrah","Shivam Dube","Jasprit Bumrah","Varun Chakaravarthy","Axar Patel","Kuldeep Yadav","Axar Patel","Kuldeep Yadav","Varun Chakaravarthy","Shivam Dube","Tilak Varma","Kuldeep Yadav","Axar Patel","Varun Chakaravarthy","Axar Patel","Kuldeep Yadav","Jasprit Bumrah","Varun Chakaravarthy","Jasprit Bumrah"]
    battersB=["Sahibzada Farhan","Fakhar Zaman","Saim Ayub","Mohammad Haris","Salman Ali Agha","Hussain Talt","Mohammad Nawaz","Shaheen Afridi","Faheem Ashraf","Haris Rauf","Abrar Ahmed"]

    batter_bowler_probs = {
    "Abhishek Sharma": {
        "Shaheen Shah Afridi": {0:0.30,1:0.25,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.28,1:0.27,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Nawaz": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Shubman Gill": {
        "Shaheen Shah Afridi": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.20,1:0.35,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Nawaz": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Suryakumar Yadav": {
        "Shaheen Shah Afridi": {0:0.20,1:0.25,2:0.05,3:0.05,4:0.25,6:0.10,'W':0.10},
        "Faheem": {0:0.22,1:0.25,2:0.05,3:0.05,4:0.25,6:0.08,'W':0.10},
        "Haris Rauf": {0:0.20,1:0.25,2:0.05,3:0.05,4:0.25,6:0.10,'W':0.10},
        "Nawaz": {0:0.20,1:0.25,2:0.05,3:0.05,4:0.25,6:0.10,'W':0.10},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Tilak Varma": {
        "Shaheen Shah Afridi": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Nawaz": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Sanju Samson": {
        "Shaheen Shah Afridi": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.10,'W':0.08},
        "Faheem": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.10,'W':0.08},
        "Haris Rauf": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.10,'W':0.08},
        "Nawaz": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.10,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Shivam Dube": {
        "Shaheen Shah Afridi": {0:0.20,1:0.20,2:0.05,3:0.02,4:0.25,6:0.20,'W':0.08},
        "Faheem": {0:0.20,1:0.20,2:0.05,3:0.02,4:0.25,6:0.20,'W':0.08},
        "Haris Rauf": {0:0.20,1:0.20,2:0.05,3:0.02,4:0.25,6:0.20,'W':0.08},
        "Nawaz": {0:0.20,1:0.20,2:0.05,3:0.02,4:0.25,6:0.20,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Rinku Singh": {
        "Shaheen Shah Afridi": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Nawaz": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Axar Patel":{
        "Shaheen Shah Afridi": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Nawaz": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Kuldeep Yadav":{
        "Shaheen Shah Afridi": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Nawaz": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Varun Chakaravarthy":{
        "Shaheen Shah Afridi": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Nawaz": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    },
    "Jasprit Bumrah":{
        "Shaheen Shah Afridi": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Faheem": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Haris Rauf": {0:0.22,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Nawaz": {0:0.25,1:0.30,2:0.05,3:0.02,4:0.25,6:0.05,'W':0.08},
        "Abrar Ahmed": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08},
        "Saim Ayub": {0:0.20,1:0.30,2:0.05,3:0.02,4:0.25,6:0.08,'W':0.08}
    }
    }

    skill = {
    "Abhishek Sharma": 1.0,
    "Shubman Gill": 1.0,
    "Suryakumar Yadav": 1.0,
    "Tilak Varma": 0.95,
    "Sanju Samson": 1.0,
    "Shivam Dube": 0.95,
    "Rinku Singh": 0.90,
    "Axar Patel": 0.7,
    "Kuldeep Yadav": 0.65,
    "Varun Chakaravarthy": 0.6,
    "Jasprit Bumrah": 0.6
    }

    predictingdata = predict(runs, batters, bowlers, 147, 20, batter_bowler_probs, skill, {})

    batter_info, bowler_info, extras, head = cricket_analysis(runs, bowlers, batters)    
    batterB_info, bowler_infoB, extrasB, headB = cricket_analysis(runsB, bowlersB, battersB) 
    G, extrasss = batter_vs_bowler_graph(runs, bowlers, batters)
    G_B, extrasss_B = batter_vs_bowler_graph(runsB, bowlersB, battersB)

    # =============================================================================
    # DSA 2.0 FUNCTIONS - GRAPH ALGORITHMS
    # =============================================================================
    
    # 1. Matchup Analysis (Team A)
    weakest_bowlers_teamA = find_weakest_bowler_per_batter(G)
    strongest_bowlers_teamA = find_strongest_bowler_per_batter(G)
    bowler_centrality_teamA = calculate_bowler_centrality(G)
    
    # Matchup Analysis (Team B)
    weakest_bowlers_teamB = find_weakest_bowler_per_batter(G_B)
    strongest_bowlers_teamB = find_strongest_bowler_per_batter(G_B)
    bowler_centrality_teamB = calculate_bowler_centrality(G_B)
    
    # Optimal bowler assignment for top batters
    top_batters_teamA = ["Abhishek Sharma", "Shubman Gill", "Suryakumar Yadav"]
    optimal_assignment_teamA = optimal_bowler_assignment(G, top_batters_teamA)
    
    top_batters_teamB = ["Sahibzada Farhan", "Fakhar Zaman", "Saim Ayub"]
    optimal_assignment_teamB = optimal_bowler_assignment(G_B, top_batters_teamB)

    # =============================================================================
    # DSA 2.0 FUNCTIONS - SLIDING WINDOW & OVERS ANALYSIS
    # =============================================================================
    
    # Prefix sums for Team A
    prefix_runs_A, prefix_wickets_A = OverAnalyzer.build_prefix_sums(head)
    
    # Best powerplay (6 overs)
    best_powerplay_teamA = OverAnalyzer.best_k_consecutive_overs(head, 6)
    best_middle_overs_teamA = OverAnalyzer.best_k_consecutive_overs(head, 4)
    
    # Rolling run rate
    rolling_rr_teamA = OverAnalyzer.rolling_run_rate(head, window_size=6)
    
    # Same for Team B
    prefix_runs_B, prefix_wickets_B = OverAnalyzer.build_prefix_sums(headB)
    best_powerplay_teamB = OverAnalyzer.best_k_consecutive_overs(headB, 6)
    best_middle_overs_teamB = OverAnalyzer.best_k_consecutive_overs(headB, 4)
    rolling_rr_teamB = OverAnalyzer.rolling_run_rate(headB, window_size=6)

    # =============================================================================
    # DSA 2.0 FUNCTIONS - BST FOR PLAYER STATS
    # =============================================================================
    
    # Build BST for Team A batters
    bst_teamA = PlayerStatsBST()
    for player, stats in batter_info.items():
        bst_teamA.insert(player, stats["runs"])
    
    # Find batters with 30+ runs
    batters_above_30_teamA = bst_teamA.find_first_above_threshold(30)
    batters_above_50_teamA = bst_teamA.find_first_above_threshold(50)
    
    # Build BST for Team B batters
    bst_teamB = PlayerStatsBST()
    for player, stats in batterB_info.items():
        bst_teamB.insert(player, stats["runs"])
    
    batters_above_30_teamB = bst_teamB.find_first_above_threshold(30)
    batters_above_50_teamB = bst_teamB.find_first_above_threshold(50)

    # =============================================================================
    # DSA 2.0 FUNCTIONS - TRIE FOR PLAYER SEARCH
    # =============================================================================
    
    # Build Trie for all players
    player_trie = PlayerTrie()
    all_players = list(batter_info.keys()) + list(bowler_info.keys()) + \
                  list(batterB_info.keys()) + list(bowler_infoB.keys())
    
    for player in set(all_players):
        player_trie.insert(player)
    
    # Example autocomplete searches
    search_results_s = player_trie.search("s")
    search_results_shah = player_trie.search("shah")
    search_results_ab = player_trie.search("ab")

    # =============================================================================
    # DSA 2.0 FUNCTIONS - DYNAMIC PROGRAMMING
    # =============================================================================
    
    # Prepare bowler data for DP allocation (Team A bowlers)
    bowlers_for_dp_A = []
    for bowler, stats in bowler_info.items():
        overs = len(stats["overs"])
        economy = stats["runs"] / overs if overs > 0 else 0
        bowlers_for_dp_A.append({"name": bowler, "economy": economy})
    
    # Optimal allocation for remaining overs
    optimal_allocation_teamA = optimal_bowling_allocation(bowlers_for_dp_A, 4, 20)
    
    # Same for Team B
    bowlers_for_dp_B = []
    for bowler, stats in bowler_infoB.items():
        overs = len(stats["overs"])
        economy = stats["runs"] / overs if overs > 0 else 0
        bowlers_for_dp_B.append({"name": bowler, "economy": economy})
    
    optimal_allocation_teamB = optimal_bowling_allocation(bowlers_for_dp_B, 4, 20)

    # =============================================================================
    # DSA 2.0 FUNCTIONS - HASHING & PATTERN DETECTION
    # =============================================================================
    
    # Detect scoring patterns
    scoring_patterns_teamA = detect_scoring_patterns(runs, pattern_length=4)
    scoring_patterns_teamB = detect_scoring_patterns(runsB, pattern_length=4)
    
    # Detect duplicate overs
    duplicate_overs_teamA = detect_duplicate_overs(head)
    duplicate_overs_teamB = detect_duplicate_overs(headB)

    # =============================================================================
    # DSA 2.0 FUNCTIONS - UNION-FIND (DSU)
    # =============================================================================
    
    # Cluster batters by dismissal patterns
    batter_clusters_teamA = cluster_batters_by_common_dismissals(G)
    batter_clusters_teamB = cluster_batters_by_common_dismissals(G_B)

    # =============================================================================
    # DSA 2.0 FUNCTIONS - PRIORITY QUEUE SCHEDULING
    # =============================================================================
    
    # Create bowler scheduler for Team A
    bowlers_schedule_data_A = []
    for bowler, stats in bowler_info.items():
        overs_bowled = len(stats["overs"])
        economy = stats["runs"] / overs_bowled if overs_bowled > 0 else 0
        bowlers_schedule_data_A.append({
            "name": bowler,
            "economy": economy,
            "wickets": stats["wickets"],
            "overs_left": 4 - overs_bowled
        })
    
    scheduler_A = BowlerScheduler(bowlers_schedule_data_A)
    next_bowler_teamA = scheduler_A.get_next_bowler()
    
    # Same for Team B
    bowlers_schedule_data_B = []
    for bowler, stats in bowler_infoB.items():
        overs_bowled = len(stats["overs"])
        economy = stats["runs"] / overs_bowled if overs_bowled > 0 else 0
        bowlers_schedule_data_B.append({
            "name": bowler,
            "economy": economy,
            "wickets": stats["wickets"],
            "overs_left": 4 - overs_bowled
        })
    
    scheduler_B = BowlerScheduler(bowlers_schedule_data_B)
    next_bowler_teamB = scheduler_B.get_next_bowler()

    # =============================================================================
    # ORIGINAL CODE - BATTERS
    # =============================================================================
    
    batter_list = []
    for player, stats in batter_info.items():
        balls = stats["balls"]
        sr = round((stats["runs"] / balls) * 100, 1) if balls > 0 else 0.0
        batter_list.append({
            "player": player,
            "runs": stats["runs"],
            "balls": balls,
            "sr": sr,
            "fours": stats["4s"],
            "sixes": stats["6s"]
        })

    batterB_list = []
    for player, stats in batterB_info.items():
        balls = stats["balls"]
        sr = round((stats["runs"] / balls) * 100, 1) if balls > 0 else 0.0
        batterB_list.append({
            "player": player,
            "runs": stats["runs"],
            "balls": balls,
            "sr": sr,
            "fours": stats["4s"],
            "sixes": stats["6s"]
        })

    sorted_batters_teamA = sort_batting_stats(batter_list)
    sorted_batters_teamB = sort_batting_stats(batterB_list)

    # =============================================================================
    # ORIGINAL CODE - BOWLERS
    # =============================================================================
   
    bowler_list = analyze_bowling_stats(bowler_info)
    bowler_listB = analyze_bowling_stats(bowler_infoB)

    # =============================================================================
    # ORIGINAL CODE - OVERS
    # =============================================================================
    
    overs = []
    temp = head
    while temp:
        overs.append({
            "over": temp.over_num,
            "runs": temp.runs,
            "wickets": temp.wickets
        })
        temp = temp.next

    oversB = []
    temp = headB
    while temp:
        oversB.append({
            "over": temp.over_num,
            "runs": temp.runs,
            "wickets": temp.wickets
        })
        temp = temp.next

    over_result = []
    for a, b in zip(oversB, overs):
        over_result.append({
            "over": str(a["over"]),
            "teamA": a["runs"],
            "teamAWickets": a["wickets"],
            "teamB": b["runs"],
            "teamBWickets": b["wickets"]
        })

    # =============================================================================
    # ORIGINAL CODE - PARTNERSHIPS
    # =============================================================================
    
    partnerships, o = analyze(runs, batters)
    partnershipsB, ob = analyze(runsB, battersB)

    pair_names, pair_runs, pair_balls = partnerships.display()
    pair_namesB, pair_runsB, pair_ballsB = partnershipsB.display()
    partnerships = [
    {
        "batsmen": pair.replace("-", " & "),
        "runs": pair_runs[i],
        "balls": pair_balls[i]
    }
    for i, pair in enumerate(pair_names)
    ]

    partnershipsB = [
    {
        "batsmen": pair.replace("-", " & "),
        "runs": pair_runsB[i],
        "balls": pair_ballsB[i]
    }
    for i, pair in enumerate(pair_namesB)
    ]

    # =============================================================================
    # ORIGINAL CODE - BATTER VS BOWLER
    # =============================================================================
    
    result = {}
    for striker in G.nodes:
        if G.nodes[striker].get("role") != "batter":
            continue

        result[striker] = []
        for bowler in G[striker]:
            data = G[striker][bowler]
            balls = data.get("balls", 0)
            runs = data.get("runs", 0)
            wickets = data.get("wickets", 0)
            sr = round((runs / balls * 100), 1) if balls > 0 else 0.0

            result[striker].append({
                "bowler": bowler,
                "runs": runs,
                "balls": balls,
                "wicket": wickets > 0,
                "sr": sr
            })

    resultB = {}
    for striker in G_B.nodes:
        if G_B.nodes[striker].get("role") != "batter":
            continue

        resultB[striker] = []
        for bowler in G_B[striker]:
            data = G_B[striker][bowler]
            balls = data.get("balls", 0)
            runs = data.get("runs", 0)
            wickets = data.get("wickets", 0)
            sr = round((runs / balls * 100), 1) if balls > 0 else 0.0

            resultB[striker].append({
                "bowler": bowler,
                "runs": runs,
                "balls": balls,
                "wicket": wickets > 0,
                "sr": sr
            })

    # =============================================================================
    # RETURN ALL DATA INCLUDING DSA 2.0 RESULTS
    # =============================================================================
    
    return {
        # Original data
        "batters": batter_list,
        "battersB": batterB_list,

        "batters_sorted_runs": sorted_batters_teamA["sorted_by_runs"],
        "batters_sorted_sr": sorted_batters_teamA["sorted_by_sr"],
        "batters_sorted_fours": sorted_batters_teamA["sorted_by_fours"],
        "batters_sorted_sixes": sorted_batters_teamA["sorted_by_sixes"],

        "battersB_sorted_runs": sorted_batters_teamB["sorted_by_runs"],
        "battersB_sorted_sr": sorted_batters_teamB["sorted_by_sr"],
        "battersB_sorted_fours": sorted_batters_teamB["sorted_by_fours"],
        "battersB_sorted_sixes": sorted_batters_teamB["sorted_by_sixes"],
        
        "bowlers_wickets": bowler_list["sorted_by_wickets"],
        "bowlers_runs": bowler_list["sorted_by_runs"],
        "bowlers_economy": bowler_list["sorted_by_economy"],
        "bowlers_wicketsB": bowler_listB["sorted_by_wickets"],
        "bowlers_runsB": bowler_listB["sorted_by_runs"],
        "bowlers_economyB": bowler_listB["sorted_by_economy"],
        
        "extras": extras,
        "overs": over_result,
        "batterVsBowler": result,
        "batterVsBowlerB": resultB,
        "partnerships": partnerships,
        "partnershipsB": partnershipsB,
        "predictingData": predictingdata,
        
        # DSA 2.0 - Graph Algorithms
        "graph_analysis": {
            "teamA": {
                "weakest_bowler_matchups": weakest_bowlers_teamA,
                "strongest_bowler_matchups": strongest_bowlers_teamA,
                "bowler_centrality": bowler_centrality_teamA,
                "optimal_assignment": optimal_assignment_teamA
            },
            "teamB": {
                "weakest_bowler_matchups": weakest_bowlers_teamB,
                "strongest_bowler_matchups": strongest_bowlers_teamB,
                "bowler_centrality": bowler_centrality_teamB,
                "optimal_assignment": optimal_assignment_teamB
            }
        },
        
        # DSA 2.0 - Sliding Window & Overs Analysis
        "over_analysis": {
            "teamA": {
                "best_powerplay": best_powerplay_teamA,
                "best_middle_overs": best_middle_overs_teamA,
                "rolling_run_rate": rolling_rr_teamA,
                "prefix_runs": prefix_runs_A,
                "prefix_wickets": prefix_wickets_A
            },
            "teamB": {
                "best_powerplay": best_powerplay_teamB,
                "best_middle_overs": best_middle_overs_teamB,
                "rolling_run_rate": rolling_rr_teamB,
                "prefix_runs": prefix_runs_B,
                "prefix_wickets": prefix_wickets_B
            }
        },
        
        # DSA 2.0 - BST Search Results
        "bst_search": {
            "teamA": {
                "batters_above_30": batters_above_30_teamA,
                "batters_above_50": batters_above_50_teamA
            },
            "teamB": {
                "batters_above_30": batters_above_30_teamB,
                "batters_above_50": batters_above_50_teamB
            }
        },
        
        # DSA 2.0 - Trie Autocomplete
        "player_search": {
            "search_s": search_results_s,
            "search_shah": search_results_shah,
            "search_ab": search_results_ab
        },
        
        # DSA 2.0 - Dynamic Programming
        "optimal_bowling_allocation": {
            "teamA": optimal_allocation_teamA,
            "teamB": optimal_allocation_teamB
        },
        
        # DSA 2.0 - Pattern Detection
        "pattern_detection": {
            "teamA": {
                "scoring_patterns": scoring_patterns_teamA,
                "duplicate_overs": duplicate_overs_teamA
            },
            "teamB": {
                "scoring_patterns": scoring_patterns_teamB,
                "duplicate_overs": duplicate_overs_teamB
            }
        },
        
        # DSA 2.0 - Union-Find Clusters
        "batter_clusters": {
            "teamA": batter_clusters_teamA,
            "teamB": batter_clusters_teamB
        },
        
        # DSA 2.0 - Priority Queue Scheduling
        "next_bowler_recommendation": {
            "teamA": next_bowler_teamA,
            "teamB": next_bowler_teamB
        }
    }