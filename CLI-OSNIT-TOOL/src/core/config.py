"""
InspectorBrain Configuration Management

Handles all configuration settings, environment variables, and user preferences
with Inspector Gadget themed defaults and professional enterprise patterns.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import Field
from pydantic_settings import BaseSettings
import json
from loguru import logger

class Settings(BaseSettings):
    """InspectorBrain application settings with Inspector Gadget theming"""

    # Application Info
    app_name: str = "InspectorBrain"
    app_version: str = "1.0.0-alpha"
    app_description: str = "Advanced OSINT TUI inspired by Inspector Gadget"

    # File Paths
    config_dir: Path = Field(default_factory=lambda: Path.home() / ".inspectorbrain")
    config_file: Path = Field(default_factory=lambda: Path.home() / ".inspectorbrain" / "config.json")
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".inspectorbrain" / "data")
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".inspectorbrain" / "cache")
    logs_dir: Path = Field(default_factory=lambda: Path.home() / ".inspectorbrain" / "logs")

    # Database Configuration
    database_url: str = Field(default="sqlite:///~/.inspectorbrain/data/investigations.db")
    database_echo: bool = False  # Set to True for SQL debugging

    # AI Configuration
    ollama_base_url: str = "http://localhost:11434"
    default_ai_model: str = "llama3.1"
    ai_timeout: int = 120  # seconds
    ai_temperature: float = 0.7
    max_conversation_history: int = 50

    # OSINT Module Settings
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    rate_limit_delay: float = 1.0  # seconds between requests
    user_agent: str = "InspectorBrain/1.0 (Educational OSINT Tool)"

    # Username Reconnaissance
    username_platforms: List[str] = [
        "github", "twitter", "instagram", "linkedin", "reddit",
        "youtube", "tiktok", "discord", "telegram", "stackoverflow"
    ]

    # Email Intelligence
    email_verification_enabled: bool = True
    breach_check_enabled: bool = True

    # Domain Analysis
    subdomain_wordlist_size: str = "medium"  # small, medium, large
    port_scan_enabled: bool = True
    common_ports: List[int] = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900]

    # TUI Theme Settings
    theme_name: str = "inspector_gadget"
    color_scheme: str = "classic_terminal"  # classic_terminal, modern_dark, retro_green
    gadget_sounds: bool = True  # Enable "Go-Go-Gadget" sound effects
    animation_speed: str = "normal"  # slow, normal, fast
    ascii_art_enabled: bool = True

    # Inspector Gadget Easter Eggs
    catchphrases_enabled: bool = True
    gadget_commands: bool = True  # Enable "Go-Go-Gadget" command prefixes
    wowser_notifications: bool = True  # Enable "Wowser!" success messages
    brain_mode: bool = True  # Enable Brain the dog references

    # Security & Privacy
    enable_logging: bool = True
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    anonymize_data: bool = True
    data_retention_days: int = 30
    respect_robots_txt: bool = True

    # Export Settings
    default_export_format: str = "json"  # json, csv, pdf, markdown
    include_metadata: bool = True
    export_dir: Path = Field(default_factory=lambda: Path.home() / "Downloads" / "InspectorBrain")

    # Advanced Features
    enable_voice_commands: bool = False  # Experimental
    hotkey_enabled: bool = True
    clipboard_integration: bool = True
    notification_enabled: bool = True

    class Config:
        env_file = ".env"
        env_prefix = "INSPECTORBRAIN_"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()
        self._load_user_config()

    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        directories = [
            self.config_dir,
            self.data_dir,
            self.cache_dir,
            self.logs_dir,
            self.export_dir
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _load_user_config(self) -> None:
        """Load user configuration from JSON file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)

                # Update settings with user config
                for key, value in user_config.items():
                    if hasattr(self, key):
                        setattr(self, key, value)

                logger.info(f"Loaded user configuration from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load user config: {e}")

    def save_config(self) -> None:
        """Save current settings to JSON file"""
        try:
            config_data = {}

            # Only save non-default values
            for field_name, field in self.__fields__.items():
                current_value = getattr(self, field_name)
                if isinstance(current_value, Path):
                    current_value = str(current_value)
                config_data[field_name] = current_value

            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2, default=str)

            logger.info(f"Saved configuration to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get_gadget_greeting(self) -> str:
        """Get a random Inspector Gadget themed greeting"""
        if not self.catchphrases_enabled:
            return "Welcome to InspectorBrain"

        greetings = [
            "Go-Go-Gadget Intelligence!",
            "Wowser! Welcome to InspectorBrain!",
            "Like Brain the dog, InspectorBrain is here to help!",
            "Inspector Gadget's finest OSINT tool at your service!",
            "Go-Go-Gadget Investigation Mode!"
        ]

        import random
        return random.choice(greetings)

    def get_success_message(self) -> str:
        """Get a random success message"""
        if not self.wowser_notifications:
            return "Operation completed successfully"

        messages = [
            "Wowser! Investigation complete!",
            "Go-Go-Gadget Success!",
            "Like Brain solving another case!",
            "Another mystery solved!",
            "Gadget would be proud!"
        ]

        import random
        return random.choice(messages)

    def get_theme_colors(self) -> Dict[str, str]:
        """Get color scheme based on selected theme"""
        themes = {
            "classic_terminal": {
                "primary": "#00FF00",      # Classic terminal green
                "secondary": "#FFFF00",    # Yellow for highlights
                "accent": "#FF0000",       # Red for errors
                "background": "#000000",   # Black background
                "text": "#FFFFFF"          # White text
            },
            "modern_dark": {
                "primary": "#61DAFB",      # React blue
                "secondary": "#F7931E",    # Orange accent
                "accent": "#FF6B6B",       # Soft red
                "background": "#1E1E1E",   # Dark grey
                "text": "#FFFFFF"          # White text
            },
            "retro_green": {
                "primary": "#39FF14",      # Neon green
                "secondary": "#FFFF00",    # Bright yellow
                "accent": "#FF1493",       # Deep pink
                "background": "#000000",   # Black
                "text": "#39FF14"          # Neon green text
            }
        }

        return themes.get(self.color_scheme, themes["classic_terminal"])

# Global settings instance
settings = Settings()