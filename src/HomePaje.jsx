import React, { useState, useEffect } from "react";
import {
  Trophy,
  TrendingUp,
  Target,
  Users,
  Swords,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const CricketAnalyzer = () => {
  const [selectedBattingStat, setSelectedBattingStat] = useState(null);
  const [selectedBowlingStat, setSelectedBowlingStat] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState("teamA");
  const [selectedBatter, setSelectedBatter] = useState(null);
  const [matchData, setMatchData] = useState();
  const [extras, setExtras] = useState(null);
  const[bowlerBRuns, setBowlerBRuns] = useState(null);
  const[bowlerBWickets, setBowlerBWickets] = useState(null);
  const[bowlerBEconomy, setBowlerBEconomy] = useState(null);
  const [oversData,setOversData] = useState(null);


  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-800 text-white p-4 rounded-lg shadow-lg border border-slate-600">
          <p className="font-bold text-lg mb-2">Over {data.over}</p>
          <div className="space-y-1">
            <p className="text-green-300">Pakistan: {data.teamA} runs {data.teamAWickets > 0 && `(${data.teamAWickets}W)`}</p>
            <p className="text-blue-300">India: {data.teamB} runs {data.teamBWickets > 0 && `(${data.teamBWickets}W)`}</p>
          </div>
        </div>
      );
    }
    return null;
  };

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/cricket-analysis", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();
        setOversData(data.overs);
        setExtras(data.extras);
        setBowlerBRuns(data.bowlers_runs);
        setBowlerBWickets(data.bowlers_wickets);
        setBowlerBEconomy(data.bowlers_economy);
        setMatchData({
          teamA: {
            name: "Pakistan",
            score: "146/10",
            overs: "19.1",
            won: false,
          },
          teamB: {
            name: "India",
            score: "150/5",
            overs: "19.4",
            won: true,
          },
          battingStats: {
            teamA: data.battersB,
            teamB: data.batters
          },
          bowlingStats: {
            teamA: data.bowlers,
            teamB: [
              {
                player: "Deepak Chahar",
                overs: 4,
                runs: 28,
                wickets: 3,
                economy: 7.0,
                maidens: 0,
              },
              {
                player: "Matheesha Pathirana",
                overs: 4,
                runs: 35,
                wickets: 2,
                economy: 8.75,
                maidens: 0,
              },
              {
                player: "Tushar Deshpande",
                overs: 4,
                runs: 48,
                wickets: 0,
                economy: 12.0,
                maidens: 0,
              },
              {
                player: "Ravindra Jadeja",
                overs: 4,
                runs: 36,
                wickets: 1,
                economy: 9.0,
                maidens: 0,
              },
              {
                player: "Moeen Ali",
                overs: 4,
                runs: 38,
                wickets: 0,
                economy: 9.5,
                maidens: 0,
              },
            ],
          },
          partnerships: {
            teamA: data.partnershipsB,
            teamB: data.partnerships,
          },
          batterVsBowler: {
            teamA: data.batterVsBowlerB,
            teamB: data.batterVsBowler,
          },
        });
      } catch (error) {
        console.error("Error fetching cricket analysis:", error);
      }
    };

    fetchAnalysis();
  }, []);

  const getSortedBattingStats = (stat) => {
    const stats = matchData.battingStats[selectedTeam];
    return stats;
  };

  const getSortedBowlingStats = (stat) => {
    if(selectedTeam==="teamA"){
      if (stat === "economy") {
      return bowlerBEconomy; // Ascending for economy
    }else if(stat === "wickets"){
      return bowlerBWickets;
    }else{
      return bowlerBRuns;
    }
    }
    const stats = matchData.bowlingStats[selectedTeam];
    return stats;
  };

  const BattingStatButton = ({ stat, label, icon: Icon }) => (
    <button
      onClick={() =>
        setSelectedBattingStat(selectedBattingStat === stat ? null : stat)
      }
      className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
        selectedBattingStat === stat
          ? "bg-blue-600 text-white shadow-lg scale-105"
          : "bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 hover:from-blue-100 hover:to-blue-200"
      }`}
    >
      <Icon className="w-5 h-5" />
      {label}
      {selectedBattingStat === stat ? (
        <ChevronUp className="w-4 h-4" />
      ) : (
        <ChevronDown className="w-4 h-4" />
      )}
    </button>
  );

  const BowlingStatButton = ({ stat, label, icon: Icon }) => (
    <button
      onClick={() =>
        setSelectedBowlingStat(selectedBowlingStat === stat ? null : stat)
      }
      className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
        selectedBowlingStat === stat
          ? "bg-green-600 text-white shadow-lg scale-105"
          : "bg-gradient-to-r from-green-50 to-green-100 text-green-700 hover:from-green-100 hover:to-green-200"
      }`}
    >
      <Icon className="w-5 h-5" />
      {label}
      {selectedBowlingStat === stat ? (
        <ChevronUp className="w-4 h-4" />
      ) : (
        <ChevronDown className="w-4 h-4" />
      )}
    </button>
  );

  return (
    matchData ? (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-green-50 to-blue-50 p-6">
      <div className=" mx-auto">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-green-600 rounded-2xl shadow-2xl p-8 mb-8 text-white">
          <div className="text-center mb-6">
            <h1 className="text-4xl font-bold mb-2">Match Analysis</h1>
            <p className="text-blue-100">T20 Cricket - Complete Statistics</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            <div
              className={`text-center p-6 rounded-xl ${
                matchData.teamA.won
                  ? "bg-green-500 bg-opacity-30 border-2 border-green-300"
                  : "bg-green-500 bg-opacity-30 border-2 border-green-300"
              }`}
            >
              <h2 className="text-2xl font-bold mb-2">
                {matchData.teamA.name}
              </h2>
              <div className="text-5xl font-extrabold mb-1">
                {matchData.teamA.score}
              </div>
              <div className="text-lg opacity-90">
                {matchData.teamA.overs} overs
              </div>
              {matchData.teamA.won && (
                <div className="mt-3 flex items-center justify-center gap-2 text-yellow-300">
                  <Trophy className="w-5 h-5" />
                  <span className="font-bold">WINNER</span>
                </div>
              )}
            </div>

            <div className="text-center">
              <div className="text-6xl font-black opacity-90">VS</div>
            </div>

            <div
              className={`text-center p-6 rounded-xl ${
                matchData.teamB.won
                  ? "bg-blue-500 bg-opacity-10"
                  : "bg-blue-500 bg-opacity-10"
              }`}
            >
              <h2 className="text-2xl font-bold mb-2">
                {matchData.teamB.name}
              </h2>
              <div className="text-5xl font-extrabold mb-1">
                {matchData.teamB.score}
              </div>
              <div className="text-lg opacity-90">
                {matchData.teamB.overs} overs
              </div>
              {matchData.teamB.won && (
                <div className="mt-3 flex items-center justify-center gap-2 text-yellow-300">
                  <Trophy className="w-5 h-5" />
                  <span className="font-bold">WINNER</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Team Selector */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => {
                setSelectedTeam("teamA");
                setSelectedBattingStat(null);
              }}
              className={`px-6 py-3 rounded-lg font-bold transition-all ${
                selectedTeam === "teamA"
                  ? "bg-green-600 text-white shadow-lg"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              {matchData.teamA.name}
            </button>
            <button
              onClick={() => {
                setSelectedTeam("teamB");
                setSelectedBattingStat(null);
              }}
              className={`px-6 py-3 rounded-lg font-bold transition-all ${
                selectedTeam === "teamB"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              {matchData.teamB.name}
            </button>
          </div>

        {/* Batting Analysis */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="w-8 h-8 text-blue-600" />
            <h2 className="text-3xl font-bold text-slate-800">
              Batting Analysis
            </h2>
          </div>

          

          {/* Stat Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <BattingStatButton stat="runs" label="Runs" icon={TrendingUp} />
            <BattingStatButton stat="sr" label="Strike Rate" icon={Target} />
            <BattingStatButton
              stat="fours"
              label="Fours (4s)"
              icon={TrendingUp}
            />
            <BattingStatButton stat="sixes" label="Sixes (6s)" icon={Target} />
          </div>

          {/* Stats Display */}
          {selectedBattingStat && (
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-xl border-2 border-blue-200">
              <h3 className="text-xl font-bold text-blue-700 mb-4">
                {selectedBattingStat === "runs" && "Runs Scored"}
                {selectedBattingStat === "sr" && "Strike Rate"}
                {selectedBattingStat === "fours" && "Fours Hit"}
                {selectedBattingStat === "sixes" && "Sixes Hit"}
              </h3>
              <div className="space-y-3">
                {getSortedBattingStats(selectedBattingStat).map(
                  (player, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-center gap-4">
                        <div
                          className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-white ${
                            idx === 0
                              ? "bg-gradient-to-br from-yellow-400 to-yellow-600"
                              : idx === 1
                              ? "bg-gradient-to-br from-gray-300 to-gray-500"
                              : idx === 2
                              ? "bg-gradient-to-br from-orange-400 to-orange-600"
                              : "bg-gradient-to-br from-blue-400 to-blue-600"
                          }`}
                        >
                          {idx + 1}
                        </div>
                        <div>
                          <div className="font-bold text-slate-800">
                            {player.player}
                          </div>
                          <div className="text-sm text-slate-600">
                            {player.runs} runs ({player.balls} balls) • SR:{" "}
                            {player.sr}
                          </div>
                        </div>
                      </div>
                      <div className="text-2xl font-bold text-blue-600">
                        {selectedBattingStat === "sr"
                          ? player[selectedBattingStat].toFixed(1)
                          : player[selectedBattingStat]}
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}
        </div>

        {/* Bowling Analysis */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Target className="w-8 h-8 text-green-600" />
            <h2 className="text-3xl font-bold text-slate-800">
              Bowling Analysis
            </h2>
          </div>

          {/* Stat Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
            <BowlingStatButton stat="wickets" label="Wickets" icon={Target} />
            <BowlingStatButton
              stat="economy"
              label="Economy"
              icon={TrendingUp}
            />
            <BowlingStatButton
              stat="runs"
              label="Runs Conceded"
              icon={Target}
            />
          </div>

          {/* Stats Display */}
          {selectedBowlingStat && (
            <div className="bg-gradient-to-br from-green-50 to-white p-6 rounded-xl border-2 border-green-200">
              <h3 className="text-xl font-bold text-green-700 mb-4">
                {selectedBowlingStat === "wickets" && "Wickets Taken"}
                {selectedBowlingStat === "economy" &&
                  "Economy Rate (Best to Worst)"}
                {selectedBowlingStat === "runs" && "Runs Conceded"}
              </h3>
              <div className="space-y-3">
                {getSortedBowlingStats(selectedBowlingStat).map(
                  (player, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-center gap-4">
                        <div
                          className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-white ${
                            idx === 0
                              ? "bg-gradient-to-br from-yellow-400 to-yellow-600"
                              : idx === 1
                              ? "bg-gradient-to-br from-gray-300 to-gray-500"
                              : idx === 2
                              ? "bg-gradient-to-br from-orange-400 to-orange-600"
                              : "bg-gradient-to-br from-green-400 to-green-600"
                          }`}
                        >
                          {idx + 1}
                        </div>
                        <div>
                          <div className="font-bold text-slate-800">
                            {player.name}
                          </div>
                          <div className="text-sm text-slate-600">
                            {player.wickets}-{player.runs} ({player.overs} ov) •
                            Econ: {player.economy}
                          </div>
                        </div>
                      </div>
                      <div className="text-2xl font-bold text-green-600">
                        {selectedBowlingStat === "economy"
                          ? player[selectedBowlingStat].toFixed(1)
                          : player[selectedBowlingStat]}
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}
        </div>

        {/* Partnerships */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Users className="w-8 h-8 text-blue-600" />
            <h2 className="text-3xl font-bold text-slate-800">
              Partnerships
            </h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-bold text-green-700 mb-4 pb-2 border-b-2 border-green-200">
                {matchData.teamA.name}
              </h3>
              <div className="space-y-3">
                {matchData.partnerships.teamA.map((p, idx) => (
                  <div
                    key={idx}
                    className="bg-gradient-to-r from-green-50 to-white p-4 rounded-lg border-l-4 border-green-500"
                  >
                    <div className="font-semibold text-slate-800">
                      {p.batsmen}
                    </div>
                    <div className="text-sm text-slate-600 mt-1">
                      <span className="font-bold text-green-600">
                        {p.runs} runs
                      </span>{" "}
                      off {p.balls} balls
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold text-blue-700 mb-4 pb-2 border-b-2 border-blue-200">
                {matchData.teamB.name}
              </h3>
              <div className="space-y-3">
                {matchData.partnerships.teamB.map((p, idx) => (
                  <div
                    key={idx}
                    className="bg-gradient-to-r from-blue-50 to-white p-4 rounded-lg border-l-4 border-blue-500"
                  >
                    <div className="font-semibold text-slate-800">
                      {p.batsmen}
                    </div>
                    <div className="text-sm text-slate-600 mt-1">
                      <span className="font-bold text-blue-600">
                        {p.runs} runs
                      </span>{" "}
                      off {p.balls} balls
                    </div>
                  </div>
                ))}
              </div>
            </div>

            
          </div>
        </div>

        {/* Batter vs Bowler */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="flex items-center gap-3 mb-6">
            <Swords className="w-8 h-8 text-green-600" />
            <h2 className="text-3xl font-bold text-slate-800">
              Batter vs Bowler Analysis
            </h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-bold text-green-700 mb-4 pb-2 border-b-2 border-green-200">
                {matchData.teamA.name} Batters
              </h3>
              <div className="space-y-3">
                {Object.keys(matchData.batterVsBowler.teamA).map(
                  (batter, idx) => (
                    <div key={idx}>
                      <button
                        onClick={() =>
                          setSelectedBatter(
                            selectedBatter === `teamB-${batter}`
                              ? null
                              : `teamB-${batter}`
                          )
                        }
                        className={`w-full text-left p-4 rounded-lg transition-all ${
                          selectedBatter === `teamB-${batter}`
                            ? "bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg"
                            : "bg-gradient-to-r from-green-50 to-white border border-green-200 hover:from-green-100 hover:to-green-50"
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="font-bold text-lg">{batter}</div>
                          {selectedBatter === `teamB-${batter}` ? (
                            <ChevronUp className="w-5 h-5" />
                          ) : (
                            <ChevronDown className="w-5 h-5" />
                          )}
                        </div>
                        {selectedBatter !== `teamB-${batter}` && (
                          <div className="text-sm mt-1 opacity-75">
                            Click to see all bowlers faced
                          </div>
                        )}
                      </button>

                      {selectedBatter === `teamB-${batter}` && (
                        <div className="mt-3 space-y-2 pl-4">
                          {matchData.batterVsBowler.teamA[batter].map(
                            (matchup, mIdx) => (
                              <div
                                key={mIdx}
                                className="bg-white p-4 rounded-lg border-l-4 border-green-500 shadow-sm"
                              >
                                <div className="flex items-center justify-between mb-2">
                                  <div className="font-semibold text-slate-800">
                                    vs {matchup.bowler}
                                  </div>
                                  <Swords className="w-4 h-4 text-green-400" />
                                </div>
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                  <div>
                                    <span className="text-slate-600">
                                      Runs:{" "}
                                    </span>
                                    <span className="text-green-600 font-bold">
                                      {matchup.runs}
                                    </span>
                                  </div>
                                  <div>
                                    <span className="text-slate-600">
                                      Balls:{" "}
                                    </span>
                                    <span className="text-slate-700 font-semibold">
                                      {matchup.balls}
                                    </span>
                                  </div>
                                  <div>
                                    <span className="text-slate-600">
                                      Strike Rate:{" "}
                                    </span>
                                    <span className="text-green-600 font-bold">
                                      {matchup.sr.toFixed(1)}
                                    </span>
                                  </div>
                                  <div>
                                    {matchup.wicket ? (
                                      <span className="text-red-600 font-bold">
                                        WICKET
                                      </span>
                                    ) : (
                                      <span className="text-green-600 font-semibold">
                                        Not Out
                                      </span>
                                    )}
                                  </div>
                                </div>
                              </div>
                            )
                          )}
                        </div>
                      )}
                    </div>
                  )
                )}
              </div>
            </div>
            <div>
              <h3 className="text-xl font-bold text-blue-700 mb-4 pb-2 border-b-2 border-blue-200">
                {matchData.teamB.name} Batters
              </h3>
              <div className="space-y-3">
                {Object.keys(matchData.batterVsBowler.teamB).map(
                  (batter, idx) => (
                    <div key={idx}>
                      <button
                        onClick={() =>
                          setSelectedBatter(
                            selectedBatter === `teamA-${batter}`
                              ? null
                              : `teamA-${batter}`
                          )
                        }
                        className={`w-full text-left p-4 rounded-lg transition-all ${
                          selectedBatter === `teamA-${batter}`
                            ? "bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg"
                            : "bg-gradient-to-r from-blue-50 to-white border border-blue-200 hover:from-blue-100 hover:to-blue-50"
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="font-bold text-lg">{batter}</div>
                          {selectedBatter === `teamA-${batter}` ? (
                            <ChevronUp className="w-5 h-5" />
                          ) : (
                            <ChevronDown className="w-5 h-5" />
                          )}
                        </div>
                        {selectedBatter !== `teamA-${batter}` && (
                          <div className="text-sm mt-1 opacity-75">
                            Click to see all bowlers faced
                          </div>
                        )}
                      </button>

                      {selectedBatter === `teamA-${batter}` && (
                        <div className="mt-3 space-y-2 pl-4">
                          {matchData.batterVsBowler.teamB[batter].map(
                            (matchup, mIdx) => (
                              <div
                                key={mIdx}
                                className="bg-white p-4 rounded-lg border-l-4 border-blue-500 shadow-sm"
                              >
                                <div className="flex items-center justify-between mb-2">
                                  <div className="font-semibold text-slate-800">
                                    vs {matchup.bowler}
                                  </div>
                                  <Swords className="w-4 h-4 text-blue-400" />
                                </div>
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                  <div>
                                    <span className="text-slate-600">
                                      Runs:{" "}
                                    </span>
                                    <span className="text-blue-600 font-bold">
                                      {matchup.runs}
                                    </span>
                                  </div>
                                  <div>
                                    <span className="text-slate-600">
                                      Balls:{" "}
                                    </span>
                                    <span className="text-slate-700 font-semibold">
                                      {matchup.balls}
                                    </span>
                                  </div>
                                  <div>
                                    <span className="text-slate-600">
                                      Strike Rate:{" "}
                                    </span>
                                    <span className="text-blue-600 font-bold">
                                      {matchup.sr.toFixed(1)}
                                    </span>
                                  </div>
                                  <div>
                                    {matchup.wicket ? (
                                      <span className="text-red-600 font-bold">
                                        WICKET
                                      </span>
                                    ) : (
                                      <span className="text-green-600 font-semibold">
                                        Not Out
                                      </span>
                                    )}
                                  </div>
                                </div>
                              </div>
                            )
                          )}
                        </div>
                      )}
                    </div>
                  )
                )}
              </div>
            </div>

            
          </div>
        </div>

        {/* Over Summary */}
        <div className="w-full min-h-screen  p-8 flex flex-col items-center justify-center">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full">
        {/* <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-slate-800 mb-6">
            Team Comparison - Over by Over
          </h1>
          
          <div className="grid grid-cols-2 gap-6 max-w-4xl mx-auto">
            <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-white mb-3">Pakistan</h3>
              <div className="flex justify-around">
                <div>
                  <p className="text-sm text-green-100">Runs</p>
                  <p className="text-3xl font-bold text-white">{teamATotal}</p>
                </div>
                <div>
                  <p className="text-sm text-green-100">Wickets</p>
                  <p className="text-3xl font-bold text-white">{teamAWicketsTotal}</p>
                </div>
                <div>
                  <p className="text-sm text-green-100">Run Rate</p>
                  <p className="text-3xl font-bold text-white">{(teamATotal / oversData.length).toFixed(1)}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-white mb-3">India</h3>
              <div className="flex justify-around">
                <div>
                  <p className="text-sm text-blue-100">Runs</p>
                  <p className="text-3xl font-bold text-white">{teamBTotal}</p>
                </div>
                <div>
                  <p className="text-sm text-blue-100">Wickets</p>
                  <p className="text-3xl font-bold text-white">{teamBWicketsTotal}</p>
                </div>
                <div>
                  <p className="text-sm text-blue-100">Run Rate</p>
                  <p className="text-3xl font-bold text-white">{(teamBTotal / oversData.length).toFixed(1)}</p>
                </div>
              </div>
            </div>
          </div>
        </div> */}
        
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={oversData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="over" 
              label={{ value: 'Over Number', position: 'insideBottom', offset: -10, fill: '#475569' }}
              tick={{ fill: '#475569', fontSize: 13, fontWeight: 'bold' }}
            />
            <YAxis 
              label={{ value: 'Runs', angle: -90, position: 'insideLeft', fill: '#475569' }}
              tick={{ fill: '#475569', fontSize: 12 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              verticalAlign="bottom" 
              height={36}
              wrapperStyle={{ paddingTop: '20px' }}
            />
            <Bar dataKey="teamA" fill="#16a34a" name="Pakistan" radius={[8, 8, 0, 0]} />
            <Bar dataKey="teamB" fill="#3b82f6" name="India" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-8">
          <h3 className="text-xl font-bold text-center text-slate-800 mb-4">Over-by-Over Breakdown</h3>
          <div className="grid grid-cols-5 gap-3">
            {oversData.map((over, index) => (
              <div 
                key={index}
                className="bg-slate-50 p-4 rounded-lg shadow border-2 border-slate-200"
              >
                <div className="text-center mb-3">
                  <div className="text-sm font-bold text-slate-700 mb-2">Over {over.over}</div>
                </div>
                
                <div className="space-y-2">
                  <div className="bg-green-100 rounded p-2 border-l-4 border-green-600">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-green-700">Pakistan</span>
                      <span className="text-lg font-bold text-green-900">{over.teamA}</span>
                    </div>
                    {over.teamAWickets > 0 && (
                      <div className="text-xs text-green-600 mt-1">
                        {over.teamAWickets} wicket{over.teamAWickets > 1 ? 's' : ''}
                      </div>
                    )}
                  </div>
                  
                  <div className="bg-blue-100 rounded p-2 border-l-4 border-blue-500">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-blue-700">India</span>
                      <span className="text-lg font-bold text-blue-900">{over.teamB}</span>
                    </div>
                    {over.teamBWickets > 0 && (
                      <div className="text-xs text-blue-600 mt-1">
                        {over.teamBWickets} wicket{over.teamBWickets > 1 ? 's' : ''}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
      </div>
    </div>
    ): (
        <p>Loading</p>
    )
    
  );
};

export default CricketAnalyzer;
