"""
This module defines the Pydantic models for the Chat entity. These models are used for data validation,
serialization and deserialization.
"""

from pydantic import BaseModel


class ChatBase(BaseModel):
    """
    A base model for chat responses that includes the common attributes.
    """

    query: str
    result: str
    # sources: Optional[str] = None
