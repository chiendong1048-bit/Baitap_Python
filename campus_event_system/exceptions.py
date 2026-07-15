"""Custom exceptions used by the campus event system."""


class CampusEventError(Exception):
    """Base class for expected application errors."""


class ValidationError(CampusEventError):
    """Raised when input or persisted domain data is invalid."""


class EventNotFoundError(CampusEventError):
    """Raised when an event ID does not exist."""


class EventFullError(CampusEventError):
    """Raised when an event has no available seats."""


class DuplicateRegistrationError(CampusEventError):
    """Raised when an attendee is already registered."""


class AuthenticationError(CampusEventError):
    """Raised when login credentials are invalid."""


class PermissionDeniedError(CampusEventError):
    """Raised when a role is not allowed to perform an action."""


class UserNotFoundError(CampusEventError):
    """Raised when a username does not exist."""
