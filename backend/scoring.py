import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from Levenshtein import ratio as levenshtein_ratio
from typing import List, Dict, Tuple
import json
import re

class ResumeScorer:
    """Advanced resume scoring system with hybrid matching."""
    
    def __init__(self):
        # Load sentence transformer model for semantic similarity
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    
    def calculate_skills_match_score(self, resume_skills: List[str], required_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """Calculate skills matching score using hard matching and fuzzy matching."""
        if not required_skills:
            return 100.0, resume_skills, []
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        matched_skills = []
        missing_skills = []
        
        # Exact matches first
        for req_skill in required_skills:
            exact_match = False
            for res_skill in resume_skills:
                if req_skill.lower() == res_skill.lower():
                    matched_skills.append(req_skill)
                    exact_match = True
                    break
            
            if not exact_match:
                # Try fuzzy matching
                best_match = None
                best_ratio = 0.0
                
                for res_skill in resume_skills:
                    ratio = levenshtein_ratio(req_skill.lower(), res_skill.lower())
                    if ratio > best_ratio and ratio >= 0.8:  # 80% similarity threshold
                        best_ratio = ratio
                        best_match = req_skill
                
                if best_match:
                    matched_skills.append(best_match)
                else:
                    missing_skills.append(req_skill)
        
        # Calculate score as percentage of required skills matched
        score = (len(matched_skills) / len(required_skills)) * 100
        
        return score, matched_skills, missing_skills
    
    def calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate semantic similarity using sentence transformers."""
        try:
            # Clean and preprocess texts
            resume_clean = self._clean_text(resume_text)
            job_clean = self._clean_text(job_description)
            
            # Get embeddings
            texts = [resume_clean, job_clean]
            embeddings = self.sentence_model.encode(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            # Convert to percentage (0-100)
            return float(similarity * 100)
            
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            # Fallback to TF-IDF similarity
            return self._calculate_tfidf_similarity(resume_text, job_description)
    
    def _calculate_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Fallback TF-IDF similarity calculation."""
        try:
            texts = [self._clean_text(text1), self._clean_text(text2)]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity * 100)
        except Exception:
            return 50.0  # Default fallback score
    
    def calculate_experience_score(self, resume_experience: int, required_experience: int) -> float:
        """Calculate experience matching score."""
        if required_experience == 0:
            return 100.0
        
        if resume_experience >= required_experience:
            # Bonus for more experience, but cap at 100
            bonus = min((resume_experience - required_experience) * 5, 20)
            return min(100.0, 100.0 + bonus)
        else:
            # Penalty for less experience
            deficit_ratio = resume_experience / required_experience
            return deficit_ratio * 100
    
    def calculate_overall_score(
        self, 
        skills_score: float, 
        semantic_score: float, 
        experience_score: float,
        weights: Dict[str, float] = None
    ) -> float:
        """Calculate overall weighted score."""
        if weights is None:
            weights = {
                'skills': 0.5,      # 50% weight for skills matching
                'semantic': 0.3,    # 30% weight for semantic similarity
                'experience': 0.2   # 20% weight for experience
            }
        
        overall_score = (
            skills_score * weights['skills'] +
            semantic_score * weights['semantic'] +
            experience_score * weights['experience']
        )
        
        return min(100.0, overall_score)
    
    def determine_verdict(self, overall_score: float) -> str:
        """Determine verdict category based on overall score."""
        if overall_score >= 75:
            return "High"
        elif overall_score >= 50:
            return "Medium"
        else:
            return "Low"
    
    def generate_suggestions(
        self, 
        missing_skills: List[str], 
        matched_skills: List[str],
        overall_score: float,
        experience_gap: int = 0
    ) -> str:
        """Generate personalized suggestions for improvement."""
        suggestions = []
        
        if missing_skills:
            if len(missing_skills) <= 3:
                suggestions.append(f"Consider acquiring these key skills: {', '.join(missing_skills[:3])}")
            else:
                suggestions.append(f"Focus on developing {len(missing_skills)} missing skills, especially: {', '.join(missing_skills[:3])}")
        
        if overall_score < 50:
            suggestions.append("Consider tailoring your resume more closely to the job requirements")
            
        if experience_gap > 0:
            suggestions.append(f"Gaining {experience_gap} more years of relevant experience would strengthen your application")
        
        if len(matched_skills) > 0:
            suggestions.append(f"Great job highlighting these relevant skills: {', '.join(matched_skills[:3])}")
        
        if overall_score >= 75:
            suggestions.append("Excellent match! Your profile aligns well with the job requirements.")
        
        return ". ".join(suggestions) if suggestions else "Keep developing your skills and tailoring your applications."
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text for analysis."""
        # Remove extra whitespace and special characters
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.strip().lower()
    
    def score_resume(
        self, 
        resume_data: Dict, 
        job_data: Dict,
        custom_weights: Dict[str, float] = None
    ) -> Dict:
        """Complete resume scoring pipeline."""
        
        # Extract data
        resume_skills = resume_data.get('skills', [])
        resume_text = resume_data.get('content', '')
        resume_experience = resume_data.get('experience_years', 0)
        
        required_skills = job_data.get('required_skills', [])
        job_text = job_data.get('content', '')
        required_experience = job_data.get('experience_required', 0)
        
        # Calculate individual scores
        skills_score, matched_skills, missing_skills = self.calculate_skills_match_score(
            resume_skills, required_skills
        )
        
        semantic_score = self.calculate_semantic_similarity(resume_text, job_text)
        experience_score = self.calculate_experience_score(resume_experience, required_experience)
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(
            skills_score, semantic_score, experience_score, custom_weights
        )
        
        # Determine verdict
        verdict = self.determine_verdict(overall_score)
        
        # Generate suggestions
        experience_gap = max(0, required_experience - resume_experience)
        suggestions = self.generate_suggestions(
            missing_skills, matched_skills, overall_score, experience_gap
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'skills_match_score': round(skills_score, 2),
            'semantic_similarity_score': round(semantic_score, 2),
            'experience_score': round(experience_score, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'suggestions': suggestions,
            'verdict': verdict
        }