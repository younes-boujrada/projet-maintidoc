from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class IndexedChunkMetadata(BaseModel):
    chunk_id: str
    document_id: str
    version: str = "v1.0 (2026-01)"
    page: int = 1
    element_type: str = "procedure_paragraph"  # procedure_paragraph, code_table, schema, photo
    famille_equipement: str  # appareils_photo or imprimantes_pro
    equipment_id: str  # Canon EOS R50 or Epson SC-P700
    groupes_acces: str  # comma-separated or primary group name
    source_sha256: str
    has_visual_element: bool = False
    linked_image_id: Optional[str] = None
    usage_test: str = "normal"  # normal, contradictoire, injection, normal (OCR)


class Citation(BaseModel):
    document_id: str
    page: int
    figure_or_element: Optional[str] = None
    snippet: str


class TicketDraft(BaseModel):
    equipment_id: str
    title: str
    description: str
    severity: Literal["FAIBLE", "MOYENNE", "CRITIQUE"] = "MOYENNE"
    recommended_part: Optional[str] = None
    approval_token: Optional[str] = None
    idempotency_key: str


class TicketRecord(BaseModel):
    ticket_id: str
    equipment_id: str
    title: str
    description: str
    severity: str
    recommended_part: Optional[str] = None
    created_at: str
    status: str = "OUVERT"
    created_by: str
    idempotency_key: str


class AgentResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    sources: List[dict] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    ticket_draft: Optional[TicketDraft] = None
    warnings: List[str] = Field(default_factory=list)
    human_interrupt_required: bool = False
