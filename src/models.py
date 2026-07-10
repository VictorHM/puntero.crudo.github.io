from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Post:
    title: str
    date: str
    url: str
    excerpt: str
    content: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class Project:
    title: str
    link: str
    image: str
    description: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class Section:
    name: str
    path: str
    input_dir: str
    output_dir: str
    type: str
    description: str


@dataclass
class SiteConfig:
    name: str
    description: str
    author: str
    year: int
    navigation: List[Dict]
    sections: List[Section]
