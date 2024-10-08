from sqlalchemy.orm import Session
from db.db_models import CVJobPair

# Initialize the repository with a db session
class CVJobRepository:
    def __init__(self, db: Session):
        self.db = db

    # Add a new CV and job profile pair to the database with status "uploaded"
    def add_cv_and_job(self, cv_filename: str, cv_content: bytes, job_filename: str, job_content: bytes):
        db_entry = CVJobPair(
            cv_filename=cv_filename,
            cv_content=cv_content,
            job_filename=job_filename,
            job_content=job_content,
            status='uploaded'
        )
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        return db_entry

    # Update the grade and insights after AI analysis with staus "completed"
    def update_grade_and_insights(self, entry_id: int, grade: int, insights: str):
        db_entry = self.get_entry_by_id(entry_id)
        if db_entry:
            db_entry.grade = grade
            db_entry.insights = insights
            db_entry.status = 'completed'
            self.db.commit()
        return db_entry

    # Get a specific entry by its ID
    def get_entry_by_id(self, entry_id: int):
        return self.db.query(CVJobPair).filter(CVJobPair.id == entry_id).first()

    # Update matching and not matching details after the AI analysis
    def update_matching_details(self, entry_id: int, matching: str, not_matching: str):
        db_entry = self.get_entry_by_id(entry_id)
        if db_entry:
            db_entry.matching = matching
            db_entry.not_matching = not_matching
            self.db.commit()
        return db_entry

    # Retrieve all entries by their status
    def get_entries_by_status(self, status: str):
        return self.db.query(CVJobPair).filter(CVJobPair.status == status).all()
