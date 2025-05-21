"""
Gradio web interface for the Voices of Independence project.
"""

import os
import logging
import gradio as gr
from utils.config import get_config, configure_logging
from database.weaviate_client import connect_to_weaviate
from database.schema import get_collection
from rag.independence_rag import independence_rag

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Get configuration
config = get_config()
MODES = config["response_modes"]

def format_sources(sources):
    """Format sources for display."""
    return "\n".join([f"- {source}" for source in sources])

def process_query(query, mode, limit):
    """
    Process a user query and return formatted results.
    
    Args:
        query (str): User query
        mode (str): Response mode
        limit (int): Number of documents to retrieve
        
    Returns:
        tuple: (response, sources)
    """
    if not query.strip():
        return "Please enter a question about American Independence.", ""
    
    try:
        # Connect to Weaviate
        client = connect_to_weaviate()
        collection = get_collection(client)
        
        if not collection:
            return "Error: Could not connect to document database.", ""
        
        # Process the query
        result = independence_rag(
            collection=collection,
            query=query,
            mode=mode,
            limit=int(limit)
        )
        
        response = result["response"]
        sources = format_sources(result["sources"])
        
        return response, sources
    
    except Exception as e:
        logger.exception(f"Error processing query: {str(e)}")
        return f"An error occurred: {str(e)}", ""

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    # Create the interface
    with gr.Blocks(title="Voices of Independence: Time Travel to 1776") as demo:
        gr.Markdown("""
        # 🎆 Voices of Independence: An AI-Powered Time Travel Through 1776
        
        Ask questions about the American Revolution and founding of the United States.
        Our AI will search through historical documents and generate responses based on primary sources.
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                query_input = gr.Textbox(
                    label="Your Question",
                    placeholder="What were the main grievances against King George III?",
                    lines=2
                )
            with gr.Column(scale=1):
                # Create dropdown with display values but return the keys
                mode_keys = list(MODES.keys())
                mode_values = list(MODES.values())
                mode_dropdown = gr.Dropdown(
                    label="Response Mode",
                    choices=mode_values,
                    value=MODES[config["default_mode"]]
                )
                limit_slider = gr.Slider(
                    label="Number of Documents to Search",
                    minimum=1,
                    maximum=10,
                    value=config["default_search_limit"],
                    step=1
                )
        
        submit_btn = gr.Button("Ask About Independence")
        
        with gr.Row():
            with gr.Column(scale=2):
                response_output = gr.Textbox(label="Response", lines=12)
            with gr.Column(scale=1):
                sources_output = gr.Textbox(label="Sources", lines=12)
        
        gr.Markdown("""
        ### Example Questions:
        - What were the key arguments for independence in 1776?
        - How did the founding fathers view democracy?
        - What complaints did the colonists have about taxes?
        - What role did Thomas Jefferson play in the Declaration of Independence?
        - What were Abigail Adams' views on women's rights?
        """)
        
        # Mode dropdown mapping
        def get_mode_key(mode_value):
            """Convert display value to key."""
            for k, v in MODES.items():
                if v == mode_value:
                    return k
            return config["default_mode"]
        
        # Handle form submission
        submit_btn.click(
            fn=lambda q, m, l: process_query(q, get_mode_key(m), l),
            inputs=[query_input, mode_dropdown, limit_slider],
            outputs=[response_output, sources_output]
        )
    
    return demo

def run_app():
    """Run the Gradio app."""
    demo = create_gradio_interface()
    demo.launch(share=True)

if __name__ == "__main__":
    run_app()
