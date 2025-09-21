import fitz  # PyMuPDF
import docx
import re
import nltk
from typing import List, Tuple, Dict
from sentence_transformers import SentenceTransformer
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TextExtractor:
    """Handles extraction of text from different file formats."""
    
    @staticmethod
    def extract_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF bytes."""
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    @staticmethod
    def extract_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX bytes."""
        try:
            doc = docx.Document(file_content)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting DOCX: {str(e)}")
    
    @staticmethod
    def extract_from_txt(file_content: bytes) -> str:
        """Extract text from TXT bytes."""
        try:
            return file_content.decode('utf-8').strip()
        except Exception as e:
            raise Exception(f"Error extracting TXT: {str(e)}")

class SkillExtractor:
    """Extracts skills and relevant information from text."""
    
    def __init__(self):
        self.common_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring'],
            'database': ['mysql', 'postgresql', 'mongodb', 'sqlite', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'tools': ['git', 'jenkins', 'jira', 'confluence', 'slack'],
            'ai_ml': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem solving', 'project management']
        }
        
        self.stop_words = set(stopwords.words('english'))
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using pattern matching."""
        text_lower = text.lower()
        found_skills = []
        
        # Extract skills from predefined lists
        for category, skills in self.common_skills.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
        
        # Extract programming languages and frameworks using patterns
        patterns = [
            r'\b(?:python|java|javascript|c\+\+|c#|php|ruby|go|rust|swift)\b',
            r'\b(?:react|angular|vue|node\.js|express|django|flask|spring)\b',
            r'\b(?:mysql|postgresql|mongodb|sqlite|redis|elasticsearch)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|terraform)\b',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            found_skills.extend(matches)
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text."""
        patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+\s*(?:years?|yrs?)',
            r'(?:experience|exp).*?(\d+)\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return max([int(match) for match in matches])
        
        return 0
    
    def extract_location(self, text: str) -> str:
        """Extract location information from text."""
        # Common location patterns
        patterns = [
            r'(?:location|based in|located in):\s*([^,\n]+)',
            r'([A-Za-z\s]+,\s*[A-Z]{2})',  # City, State format
            r'\b([A-Za-z\s]+,\s*(?:India|USA|UK|Canada|Australia))\b',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
        
        return ""
    
    def extract_job_role(self, text: str) -> str:
        """Extract job role/title from text."""
        common_roles = [
            'software engineer', 'data scientist', 'web developer', 'full stack developer',
            'frontend developer', 'backend developer', 'devops engineer', 'product manager',
            'ui/ux designer', 'business analyst', 'project manager', 'qa engineer'
        ]
        
        text_lower = text.lower()
        for role in common_roles:
            if role in text_lower:
                return role.title()
        
        # Try to extract from common patterns
        patterns = [
            r'(?:role|position|title):\s*([^\n,]+)',
            r'seeking\s+(?:a\s+)?([^\n,]+?)\s+(?:position|role)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return matches[0].strip().title()
        
        return "Not Specified"

class ContentProcessor:
    """Main processor for handling resume and job description content."""
    
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.skill_extractor = SkillExtractor()
    
    def process_resume(self, file_content: bytes, filename: str) -> Dict:
        """Process resume file and extract relevant information."""
        file_extension = filename.lower().split('.')[-1]
        
        # Extract text based on file type
        if file_extension == 'pdf':
            text = self.text_extractor.extract_from_pdf(file_content)
        elif file_extension == 'docx':
            text = self.text_extractor.extract_from_docx(file_content)
        elif file_extension == 'txt':
            text = self.text_extractor.extract_from_txt(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Extract structured information
        skills = self.skill_extractor.extract_skills(text)
        experience_years = self.skill_extractor.extract_experience_years(text)
        location = self.skill_extractor.extract_location(text)
        job_role = self.skill_extractor.extract_job_role(text)
        
        return {
            'content': text,
            'skills': skills,
            'experience_years': experience_years,
            'location': location,
            'job_role': job_role
        }
    
    def process_job_description(self, content: str) -> Dict:
        """Process job description and extract required skills."""
        skills = self.skill_extractor.extract_skills(content)
        experience_required = self.skill_extractor.extract_experience_years(content)
        location = self.skill_extractor.extract_location(content)
        
        return {
            'content': content,
            'required_skills': skills,
            'experience_required': experience_required,
            'location': location
        }