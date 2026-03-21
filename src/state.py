from typing import List, Literal, Union, Optional
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    user_input: str # The story beat or theme
    research_data: Optional[str] # Facts if search was needed
    draft_story: str # Current version of story
    judge_feedback: Optional[str] # Feedback from judge
    status: Literal["approved", "retry_writer", "rejected", "research"]
    needs_search: bool # Flag for research
    rejection_reason: Optional[str] # Reason for rejection
    retry_count: int # How many loops we've done

class SafetyCheck(BaseModel):
    is_safe: bool = Field(description="Is the topic safe and appropriate for kids aged 5-10?")
    needs_search: bool = Field(description="Does this topic require factual research or real-world details for a better story?")
    reason: str = Field(description="If unsafe, provide a short explanation.")

class StoryScorecard(BaseModel):
    is_safe: bool = Field(description="Is the story appropriate for children aged 5-10?")
    reasoning: str = Field(description="Brief explanation of why it passed/failed.")
    action: Literal["approved", "retry_writer"] = Field(
        description="Should we finish or rewrite?"
    )
