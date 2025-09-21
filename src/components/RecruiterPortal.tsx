import React, { useState } from 'react';
import { Plus, Building, MapPin, Clock, Users, Star, CheckCircle } from 'lucide-react';

export const RecruiterPortal: React.FC = () => {
  const [activeTab, setActiveTab] = useState('post');
  const [jobForm, setJobForm] = useState({
    title: '',
    company: '',
    location: '',
    experience_required: 0,
    content: ''
  });
  const [posting, setPosting] = useState(false);
  const [postResult, setPostResult] = useState<any>(null);

  const handleInputChange = (field: string, value: string | number) => {
    setJobForm(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobForm.title || !jobForm.content) return;

    setPosting(true);
    
    // Simulate API call
    setTimeout(() => {
      setPostResult({
        job_id: 456,
        required_skills: ['Python', 'Django', 'PostgreSQL', 'AWS', 'Docker'],
        experience_required: jobForm.experience_required,
        location: jobForm.location || 'Remote'
      });
      setPosting(false);
    }, 1500);
  };

  const mockJobs = [
    {
      id: 1,
      title: 'Senior Python Developer',
      company: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      experience_required: 5,
      candidates: 23,
      high_matches: 8,
      posted_date: '2024-01-15'
    },
    {
      id: 2,
      title: 'Data Scientist',
      company: 'AI Solutions Ltd.',
      location: 'New York, NY',
      experience_required: 3,
      candidates: 15,
      high_matches: 5,
      posted_date: '2024-01-14'
    },
    {
      id: 3,
      title: 'Full Stack Developer',
      company: 'StartupXYZ',
      location: 'Remote',
      experience_required: 2,
      candidates: 31,
      high_matches: 12,
      posted_date: '2024-01-13'
    }
  ];

  const SkillChip = ({ skill }: { skill: string }) => (
    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 mr-1 mb-1">
      {skill}
    </span>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <Users className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Recruiter Portal</h2>
            <p className="text-gray-600">Manage job postings and review candidate matches</p>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('post')}
            className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
              activeTab === 'post'
                ? 'bg-white text-purple-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Post New Job
          </button>
          <button
            onClick={() => setActiveTab('manage')}
            className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
              activeTab === 'manage'
                ? 'bg-white text-purple-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Manage Jobs
          </button>
        </div>
      </div>

      {activeTab === 'post' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Job Posting Form */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create Job Posting</h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Title *
                </label>
                <input
                  type="text"
                  value={jobForm.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  placeholder="e.g., Senior Python Developer"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Building className="w-4 h-4 inline mr-1" />
                  Company
                </label>
                <input
                  type="text"
                  value={jobForm.company}
                  onChange={(e) => handleInputChange('company', e.target.value)}
                  placeholder="e.g., TechCorp Inc."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <MapPin className="w-4 h-4 inline mr-1" />
                    Location
                  </label>
                  <input
                    type="text"
                    value={jobForm.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                    placeholder="e.g., San Francisco, CA"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Clock className="w-4 h-4 inline mr-1" />
                    Experience (Years)
                  </label>
                  <input
                    type="number"
                    value={jobForm.experience_required}
                    onChange={(e) => handleInputChange('experience_required', parseInt(e.target.value) || 0)}
                    min="0"
                    max="20"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Description *
                </label>
                <textarea
                  value={jobForm.content}
                  onChange={(e) => handleInputChange('content', e.target.value)}
                  placeholder="Paste the complete job description here..."
                  rows={8}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={posting || !jobForm.title || !jobForm.content}
                className="w-full bg-purple-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {posting ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Posting...</span>
                  </div>
                ) : (
                  <>
                    <Plus className="w-4 h-4 inline mr-2" />
                    Post Job
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Post Result */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Posting Results</h3>
            
            {!postResult ? (
              <div className="text-center py-12">
                <Plus className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">Fill out the form to post a new job</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Success Message */}
                <div className="flex items-center space-x-2 text-green-600 bg-green-50 p-3 rounded-lg">
                  <CheckCircle className="w-5 h-5" />
                  <span className="font-medium">Job posted successfully!</span>
                </div>

                {/* Job Info */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-sm text-gray-600">Job ID</p>
                    <p className="font-semibold text-gray-900">#{postResult.job_id}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-sm text-gray-600">Experience Required</p>
                    <p className="font-semibold text-gray-900">{postResult.experience_required} years</p>
                  </div>
                </div>

                {/* Location */}
                <div className="flex items-center space-x-2">
                  <MapPin className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Location:</span>
                  <span className="font-medium text-gray-900">{postResult.location}</span>
                </div>

                {/* Required Skills */}
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Required Skills Detected</h4>
                  <div className="flex flex-wrap">
                    {postResult.required_skills.map((skill: string, index: number) => (
                      <SkillChip key={index} skill={skill} />
                    ))}
                  </div>
                </div>

                {/* Next Steps */}
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="flex items-start space-x-2">
                    <Star className="w-5 h-5 text-purple-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-purple-900 mb-1">What's Next?</h4>
                      <p className="text-sm text-purple-700">
                        Your job is now live! Candidates can now apply and get matched against your requirements. Check the Results section to see candidate matches.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        /* Job Management */
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Active Job Postings</h3>
          
          <div className="space-y-4">
            {mockJobs.map((job) => (
              <div key={job.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="text-lg font-semibold text-gray-900">{job.title}</h4>
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                        Active
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                      <div className="flex items-center space-x-1">
                        <Building className="w-4 h-4" />
                        <span>{job.company}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPin className="w-4 h-4" />
                        <span>{job.location}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{job.experience_required}+ years</span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-6 text-sm">
                      <div className="flex items-center space-x-1">
                        <Users className="w-4 h-4 text-blue-600" />
                        <span className="text-gray-600">{job.candidates} candidates</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Star className="w-4 h-4 text-green-600" />
                        <span className="text-gray-600">{job.high_matches} high matches</span>
                      </div>
                      <span className="text-gray-500">Posted {job.posted_date}</span>
                    </div>
                  </div>

                  <div className="flex space-x-2">
                    <button className="px-4 py-2 text-purple-600 border border-purple-600 rounded-lg hover:bg-purple-50 transition-colors">
                      View Matches
                    </button>
                    <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                      Edit Job
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};