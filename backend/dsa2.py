"""
Advanced DSA Extensions for Cricket Analysis
Implements concepts from DSA Possibilities PDF without modifying existing functions
"""

import networkx as nx
from collections import deque, defaultdict
import heapq

# =============================================================================
# 1. GRAPH ALGORITHMS ON BATTER VS BOWLER GRAPH
# =============================================================================

def find_weakest_bowler_per_batter(G):
    """
    Find the bowler each batter scores most easily against
    Uses weighted shortest path concept (min resistance)
    """
    result = {}
    for batter in G.nodes:
        if G.nodes[batter].get("role") != "batter":
            continue
        
        best_matchup = None
        max_runs_per_ball = 0
        
        for bowler in G[batter]:
            data = G[batter][bowler]
            balls = data.get("balls", 0)
            runs = data.get("runs", 0)
            
            if balls > 0:
                runs_per_ball = runs / balls
                if runs_per_ball > max_runs_per_ball:
                    max_runs_per_ball = runs_per_ball
                    best_matchup = bowler
        
        if best_matchup:
            result[batter] = {
                "bowler": best_matchup,
                "runs_per_ball": round(max_runs_per_ball, 2)
            }
    
    return result


def find_strongest_bowler_per_batter(G):
    """
    Find the bowler each batter struggles most against
    """
    result = {}
    for batter in G.nodes:
        if G.nodes[batter].get("role") != "batter":
            continue
        
        worst_matchup = None
        min_runs_per_ball = float('inf')
        
        for bowler in G[batter]:
            data = G[batter][bowler]
            balls = data.get("balls", 0)
            runs = data.get("runs", 0)
            wickets = data.get("wickets", 0)
            
            if balls > 0:
                # Lower is worse for batter (especially with wickets)
                runs_per_ball = runs / balls
                if wickets > 0:
                    runs_per_ball *= 0.5  # Penalty for getting out
                
                if runs_per_ball < min_runs_per_ball:
                    min_runs_per_ball = runs_per_ball
                    worst_matchup = bowler
        
        if worst_matchup:
            result[batter] = {
                "bowler": worst_matchup,
                "runs_per_ball": round(min_runs_per_ball, 2)
            }
    
    return result


def calculate_bowler_centrality(G):
    """
    Calculate which bowlers are most 'central' (dominant across batters)
    Uses degree centrality and weighted scoring
    """
    bowler_centrality = {}
    
    for node in G.nodes:
        if G.nodes[node].get("role") == "bowler":
            total_wickets = 0
            total_batters_faced = 0
            total_balls = 0
            
            # Find all batters who faced this bowler
            for batter in G.nodes:
                if G.nodes[batter].get("role") == "batter" and G.has_edge(batter, node):
                    total_batters_faced += 1
                    data = G[batter][node]
                    total_wickets += data.get("wickets", 0)
                    total_balls += data.get("balls", 0)
            
            if total_balls > 0:
                centrality_score = (total_batters_faced * 10) + (total_wickets * 50)
                bowler_centrality[node] = {
                    "centrality_score": centrality_score,
                    "batters_faced": total_batters_faced,
                    "wickets": total_wickets,
                    "balls": total_balls
                }
    
    # Sort by centrality score
    return dict(sorted(bowler_centrality.items(), 
                      key=lambda x: x[1]["centrality_score"], 
                      reverse=True))


def optimal_bowler_assignment(G, batters_to_target):
    """
    Greedy algorithm to assign bowlers optimally to minimize runs
    Simulates min-cost matching concept
    """
    assignments = []
    used_bowlers = set()
    
    for batter in batters_to_target:
        if batter not in G.nodes or G.nodes[batter].get("role") != "batter":
            continue
        
        best_bowler = None
        min_cost = float('inf')
        
        for bowler in G[batter]:
            if bowler in used_bowlers:
                continue
            
            data = G[batter][bowler]
            balls = data.get("balls", 0)
            runs = data.get("runs", 0)
            
            if balls > 0:
                cost = runs / balls  # Lower is better
                if cost < min_cost:
                    min_cost = cost
                    best_bowler = bowler
        
        if best_bowler:
            assignments.append({
                "batter": batter,
                "bowler": best_bowler,
                "expected_runs_per_ball": round(min_cost, 2)
            })
            used_bowlers.add(best_bowler)
    
    return assignments


# =============================================================================
# 2. SLIDING WINDOW & PREFIX SUM ON OVERS
# =============================================================================

