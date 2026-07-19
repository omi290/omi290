from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    """Abstract base class for all SVG generators."""
    
    def __init__(self, config: dict):
        self.config = config

    @property
    @abstractmethod
    def filename(self) -> str:
        """The base filename for the output SVG (without .svg extension)."""
        pass

    @abstractmethod
    def fetch_data(self):
        """Fetch necessary data (API calls, file reads) for this component."""
        pass

    @abstractmethod
    def render_svg(self) -> str:
        """Generates and returns the SVG string."""
        pass
