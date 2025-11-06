import heapq

def analyze_bowling_stats(bowlers_data):
    """
    Analyze bowling statistics using heaps
    
    Args:
        bowlers_data: Dictionary with structure:
                     {'bowler_name': {'overs': [1,2,4], 'runs': 20, 'wickets': 2}, ...}
    
    Returns:
        Dictionary containing sorted lists by different metrics
    """
    
    # Heaps for different metrics
    # Python heapq is min-heap, so negate values for max-heap behavior
    economy_heap = []  # Min heap for economy (ascending)
    runs_heap = []     # Min heap for runs (ascending)
    wickets_heap = []  # Max heap for wickets (descending - negate values)
    
    results = {}
    
    # Process each bowler
    for bowler_name, stats in bowlers_data.items():
        overs = stats['overs']
        runs = stats['runs']
        wickets = stats['wickets']
        
        # Calculate total overs bowled
        total_overs = len(overs)
        
        # Calculate economy rate (runs per over)
        if total_overs > 0:
            economy = runs / total_overs
        else:
            economy = 0
        
        # Push to heaps
        # Economy heap - Min heap (ascending order - best economy first)
        heapq.heappush(economy_heap, (economy, bowler_name, runs, wickets, total_overs))
        
        # Runs heap - Min heap (ascending order - least runs first)
        heapq.heappush(runs_heap, (runs, bowler_name, economy, wickets, total_overs))
        
        # Wickets heap - Max heap (descending order - most wickets first)
        heapq.heappush(wickets_heap, (-wickets, bowler_name, economy, runs, total_overs))
    
    # i) Sort by Economy (Ascending)
    sorted_by_economy = []
    temp_heap = economy_heap.copy()
    while temp_heap:
        economy, name, runs, wickets, overs = heapq.heappop(temp_heap)
        sorted_by_economy.append({
            'name': name,
            'economy': economy,
            'runs': runs,
            'wickets': wickets,
            'overs': overs
        })
    results['sorted_by_economy'] = sorted_by_economy
    
    # ii) Sort by Runs (Ascending)
    sorted_by_runs = []
    temp_heap = runs_heap.copy()
    while temp_heap:
        runs, name, economy, wickets, overs = heapq.heappop(temp_heap)
        sorted_by_runs.append({
            'name': name,
            'runs': runs,
            'economy': economy,
            'wickets': wickets,
            'overs': overs
        })
    results['sorted_by_runs'] = sorted_by_runs
    
    # iii) Sort by Wickets (Descending)
    sorted_by_wickets = []
    temp_heap = wickets_heap.copy()
    while temp_heap:
        neg_wickets, name, economy, runs, overs = heapq.heappop(temp_heap)
        sorted_by_wickets.append({
            'name': name,
            'wickets': -neg_wickets,
            'economy': economy,
            'runs': runs,
            'overs': overs
        })
    results['sorted_by_wickets'] = sorted_by_wickets
    
    return results


def print_results(results):
    """Pretty print the analysis results"""
    
    print("=" * 70)
    print("BOWLING STATISTICS ANALYSIS")
    print("=" * 70)
    
    # i) Players sorted by Economy (Ascending order - Best economy first)
    print("\ni) PLAYERS SORTED BY ECONOMY (Ascending Order - Best First):")
    print(f"   {'Rank':<6} {'Bowler':<20} {'Economy':<10} {'Runs':<8} {'Wickets':<10} {'Overs':<8}")
    print("   " + "-" * 72)
    for i, player in enumerate(results['sorted_by_economy'], 1):
        print(f"   {i:<6} {player['name']:<20} {player['economy']:<10.2f} "
              f"{player['runs']:<8} {player['wickets']:<10} {player['overs']:<8}")
    
    # ii) Players sorted by Runs (Ascending order - Least runs first)
    print("\n\nii) PLAYERS SORTED BY RUNS CONCEDED (Ascending Order - Least First):")
    print(f"   {'Rank':<6} {'Bowler':<20} {'Runs':<8} {'Economy':<10} {'Wickets':<10} {'Overs':<8}")
    print("   " + "-" * 72)
    for i, player in enumerate(results['sorted_by_runs'], 1):
        print(f"   {i:<6} {player['name']:<20} {player['runs']:<8} "
              f"{player['economy']:<10.2f} {player['wickets']:<10} {player['overs']:<8}")
    
    # iii) Players sorted by Wickets (Descending order - Most wickets first)
    print("\n\niii) PLAYERS SORTED BY WICKETS (Descending Order - Most First):")
    print(f"   {'Rank':<6} {'Bowler':<20} {'Wickets':<10} {'Economy':<10} {'Runs':<8} {'Overs':<8}")
    print("   " + "-" * 72)
    for i, player in enumerate(results['sorted_by_wickets'], 1):
        print(f"   {i:<6} {player['name']:<20} {player['wickets']:<10} "
              f"{player['economy']:<10.2f} {player['runs']:<8} {player['overs']:<8}")
    
    print("=" * 70)


# Example usage
if __name__ == "__main__":
    # Sample bowling data - Single dictionary with all bowlers
    bowlers_data = {
        'Shaheen Shah Afridi': {'overs': [1, 3, 5, 17], 'runs': 20, 'wickets': 1},
        'Faheem': {'overs': [2, 4, 6, 19], 'runs': 29, 'wickets': 3},
        'Nawaz': {'overs': [7], 'runs': 6, 'wickets': 0},
        'Haris Rauf': {'overs': [8, 15, 18, 20], 'runs': 50, 'wickets': 0},
        'Abrar Ahmed': {'overs': [9, 11, 13, 16], 'runs': 29, 'wickets': 1},
        'Saim Ayub': {'overs': [10, 12, 14], 'runs': 16, 'wickets': 0}
    }
    
    # Analyze bowling statistics
    results = analyze_bowling_stats(bowlers_data)
    
    # Print formatted results
    print_results(results)
    
    print("\n\nYou can add more bowlers to the dictionary and run again!")
    print("\nExample format:")
    print('{"BowlerName": {"overs": [1,2,4], "runs": 20, "wickets": 2}}')