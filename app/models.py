from __future__ import annotations

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text

from .database import Base


class ScanModel(Base):
    """Persistent representation of a single ZAP scan."""

    __tablename__ = "scans"

    id           = Column(String,  primary_key=True, nullable=False)
    target       = Column(String,  nullable=False)
    status       = Column(String,  nullable=False, default="queued")
    created_at   = Column(Float,   nullable=False)
    started_at   = Column(Float,   nullable=True)
    finished_at  = Column(Float,   nullable=True)
    error        = Column(Text,    nullable=True)
    return_code  = Column(Integer, nullable=True)
    # alerts and summary are stored as JSON text to avoid extra tables
    alerts_json  = Column(Text,    nullable=True)
    summary_json = Column(Text,    nullable=True)
    # file-system paths written by the subprocess runner
    report_json  = Column(Text,    nullable=True)
    report_html  = Column(Text,    nullable=True)
    log_file     = Column(Text,    nullable=True)
    team_id      = Column(String,  ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)


class ScheduleModel(Base):
    """A user-created scheduled scan stored in the database."""

    __tablename__ = "schedules"

    id                = Column(String,  primary_key=True, nullable=False)
    target            = Column(String,  nullable=False)
    cron              = Column(String,  nullable=False)   # 5-field UTC cron expression
    tz                = Column(String,  nullable=False, default="UTC")  # display timezone
    created_at        = Column(Float,   nullable=False)
    enabled           = Column(Boolean, nullable=False, default=True)
    # Comma-separated e-mail addresses to notify after each scheduled scan
    distribution_list = Column(Text,    nullable=True)
    team_id           = Column(String,  ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)


class TeamModel(Base):
    """A team that can own application users."""

    __tablename__ = "teams"

    id         = Column(String, primary_key=True, nullable=False)
    name       = Column(String, nullable=False, unique=True)
    created_at = Column(Float,  nullable=False)


class AppUserModel(Base):
    """An application user with an e-mail address, role, and an assigned team."""

    __tablename__ = "app_users"

    id         = Column(String, primary_key=True, nullable=False)
    email      = Column(String, nullable=False, unique=True)
    role       = Column(String, nullable=False, default="user")
    team_id    = Column(String, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(Float,  nullable=False)
