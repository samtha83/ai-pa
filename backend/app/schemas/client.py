from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator


ClientStatus = Literal["active", "inactive"]


class ClientCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=320)
    phone: str | None = Field(default=None, max_length=32)
    timezone: str = Field(default="UTC", min_length=1, max_length=64)
    service_type: str | None = Field(default=None, max_length=100)
    goals: list[str] = Field(default_factory=list, max_length=50)
    status: ClientStatus = "active"

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value:
            raise ValueError("Client name cannot be blank.")
        return value

    @field_validator("timezone")
    @classmethod
    def timezone_must_be_known(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Timezone must be a valid IANA timezone.") from exc
        return value


class ClientUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=320)
    phone: str | None = Field(default=None, max_length=32)
    timezone: str | None = Field(default=None, min_length=1, max_length=64)
    service_type: str | None = Field(default=None, max_length=100)
    goals: list[str] | None = Field(default=None, max_length=50)
    status: ClientStatus | None = None

    @field_validator("status", mode="before")
    @classmethod
    def status_cannot_be_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("Status cannot be null.")
        return value

    @field_validator("name")
    @classmethod
    def name_cannot_be_null_or_blank(cls, value: str | None) -> str:
        if value is None or not value:
            raise ValueError("Client name cannot be blank or null.")
        return value

    @field_validator("timezone")
    @classmethod
    def timezone_must_be_known(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Timezone cannot be null.")
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Timezone must be a valid IANA timezone.") from exc
        return value

    @field_validator("goals")
    @classmethod
    def goals_cannot_be_null(cls, value: list[str] | None) -> list[str]:
        if value is None:
            raise ValueError("Goals cannot be null.")
        return value


class ClientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    provider_id: str
    name: str
    email: str | None
    phone: str | None
    timezone: str
    service_type: str | None
    goals: list[str]
    status: ClientStatus
    created_at: datetime
    updated_at: datetime