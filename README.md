# Resume Relevance Check System

A comprehensive AI-powered resume-job matching platform that helps students find relevant opportunities and assists recruiters in identifying the best candidates.

## 🚀 Features

### For Students
- **Smart Resume Upload**: Upload resumes in PDF, DOCX, or TXT format
- **Skill Extraction**: Automatic extraction of technical and soft skills
- **Job Compatibility**: Get instant compatibility scores with job descriptions
- **Personalized Feedback**: Receive detailed suggestions for improvement

### For Recruiters
- **Job Posting Management**: Easy-to-use interface for posting job descriptions
- **Candidate Matching**: AI-powered matching with detailed scoring
- **Skills Analysis**: Automatic extraction of required skills from job descriptions
- **Candidate Pipeline**: Manage and review candidate applications

### Advanced Analytics
- **Multi-dimensional Scoring**: Skills match, semantic similarity, and experience scoring
- **Detailed Insights**: Comprehensive analysis with matched/missing skills
- **Real-time Dashboard**: Live statistics and match distribution
- **Export Capabilities**: Download results for further analysis

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Vite** for build tooling

### Backend
- **FastAPI** (Python) for REST API
- **SQLAlchemy** for database ORM
- **SQLite** for data storage
- **Sentence Transformers** for semantic analysis
- **NLTK** for natural language processing

### AI/ML Components
- **Resume Parsing**: Extract text from PDF, DOCX, TXT files
- **Skill Extraction**: Pattern matching and NLP-based skill identification
- **Semantic Matching**: Sentence transformer models for content similarity
- **Scoring Algorithm**: Multi-factor scoring with configurable weights

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **pip** (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd resume-relevance-system
```

### 2. Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from db import init_db; init_db()"

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### 3. Setup Frontend

```bash
# Navigate to project root (open new terminal)
cd resume-relevance-system

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Optional: Run Streamlit Demo

```bash
# In the project root directory
pip install streamlit plotly streamlit-option-menu streamlit-lottie

# Run the Streamlit demo
streamlit run streamlit_demo.py
```

The Streamlit demo will be available at `http://localhost:8501`

## 📁 Project Structure

```
resume-relevance-system/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application
│   ├── models.py           # Database models
│   ├── parsers.py          # Resume/JD parsing logic
│   ├── scoring.py          # Scoring algorithms
│   ├── db.py               # Database configuration
│   └── requirements.txt    # Python dependencies
├── src/                    # React frontend
│   ├── components/         # React components
│   │   ├── Header.tsx      # Navigation header
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── StudentPortal.tsx # Student interface
│   │   ├── RecruiterPortal.tsx # Recruiter interface
│   │   └── Results.tsx     # Results analysis
│   ├── App.tsx            # Main app component
│   └── main.tsx           # App entry point
├── samples/               # Sample files for testing
│   ├── sample_resume.txt  # Example resume
│   └── sample_jd.txt      # Example job description
└── streamlit_demo.py      # Streamlit demo application
```

## 🔧 API Endpoints

### Resume Management
- `POST /api/v1/resume/upload` - Upload and process resume
- `GET /api/v1/resume/{resume_id}` - Get resume details

### Job Description Management
- `POST /api/v1/jd/upload` - Upload job description
- `GET /api/v1/jobs` - List job descriptions

### Evaluation
- `POST /api/v1/evaluate/{resume_id}/{job_id}` - Evaluate resume against job
- `GET /api/v1/results` - Get evaluation results with filters

### Analytics
- `GET /api/v1/dashboard/stats` - Get dashboard statistics
- `GET /health` - Health check endpoint

## 🎯 Usage Examples

### Upload a Resume (Student)
1. Navigate to the Student Portal
2. Drag and drop your resume or click to browse
3. Optionally add job role and location preferences
4. Click "Analyze Resume" to process

### Post a Job (Recruiter)
1. Go to the Recruiter Portal
2. Fill in job details (title, company, location, experience)
3. Paste the complete job description
4. Click "Post Job" to publish

### View Results
1. Visit the Results section
2. Use filters to narrow down matches
3. View detailed scoring breakdowns
4. Export results for further analysis

## 🔍 Scoring Algorithm

The system uses a multi-dimensional scoring approach:

### 1. Skills Match Score (50% weight)
- Exact skill matching
- Fuzzy matching with 80% similarity threshold
- Percentage of required skills found

### 2. Semantic Similarity Score (30% weight)
- Sentence transformer embeddings
- Cosine similarity between resume and job description
- Fallback to TF-IDF similarity

### 3. Experience Score (20% weight)
- Comparison of candidate experience vs. required experience
- Bonus points for exceeding requirements
- Proportional scoring for less experience

### Overall Verdict Categories
- **High Match**: 75%+ overall score
- **Medium Match**: 50-74% overall score
- **Low Match**: <50% overall score

## 🐳 Docker Deployment

```bash
# Build and run backend with Docker
cd backend
docker build -t resume-backend .
docker run -p 8000:8000 resume-backend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the sample files in `/samples` for examples

## 🔮 Future Enhancements

- [ ] Machine learning model training on historical data
- [ ] Integration with job boards and ATS systems
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Real-time notifications
- [ ] Mobile application
- [ ] Video interview scheduling
- [ ] Skill gap analysis and learning recommendations

---

**ResumeMatch AI** - Revolutionizing recruitment with intelligent matching! 🚀
</README.md>