class OverAnalyzer:
    """
    Implements sliding window and prefix sum on linked list of overs
    """
    
    @staticmethod
    def build_prefix_sums(overs_head):
        """Build prefix sum array from linked list"""
        prefix_runs = [0]
        prefix_wickets = [0]
        
        curr = overs_head
        while curr:
            prefix_runs.append(prefix_runs[-1] + curr.runs)
            prefix_wickets.append(prefix_wickets[-1] + curr.wickets)
            curr = curr.next
        
        return prefix_runs, prefix_wickets
    
    @staticmethod
    def get_runs_between_overs(prefix_runs, start_over, end_over):
        """O(1) query for runs between overs using prefix sum"""
        if start_over < 1 or end_over >= len(prefix_runs):
            return 0
        return prefix_runs[end_over] - prefix_runs[start_over - 1]
    
    @staticmethod
    def best_k_consecutive_overs(overs_head, k):
        """
        Find best k consecutive overs (max runs) using sliding window
        """
        if not overs_head or k <= 0:
            return None
        
        # Convert to array for easier sliding window
        overs = []
        curr = overs_head
        while curr:
            overs.append({"over": curr.over_num, "runs": curr.runs, "wickets": curr.wickets})
            curr = curr.next
        
        if len(overs) < k:
            return None
        
        # Initialize window
        window_runs = sum(o["runs"] for o in overs[:k])
        max_runs = window_runs
        best_start = 0
        
        # Slide window
        for i in range(k, len(overs)):
            window_runs += overs[i]["runs"] - overs[i - k]["runs"]
            if window_runs > max_runs:
                max_runs = window_runs
                best_start = i - k + 1
        
        return {
            "start_over": overs[best_start]["over"],
            "end_over": overs[best_start + k - 1]["over"],
            "total_runs": max_runs,
            "overs": overs[best_start:best_start + k]
        }
    
    @staticmethod
    def rolling_run_rate(overs_head, window_size=6):
        """Calculate rolling run rate over window_size overs"""
        overs = []
        curr = overs_head
        while curr:
            overs.append(curr.runs)
            curr = curr.next
        
        rolling_rates = []
        for i in range(len(overs)):
            start = max(0, i - window_size + 1)
            window_runs = sum(overs[start:i + 1])
            window_overs = i - start + 1
            rolling_rates.append({
                "over": i + 1,
                "run_rate": round(window_runs / window_overs, 2)
            })
        
        return rolling_rates


# =============================================================================
# 3. BINARY SEARCH TREE FOR PLAYER STATS
# =============================================================================

class BSTNode:
    def __init__(self, player, runs):
        self.player = player
        self.runs = runs
        self.left = None
        self.right = None


class PlayerStatsBST:
    """BST to maintain players sorted by runs with O(log n) operations"""
    
    def __init__(self):
        self.root = None
    
    def insert(self, player, runs):
        """Insert player into BST"""
        if not self.root:
            self.root = BSTNode(player, runs)
        else:
            self._insert_recursive(self.root, player, runs)
    
    def _insert_recursive(self, node, player, runs):
        if runs < node.runs:
            if node.left is None:
                node.left = BSTNode(player, runs)
            else:
                self._insert_recursive(node.left, player, runs)
        else:
            if node.right is None:
                node.right = BSTNode(player, runs)
            else:
                self._insert_recursive(node.right, player, runs)
    
    def find_first_above_threshold(self, threshold):
        """Binary search for first player with >= threshold runs"""
        result = []
        self._find_above_threshold(self.root, threshold, result)
        return result
    
    def _find_above_threshold(self, node, threshold, result):
        if not node:
            return
        
        if node.runs >= threshold:
            self._find_above_threshold(node.left, threshold, result)
            result.append({"player": node.player, "runs": node.runs})
            self._find_above_threshold(node.right, threshold, result)
        else:
            self._find_above_threshold(node.right, threshold, result)
    
    def inorder_traversal(self):
        """Return players in sorted order by runs"""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append({"player": node.player, "runs": node.runs})
            self._inorder(node.right, result)


# =============================================================================
# 4. TRIE FOR PLAYER NAME SEARCH
# =============================================================================

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.player_name = None


