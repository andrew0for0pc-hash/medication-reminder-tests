"""Validation for the medication reminder form (KAN-11)."""
from datetime import datetime


def create_reminder(name, scheduled_at, now):
    if not isinstance(name, str) or not name.strip():
        raise ValueError('Medicine name is required')
    if (not isinstance(now, datetime) or now.tzinfo is None
            or now.utcoffset() is None):
        raise ValueError('now must include timezone')
    if not isinstance(scheduled_at, str):
        raise ValueError('Date must be an ISO string')
    try:
        when = datetime.fromisoformat(scheduled_at)
    except ValueError as error:
        raise ValueError('Invalid ISO date') from error
    if when.tzinfo is None or when.utcoffset() is None:
        raise ValueError('Date must include timezone')
    if when <= now:
        raise ValueError('Date must be in the future')
    return {'medicine': name, 'scheduled_at': when.isoformat(),
            'status': 'planned'}
