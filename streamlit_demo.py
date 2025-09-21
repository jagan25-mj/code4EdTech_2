import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Resume Relevance Check System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glassmorphism design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.18);
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.18);
        padding: 1.5rem;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .skill-chip {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .missing-skill-chip {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .verdict-high {
        color: #10B981;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .verdict-medium {
        color: #F59E0B;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .verdict-low {
        color: #EF4444;
        font-weight: bold;
        font-size: 1.2em;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def make_api_request(endpoint, method="GET", data=None, files=None):
    """Make API request with error handling."""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, data=data, files=files)
            else:
                response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to backend. Please ensure the API server is running."
    except Exception as e:
        return None, f"Error: {str(e)}"

def render_skills_chips(skills, chip_type="skill"):
    """Render skills as styled chips."""
    if not skills:
        return "No skills detected"
    
    chips_html = ""
    css_class = "skill-chip" if chip_type == "skill" else "missing-skill-chip"
    
    for skill in skills[:10]:  # Limit to first 10 skills
        chips_html += f'<span class="{css_class}">{skill}</span>'
    
    if len(skills) > 10:
        chips_html += f'<span class="{css_class}">+{len(skills)-10} more</span>'
    
    return chips_html

def render_verdict(verdict):
    """Render verdict with appropriate styling."""
    css_class = f"verdict-{verdict.lower()}"
    icon = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}.get(verdict, "⚪")
    return f'<span class="{css_class}">{icon} {verdict} Match</span>'

# Sidebar Navigation
st.sidebar.title("🎯 Resume Relevance System")
page = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Dashboard", "📝 Student Portal", "👔 Recruiter Portal", "📊 Results Analysis", "🔍 Resume Details"]
)

