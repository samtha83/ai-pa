from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProviderProfileUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=255)
    business_name: str | None = Field(default=None, min_length=1, max_length=255)
    timezone: str | None = Field(default=None, min_length=1, max_length=64)
    tone: str | None = Field(default=None, min_length=1, max_length=80)
    modality: str | None = Field(default=None, min_length=1, max_length=100)
    service_type: str | None = Field(default=None, min_length=1, max_length=100)
    template_settings: dict[str, object] | None = None
    boundaries: dict[str, object] | None = None

    @field_validator("name", "timezone")
    @classmethod
    def required_profile_values_cannot_be_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("This field cannot be null.")
        return value

    @field_validator("timezone")
    @classmethod
    def timezone_must_be_known(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Timezone must be a valid IANA timezone.") from exc
        return value


class ProviderProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    business_name: str | None
    timezone: str
    tone: str | None
    modality: str | None
    service_type: str | None
    template_settings: dict[str, object] | None
    boundaries: dict[str, object] | None
    created_at: datetime
    updated_at: datetime