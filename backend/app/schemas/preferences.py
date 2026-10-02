from datetime import date, datetime, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


Weekday = Literal[
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
SummaryTemplate = Literal["standard", "concise", "detailed"]


class WorkingHoursWindow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: time
    end: time

    @field_validator("start", "end")
    @classmethod
    def require_local_clock_time(cls, value: time) -> time:
        if value.utcoffset() is not None:
            raise ValueError("Working-hour times must not include a timezone offset.")
        return value

    @model_validator(mode="after")
    def validate_window(self) -> "WorkingHoursWindow":
        if self.start >= self.end:
            raise ValueError("Working-hours end must be later than start.")
        return self


class ProviderPreferencesUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    working_hours: dict[Weekday, WorkingHoursWindow]
    session_duration: int = Field(ge=15, le=240)
    buffer_time: int = Field(ge=0, le=120)
    blackout_dates: list[date] = Field(max_length=365)
    max_sessions_per_day: int = Field(ge=1, le=16)
    summary_template: SummaryTemplate

    @model_validator(mode="after")
    def validate_working_hours(self) -> "ProviderPreferencesUpdate":
        if not self.working_hours:
            raise ValueError("At least one working-hours day must be configured.")
        return self

    @model_validator(mode="after")
    def validate_blackout_dates(self) -> "ProviderPreferencesUpdate":
        if len(set(self.blackout_dates)) != len(self.blackout_dates):
            raise ValueError("Blackout dates must be unique.")
        return self


class ProviderPreferencesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider_id: str
    working_hours: dict[Weekday, WorkingHoursWindow]
    session_duration: int
    buffer_time: int
    blackout_dates: list[date]
    max_sessions_per_day: int
    summary_template: SummaryTemplate
    created_at: datetime
    updated_at: datetime