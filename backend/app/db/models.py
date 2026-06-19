import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Boolean
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="officer")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Officer(Base):
    __tablename__ = "officers"

    id = Column(String(50), primary_key=True)  # e.g., 'OFF-2024-001'
    name = Column(String(255), nullable=False)
    rank = Column(String(100), nullable=False)
    station = Column(String(255), nullable=False)
    badge = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(String(50), primary_key=True)  # e.g., 'CMP-2024-001'
    fir_number = Column(String(100), nullable=True, index=True)
    complainant_name = Column(String(255), nullable=False)
    mobile_number = Column(String(50), nullable=False)
    address = Column(Text, nullable=True)
    incident_date = Column(String(100), nullable=True)
    incident_time = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    suspect_details = Column(Text, nullable=True)
    witness_details = Column(Text, nullable=True)
    crime_type = Column(String(100), nullable=True)
    property_details = Column(Text, nullable=True)
    status = Column(String(50), default="Draft", index=True)
    officer_id = Column(String(50), ForeignKey("officers.id"), nullable=True)
    officer_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    transcript = Column(Text, nullable=True)
    completion_percentage = Column(Integer, default=0)

    # Relationships
    officer = relationship("Officer")
    fir = relationship("FIR", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    legal_analysis = relationship("LegalAnalysis", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    evidence_analysis = relationship("EvidenceAnalysis", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    timeline = relationship("CaseTimeline", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    risk_assessment = relationship("RiskAssessment", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    investigation_report = relationship("InvestigationReport", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    action_recommendations = relationship("ActionRecommendation", back_populates="complaint", uselist=False, cascade="all, delete-orphan")


class FIR(Base):
    __tablename__ = "firs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fir_number = Column(String(100), unique=True, nullable=False, index=True)
    complaint_id = Column(String(50), ForeignKey("complaints.id"), nullable=False, unique=True)
    narrative = Column(Text, nullable=False)
    raw_fir_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="fir")


class LegalAnalysis(Base):
    __tablename__ = "legal_analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(50), ForeignKey("complaints.id"), nullable=False, unique=True)
    recommended_sections = Column(JSON, nullable=False)
    legal_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="legal_analysis")


class EvidenceAnalysis(Base):
    __tablename__ = "evidence_analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(50), ForeignKey("complaints.id"), nullable=False, unique=True)
    evidence_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="evidence_analysis")


class CaseTimeline(Base):
    __tablename__ = "case_timelines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(50), ForeignKey("complaints.id"), nullable=False, unique=True)
    timeline_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="timeline")


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(50), ForeignKey("complaints.id"), nullable=False, unique=True)
    assessment_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="risk_assessment")


class InvestigationReport(Base):
    __tablename__ = "investigation_reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(50), ForeignKey("complaints.id"), nullable=False, unique=True)
    report_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="investigation_report")


class ActionRecommendation(Base):
    __tablename__ = "action_recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(50), ForeignKey("complaints.id"), nullable=False, unique=True)
    recommendations_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="action_recommendations")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AnalyticsMetric(Base):
    __tablename__ = "analytics_metrics"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String(255), nullable=False)
    metric_value = Column(JSON, nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
