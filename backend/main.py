from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
from dotenv import load_dotenv

from .db import get_db, init_db
from .models import Resume, JobDescription, Evaluation, ResumeUpload, JobDescriptionUpload, EvaluationResult, DashboardStats, ResumeDetail
from .parsers import ContentProcessor
from .scoring import ResumeScorer

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Resume Relevance Check API",
    description="Automated Resume-Job Matching System",
    version="1.0.0"
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
content_processor = ContentProcessor()
resume_scorer = ResumeScorer()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Resume Relevance Check API is running"}

@app.post("/api/v1/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_role: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload and process a resume."""
    try:
        # Validate file type
        allowed_types = ['pdf', 'docx', 'txt']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_extension} not supported. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Process resume
        processed_data = content_processor.process_resume(file_content, file.filename)
        
        # Create resume record
        resume = Resume(
            filename=file.filename,
            file_type=file_extension,
            content=processed_data['content'],
            extracted_skills=json.dumps(processed_data['skills']),
            location=location or processed_data['location'],
            job_role=job_role or processed_data['job_role'],
            experience_years=processed_data['experience_years']
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return {
            "message": "Resume uploaded successfully",
            "resume_id": resume.id,
            "extracted_skills": processed_data['skills'],
            "experience_years": processed_data['experience_years'],
            "location": resume.location,
            "job_role": resume.job_role
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@app.post("/api/v1/jd/upload")
async def upload_job_description(
    jd_data: JobDescriptionUpload,
    db: Session = Depends(get_db)
):
    """Upload and process a job description."""
    try:
        # Process job description
        processed_data = content_processor.process_job_description(jd_data.content)
        
        # Create job description record
        job_desc = JobDescription(
            title=jd_data.title,
            company=jd_data.company,
            content=jd_data.content,
            required_skills=json.dumps(processed_data['required_skills']),
            location=jd_data.location or processed_data['location'],
            experience_required=jd_data.experience_required or processed_data['experience_required']
        )
        
        db.add(job_desc)
        db.commit()
        db.refresh(job_desc)
        
        return {
            "message": "Job description uploaded successfully",
            "job_id": job_desc.id,
            "required_skills": processed_data['required_skills'],
            "experience_required": job_desc.experience_required,
            "location": job_desc.location
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing job description: {str(e)}")

@app.post("/api/v1/evaluate/{resume_id}/{job_id}")
async def evaluate_resume(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):
    """Evaluate a resume against a job description."""
    try:
        # Get resume and job description
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        job_desc = db.query(JobDescription).filter(JobDescription.id == job_id).first()
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        if not job_desc:
            raise HTTPException(status_code=404, detail="Job description not found")
        
        # Prepare data for scoring
        resume_data = {
            'content': resume.content,
            'skills': resume.get_skills(),
            'experience_years': resume.experience_years
        }
        
        job_data = {
            'content': job_desc.content,
            'required_skills': job_desc.get_required_skills(),
            'experience_required': job_desc.experience_required
        }
        
        # Calculate scores
        score_result = resume_scorer.score_resume(resume_data, job_data)
        
        # Check if evaluation already exists
        existing_eval = db.query(Evaluation).filter(
            Evaluation.resume_id == resume_id,
            Evaluation.job_description_id == job_id
        ).first()
        
        if existing_eval:
            # Update existing evaluation
            for key, value in score_result.items():
                if key in ['matched_skills', 'missing_skills']:
                    setattr(existing_eval, key, json.dumps(value))
                else:
                    setattr(existing_eval, key, value)
        else:
            # Create new evaluation
            evaluation = Evaluation(
                resume_id=resume_id,
                job_description_id=job_id,
                overall_score=score_result['overall_score'],
                skills_match_score=score_result['skills_match_score'],
                semantic_similarity_score=score_result['semantic_similarity_score'],
                experience_score=score_result['experience_score'],
                matched_skills=json.dumps(score_result['matched_skills']),
                missing_skills=json.dumps(score_result['missing_skills']),
                suggestions=score_result['suggestions'],
                verdict=score_result['verdict']
            )
            db.add(evaluation)
        
        db.commit()
        
        return {
            "message": "Resume evaluated successfully",
            "evaluation_result": score_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating resume: {str(e)}")

@app.get("/api/v1/results", response_model=List[EvaluationResult])
async def get_evaluations(
    job_id: Optional[int] = Query(None),
    verdict: Optional[str] = Query(None),
    min_score: Optional[float] = Query(None),
    location: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get evaluations with filtering options."""
    try:
        query = db.query(Evaluation)
        
        # Apply filters
        if job_id:
            query = query.filter(Evaluation.job_description_id == job_id)
        if verdict:
            query = query.filter(Evaluation.verdict == verdict)
        if min_score is not None:
            query = query.filter(Evaluation.overall_score >= min_score)
        if location:
            query = query.join(Resume).filter(Resume.location.ilike(f"%{location}%"))
        
        # Apply pagination
        evaluations = query.offset(skip).limit(limit).all()
        
        # Convert to response model
        results = []
        for eval in evaluations:
            result = EvaluationResult(
                id=eval.id,
                resume_id=eval.resume_id,
                job_description_id=eval.job_description_id,
                overall_score=eval.overall_score,
                skills_match_score=eval.skills_match_score,
                semantic_similarity_score=eval.semantic_similarity_score,
                experience_score=eval.experience_score,
                matched_skills=eval.get_matched_skills(),
                missing_skills=eval.get_missing_skills(),
                suggestions=eval.suggestions,
                verdict=eval.verdict,
                created_at=eval.created_at
            )
            results.append(result)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving evaluations: {str(e)}")

@app.get("/api/v1/resume/{resume_id}", response_model=ResumeDetail)
async def get_resume_detail(resume_id: int, db: Session = Depends(get_db)):
    """Get detailed resume information with evaluations."""
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Get evaluations for this resume
        evaluations = []
        for eval in resume.evaluations:
            eval_result = EvaluationResult(
                id=eval.id,
                resume_id=eval.resume_id,
                job_description_id=eval.job_description_id,
                overall_score=eval.overall_score,
                skills_match_score=eval.skills_match_score,
                semantic_similarity_score=eval.semantic_similarity_score,
                experience_score=eval.experience_score,
                matched_skills=eval.get_matched_skills(),
                missing_skills=eval.get_missing_skills(),
                suggestions=eval.suggestions,
                verdict=eval.verdict,
                created_at=eval.created_at
            )
            evaluations.append(eval_result)
        
        resume_detail = ResumeDetail(
            id=resume.id,
            filename=resume.filename,
            content=resume.content,
            extracted_skills=resume.get_skills(),
            location=resume.location,
            job_role=resume.job_role,
            experience_years=resume.experience_years,
            uploaded_at=resume.uploaded_at,
            evaluations=evaluations
        )
        
        return resume_detail
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving resume details: {str(e)}")

@app.get("/api/v1/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    try:
        total_resumes = db.query(Resume).count()
        total_jobs = db.query(JobDescription).count()
        total_evaluations = db.query(Evaluation).count()
        
        high_matches = db.query(Evaluation).filter(Evaluation.verdict == "High").count()
        medium_matches = db.query(Evaluation).filter(Evaluation.verdict == "Medium").count()
        low_matches = db.query(Evaluation).filter(Evaluation.verdict == "Low").count()
        
        # Calculate average score
        avg_score_result = db.query(Evaluation).all()
        average_score = sum([eval.overall_score for eval in avg_score_result]) / len(avg_score_result) if avg_score_result else 0.0
        
        stats = DashboardStats(
            total_resumes=total_resumes,
            total_jobs=total_jobs,
            total_evaluations=total_evaluations,
            high_matches=high_matches,
            medium_matches=medium_matches,
            low_matches=low_matches,
            average_score=round(average_score, 2)
        )
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dashboard stats: {str(e)}")

@app.get("/api/v1/jobs")
async def get_job_descriptions(
    active_only: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get list of job descriptions."""
    try:
        query = db.query(JobDescription)
        
        if active_only:
            query = query.filter(JobDescription.is_active == True)
        
        jobs = query.offset(skip).limit(limit).all()
        
        result = []
        for job in jobs:
            result.append({
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "experience_required": job.experience_required,
                "required_skills": job.get_required_skills(),
                "uploaded_at": job.uploaded_at
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job descriptions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)