class PlayerTrie:
    """Trie for efficient player name autocomplete and search"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, name):
        """Insert player name into trie"""
        node = self.root
        for char in name.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.player_name = name
    
    def search(self, prefix):
        """Find all players matching prefix"""
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        return self._collect_names(node)
    
    def _collect_names(self, node):
        """Collect all names from this node downward"""
        names = []
        if node.is_end:
            names.append(node.player_name)
        
        for child in node.children.values():
            names.extend(self._collect_names(child))
        
        return names


# =============================================================================
# 5. DYNAMIC PROGRAMMING - BOWLING ALLOCATION
# =============================================================================

def optimal_bowling_allocation(bowlers, max_overs_per_bowler, total_overs):
    """
    DP: Allocate overs to bowlers to minimize expected runs
    bowlers: list of {"name": str, "economy": float}
    """
    n = len(bowlers)
    
    # dp[i][j] = min runs conceded using first i bowlers for j overs
    dp = [[float('inf')] * (total_overs + 1) for _ in range(n + 1)]
    allocation = [[[] for _ in range(total_overs + 1)] for _ in range(n + 1)]
    
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        bowler = bowlers[i - 1]
        for j in range(total_overs + 1):
            # Try allocating k overs to this bowler
            for k in range(min(max_overs_per_bowler, j) + 1):
                if dp[i - 1][j - k] != float('inf'):
                    cost = dp[i - 1][j - k] + k * bowler["economy"]
                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        allocation[i][j] = allocation[i - 1][j - k] + [{
                            "bowler": bowler["name"],
                            "overs": k
                        }]
    
    return {
        "min_expected_runs": round(dp[n][total_overs], 1),
        "allocation": allocation[n][total_overs]
    }


# =============================================================================
# 6. HASHING - PATTERN DETECTION
# =============================================================================

def detect_scoring_patterns(runs, pattern_length=4):
    """
    Use rolling hash to detect repeating scoring patterns
    """
    if len(runs) < pattern_length:
        return {}
    
    pattern_count = defaultdict(int)
    
    for i in range(len(runs) - pattern_length + 1):
        pattern = tuple(runs[i:i + pattern_length])
        pattern_count[pattern] += 1
    
    # Return patterns that occur more than once
    repeated = {
        str(pattern): count 
        for pattern, count in pattern_count.items() 
        if count > 1
    }
    
    return dict(sorted(repeated.items(), key=lambda x: x[1], reverse=True))


def detect_duplicate_overs(overs_head):
    """
    Hash table to detect duplicate over performances
    """
    over_hash = {}
    duplicates = []
    
    curr = overs_head
    while curr:
        key = (curr.runs, curr.wickets)
        if key in over_hash:
            duplicates.append({
                "pattern": f"{curr.runs} runs, {curr.wickets} wickets",
                "overs": over_hash[key] + [curr.over_num]
            })
            over_hash[key].append(curr.over_num)
        else:
            over_hash[key] = [curr.over_num]
        curr = curr.next
    
    return duplicates


# =============================================================================
# 7. UNION-FIND (DSU) - BOWLER CLUSTERS
# =============================================================================

class UnionFind:
    """DSU implementation"""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1


def cluster_batters_by_common_dismissals(G):
    """
    Group batters dismissed by similar set of bowlers using DSU
    """
    batters = [n for n in G.nodes if G.nodes[n].get("role") == "batter"]
    n = len(batters)
    
    if n == 0:
        return {}
    
    batter_to_idx = {b: i for i, b in enumerate(batters)}
    uf = UnionFind(n)
    
    # Union batters who were dismissed by same bowlers
    for i, b1 in enumerate(batters):
        for j, b2 in enumerate(batters):
            if i >= j:
                continue
            
            # Find common bowlers who dismissed both
            dismissed_by_1 = {bw for bw in G[b1] if G[b1][bw].get("wickets", 0) > 0}
            dismissed_by_2 = {bw for bw in G[b2] if G[b2][bw].get("wickets", 0) > 0}
            
            if dismissed_by_1 & dismissed_by_2:  # Common dismissals
                uf.union(i, j)
    
    # Group by cluster
    clusters = defaultdict(list)
    for i, batter in enumerate(batters):
        root = uf.find(i)
        clusters[root].append(batter)
    
    return {f"Cluster {i+1}": batters for i, batters in enumerate(clusters.values())}


# =============================================================================
# 8. PRIORITY SCHEDULING - DYNAMIC BOWLER ROTATION
# =============================================================================

class BowlerScheduler:
    """Priority queue based bowler scheduling"""
    
    def __init__(self, bowlers):
        """
        bowlers: [{"name": str, "economy": float, "wickets": int, "overs_left": int}]
        """
        self.heap = []
        for b in bowlers:
            priority = self._calculate_priority(b)
            heapq.heappush(self.heap, (-priority, b["name"], b))
    
    def _calculate_priority(self, bowler):
        """Higher is better - based on economy and wickets"""
        return bowler["wickets"] * 10 - bowler["economy"]
    
    def get_next_bowler(self):
        """Get highest priority bowler"""
        if not self.heap:
            return None
        
        _, name, bowler = heapq.heappop(self.heap)
        return bowler
    
    def return_bowler(self, bowler, runs_conceded, wickets_taken):
        """Update and return bowler to queue"""
        bowler["overs_left"] -= 1
        if bowler["overs_left"] > 0:
            # Update stats
            bowler["wickets"] += wickets_taken
            priority = self._calculate_priority(bowler)
            heapq.heappush(self.heap, (-priority, bowler["name"], bowler))


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("DSA Extensions for Cricket Analysis")
    print("=" * 60)
    print("\nThese functions work alongside existing analysis code:")
    print("1. Graph algorithms - matchup analysis")
    print("2. Sliding window - best powerplay overs")
    print("3. BST - fast player lookup")
    print("4. Trie - autocomplete player names")
    print("5. DP - optimal bowling allocation")
    print("6. Hashing - pattern detection")
    print("7. Union-Find - cluster analysis")
    print("8. Priority queue - dynamic scheduling")