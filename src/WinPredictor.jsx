import React, { useState, useEffect } from 'react';
import { TrendingUp, Trophy } from 'lucide-react';

export const CricketWinPredictor = ({predictingData}) => {
  const [teamAName, setTeamAName] = useState('Pakistan');
  const [teamBName, setTeamBName] = useState('India');
  const [teamATotal, setTeamATotal] = useState(146);
  const [teamAWickets, setTeamAWickets] = useState(10);
  const [totalOvers, setTotalOvers] = useState(20);
  const [matchData, setMatchData] = useState(predictingData);

  const getProbabilityColor = (prob) => {
    if (prob >= 70) return 'text-green-600';
    if (prob >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getProgressBarColor = (prob) => {
    if (prob >= 70) return 'bg-green-500';
    if (prob >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="mx-auto">
        <div className="bg-white rounded-2xl shadow-2xl p-8 mb-6">
          <h1 className="text-4xl font-bold text-center mb-8 text-indigo-900 flex items-center justify-center gap-3">
            <Trophy className="w-10 h-10" />
            Cricket Match Win Predictor
          </h1>

          {/* Over Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {matchData.map((data, idx) => (
              <div
                key={idx}
                className="bg-white border-2 border-gray-200 rounded-xl p-5 shadow-lg hover:shadow-2xl transition-all hover:scale-105"
              >
                {/* Over Header */}
                <div className="text-center mb-4">
                  <div className="inline-block bg-indigo-600 text-white px-4 py-1 rounded-full text-sm font-bold">
                    After Over {data.over}
                  </div>
                </div>

                {/* Match Score */}
                <div className="text-center mb-4 pb-4 border-b-2 border-gray-200">
                  <div className="flex items-center justify-center gap-2 text-lg font-bold text-gray-800">
                    <span className="text-green-600">{teamAName}</span>
                    <span>{teamATotal}/{teamAWickets}</span>
                  </div>
                  <div className="text-gray-400 font-bold my-1">vs</div>
                  <div className="flex items-center justify-center gap-2 text-lg font-bold text-gray-800">
                    <span className="text-blue-600">{teamBName}</span>
                    <span>{data.teamBScore}/{data.teamBWickets}</span>
                  </div>
                </div>

                {/* Win Probabilities */}
                <div className="space-y-3">
                  {/* Team A */}
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700">{teamAName}</span>
                      <span className={`text-xl font-bold ${getProbabilityColor(data.teamAWinProb)}`}>
                        {data.teamAWinProb.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                      <div
                        className={`h-full ${getProgressBarColor(data.teamAWinProb)} transition-all duration-500`}
                        style={{ width: `${data.teamAWinProb}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Team B */}
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700">{teamBName}</span>
                      <span className={`text-xl font-bold ${getProbabilityColor(data.teamBWinProb)}`}>
                        {data.teamBWinProb.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                      <div
                        className={`h-full ${getProgressBarColor(data.teamBWinProb)} transition-all duration-500`}
                        style={{ width: `${data.teamBWinProb}%` }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* Runs Needed */}
                <div className="mt-4 text-center">
                  <div className="text-xs text-gray-500">
                    {teamBName} needs {Math.max(0, teamATotal - data.teamBScore+1)} runs
                  </div>
                  <div className="text-xs text-gray-500">
                    from {(totalOvers - Math.floor(data.over)) * 6 - ((data.over - Math.floor(data.over))*10).toFixed(0)} balls
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default CricketWinPredictor;