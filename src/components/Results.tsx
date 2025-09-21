import React, { useState } from 'react';
import { Search, Filter, Star, CheckCircle, AlertCircle, XCircle, Eye, Download } from 'lucide-react';

export const Results: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [verdictFilter, setVerdictFilter] = useState('All');
  const [minScore, setMinScore] = useState(0);

  const mockResults = [
    {
      id: 1,
      resume_id: 123,
      job_id: 456,
      candidate_name: 'John Smith',
      job_title: 'Senior Python Developer',
      overall_score: 87.5,
      skills_match_score: 92.0,
      semantic_similarity_score: 85.0,
      experience_score: 85.0,
      verdict: 'High',
      matched_skills: ['Python', 'Django', 'PostgreSQL', 'AWS'],
      missing_skills: ['Kubernetes', 'Redis'],
      created_at: '2024-01-15T10:30:00Z'
    },
    {
      id: 2,
      resume_id: 124,
      job_id: 456,
      candidate_name: 'Sarah Johnson',
      job_title: 'Senior Python Developer',
      overall_score: 72.3,
      skills_match_score: 78.0,
      semantic_similarity_score: 70.0,
      experience_score: 69.0,
      verdict: 'Medium',
      matched_skills: ['Python', 'Flask', 'MySQL'],
      missing_skills: ['Django', 'PostgreSQL', 'AWS', 'Docker'],
      created_at: '2024-01-15T09:15:00Z'
    },
    {
      id: 3,
      resume_id: 125,
      job_id: 457,
      candidate_name: 'Mike Chen',
      job_title: 'Data Scientist',
      overall_score: 91.2,
      skills_match_score: 95.0,
      semantic_similarity_score: 88.0,
      experience_score: 90.0,
      verdict: 'High',
      matched_skills: ['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'SQL'],
      missing_skills: ['PyTorch'],
      created_at: '2024-01-14T16:45:00Z'
    },
    {
      id: 4,
      resume_id: 126,
      job_id: 458,
      candidate_name: 'Emily Davis',
      job_title: 'Full Stack Developer',
      overall_score: 45.8,
      skills_match_score: 52.0,
      semantic_similarity_score: 42.0,
      experience_score: 43.0,
      verdict: 'Low',
      matched_skills: ['JavaScript', 'HTML', 'CSS'],
      missing_skills: ['React', 'Node.js', 'MongoDB', 'Docker', 'AWS'],
      created_at: '2024-01-14T14:20:00Z'
    }
  ];

  const getVerdictIcon = (verdict: string) => {
    switch (verdict) {
      case 'High':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'Medium':
        return <AlertCircle className="w-5 h-5 text-yellow-600" />;
      case 'Low':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return null;
    }
  };

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'High':
        return 'text-green-700 bg-green-100';
      case 'Medium':
        return 'text-yellow-700 bg-yellow-100';
      case 'Low':
        return 'text-red-700 bg-red-100';
      default:
        return 'text-gray-700 bg-gray-100';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 75) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const SkillChip = ({ skill, type = 'matched' }: { skill: string; type?: 'matched' | 'missing' }) => (
    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium mr-1 mb-1 ${
      type === 'matched' 
        ? 'bg-green-100 text-green-800' 
        : 'bg-red-100 text-red-800'
    }`}>
      {skill}
    </span>
  );

  const filteredResults = mockResults.filter(result => {
    const matchesSearch = result.candidate_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         result.job_title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesVerdict = verdictFilter === 'All' || result.verdict === verdictFilter;
    const matchesScore = result.overall_score >= minScore;
    
    return matchesSearch && matchesVerdict && matchesScore;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <Star className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Results Analysis</h2>
            <p className="text-gray-600">Comprehensive analysis of resume-job matches</p>
          </div>
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search candidates or jobs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>

          <select
            value={verdictFilter}
            onChange={(e) => setVerdictFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value="All">All Verdicts</option>
            <option value="High">High Match</option>
            <option value="Medium">Medium Match</option>
            <option value="Low">Low Match</option>
          </select>

          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600 whitespace-nowrap">Min Score:</span>
            <input
              type="range"
              min="0"
              max="100"
              value={minScore}
              onChange={(e) => setMinScore(parseInt(e.target.value))}
              className="flex-1"
            />
            <span className="text-sm font-medium text-gray-900 w-8">{minScore}%</span>
          </div>

          <button className="flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors">
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Results Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Results</p>
              <p className="text-2xl font-bold text-gray-900">{filteredResults.length}</p>
            </div>
            <Filter className="w-8 h-8 text-gray-400" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">High Matches</p>
              <p className="text-2xl font-bold text-green-600">
                {filteredResults.filter(r => r.verdict === 'High').length}
              </p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-400" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Medium Matches</p>
              <p className="text-2xl font-bold text-yellow-600">
                {filteredResults.filter(r => r.verdict === 'Medium').length}
              </p>
            </div>
            <AlertCircle className="w-8 h-8 text-yellow-400" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Average Score</p>
              <p className="text-2xl font-bold text-blue-600">
                {filteredResults.length > 0 
                  ? Math.round(filteredResults.reduce((sum, r) => sum + r.overall_score, 0) / filteredResults.length)
                  : 0}%
              </p>
            </div>
            <Star className="w-8 h-8 text-blue-400" />
          </div>
        </div>
      </div>

      {/* Results List */}
      <div className="space-y-4">
        {filteredResults.map((result) => (
          <div key={result.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">{result.candidate_name}</h3>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getVerdictColor(result.verdict)}`}>
                    {getVerdictIcon(result.verdict)}
                    <span className="ml-1">{result.verdict} Match</span>
                  </span>
                </div>
                <p className="text-gray-600 mb-1">Applied for: <span className="font-medium">{result.job_title}</span></p>
                <p className="text-sm text-gray-500">Resume ID: #{result.resume_id} | Job ID: #{result.job_id}</p>
              </div>

              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <p className="text-sm text-gray-600">Overall Score</p>
                  <p className={`text-2xl font-bold ${getScoreColor(result.overall_score)}`}>
                    {result.overall_score.toFixed(1)}%
                  </p>
                </div>
                <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  <Eye className="w-4 h-4" />
                  <span>View Details</span>
                </button>
              </div>
            </div>

            {/* Score Breakdown */}
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <p className="text-sm text-gray-600">Skills Match</p>
                <p className={`text-lg font-semibold ${getScoreColor(result.skills_match_score)}`}>
                  {result.skills_match_score.toFixed(1)}%
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-600">Semantic Score</p>
                <p className={`text-lg font-semibold ${getScoreColor(result.semantic_similarity_score)}`}>
                  {result.semantic_similarity_score.toFixed(1)}%
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-600">Experience</p>
                <p className={`text-lg font-semibold ${getScoreColor(result.experience_score)}`}>
                  {result.experience_score.toFixed(1)}%
                </p>
              </div>
            </div>

            {/* Skills Analysis */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-2">✅ Matched Skills</h4>
                <div className="flex flex-wrap">
                  {result.matched_skills.map((skill, index) => (
                    <SkillChip key={index} skill={skill} type="matched" />
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-2">❌ Missing Skills</h4>
                <div className="flex flex-wrap">
                  {result.missing_skills.map((skill, index) => (
                    <SkillChip key={index} skill={skill} type="missing" />
                  ))}
                </div>
              </div>
            </div>

            {/* Timestamp */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                Evaluated on {new Date(result.created_at).toLocaleDateString()} at {new Date(result.created_at).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}

        {filteredResults.length === 0 && (
          <div className="text-center py-12 bg-white rounded-xl shadow-sm border border-gray-200">
            <Search className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
            <p className="text-gray-500">Try adjusting your filters or search terms</p>
          </div>
        )}
      </div>
    </div>
  );
};