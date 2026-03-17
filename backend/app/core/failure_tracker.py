"""Track failures for adaptive circuit breaker thresholds."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from pytz import UTC  # Import pytz for timezone support


@dataclass
class FailureEvent:
    """Represents a single failure event."""

    timestamp: datetime
    error_type: str
    detail: Optional[str] = None


@dataclass
class FailureStats:
    """Provides statistics about a set of failure events."""

    total: int
    recent: int
    failure_rate: float
    error_types: Dict[str, int] = field(default_factory=dict)


class FailureTracker:
    """Tracks failure events for a named operation."""

    def __init__(
        self,
        window_seconds: int = 300,
        history_limit: int = 200,
    ) -> None:
        """
        Initializes a FailureTracker instance.

        Args:
            window_seconds: The time window (in seconds) to consider recent events.
            history_limit: The maximum number of events to store for each operation.
        """
        self._window = timedelta(seconds=window_seconds)
        self._history_limit = history_limit
        self._events: Dict[str, List[FailureEvent]] = {}
        self._successes: Dict[str, List[datetime]] = {}

    def record_failure(
        self,
        name: str,
        error_type: str,
        detail: Optional[str] = None,
    ) -> None:
        """
        Records a failure event for the given operation.

        Args:
            name: The name of the operation.
            error_type: The type of error that occurred.
            detail: Additional details about the error (optional).
        """
        events = self._events.setdefault(name, [])
        events.append(FailureEvent(timestamp=datetime.now(UTC), error_type=error_type, detail=detail))
        if len(events) > self._history_limit:
            self._events[name] = events[-self._history_limit :]

    def record_success(self, name: str) -> None:
        """
        Records a success event for the given operation.

        Args:
            name: The name of the operation.
        """
        successes = self._successes.setdefault(name, [])
        successes.append(datetime.now(UTC))
        if len(successes) > self._history_limit:
            self._successes[name] = successes[-self._history_limit :]

    def get_stats(self, name: str) -> FailureStats:
        """
        Retrieves statistics about the given operation.

        Args:
            name: The name of the operation.

        Returns:
            FailureStats: Statistics about the operation.
        """
        now = datetime.now(UTC)
        events = self._events.get(name, [])
        successes = self._successes.get(name, [])

        # Filter recent events within the time window
        recent_events = [e for e in events if now - e.timestamp <= self._window]
        recent_successes = [s for s in successes if now - s <= self._window]

        # Calculate total recent events and failure rate
        total_recent = len(recent_events) + len(recent_successes)
        failure_rate = len(recent_events) / total_recent if total_recent else 0.0

        # Count error types
        error_types: Dict[str, int] = {}
        for event in recent_events:
            error_types[event.error_type] = error_types.get(event.error_type, 0) + 1

        return FailureStats(
            total=len(events),
            recent=len(recent_events),
            failure_rate=failure_rate,
            error_types=error_types,
        )

    def get_recent_errors(self, name: str, limit: int = 5) -> List[FailureEvent]:
        """
        Retrieves the most recent failure events for the given operation.

        Args:
            name: The name of the operation.
            limit: The maximum number of events to return (default: 5).

        Returns:
            List[FailureEvent]: Recent failure events.
        """
        return self._events.get(name, [])[-limit:]

    def reset(self, name: str) -> None:
        """
        Resets the failure tracker for the given operation.

        Args:
            name: The name of the operation.
        """
        self._events.pop(name, None)
        self._successes.pop(name, None)
```

Note: I've used `pytz` library for timezone support, you can install it using `pip install pytz`. Also, I've added type hints for function parameters and return types, which can help with code readability and maintainability.