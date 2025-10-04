import React, { useState } from 'react';
import { 
  Network, 
  TrendingUp, 
  Search, 
  Zap, 
  Users, 
  Target,
  Clock,
  Activity,
  ChevronDown,
  ChevronUp,
  Award,
  AlertCircle
} from 'lucide-react';

const DSA2Analysis = ({ dsa2Data, teamAName = "Team A", teamBName = "Team B" }) => {
  const [expandedSections, setExpandedSections] = useState({});
  const [selectedTeam, setSelectedTeam] = useState("teamA");

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  if (!dsa2Data) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
        <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No advanced analysis data available</p>
      </div>
    );
  }

  const SectionHeader = ({ icon: Icon, title, sectionKey, color = "blue" }) => (
    <button
      onClick={() => toggleSection(sectionKey)}
      className={`w-full flex items-center justify-between p-4 bg-gradient-to-r from-${color}-50 to-white rounded-lg border-2 border-${color}-200 hover:border-${color}-300 transition-all`}
    >
      <div className="flex items-center gap-3">
        <Icon className={`w-6 h-6 text-${color}-600`} />
        <h3 className={`text-xl font-bold text-${color}-800`}>{title}</h3>
      </div>
      {expandedSections[sectionKey] ? (
        <ChevronUp className={`w-5 h-5 text-${color}-600`} />
      ) : (
        <ChevronDown className={`w-5 h-5 text-${color}-600`} />
      )}
    </button>
  );

  const TeamSelector = () => (
    <div className="flex gap-4 mb-6">
      <button
        onClick={() => setSelectedTeam("teamA")}
        className={`px-6 py-3 rounded-lg font-bold transition-all ${
          selectedTeam === "teamA"
            ? "bg-green-600 text-white shadow-lg"
            : "bg-gray-200 text-gray-700 hover:bg-gray-300"
        }`}
      >
        {teamAName}
      </button>
      <button
        onClick={() => setSelectedTeam("teamB")}
        className={`px-6 py-3 rounded-lg font-bold transition-all ${
          selectedTeam === "teamB"
            ? "bg-blue-600 text-white shadow-lg"
            : "bg-gray-200 text-gray-700 hover:bg-gray-300"
        }`}
      >
        {teamBName}
      </button>
    </div>
  );

  return (
    <div className="w-full mt-8 space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 rounded-2xl shadow-2xl p-8 text-white">
        <div className="flex items-center gap-4 mb-4">
          <Zap className="w-10 h-10" />
          <h2 className="text-3xl font-bold">Advanced Cricket Analytics</h2>
        </div>
        <p className="text-blue-100">Deep insights using advanced data structures and algorithms</p>
      </div>

      <TeamSelector />

      {/* 1. Graph-Based Matchup Analysis */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Network} 
          title="Player Matchup Analysis (Graph Algorithms)" 
          sectionKey="graphAnalysis"
          color="purple"
        />
        
        {expandedSections.graphAnalysis && (
          <div className="mt-6 space-y-6">
            {/* Weakest Bowler Matchups */}
            <div className="bg-gradient-to-br from-green-50 to-white p-6 rounded-xl border-2 border-green-200">
              <h4 className="text-lg font-bold text-green-800 mb-4 flex items-center gap-2">
                <Target className="w-5 h-5" />
                Favorable Bowling Matchups (Highest Scoring Rate)
              </h4>
              <div className="space-y-3">
                {Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.weakest_bowler_matchups || {}).map(([batter, data]) => (
                  <div key={batter} className="bg-white p-4 rounded-lg shadow-sm border-l-4 border-green-500">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-bold text-slate-800">{batter}</div>
                        <div className="text-sm text-slate-600 mt-1">
                          vs <span className="font-semibold text-green-700">{data.bowler}</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-green-600">{data.runs_per_ball}</div>
                        <div className="text-xs text-slate-600">runs/ball</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Strongest Bowler Matchups */}
            <div className="bg-gradient-to-br from-red-50 to-white p-6 rounded-xl border-2 border-red-200">
              <h4 className="text-lg font-bold text-red-800 mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5" />
                Challenging Matchups (Lowest Scoring Rate)
              </h4>
              <div className="space-y-3">
                {Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.strongest_bowler_matchups || {}).map(([batter, data]) => (
                  <div key={batter} className="bg-white p-4 rounded-lg shadow-sm border-l-4 border-red-500">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-bold text-slate-800">{batter}</div>
                        <div className="text-sm text-slate-600 mt-1">
                          struggles vs <span className="font-semibold text-red-700">{data.bowler}</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-red-600">{data.runs_per_ball}</div>
                        <div className="text-xs text-slate-600">runs/ball</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Bowler Centrality */}
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-xl border-2 border-blue-200">
              <h4 className="text-lg font-bold text-blue-800 mb-4 flex items-center gap-2">
                <Award className="w-5 h-5" />
                Most Dominant Bowlers (Centrality Score)
              </h4>
              <div className="space-y-3">
                {Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.bowler_centrality || {}).slice(0, 5).map(([bowler, data], idx) => (
                  <div key={bowler} className="bg-white p-4 rounded-lg shadow-sm flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-white ${
                      idx === 0 ? 'bg-yellow-500' : idx === 1 ? 'bg-gray-400' : idx === 2 ? 'bg-orange-500' : 'bg-blue-500'
                    }`}>
                      {idx + 1}
                    </div>
                    <div className="flex-1">
                      <div className="font-bold text-slate-800">{bowler}</div>
                      <div className="text-sm text-slate-600">
                        {data.batters_faced} batters faced • {data.wickets} wickets • {data.balls} balls
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold text-blue-600">{data.centrality_score}</div>
                      <div className="text-xs text-slate-600">dominance</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Optimal Assignment */}
            {dsa2Data.graph_analysis?.[selectedTeam]?.optimal_assignment && (
              <div className="bg-gradient-to-br from-purple-50 to-white p-6 rounded-xl border-2 border-purple-200">
                <h4 className="text-lg font-bold text-purple-800 mb-4 flex items-center gap-2">
                  <Zap className="w-5 h-5" />
                  Optimal Bowler Assignment (Greedy Algorithm)
                </h4>
                <div className="space-y-3">
                  {dsa2Data.graph_analysis[selectedTeam].optimal_assignment.map((assignment, idx) => (
                    <div key={idx} className="bg-white p-4 rounded-lg shadow-sm border-l-4 border-purple-500">
                      <div className="flex justify-between items-center">
                        <div>
                          <div className="font-bold text-slate-800">{assignment.batter}</div>
                          <div className="text-sm text-slate-600 mt-1">
                            Best bowled by: <span className="font-semibold text-purple-700">{assignment.bowler}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xl font-bold text-purple-600">{assignment.expected_runs_per_ball}</div>
                          <div className="text-xs text-slate-600">expected runs/ball</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 2. Sliding Window Analysis */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Activity} 
          title="Momentum Analysis (Sliding Window)" 
          sectionKey="slidingWindow"
          color="indigo"
        />
        
        {expandedSections.slidingWindow && (
          <div className="mt-6 space-y-6">
            {/* Best Powerplay */}
            {dsa2Data.over_analysis?.[selectedTeam]?.best_powerplay && (
              <div className="bg-gradient-to-br from-indigo-50 to-white p-6 rounded-xl border-2 border-indigo-200">
                <h4 className="text-lg font-bold text-indigo-800 mb-4">Best 6 Consecutive Overs (Powerplay)</h4>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <div className="text-sm text-slate-600">Overs</div>
                    <div className="text-2xl font-bold text-indigo-600">
                      {dsa2Data.over_analysis[selectedTeam].best_powerplay.start_over} - {dsa2Data.over_analysis[selectedTeam].best_powerplay.end_over}
                    </div>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <div className="text-sm text-slate-600">Total Runs</div>
                    <div className="text-2xl font-bold text-indigo-600">
                      {dsa2Data.over_analysis[selectedTeam].best_powerplay.total_runs}
                    </div>
                  </div>
                </div>
                <div className="flex gap-2 flex-wrap">
                  {dsa2Data.over_analysis[selectedTeam].best_powerplay.overs.map((over, idx) => (
                    <div key={idx} className="bg-indigo-100 px-3 py-2 rounded-lg">
                      <div className="text-xs text-indigo-700">Over {over.over}</div>
                      <div className="font-bold text-indigo-900">{over.runs} runs</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Rolling Run Rate */}
            {dsa2Data.over_analysis?.[selectedTeam]?.rolling_run_rate && (
              <div className="bg-gradient-to-br from-cyan-50 to-white p-6 rounded-xl border-2 border-cyan-200">
                <h4 className="text-lg font-bold text-cyan-800 mb-4 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Rolling Run Rate (6-over window)
                </h4>
                <div className="grid grid-cols-5 gap-2">
                  {dsa2Data.over_analysis[selectedTeam].rolling_run_rate.map((data, idx) => (
                    <div key={idx} className="bg-white p-3 rounded-lg shadow-sm text-center">
                      <div className="text-xs text-slate-600">Over {data.over}</div>
                      <div className="text-lg font-bold text-cyan-600">{data.run_rate}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 3. BST Search Results */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Search} 
          title="Quick Player Search (Binary Search Tree)" 
          sectionKey="bstSearch"
          color="green"
        />
        
        {expandedSections.bstSearch && (
          <div className="mt-6 space-y-6">
            <div className="grid grid-cols-2 gap-6">
              {/* 30+ Runs */}
              <div className="bg-gradient-to-br from-green-50 to-white p-6 rounded-xl border-2 border-green-200">
                <h4 className="text-lg font-bold text-green-800 mb-4">Batters with 30+ Runs</h4>
                <div className="space-y-2">
                  {dsa2Data.bst_search?.[selectedTeam]?.batters_above_30?.map((batter, idx) => (
                    <div key={idx} className="bg-white p-3 rounded-lg shadow-sm flex justify-between items-center">
                      <span className="font-semibold text-slate-800">{batter.player}</span>
                      <span className="text-green-600 font-bold">{batter.runs}</span>
                    </div>
                  )) || <p className="text-slate-600 text-sm">No players found</p>}
                </div>
              </div>

              {/* 50+ Runs */}
              <div className="bg-gradient-to-br from-yellow-50 to-white p-6 rounded-xl border-2 border-yellow-200">
                <h4 className="text-lg font-bold text-yellow-800 mb-4">Batters with 50+ Runs</h4>
                <div className="space-y-2">
                  {dsa2Data.bst_search?.[selectedTeam]?.batters_above_50?.map((batter, idx) => (
                    <div key={idx} className="bg-white p-3 rounded-lg shadow-sm flex justify-between items-center">
                      <span className="font-semibold text-slate-800">{batter.player}</span>
                      <span className="text-yellow-600 font-bold">{batter.runs}</span>
                    </div>
                  )) || <p className="text-slate-600 text-sm">No players found</p>}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 4. Player Name Search (Trie) */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Search} 
          title="Player Name Autocomplete (Trie)" 
          sectionKey="trieSearch"
          color="teal"
        />
        
        {expandedSections.trieSearch && (
          <div className="mt-6 space-y-4">
            <div className="grid grid-cols-3 gap-4">
              {Object.entries(dsa2Data.player_search || {}).map(([searchKey, results]) => (
                <div key={searchKey} className="bg-gradient-to-br from-teal-50 to-white p-4 rounded-xl border-2 border-teal-200">
                  <h4 className="text-sm font-bold text-teal-800 mb-3">Search: "{searchKey.replace('search_', '')}"</h4>
                  <div className="space-y-1">
                    {results.slice(0, 5).map((player, idx) => (
                      <div key={idx} className="text-sm text-slate-700 bg-white px-2 py-1 rounded">
                        {player}
                      </div>
                    ))}
                    {results.length > 5 && (
                      <div className="text-xs text-teal-600 mt-2">+{results.length - 5} more</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 5. Dynamic Programming - Bowling Allocation */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Clock} 
          title="Optimal Bowling Strategy (Dynamic Programming)" 
          sectionKey="dpAllocation"
          color="orange"
        />
        
        {expandedSections.dpAllocation && dsa2Data.optimal_bowling_allocation?.[selectedTeam] && (
          <div className="mt-6">
            <div className="bg-gradient-to-br from-orange-50 to-white p-6 rounded-xl border-2 border-orange-200">
              <div className="mb-6">
                <div className="text-sm text-slate-600">Minimum Expected Runs</div>
                <div className="text-4xl font-bold text-orange-600">
                  {dsa2Data.optimal_bowling_allocation[selectedTeam].min_expected_runs}
                </div>
              </div>
              <h4 className="text-lg font-bold text-orange-800 mb-4">Optimal Over Allocation</h4>
              <div className="space-y-2">
                {dsa2Data.optimal_bowling_allocation[selectedTeam].allocation.filter(a => a.overs > 0).map((allocation, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-lg shadow-sm flex justify-between items-center">
                    <span className="font-semibold text-slate-800">{allocation.bowler}</span>
                    <span className="text-orange-600 font-bold">{allocation.overs} overs</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 6. Pattern Detection (Hashing) */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Activity} 
          title="Scoring Pattern Detection (Hashing)" 
          sectionKey="patterns"
          color="pink"
        />
        
        {expandedSections.patterns && (
          <div className="mt-6 space-y-6">
            {/* Scoring Patterns */}
            <div className="bg-gradient-to-br from-pink-50 to-white p-6 rounded-xl border-2 border-pink-200">
              <h4 className="text-lg font-bold text-pink-800 mb-4">Repeated Scoring Patterns</h4>
              <div className="space-y-2">
                {Object.entries(dsa2Data.pattern_detection?.[selectedTeam]?.scoring_patterns || {}).slice(0, 5).map(([pattern, count]) => (
                  <div key={pattern} className="bg-white p-3 rounded-lg shadow-sm flex justify-between items-center">
                    <span className="font-mono text-sm text-slate-700">{pattern}</span>
                    <span className="text-pink-600 font-bold">{count}x</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Duplicate Overs */}
            {dsa2Data.pattern_detection?.[selectedTeam]?.duplicate_overs?.length > 0 && (
              <div className="bg-gradient-to-br from-rose-50 to-white p-6 rounded-xl border-2 border-rose-200">
                <h4 className="text-lg font-bold text-rose-800 mb-4">Similar Over Performances</h4>
                <div className="space-y-2">
                  {dsa2Data.pattern_detection[selectedTeam].duplicate_overs.map((dup, idx) => (
                    <div key={idx} className="bg-white p-3 rounded-lg shadow-sm">
                      <div className="font-semibold text-slate-800">{dup.pattern}</div>
                      <div className="text-sm text-slate-600">Overs: {dup.overs.join(', ')}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 7. Batter Clusters (Union-Find) */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Users} 
          title="Batter Grouping by Dismissal Pattern (Union-Find)" 
          sectionKey="clusters"
          color="violet"
        />
        
        {expandedSections.clusters && (
          <div className="mt-6">
            <div className="bg-gradient-to-br from-violet-50 to-white p-6 rounded-xl border-2 border-violet-200">
              <div className="space-y-4">
                {Object.entries(dsa2Data.batter_clusters?.[selectedTeam] || {}).map(([cluster, batters]) => (
                  <div key={cluster} className="bg-white p-4 rounded-lg shadow-sm">
                    <h4 className="font-bold text-violet-800 mb-2">{cluster}</h4>
                    <div className="flex flex-wrap gap-2">
                      {batters.map((batter, idx) => (
                        <span key={idx} className="bg-violet-100 text-violet-700 px-3 py-1 rounded-full text-sm font-semibold">
                          {batter}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 8. Next Bowler Recommendation (Priority Queue) */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <SectionHeader 
          icon={Target} 
          title="Smart Bowler Selection (Priority Queue)" 
          sectionKey="nextBowler"
          color="emerald"
        />
        
        {expandedSections.nextBowler && dsa2Data.next_bowler_recommendation?.[selectedTeam] && (
          <div className="mt-6">
            <div className="bg-gradient-to-br from-emerald-50 to-white p-6 rounded-xl border-2 border-emerald-200">
              <h4 className="text-lg font-bold text-emerald-800 mb-4">Recommended Next Bowler</h4>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-3xl font-bold text-emerald-600 mb-4">
                  {dsa2Data.next_bowler_recommendation[selectedTeam].name}
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <div className="text-sm text-slate-600">Economy</div>
                    <div className="text-xl font-bold text-slate-800">
                      {dsa2Data.next_bowler_recommendation[selectedTeam].economy.toFixed(2)}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-slate-600">Wickets</div>
                    <div className="text-xl font-bold text-slate-800">
                      {dsa2Data.next_bowler_recommendation[selectedTeam].wickets}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-slate-600">Overs Left</div>
                    <div className="text-xl font-bold text-slate-800">
                      {dsa2Data.next_bowler_recommendation[selectedTeam].overs_left}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DSA2Analysis;