# Main content based on selected page
if page == "🏠 Dashboard":
    st.markdown('<div class="main-header"><h1>📄 Resume Relevance Check System</h1><p>AI-Powered Resume-Job Matching Platform</p></div>', unsafe_allow_html=True)
    
    # Get dashboard stats
    stats_data, error = make_api_request("/api/v1/dashboard/stats")
    
    if error:
        st.error(error)
    else:
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h2 style="color: #667eea;">{stats_data.get("total_resumes", 0)}</h2>
                <p>Total Resumes</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h2 style="color: #764ba2;">{stats_data.get("total_jobs", 0)}</h2>
                <p>Active Jobs</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h2 style="color: #f093fb;">{stats_data.get("total_evaluations", 0)}</h2>
                <p>Evaluations</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h2 style="color: #10B981;">{stats_data.get("average_score", 0):.1f}%</h2>
                <p>Avg Score</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Match distribution chart
        st.subheader("📈 Match Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for verdicts
            labels = ["High Match", "Medium Match", "Low Match"]
            values = [
                stats_data.get("high_matches", 0),
                stats_data.get("medium_matches", 0),
                stats_data.get("low_matches", 0)
            ]
            colors = ["#10B981", "#F59E0B", "#EF4444"]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker=dict(colors=colors)
            )])
            fig_pie.update_layout(
                title="Match Quality Distribution",
                font=dict(size=14),
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart for summary
            summary_data = {
                "Metric": ["Total Resumes", "Total Jobs", "Evaluations", "High Matches"],
                "Count": [
                    stats_data.get("total_resumes", 0),
                    stats_data.get("total_jobs", 0),
                    stats_data.get("total_evaluations", 0),
                    stats_data.get("high_matches", 0)
                ]
            }
            
            fig_bar = px.bar(
                summary_data,
                x="Metric",
                y="Count",
                color="Metric",
                title="System Overview"
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

elif page == "📝 Student Portal":
    st.title("📝 Student Portal")
    st.write("Upload your resume and get instant feedback on job compatibility")
    
    tab1, tab2 = st.tabs(["📤 Upload Resume", "📋 My Evaluations"])
    
    with tab1:
        st.subheader("Upload Your Resume")
        
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your resume in PDF, DOCX, or TXT format"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            job_role = st.text_input("Preferred Job Role (Optional)")
        with col2:
            location = st.text_input("Location (Optional)")
        
        if uploaded_file is not None and st.button("🚀 Upload & Analyze"):
            with st.spinner("Processing your resume..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {
                    "job_role": job_role if job_role else None,
                    "location": location if location else None
                }
                
                result, error = make_api_request("/api/v1/resume/upload", "POST", data, files)
                
                if error:
                    st.error(error)
                else:
                    st.success("✅ Resume uploaded successfully!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Resume ID", result["resume_id"])
                        st.metric("Experience Years", result["experience_years"])
                    
                    with col2:
                        st.write("**Detected Job Role:**", result.get("job_role", "Not specified"))
                        st.write("**Location:**", result.get("location", "Not specified"))
                    
                    st.subheader("🔍 Extracted Skills")
                    if result["extracted_skills"]:
                        skills_html = render_skills_chips(result["extracted_skills"])
                        st.markdown(skills_html, unsafe_allow_html=True)
                    else:
                        st.info("No skills detected. Consider adding more technical skills to your resume.")
    
    with tab2:
        st.subheader("Your Recent Evaluations")
        # This would show evaluations for the current user
        st.info("Feature coming soon: View your evaluation history")

elif page == "👔 Recruiter Portal":
    st.title("👔 Recruiter Portal")
    st.write("Manage job descriptions and review candidate matches")
    
    tab1, tab2 = st.tabs(["📋 Post Job", "🔍 Review Candidates"])
    
    with tab1:
        st.subheader("Post New Job Description")
        
        with st.form("job_form"):
            job_title = st.text_input("Job Title *", placeholder="e.g., Senior Python Developer")
            company = st.text_input("Company", placeholder="e.g., TechCorp Inc.")
            job_location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
            experience_required = st.number_input("Required Experience (Years)", min_value=0, max_value=20, value=2)
            
            job_description = st.text_area(
                "Job Description *",
                height=300,
                placeholder="Paste the complete job description here..."
            )
            
            submitted = st.form_submit_button("📤 Post Job")
            
            if submitted:
                if job_title and job_description:
                    with st.spinner("Processing job description..."):
                        data = {
                            "title": job_title,
                            "company": company,
                            "content": job_description,
                            "location": job_location,
                            "experience_required": experience_required
                        }
                        
                        result, error = make_api_request("/api/v1/jd/upload", "POST", data)
                        
                        if error:
                            st.error(error)
                        else:
                            st.success("✅ Job description posted successfully!")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Job ID", result["job_id"])
                                st.metric("Experience Required", f"{result['experience_required']} years")
                            
                            with col2:
                                st.write("**Location:**", result.get("location", "Not specified"))
                            
                            st.subheader("🎯 Required Skills Detected")
                            if result["required_skills"]:
                                skills_html = render_skills_chips(result["required_skills"])
                                st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.error("Please fill in the required fields (marked with *)")
    
    with tab2:
        st.subheader("Available Jobs")
        
        jobs_data, error = make_api_request("/api/v1/jobs")
        
        if error:
            st.error(error)
        elif jobs_data:
            for job in jobs_data:
                with st.expander(f"🏢 {job['title']} at {job.get('company', 'Unknown Company')}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Job ID:** {job['id']}")
                        st.write(f"**Location:** {job.get('location', 'Not specified')}")
                    
                    with col2:
                        st.write(f"**Experience:** {job['experience_required']} years")
                        st.write(f"**Posted:** {job['uploaded_at'][:10]}")
                    
                    with col3:
                        if st.button(f"📊 View Candidates", key=f"view_{job['id']}"):
                            st.session_state.selected_job_id = job['id']
                    
                    if job['required_skills']:
                        st.write("**Required Skills:**")
                        skills_html = render_skills_chips(job['required_skills'])
                        st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No job descriptions found. Post your first job to get started!")

elif page == "📊 Results Analysis":
    st.title("📊 Results Analysis")
    st.write("Comprehensive analysis of all resume evaluations")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        job_filter = st.selectbox("Filter by Job", ["All Jobs"] + [f"Job {i}" for i in range(1, 6)])
    
    with col2:
        verdict_filter = st.selectbox("Verdict", ["All", "High", "Medium", "Low"])
    
    with col3:
        min_score = st.slider("Minimum Score", 0, 100, 0)
    
    with col4:
        location_filter = st.text_input("Location Contains")
    
    # Build query parameters
    params = {}
    if verdict_filter != "All":
        params["verdict"] = verdict_filter
    if min_score > 0:
        params["min_score"] = min_score
    if location_filter:
        params["location"] = location_filter
    
    # Construct query string
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    endpoint = f"/api/v1/results?{query_string}" if query_string else "/api/v1/results"
    
    evaluations_data, error = make_api_request(endpoint)
    
    if error:
        st.error(error)
    elif evaluations_data:
        st.subheader(f"📈 Found {len(evaluations_data)} Evaluations")
        
        # Create DataFrame for analysis
        df_data = []
        for eval_data in evaluations_data:
            df_data.append({
                "Resume ID": eval_data["resume_id"],
                "Job ID": eval_data["job_description_id"],
                "Overall Score": eval_data["overall_score"],
                "Skills Match": eval_data["skills_match_score"],
                "Semantic Score": eval_data["semantic_similarity_score"],
                "Experience Score": eval_data["experience_score"],
                "Verdict": eval_data["verdict"],
                "Date": eval_data["created_at"][:10]
            })
        
        df = pd.DataFrame(df_data)
        
        # Display summary charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Score distribution
            fig_hist = px.histogram(
                df,
                x="Overall Score",
                nbins=20,
                title="Score Distribution",
                color_discrete_sequence=["#667eea"]
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Verdict counts
            verdict_counts = df["Verdict"].value_counts()
            fig_pie = px.pie(
                values=verdict_counts.values,
                names=verdict_counts.index,
                title="Verdict Distribution",
                color_discrete_map={"High": "#10B981", "Medium": "#F59E0B", "Low": "#EF4444"}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detailed results table
        st.subheader("📋 Detailed Results")
        
        for eval_data in evaluations_data:
            with st.expander(f"Resume {eval_data['resume_id']} vs Job {eval_data['job_description_id']} - Score: {eval_data['overall_score']:.1f}%"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Overall Score", f"{eval_data['overall_score']:.1f}%")
                
                with col2:
                    st.metric("Skills Match", f"{eval_data['skills_match_score']:.1f}%")
                
                with col3:
                    st.metric("Semantic Score", f"{eval_data['semantic_similarity_score']:.1f}%")
                
                with col4:
                    st.metric("Experience Score", f"{eval_data['experience_score']:.1f}%")
                
                # Verdict
                verdict_html = render_verdict(eval_data["verdict"])
                st.markdown(f"**Verdict:** {verdict_html}", unsafe_allow_html=True)
                
                # Skills analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**✅ Matched Skills:**")
                    if eval_data["matched_skills"]:
                        skills_html = render_skills_chips(eval_data["matched_skills"])
                        st.markdown(skills_html, unsafe_allow_html=True)
                    else:
                        st.write("None")
                
                with col2:
                    st.write("**❌ Missing Skills:**")
                    if eval_data["missing_skills"]:
                        skills_html = render_skills_chips(eval_data["missing_skills"], "missing")
                        st.markdown(skills_html, unsafe_allow_html=True)
                    else:
                        st.write("None")
                
                # Suggestions
                if eval_data["suggestions"]:
                    st.write("**💡 Suggestions:**")
                    st.info(eval_data["suggestions"])
    else:
        st.info("No evaluations found matching your criteria.")

elif page == "🔍 Resume Details":
    st.title("🔍 Resume Details")
    
    resume_id = st.number_input("Enter Resume ID", min_value=1, value=1)
    
    if st.button("🔍 Load Resume Details"):
        resume_data, error = make_api_request(f"/api/v1/resume/{resume_id}")
        
        if error:
            st.error(error)
        elif resume_data:
            st.success(f"✅ Resume Found: {resume_data['filename']}")
            
            # Resume overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Experience", f"{resume_data['experience_years']} years")
            
            with col2:
                st.write(f"**Job Role:** {resume_data.get('job_role', 'Not specified')}")
            
            with col3:
                st.write(f"**Location:** {resume_data.get('location', 'Not specified')}")
            
            # Extracted skills
            st.subheader("🎯 Extracted Skills")
            if resume_data["extracted_skills"]:
                skills_html = render_skills_chips(resume_data["extracted_skills"])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No skills extracted")
            
            # Resume content preview
            st.subheader("📄 Resume Content Preview")
            with st.expander("View Full Resume Content"):
                st.text_area("Content", resume_data["content"], height=300, disabled=True)
            
            # Evaluation history
            st.subheader("📊 Evaluation History")
            
            if resume_data["evaluations"]:
                for eval_data in resume_data["evaluations"]:
                    with st.expander(f"Evaluation vs Job {eval_data['job_description_id']} - {eval_data['created_at'][:10]}"):
                        # Score breakdown
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Overall", f"{eval_data['overall_score']:.1f}%")
                        
                        with col2:
                            st.metric("Skills", f"{eval_data['skills_match_score']:.1f}%")
                        
                        with col3:
                            st.metric("Semantic", f"{eval_data['semantic_similarity_score']:.1f}%")
                        
                        with col4:
                            st.metric("Experience", f"{eval_data['experience_score']:.1f}%")
                        
                        # Verdict and suggestions
                        verdict_html = render_verdict(eval_data["verdict"])
                        st.markdown(f"**Verdict:** {verdict_html}", unsafe_allow_html=True)
                        
                        if eval_data["suggestions"]:
                            st.write("**💡 Suggestions:**")
                            st.info(eval_data["suggestions"])
            else:
                st.info("No evaluations found for this resume")
        
# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🚀 Resume Relevance Check System | AI-Powered Recruitment Platform"
    "</div>",
    unsafe_allow_html=True
)

# Health check indicator in sidebar
with st.sidebar:
    st.markdown("---")
    
    health_data, health_error = make_api_request("/health")
    
    if health_error:
        st.error("🔴 Backend Offline")
        st.caption("API server is not responding")
    else:
        st.success("🟢 Backend Online")
        st.caption("API server is running")