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
  AlertCircle,
  BarChart3,
  Shield,
  ArrowUpRight,
  ArrowDownRight,
  Minus
} from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend, Cell } from 'recharts';

const DSA2Analysis = ({ dsa2Data, teamAName = "Team A", teamBName = "Team B" }) => {
  const [expandedSections, setExpandedSections] = useState({});
  const [selectedTeam, setSelectedTeam] = useState("teamA");
  const [theme, setTheme] = useState("light");

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const toggleTheme = () => {
    setTheme(prev => prev === "light" ? "dark" : "light");
  };

  if (!dsa2Data) {
    return (
      <div className={`${theme === 'dark' ? 'bg-slate-900' : 'bg-white'} rounded-xl shadow-lg p-12 text-center border ${theme === 'dark' ? 'border-slate-700' : 'border-gray-200'}`}>
        <AlertCircle className={`w-16 h-16 ${theme === 'dark' ? 'text-slate-500' : 'text-gray-400'} mx-auto mb-4`} />
        <p className={`${theme === 'dark' ? 'text-slate-400' : 'text-gray-600'} text-lg font-medium`}>No advanced analysis data available</p>
      </div>
    );
  }

  const isDark = theme === 'dark';
  const bgPrimary = isDark ? 'bg-slate-950' : 'bg-gray-50';
  const bgSecondary = isDark ? 'bg-slate-900' : 'bg-white';
  const bgTertiary = isDark ? 'bg-slate-800' : 'bg-gray-50';
  const bgQuaternary = isDark ? 'bg-slate-750' : 'bg-white';
  const textPrimary = isDark ? 'text-slate-100' : 'text-gray-900';
  const textSecondary = isDark ? 'text-slate-400' : 'text-gray-600';
  const textTertiary = isDark ? 'text-slate-500' : 'text-gray-500';
  const borderPrimary = isDark ? 'border-slate-700' : 'border-gray-200';
  const borderSecondary = isDark ? 'border-slate-600' : 'border-gray-300';
  const hoverBg = isDark ? 'hover:bg-slate-800' : 'hover:bg-gray-100';

  const SectionHeader = ({ icon: Icon, title, sectionKey }) => (
    <button
      onClick={() => toggleSection(sectionKey)}
      className={`w-full flex items-center justify-between p-4 ${bgTertiary} rounded-lg border ${borderPrimary} ${hoverBg} transition-all group`}
    >
      <div className="flex items-center gap-3">
        <div className={`p-2 ${isDark ? 'bg-blue-500/10' : 'bg-blue-50'} rounded-lg`}>
          <Icon className={`w-5 h-5 ${isDark ? 'text-blue-400' : 'text-blue-600'}`} />
        </div>
        <h3 className={`text-base font-semibold ${textPrimary} tracking-tight`}>{title}</h3>
      </div>
      {expandedSections[sectionKey] ? (
        <ChevronUp className={`w-5 h-5 ${textSecondary}`} />
      ) : (
        <ChevronDown className={`w-5 h-5 ${textSecondary}`} />
      )}
    </button>
  );

  const TeamSelector = () => (
    <div className="flex items-center gap-4">
      <div className={`flex gap-2 p-1 ${bgTertiary} rounded-lg border ${borderPrimary}`}>
        <button
          onClick={() => setSelectedTeam("teamA")}
          className={`px-6 py-2.5 rounded-md font-semibold text-sm transition-all ${
            selectedTeam === "teamA"
              ? `${isDark ? 'bg-blue-500 text-white' : 'bg-blue-600 text-white'} shadow-md`
              : `${textSecondary} ${hoverBg}`
          }`}
        >
          {teamAName}
        </button>
        <button
          onClick={() => setSelectedTeam("teamB")}
          className={`px-6 py-2.5 rounded-md font-semibold text-sm transition-all ${
            selectedTeam === "teamB"
              ? `${isDark ? 'bg-blue-500 text-white' : 'bg-blue-600 text-white'} shadow-md`
              : `${textSecondary} ${hoverBg}`
          }`}
        >
          {teamBName}
        </button>
      </div>
      <button
        onClick={toggleTheme}
        className={`px-4 py-2.5 rounded-lg border ${borderPrimary} ${bgTertiary} ${textSecondary} hover:${textPrimary} transition-all font-medium text-sm`}
      >
        {isDark ? '☀️ Light' : '🌙 Dark'}
      </button>
    </div>
  );

  const MetricCard = ({ label, value, subtext, trend }) => (
    <div className={`${bgTertiary} border ${borderPrimary} rounded-lg p-4`}>
      <div className={`text-xs font-semibold ${textTertiary} uppercase tracking-wider mb-2`}>{label}</div>
      <div className="flex items-baseline gap-2">
        <div className={`text-2xl font-bold ${textPrimary}`}>{value}</div>
        {trend && (
          <div className={`flex items-center text-xs font-medium ${
            trend > 0 ? 'text-green-600' : trend < 0 ? 'text-red-600' : textSecondary
          }`}>
            {trend > 0 ? <ArrowUpRight className="w-3 h-3" /> : trend < 0 ? <ArrowDownRight className="w-3 h-3" /> : <Minus className="w-3 h-3" />}
            {Math.abs(trend)}%
          </div>
        )}
      </div>
      {subtext && <div className={`text-xs ${textTertiary} mt-1`}>{subtext}</div>}
    </div>
  );

  // Prepare chart data for rolling run rate
  const prepareRunRateChartData = () => {
    const data = dsa2Data.over_analysis?.[selectedTeam]?.rolling_run_rate || [];
    return data.map(item => ({
      over: `O${item.over}`,
      runRate: parseFloat(item.run_rate)
    }));
  };

  // Prepare bowler centrality radar chart data
  const prepareCentralityRadarData = () => {
    const bowlers = Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.bowler_centrality || {}).slice(0, 5);
    return bowlers.map(([name, data]) => ({
      bowler: name.split(' ').pop(),
      centrality: parseFloat(data.centrality_score),
      wickets: data.wickets,
      effectiveness: (data.wickets / data.balls * 100).toFixed(1)
    }));
  };

  // Prepare matchup comparison data
  const prepareMatchupComparisonData = () => {
    const favorable = Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.weakest_bowler_matchups || {}).slice(0, 5);
    const challenging = Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.strongest_bowler_matchups || {}).slice(0, 5);
    
    return favorable.map(([batter, data], idx) => ({
      batter: batter.split(' ').pop(),
      favorable: parseFloat(data.runs_per_ball),
      challenging: challenging[idx] ? parseFloat(challenging[idx][1].runs_per_ball) : 0
    }));
  };

  const COLORS = isDark 
    ? ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
    : ['#2563eb', '#059669', '#d97706', '#dc2626', '#7c3aed', '#db2777'];

  return (
    <div className={`w-full min-h-screen ${bgPrimary} p-6 transition-colors duration-200`}>
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className={`${bgSecondary} rounded-xl shadow-sm p-6 border ${borderPrimary}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`p-3 ${isDark ? 'bg-blue-500/10' : 'bg-blue-50'} rounded-xl`}>
                <BarChart3 className={`w-8 h-8 ${isDark ? 'text-blue-400' : 'text-blue-600'}`} />
              </div>
              <div>
                <h1 className={`text-2xl font-bold ${textPrimary}`}>Advanced Cricket Analytics Dashboard</h1>
                <p className={`${textSecondary} text-sm mt-0.5`}>Algorithmic insights powered by advanced data structures</p>
              </div>
            </div>
          </div>
        </div>

        <TeamSelector />

        {/* 1. Graph-Based Matchup Analysis */}
        <div className={`${bgSecondary} rounded-xl shadow-sm border ${borderPrimary}`}>
          <div className="p-5">
            <SectionHeader 
              icon={Network} 
              title="Graph-Based Player Matchup Analysis" 
              sectionKey="graphAnalysis"
            />
            
            {expandedSections.graphAnalysis && (
              <div className="mt-6 space-y-5">
                {/* Matchup Comparison Chart */}
                <div className={`${bgTertiary} p-5 rounded-lg border ${borderPrimary}`}>
                  <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                    Favorable vs Challenging Matchups Comparison
                  </h4>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={prepareMatchupComparisonData()}>
                      <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e5e7eb'} />
                      <XAxis dataKey="batter" stroke={isDark ? '#94a3b8' : '#6b7280'} style={{ fontSize: '12px' }} />
                      <YAxis stroke={isDark ? '#94a3b8' : '#6b7280'} style={{ fontSize: '12px' }} label={{ value: 'Runs/Ball', angle: -90, position: 'insideLeft', style: { fill: isDark ? '#94a3b8' : '#6b7280' } }} />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: isDark ? '#1e293b' : '#ffffff',
                          border: `1px solid ${isDark ? '#475569' : '#e5e7eb'}`,
                          borderRadius: '8px',
                          color: isDark ? '#f1f5f9' : '#111827'
                        }}
                      />
                      <Legend />
                      <Bar dataKey="favorable" fill="#10b981" name="Favorable" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="challenging" fill="#ef4444" name="Challenging" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                  {/* Weakest Bowler Matchups */}
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-green-900/30' : 'border-green-200'}`}>
                    <div className="flex items-center gap-2 mb-4">
                      <Target className={`w-5 h-5 ${isDark ? 'text-green-400' : 'text-green-600'}`} />
                      <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide`}>
                        Favorable Bowling Matchups
                      </h4>
                    </div>
                    <div className="space-y-2.5">
                      {Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.weakest_bowler_matchups || {}).map(([batter, data]) => (
                        <div key={batter} className={`${bgQuaternary} p-3.5 rounded-lg border ${borderPrimary} ${hoverBg} transition-colors`}>
                          <div className="flex justify-between items-center">
                            <div className="flex-1">
                              <div className={`font-semibold ${textPrimary} text-sm`}>{batter}</div>
                              <div className={`text-xs ${textSecondary} mt-1`}>
                                vs <span className={`${isDark ? 'text-green-400' : 'text-green-600'} font-medium`}>{data.bowler}</span>
                              </div>
                            </div>
                            <div className="text-right ml-4">
                              <div className={`text-xl font-bold ${isDark ? 'text-green-400' : 'text-green-600'}`}>{data.runs_per_ball}</div>
                              <div className={`text-xs ${textTertiary} uppercase`}>RPB</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Strongest Bowler Matchups */}
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-red-900/30' : 'border-red-200'}`}>
                    <div className="flex items-center gap-2 mb-4">
                      <Shield className={`w-5 h-5 ${isDark ? 'text-red-400' : 'text-red-600'}`} />
                      <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide`}>
                        Challenging Matchups
                      </h4>
                    </div>
                    <div className="space-y-2.5">
                      {Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.strongest_bowler_matchups || {}).map(([batter, data]) => (
                        <div key={batter} className={`${bgQuaternary} p-3.5 rounded-lg border ${borderPrimary} ${hoverBg} transition-colors`}>
                          <div className="flex justify-between items-center">
                            <div className="flex-1">
                              <div className={`font-semibold ${textPrimary} text-sm`}>{batter}</div>
                              <div className={`text-xs ${textSecondary} mt-1`}>
                                struggles vs <span className={`${isDark ? 'text-red-400' : 'text-red-600'} font-medium`}>{data.bowler}</span>
                              </div>
                            </div>
                            <div className="text-right ml-4">
                              <div className={`text-xl font-bold ${isDark ? 'text-red-400' : 'text-red-600'}`}>{data.runs_per_ball}</div>
                              <div className={`text-xs ${textTertiary} uppercase`}>RPB</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Bowler Centrality with Radar Chart */}
                <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-amber-900/30' : 'border-amber-200'}`}>
                  <div className="flex items-center gap-2 mb-4">
                    <Award className={`w-5 h-5 ${isDark ? 'text-amber-400' : 'text-amber-600'}`} />
                    <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide`}>
                      Bowler Centrality Rankings
                    </h4>
                  </div>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                    <div>
                      <ResponsiveContainer width="100%" height={250}>
                        <RadarChart data={prepareCentralityRadarData()}>
                          <PolarGrid stroke={isDark ? '#475569' : '#d1d5db'} />
                          <PolarAngleAxis dataKey="bowler" stroke={isDark ? '#94a3b8' : '#6b7280'} style={{ fontSize: '11px' }} />
                          <PolarRadiusAxis stroke={isDark ? '#94a3b8' : '#6b7280'} style={{ fontSize: '10px' }} />
                          <Radar name="Centrality" dataKey="centrality" stroke={COLORS[2]} fill={COLORS[2]} fillOpacity={0.6} />
                          <Tooltip 
                            contentStyle={{ 
                              backgroundColor: isDark ? '#1e293b' : '#ffffff',
                              border: `1px solid ${isDark ? '#475569' : '#e5e7eb'}`,
                              borderRadius: '8px'
                            }}
                          />
                        </RadarChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="space-y-2">
                      {Object.entries(dsa2Data.graph_analysis?.[selectedTeam]?.bowler_centrality || {}).slice(0, 5).map(([bowler, data], idx) => (
                        <div key={bowler} className={`${bgQuaternary} p-3 rounded-lg border ${borderPrimary} flex items-center gap-3`}>
                          <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xs ${
                            idx === 0 ? 'bg-amber-500 text-white' : 
                            idx === 1 ? 'bg-gray-400 text-white' : 
                            idx === 2 ? 'bg-orange-500 text-white' : 
                            isDark ? 'bg-blue-500 text-white' : 'bg-blue-600 text-white'
                          }`}>
                            #{idx + 1}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className={`font-semibold ${textPrimary} text-sm truncate`}>{bowler}</div>
                            <div className={`text-xs ${textTertiary} font-mono mt-0.5`}>
                              {data.batters_faced}B • {data.wickets}W • {data.balls}Balls
                            </div>
                          </div>
                          <div className="text-right">
                            <div className={`text-lg font-bold ${isDark ? 'text-blue-400' : 'text-blue-600'}`}>{data.centrality_score}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Optimal Assignment */}
                {dsa2Data.graph_analysis?.[selectedTeam]?.optimal_assignment && (
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-purple-900/30' : 'border-purple-200'}`}>
                    <div className="flex items-center gap-2 mb-4">
                      <Zap className={`w-5 h-5 ${isDark ? 'text-purple-400' : 'text-purple-600'}`} />
                      <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide`}>
                        Optimal Bowler Assignment (Greedy Algorithm)
                      </h4>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                      {dsa2Data.graph_analysis[selectedTeam].optimal_assignment.map((assignment, idx) => (
                        <div key={idx} className={`${bgQuaternary} p-4 rounded-lg border ${borderPrimary} ${hoverBg} transition-colors`}>
                          <div className={`font-semibold ${textPrimary} text-sm mb-2`}>{assignment.batter}</div>
                          <div className={`text-xs ${textSecondary} mb-2`}>
                            → <span className={`${isDark ? 'text-purple-400' : 'text-purple-600'} font-medium`}>{assignment.bowler}</span>
                          </div>
                          <div className={`text-lg font-bold ${isDark ? 'text-purple-400' : 'text-purple-600'}`}>
                            {assignment.expected_runs_per_ball}
                            <span className={`text-xs ${textTertiary} ml-1 font-normal`}>RPB</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 2. Sliding Window Analysis */}
        <div className={`${bgSecondary} rounded-xl shadow-sm border ${borderPrimary}`}>
          <div className="p-5">
            <SectionHeader 
              icon={Activity} 
              title="Momentum Analysis (Sliding Window Algorithm)" 
              sectionKey="slidingWindow"
            />
            
            {expandedSections.slidingWindow && (
              <div className="mt-6 space-y-5">
                {/* Best Powerplay */}
                {dsa2Data.over_analysis?.[selectedTeam]?.best_powerplay && (
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-indigo-900/30' : 'border-indigo-200'}`}>
                    <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                      Optimal 6-Over Window Performance
                    </h4>
                    <div className="grid grid-cols-2 gap-4 mb-5">
                      <MetricCard 
                        label="Over Range"
                        value={`${dsa2Data.over_analysis[selectedTeam].best_powerplay.start_over}-${dsa2Data.over_analysis[selectedTeam].best_powerplay.end_over}`}
                      />
                      <MetricCard 
                        label="Total Runs"
                        value={dsa2Data.over_analysis[selectedTeam].best_powerplay.total_runs}
                      />
                    </div>
                    <div className="grid grid-cols-6 gap-2.5">
                      {dsa2Data.over_analysis[selectedTeam].best_powerplay.overs.map((over, idx) => (
                        <div key={idx} className={`${bgQuaternary} border ${borderPrimary} px-3 py-3 rounded-lg text-center`}>
                          <div className={`text-xs ${textTertiary} font-semibold mb-1`}>O{over.over}</div>
                          <div className={`font-bold text-lg ${isDark ? 'text-indigo-400' : 'text-indigo-600'}`}>{over.runs}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Rolling Run Rate with Chart */}
                {dsa2Data.over_analysis?.[selectedTeam]?.rolling_run_rate && (
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-cyan-900/30' : 'border-cyan-200'}`}>
                    <div className="flex items-center gap-2 mb-4">
                      <TrendingUp className={`w-5 h-5 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`} />
                      <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide`}>
                        Rolling Run Rate Analysis
                      </h4>
                    </div>
                    <ResponsiveContainer width="100%" height={250}>
                      <LineChart data={prepareRunRateChartData()}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e5e7eb'} />
                        <XAxis dataKey="over" stroke={isDark ? '#94a3b8' : '#6b7280'} style={{ fontSize: '12px' }} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#6b7280'} style={{ fontSize: '12px' }} label={{ value: 'Run Rate', angle: -90, position: 'insideLeft', style: { fill: isDark ? '#94a3b8' : '#6b7280' } }} />
                        <Tooltip 
                          contentStyle={{ 
                            backgroundColor: isDark ? '#1e293b' : '#ffffff',
                            border: `1px solid ${isDark ? '#475569' : '#e5e7eb'}`,
                            borderRadius: '8px'
                          }}
                        />
                        <Line type="monotone" dataKey="runRate" stroke={isDark ? '#22d3ee' : '#0891b2'} strokeWidth={2} dot={{ fill: isDark ? '#22d3ee' : '#0891b2', r: 4 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 3. BST Search Results */}
        <div className={`${bgSecondary} rounded-xl shadow-sm border ${borderPrimary}`}>
          <div className="p-5">
            <SectionHeader 
              icon={Search} 
              title="Binary Search Tree Query Results" 
              sectionKey="bstSearch"
            />
            
            {expandedSections.bstSearch && (
              <div className="mt-6 space-y-5">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                  {/* 30+ Runs */}
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-green-900/30' : 'border-green-200'}`}>
                    <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                      Batters: Runs ≥ 30
                    </h4>
                    <div className="space-y-2">
                      {dsa2Data.bst_search?.[selectedTeam]?.batters_above_30?.map((batter, idx) => (
                        <div key={idx} className={`${bgQuaternary} p-3 rounded-lg border ${borderPrimary} flex justify-between items-center`}>
                          <span className={`font-medium ${textPrimary} text-sm`}>{batter.player}</span>
                          <span className={`${isDark ? 'text-green-400' : 'text-green-600'} font-bold font-mono text-sm`}>{batter.runs}</span>
                        </div>
                      )) || <p className={`${textTertiary} text-sm`}>No players found</p>}
                    </div>
                  </div>

                  {/* 50+ Runs */}
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-amber-900/30' : 'border-amber-200'}`}>
                    <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                      Batters: Runs ≥ 50
                    </h4>
                    <div className="space-y-2">
                      {dsa2Data.bst_search?.[selectedTeam]?.batters_above_50?.map((batter, idx) => (
                        <div key={idx} className={`${bgQuaternary} p-3 rounded-lg border ${borderPrimary} flex justify-between items-center`}>
                          <span className={`font-medium ${textPrimary} text-sm`}>{batter.player}</span>
                          <span className={`${isDark ? 'text-amber-400' : 'text-amber-600'} font-bold font-mono text-sm`}>{batter.runs}</span>
                        </div>
                      )) || <p className={`${textTertiary} text-sm`}>No players found</p>}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 4. Dynamic Programming - Bowling Allocation */}
        <div className={`${bgSecondary} rounded-xl shadow-sm border ${borderPrimary}`}>
          <div className="p-5">
            <SectionHeader 
              icon={Clock} 
              title="Dynamic Programming: Bowling Optimization" 
              sectionKey="dpAllocation"
            />
            
            {expandedSections.dpAllocation && dsa2Data.optimal_bowling_allocation?.[selectedTeam] && (
              <div className="mt-6">
                <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-orange-900/30' : 'border-orange-200'}`}>
                  <div className={`mb-5 p-5 ${bgQuaternary} rounded-lg border ${borderPrimary}`}>
                    <div className={`text-xs font-semibold ${textTertiary} uppercase tracking-wider mb-2`}>
                      Minimized Expected Runs
                    </div>
                    <div className={`text-4xl font-bold ${isDark ? 'text-orange-400' : 'text-orange-600'}`}>
                      {dsa2Data.optimal_bowling_allocation[selectedTeam].min_expected_runs}
                    </div>
                  </div>
                  <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                    Optimal Over Distribution
                  </h4>
                  <div className="space-y-2.5">
                    {dsa2Data.optimal_bowling_allocation[selectedTeam].allocation.filter(a => a.overs > 0).map((allocation, idx) => (
                      <div key={idx} className={`${bgQuaternary} p-4 rounded-lg border ${borderPrimary} flex justify-between items-center`}>
                        <span className={`font-medium ${textPrimary} text-sm`}>{allocation.bowler}</span>
                        <span className={`${isDark ? 'text-orange-400' : 'text-orange-600'} font-bold font-mono`}>{allocation.overs} overs</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 5. Pattern Detection (Hashing) */}
        <div className={`${bgSecondary} rounded-xl shadow-sm border ${borderPrimary}`}>
          <div className="p-5">
            <SectionHeader 
              icon={Activity} 
              title="Hash-Based Pattern Detection" 
              sectionKey="patterns"
            />
            
            {expandedSections.patterns && (
              <div className="mt-6 space-y-5">
                {/* Scoring Patterns */}
                <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-pink-900/30' : 'border-pink-200'}`}>
                  <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                    Recurring Score Sequences
                  </h4>
                  <div className="space-y-2">
                    {Object.entries(dsa2Data.pattern_detection?.[selectedTeam]?.scoring_patterns || {}).slice(0, 5).map(([pattern, count]) => (
                      <div key={pattern} className={`${bgQuaternary} p-3 rounded-lg border ${borderPrimary} flex justify-between items-center`}>
                        <span className={`font-mono text-sm ${textPrimary}`}>{pattern}</span>
                        <span className={`${isDark ? 'text-pink-400' : 'text-pink-600'} font-bold`}>{count}x</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Duplicate Overs */}
                {dsa2Data.pattern_detection?.[selectedTeam]?.duplicate_overs?.length > 0 && (
                  <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-rose-900/30' : 'border-rose-200'}`}>
                    <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                      Identical Over Performances
                    </h4>
                    <div className="space-y-2">
                      {dsa2Data.pattern_detection[selectedTeam].duplicate_overs.map((dup, idx) => (
                        <div key={idx} className={`${bgQuaternary} p-3 rounded-lg border ${borderPrimary}`}>
                          <div className={`font-medium ${textPrimary} font-mono text-sm`}>{dup.pattern}</div>
                          <div className={`text-xs ${textSecondary} mt-1`}>Overs: {dup.overs.join(', ')}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 6. Batter Clusters (Union-Find) */}
        <div className={`${bgSecondary} rounded-xl shadow-sm border ${borderPrimary}`}>
          <div className="p-5">
            <SectionHeader 
              icon={Users} 
              title="Union-Find: Dismissal Pattern Clustering" 
              sectionKey="clusters"
            />
            
            {expandedSections.clusters && (
              <div className="mt-6">
                <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-violet-900/30' : 'border-violet-200'}`}>
                  <div className="space-y-4">
                    {Object.entries(dsa2Data.batter_clusters?.[selectedTeam] || {}).map(([cluster, batters]) => (
                      <div key={cluster} className={`${bgQuaternary} p-4 rounded-lg border ${borderPrimary}`}>
                        <h4 className={`font-semibold ${isDark ? 'text-violet-400' : 'text-violet-600'} mb-3 uppercase text-xs tracking-wide`}>{cluster}</h4>
                        <div className="flex flex-wrap gap-2">
                          {batters.map((batter, idx) => (
                            <span key={idx} className={`${isDark ? 'bg-violet-500/10 border-violet-500/30 text-violet-300' : 'bg-violet-50 border-violet-300 text-violet-700'} border px-3 py-1.5 rounded-lg text-sm font-medium`}>
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
        </div>

        {/* 7. Next Bowler Recommendation (Priority Queue) */}
        <div className={`${bgSecondary} rounded-xl shadow-sm border ${borderPrimary}`}>
          <div className="p-5">
            <SectionHeader 
              icon={Target} 
              title="Priority Queue: Optimal Bowler Selection" 
              sectionKey="nextBowler"
            />
            
            {expandedSections.nextBowler && dsa2Data.next_bowler_recommendation?.[selectedTeam] && (
              <div className="mt-6">
                <div className={`${bgTertiary} p-5 rounded-lg border ${isDark ? 'border-green-900/30' : 'border-green-200'}`}>
                  <h4 className={`text-sm font-semibold ${textPrimary} uppercase tracking-wide mb-4`}>
                    Recommended Next Bowler
                  </h4>
                  <div className={`${bgQuaternary} p-6 rounded-lg border ${borderPrimary}`}>
                    <div className={`text-3xl font-bold ${isDark ? 'text-green-400' : 'text-green-600'} mb-6`}>
                      {dsa2Data.next_bowler_recommendation[selectedTeam].name}
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                      <MetricCard 
                        label="Economy"
                        value={dsa2Data.next_bowler_recommendation[selectedTeam].economy.toFixed(2)}
                      />
                      <MetricCard 
                        label="Wickets"
                        value={dsa2Data.next_bowler_recommendation[selectedTeam].wickets}
                      />
                      <MetricCard 
                        label="Overs Left"
                        value={dsa2Data.next_bowler_recommendation[selectedTeam].overs_left}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DSA2Analysis;