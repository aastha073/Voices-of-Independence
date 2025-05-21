"""
Visualization functions for the Voices of Independence project.
"""

import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
from utils.opik_tracking import opik

logger = logging.getLogger(__name__)

@opik.track
def create_timeline_visualization(docs_list, save_path=None, show=False):
    """
    Create a timeline visualization of historical documents.
    
    Args:
        docs_list (list): List of document dictionaries with metadata
        save_path (str, optional): Path to save the visualization
        show (bool): Whether to display the visualization
        
    Returns:
        plt: Matplotlib figure
    """
    logger.info(f"Creating timeline visualization with {len(docs_list)} documents")
    
    # Convert to DataFrame
    df = pd.DataFrame(docs_list)
    
    # Convert date strings to datetime objects
    df['datetime'] = pd.to_datetime(df['date'])
    df = df.sort_values('datetime')
    
    # Create color mapping for document types
    doc_types = df['document_type'].unique()
    color_map = {}
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33']
    for i, doc_type in enumerate(doc_types):
        color_map[doc_type] = colors[i % len(colors)]
    
    # Create the figure
    plt.figure(figsize=(15, 8))
    
    # Plot each document as a point
    for doc_type in doc_types:
        subset = df[df['document_type'] == doc_type]
        plt.scatter(subset['datetime'], [1] * len(subset), 
                   color=color_map[doc_type], s=100, label=doc_type)
    
    # Add document titles as annotations
    for _, row in df.iterrows():
        plt.annotate(row['title'], 
                    (row['datetime'], 1), 
                    rotation=45, 
                    ha='right', 
                    va='bottom')
    
    # Format the chart
    plt.yticks([])
    plt.xlabel('Date', fontsize=14)
    plt.title('Timeline of Historical Documents', fontsize=16)
    plt.legend(title='Document Type')
    
    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
    plt.gcf().autofmt_xdate()
    
    # Set grid
    plt.grid(True, axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path)
        logger.info(f"Timeline visualization saved to {save_path}")
    
    # Show if requested
    if show:
        plt.show()
    
    return plt