"""
UI module for the Voices of Independence project.
Provides Gradio web interface.
"""

from .gradio_app import create_gradio_interface, run_app

__all__ = [
    'create_gradio_interface',
    'run_app'
]