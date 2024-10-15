from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.db_models import CVJobPair


# Initialize the repository with a db session
class CVJobRepository:
    def __init__(self, db: Session):
        self.db = db

    # Add a new CV and job profile pair to the database with status "pending"
    def add_cv_and_job(self, cv_filename: str, cv_content: bytes, job_filename: str, job_content: bytes):
        try:
            db_entry = CVJobPair(
                cv_filename=cv_filename,
                cv_content=cv_content,
                job_filename=job_filename,
                job_content=job_content,
                status='Pending'
            )
            self.db.add(db_entry)
            self.db.commit()
            self.db.refresh(db_entry)
            return db_entry
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    # Update the grade and insights after AI analysis with status "completed"
    def update_grade_and_insights(self, entry_id: int, grade: str, insights: str):
        try:
            db_entry = self.get_entry_by_id(entry_id)
            if db_entry:
                db_entry.grade = grade
                db_entry.insights = insights
                db_entry.status = 'AI-Graded'
                self.db.commit()
            return db_entry
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    # Get a specific entry by its ID
    def get_entry_by_id(self, entry_id: int):
        return self.db.query(CVJobPair).filter(CVJobPair.id == entry_id).first()

    # Update matching and not matching details after the AI analysis
    def update_matching_details(self, entry_id: int, matching: str, not_matching: str):
        try:
            db_entry = self.get_entry_by_id(entry_id)
            if db_entry:
                db_entry.matching = matching
                db_entry.not_matching = not_matching
                self.db.commit()
            return db_entry
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    # Update the row with new data
    def update_row(self, cv_filename: str, job_filename: str, grade: str, status: str):
        try:
            db_entry = self.db.query(CVJobPair).filter(
                CVJobPair.cv_filename == cv_filename,
                CVJobPair.job_filename == job_filename
            ).first()

            if db_entry:
                db_entry.grade = grade
                db_entry.status = status
                self.db.commit()
                self.db.refresh(db_entry)
            else:
                raise ValueError("Entry not found in the database.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    # Retrieve all entries from the database
    def get_all_entries(self):
        try:
            return self.db.query(CVJobPair).all()
        except SQLAlchemyError as e:
            raise e

    def get_status_count(self, status):
        try:
            return self.db.query(CVJobPair).filter(CVJobPair.status == status).count()
        except SQLAlchemyError as e:
            raise e

    # Update the grade for a given entry manually
    def update_grade(self, entry_id: int, new_grade: str):
        try:
            db_entry = self.get_entry_by_id(entry_id)
            if db_entry:
                db_entry.grade = new_grade
                db_entry.status = 'Manually Graded'
                self.db.commit()
                self.db.refresh(db_entry)
            else:
                raise ValueError("Entry not found in the database.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    # Update the status for a post to "Validated"
    def validate_grade(self, entry_id: int):
        try:
            db_entry = self.get_entry_by_id(entry_id)
            if db_entry:
                db_entry.status = "Validated"
                self.db.commit()
                self.db.refresh(db_entry)
            else:
                raise ValueError("Entry not found in the database.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e