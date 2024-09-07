from typing import List, Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from pydantic.v1 import BaseModel, Field


class GithubProfileSummary(BaseModel):
    summary: str = Field(description="summary")
    projects: List[str] = Field(description="Github repositories and description")
    skills: List[str] = Field(description="programming languages used")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "projects": self.projects,
            "languages": self.skills
        }

summary_parser = PydanticOutputParser(pydantic_object=GithubProfileSummary)