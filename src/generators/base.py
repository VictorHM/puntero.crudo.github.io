import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models import Section


class SectionGenerator(ABC):
    """Base class for section generators (Blog, Projects, etc)."""

    def __init__(self, section: Section, site_config: Dict[str, Any]):
        self.section = section
        self.site_config = site_config
        self.input_dir = section.input_dir
        self.output_dir = section.output_dir

    @abstractmethod
    def generate(self) -> List[Dict[str, Any]]:
        """Generate content for this section. Returns list of generated items."""
        pass

    def ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        os.makedirs(self.output_dir, exist_ok=True)
