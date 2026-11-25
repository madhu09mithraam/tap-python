class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass


class InputFileError(PipelineError):
    """Raised when an input file is missing."""
    pass


class ConfigFileError(PipelineError):
    """Raised when configuration is missing or invalid."""
    pass


class MissingColumnError(PipelineError):
    """Raised when required columns are missing."""
    pass


class EmptyDataError(PipelineError):
    """Raised when the dataset is empty."""
    pass