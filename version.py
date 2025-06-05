# -*- coding: utf-8 -*-
"""Version information for VLM Studio Lite."""

__version__ = "2.0.0"
__author__ = "VLM Studio Lite Contributors"
__email__ = "sorrowscry86@users.noreply.github.com"
__description__ = "Multi-Agent AI Development Platform with Enhanced Monitoring"
__url__ = "https://github.com/sorrowscry86/Codeystack"
__license__ = "MIT"
__status__ = "Production"

# Version info tuple for programmatic access
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Build information
BUILD_DATE = "2025-06-05"
BUILD_NUMBER = "20250605.1"

# Supported Python versions
PYTHON_REQUIRES = ">=3.11"

# Feature flags for this version
FEATURES = {
    "agent_monitoring": True,
    "multi_llm_providers": True,
    "real_time_dashboard": True,
    "dynamic_configuration": True,
    "docker_support": True,
    "api_backend": True,
    "performance_analytics": True,
    "session_persistence": True
}

# Provider compatibility matrix
SUPPORTED_PROVIDERS = {
    "openai": ">=1.51.0",
    "google-generativeai": ">=0.8.0", 
    "anthropic": ">=0.28.0",
    "ollama": ">=0.2.0",
    "requests": ">=2.32.0"  # For OpenRouter and others
}

def get_version():
    """Return the version string."""
    return __version__

def get_version_info():
    """Return version information as a dictionary."""
    return {
        "version": __version__,
        "build_date": BUILD_DATE,
        "build_number": BUILD_NUMBER,
        "python_requires": PYTHON_REQUIRES,
        "features": FEATURES,
        "supported_providers": SUPPORTED_PROVIDERS
    }

if __name__ == "__main__":
    print(f"VLM Studio Lite v{__version__}")
    print(f"Build: {BUILD_NUMBER} ({BUILD_DATE})")
    print(f"Python: {PYTHON_REQUIRES}")
    print(f"Status: {__status__}")
