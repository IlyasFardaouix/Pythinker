"""Application service for typo correction analytics and feedback."""

from __future__ import annotations

from typing import Any, Dict

from app.infrastructure.observability.typo_correction_analytics import (
    TypoCorrectionAnalytics,
    get_typo_correction_analytics,
)


class TypoCorrectionService:
    """
    Coordinates typo correction feedback and analytics queries.

    This service provides methods to retrieve typo correction analytics and submit user feedback.
    """

    def __init__(self) -> None:
        """
        Initializes the typo correction service.

        This method is not intended to be called directly. Instead, use the get_typo_correction_service function.
        """

    def get_summary(self) -> Dict[str, Any]:
        """
        Retrieves a summary of typo correction analytics.

        Returns:
            A dictionary containing typo correction analytics data.
        """
        return get_typo_correction_analytics().get_summary()

    def submit_feedback(self, *, original_text: str, corrected_text: str, user_override: str) -> None:
        """
        Submits user feedback for typo correction.

        Args:
            original_text: The original text with the typo.
            corrected_text: The corrected text.
            user_override: The user's override correction (if any).
        """
        get_typo_correction_analytics().record_feedback(
            original=original_text,
            corrected=corrected_text,
            user_override=user_override,
        )


_typo_correction_service: TypoCorrectionService | None = None


def get_typo_correction_service() -> TypoCorrectionService:
    """
    Retrieves the singleton instance of the typo correction service.

    If the service instance does not exist, it is created and stored in the _typo_correction_service variable.

    Returns:
        The singleton instance of the typo correction service.
    """
    global _typo_correction_service
    if _typo_correction_service is None:
        _typo_correction_service = TypoCorrectionService()
    return _typo_correction_service