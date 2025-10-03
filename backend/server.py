from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Cricket_analyzer import analyze
from cric import analyze_bowling_stats
from dsa import batter_vs_bowler_graph
from dsa_info import cricket_analysis
from batting_sort import sort_batting_stats

# create app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or ["http://localhost:3000"] for dev
    allow_methods=["*"],
    allow_headers=["*"]
)

# root endpoint
@app.post("/cricket-analysis")
def cricket_analysis_api():
    runs = [0,4,0,0,1,2,"W",0,1,0,0,2,0,0,"W",0,1,1,1,1,2,0,4,"W",0,0,1,0,0,4,0,0,4,6,0,1,0,4,0,0,1,1,1,1,4,1,0,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,6,1,1,1,1,0,0,0,6,0,1,"W",0,0,1,0,1,1,1,0,1,1,4,1,4,1,1,6,6,"WD",1,1,0,1,1,1,1,0,2,1,1,1,"WD",1,1,2,1,6,1,1,1,4,0,"W",2,6,1,4]
    bowlers = ["Shaheen Shah Afridi", "Faheem", "Shaheen Shah Afridi","Faheem","Shaheen Shah Afridi","Faheem","Nawaz","Haris Rauf","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Abrar Ahmed","Saim Ayub","Haris Rauf","Abrar Ahmed","Shaheen Shah Afridi","Haris Rauf","Faheem","Haris Rauf"]
    batters = ["Abhishek Sharma","Shubman Gill","Suryakumar Yadav","Tilak Varma","Sanju Samson","Shivam Dube","Rinku Singh","Axar Patel","Kuldeep Yadav","Varun Chakaravarthy","Jasprit Bumrah"]

    runsB=[0,0,0,0,4,0,"LB1",0,0,2,4,0,1,1,1,1,0,4,4,0,6,1,"B1",1,0,1,0,2,1,1,0,0,1,2,1,4,1,1,1,0,2,6,1,2,0,4,1,0,"WD",1,6,"B1",2,1,1,0,1,6,"W",1,2,1,1,4,0,4,1,1,4,0,1,1,2,"WD",0,1,"WD",2,1,"W",0,0,1,"W",1,1,2,2,0,6,"W",1,1,2,1,"W",0,1,1,"W",0,"WD",0,"W",0,"W",1,4,0,2,"W",0,2,0,0,1,1,1,"W"]
    bowlersB=["Shivam Dube","Jasprit Bumrah","Shivam Dube","Jasprit Bumrah","Varun Chakaravarthy","Axar Patel","Kuldeep Yadav","Axar Patel","Kuldeep Yadav","Varun Chakaravarthy","Shivam Dube","Tilak Varma","Kuldeep Yadav","Axar Patel","Varun Chakaravarthy","Axar Patel","Kuldeep Yadav","Jasprit Bumrah","Varun Chakaravarthy","Jasprit Bumrah"]
    battersB=["Sahibzada Farhan","Fakhar Zaman","Saim Ayub","Mohammad Haris","Salman Ali Agha","Hussain Talt","Mohammad Nawaz","Shaheen Afridi","Faheem Ashraf","Haris Rauf","Abrar Ahmed"]

    batter_info, bowler_info, extras, head = cricket_analysis(runs, bowlers, batters)    
    batterB_info, bowler_infoB, extrasB, headB = cricket_analysis(runsB, bowlersB, battersB) 
    G, extrasss = batter_vs_bowler_graph(runs, bowlers, batters)
    G_B, extrasss = batter_vs_bowler_graph(runsB, bowlersB, battersB)

    # --- Batters ---
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

    # --- Bowlers ---

    bowler_input = []
    for i in bowler_info:
        d={}
        d[i]=bowler_info[i]
        bowler_input.append(d)
    bowler_list = analyze_bowling_stats(bowler_input)
    print(bowler_input)

    # --- Overs summary ---
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

    #Partnerships
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

    #Batter vs Bowler
    result={}
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

    resultB={}
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

    return {
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
        "extras": extras,
        "overs": over_result,
        "batterVsBowler": result,
        "batterVsBowlerB": resultB,
        "partnerships": partnerships,
        "partnershipsB": partnershipsB
        
    }



