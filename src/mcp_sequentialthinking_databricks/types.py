"""Type definitions for the sequential thinking server."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ToolRecommendation(BaseModel):
    """Recommendation for a tool to use in a step."""
    
    tool_name: str = Field(description="Name of the tool being recommended")
    confidence: float = Field(
        ge=0, le=1, description="0-1 indicating confidence in recommendation"
    )
    rationale: str = Field(description="Why this tool is recommended")
    priority: int = Field(description="Order in the recommendation sequence")
    suggested_inputs: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional suggested parameters"
    )
    alternatives: Optional[List[str]] = Field(
        default=None, description="Alternative tools that could be used"
    )


class StepRecommendation(BaseModel):
    """Recommendation for a single step in the problem-solving process."""
    
    step_description: str = Field(description="What needs to be done")
    recommended_tools: List[ToolRecommendation] = Field(
        description="Tools recommended for this step"
    )
    expected_outcome: str = Field(description="What to expect from this step")
    next_step_conditions: Optional[List[str]] = Field(
        default=None, description="Conditions to consider for the next step"
    )


class ThoughtData(BaseModel):
    """Data for a single thought in the sequential thinking process."""
    
    available_mcp_tools: List[str] = Field(
        description="Array of MCP tool names available for use"
    )
    thought: str = Field(description="Your current thinking step")
    next_thought_needed: bool = Field(
        description="Whether another thought step is needed"
    )
    thought_number: int = Field(ge=1, description="Current thought number")
    total_thoughts: int = Field(ge=1, description="Estimated total thoughts needed")
    is_revision: Optional[bool] = Field(
        default=None, description="Whether this revises previous thinking"
    )
    revises_thought: Optional[int] = Field(
        default=None, ge=1, description="Which thought is being reconsidered"
    )
    branch_from_thought: Optional[int] = Field(
        default=None, ge=1, description="Branching point thought number"
    )
    branch_id: Optional[str] = Field(default=None, description="Branch identifier")
    needs_more_thoughts: Optional[bool] = Field(
        default=None, description="If more thoughts are needed"
    )
    current_step: Optional[StepRecommendation] = Field(
        default=None, description="Current step recommendation"
    )
    previous_steps: Optional[List[StepRecommendation]] = Field(
        default=None, description="Steps already recommended"
    )
    remaining_steps: Optional[List[str]] = Field(
        default=None, description="High-level descriptions of upcoming steps"
    )


class Tool(BaseModel):
    """Definition of an MCP tool."""
    
    name: str
    description: str
    inputSchema: Dict[str, Any]
