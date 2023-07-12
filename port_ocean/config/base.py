import os
import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseSettings

PROVIDER_WRAPPER_PATTERN = r"\{\{ from (.*) \}\}"
PROVIDER_CONFIG_PATTERN = r"^[a-zA-Z0-9]+ .*$"


def read_yaml_config_settings_source(
    settings: "BaseOceanSettings", base_path: str
) -> str:
    yaml_file = getattr(settings.__config__, "yaml_file", "")

    assert yaml_file, "Settings.yaml_file not properly configured"

    path = Path(base_path, yaml_file)

    if not path.exists():
        raise FileNotFoundError(f"Could not open yaml settings file at: {path}")

    return path.read_text("utf-8")


def parse_config_provider(value: str) -> tuple[str, str]:
    match = re.match(PROVIDER_CONFIG_PATTERN, value)
    if not match:
        raise ValueError(
            f"Invalid pattern: {value}. Pattern should match: {PROVIDER_CONFIG_PATTERN}"
        )

    provider_type, provider_value = value.split(" ", 1)

    return provider_type, provider_value


def load_from_config_provider(provider_type: str, value: str) -> Any:
    if provider_type == "env":
        result = os.environ.get(value)
        if result is None:
            raise ValueError(f"Environment variable not found: {value}")
        return result
    else:
        raise ValueError(f"Invalid provider type: {provider_type}")


def load_providers(settings: "BaseOceanSettings", base_path: str) -> dict[str, Any]:
    yaml_content = read_yaml_config_settings_source(settings, base_path)
    matches = re.finditer(PROVIDER_WRAPPER_PATTERN, yaml_content)
    for match in matches:
        provider_type, provider_value = parse_config_provider(match.group(1))
        data = load_from_config_provider(provider_type, provider_value)
        # Replace the provider wrapper with the actual value
        yaml_content = re.sub(re.escape(match.group()), data, yaml_content, count=1)

    return yaml.safe_load(yaml_content)


class BaseOceanSettings(BaseSettings):
    base_path: str

    class Config:
        yaml_file = "./config.yaml"

        @classmethod
        def customise_sources(cls, init_settings, *_, **__):  # type: ignore
            return (
                init_settings,
                lambda s: load_providers(s, init_settings.init_kwargs["base_path"]),
            )
