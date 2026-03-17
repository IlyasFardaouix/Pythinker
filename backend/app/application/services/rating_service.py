"""Application service for report ratings."""

from functools import lru_cache
from typing import Optional

from app.infrastructure.models.documents import RatingDocument


class RatingService:
    """Service for persisting rating submissions."""

    async def submit_rating(
        self,
        session_id: str,
        report_id: str,
        user_id: str,
        user_email: str,
        user_name: str,
        rating: int,
        feedback: Optional[str] = None,
    ) -> None:
        """
        Submit a rating for a report.

        Args:
            session_id: Unique identifier for the user session.
            report_id: Unique identifier for the report being rated.
            user_id: Unique identifier for the user submitting the rating.
            user_email: Email address of the user submitting the rating.
            user_name: Name of the user submitting the rating.
            rating: The rating value (e.g., 1-5).
            feedback: Optional feedback provided by the user.

        Returns:
            None
        """
        doc = RatingDocument(
            session_id=session_id,
            report_id=report_id,
            user_id=user_id,
            user_email=user_email,
            user_name=user_name,
            rating=rating,
            feedback=feedback,
        )
        await doc.insert()


@lru_cache(maxsize=1)  # Cache the instance to avoid creating multiple instances
def get_rating_service() -> RatingService:
    """Get an instance of the RatingService."""
    return RatingService()