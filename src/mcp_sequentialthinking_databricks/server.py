"""Sequential thinking server implementation."""

import logging
import os
from typing import Dict, List, Optional
from .types import ThoughtData, Tool, StepRecommendation, ToolRecommendation
from .schema import SEQUENTIAL_THINKING_TOOL

logger = logging.getLogger(__name__)


class ToolAwareSequentialThinkingServer:
    """Server for managing sequential thinking with tool recommendations."""
    
    def __init__(self, max_history_size: Optional[int] = None):
        """Initialize the server.
        
        Args:
            max_history_size: Maximum number of thoughts to retain in history
        """
        self.thought_history: List[ThoughtData] = []
        self.branches: Dict[str, List[ThoughtData]] = {}
        self.available_tools: Dict[str, Tool] = {}
        self.max_history_size = max_history_size or int(
            os.environ.get("MAX_HISTORY_SIZE", "1000")
        )
        
        # Always include the sequential thinking tool
        self._add_tool(SEQUENTIAL_THINKING_TOOL)
        
        logger.info(
            f"Initialized sequential thinking server with max history: {self.max_history_size}"
        )
    
    def _add_tool(self, tool: Tool) -> None:
        """Add a tool to the available tools."""
        if tool.name in self.available_tools:
            logger.warning(f"Tool '{tool.name}' already exists, skipping")
            return
        self.available_tools[tool.name] = tool
        logger.info(f"Added tool: {tool.name}")
    
    def get_available_tools(self) -> List[Tool]:
        """Get list of available tools."""
        return list(self.available_tools.values())
    
    def clear_history(self) -> None:
        """Clear thought history and branches."""
        self.thought_history = []
        self.branches = {}
        logger.info("History cleared")
    
    def _format_recommendation(self, step: StepRecommendation) -> str:
        """Format a step recommendation for display."""
        tools_text = []
        for tool in step.recommended_tools:
            alternatives = (
                f" (alternatives: {', '.join(tool.alternatives)})"
                if tool.alternatives
                else ""
            )
            inputs = (
                f"\n    Suggested inputs: {tool.suggested_inputs}"
                if tool.suggested_inputs
                else ""
            )
            tools_text.append(
                f"  - {tool.tool_name} (priority: {tool.priority}){alternatives}\n"
                f"    Rationale: {tool.rationale}{inputs}"
            )
        
        conditions = (
            f"\nConditions for next step:\n  - {chr(10).join(f'  - {c}' for c in step.next_step_conditions)}"
            if step.next_step_conditions
            else ""
        )
        
        return (
            f"Step: {step.step_description}\n"
            f"Recommended Tools:\n{chr(10).join(tools_text)}\n"
            f"Expected Outcome: {step.expected_outcome}{conditions}"
        )
    
    def _format_thought(self, thought_data: ThoughtData) -> str:
        """Format a thought for display."""
        prefix = ""
        context = ""
        
        if thought_data.is_revision:
            prefix = "🔄 Revision"
            context = f" (revising thought {thought_data.revises_thought})"
        elif thought_data.branch_from_thought:
            prefix = "🌿 Branch"
            context = f" (from thought {thought_data.branch_from_thought}, ID: {thought_data.branch_id})"
        else:
            prefix = "💭 Thought"
        
        header = f"{prefix} {thought_data.thought_number}/{thought_data.total_thoughts}{context}"
        content = thought_data.thought
        
        # Add recommendation information if present
        if thought_data.current_step:
            content = f"{thought_data.thought}\n\nRecommendation:\n{self._format_recommendation(thought_data.current_step)}"
        
        border = "─" * max(len(header), len(content) + 4)
        
        return f"\n┌{border}┐\n│ {header} │\n├{border}┤\n│ {content} │\n└{border}┘"
    
    def process_thought(self, thought_data: ThoughtData) -> Dict:
        """Process a thought and return the result.
        
        Args:
            thought_data: The thought data to process
            
        Returns:
            Dict containing the processing result
        """
        try:
            # Adjust total_thoughts if needed
            if thought_data.thought_number > thought_data.total_thoughts:
                thought_data.total_thoughts = thought_data.thought_number
            
            # Store the current step in thought history
            if thought_data.current_step:
                if not thought_data.previous_steps:
                    thought_data.previous_steps = []
                thought_data.previous_steps.append(thought_data.current_step)
            
            # Add to history
            self.thought_history.append(thought_data)
            
            # Prevent memory leaks by limiting history size
            if len(self.thought_history) > self.max_history_size:
                self.thought_history = self.thought_history[-self.max_history_size:]
                logger.info(f"History trimmed to {self.max_history_size} items")
            
            # Handle branches
            if thought_data.branch_from_thought and thought_data.branch_id:
                if thought_data.branch_id not in self.branches:
                    self.branches[thought_data.branch_id] = []
                self.branches[thought_data.branch_id].append(thought_data)
            
            # Format and log the thought
            formatted_thought = self._format_thought(thought_data)
            logger.info(formatted_thought)
            
            # Return response
            return {
                "thought_number": thought_data.thought_number,
                "total_thoughts": thought_data.total_thoughts,
                "next_thought_needed": thought_data.next_thought_needed,
                "branches": list(self.branches.keys()),
                "thought_history_length": len(self.thought_history),
                "available_mcp_tools": thought_data.available_mcp_tools,
                "current_step": thought_data.current_step.model_dump() if thought_data.current_step else None,
                "previous_steps": [s.model_dump() for s in thought_data.previous_steps] if thought_data.previous_steps else None,
                "remaining_steps": thought_data.remaining_steps,
            }
        except Exception as e:
            logger.error(f"Error processing thought: {e}", exc_info=True)
            return {
                "error": str(e),
                "status": "failed"
            }
