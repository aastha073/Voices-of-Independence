"""
Historical document sources for the Voices of Independence project.
Each source includes metadata and URL for fetching.
"""

# Define sources for historical documents
SOURCES = {
    "founding_documents": [
        {
            "title": "Declaration of Independence",
            "url": "https://www.archives.gov/founding-docs/declaration-transcript",
            "date": "1776-07-04",
            "authors": ["Thomas Jefferson", "Continental Congress"],
            "type": "founding_document"
        },
        {
            "title": "The Constitution of the United States",
            "url": "https://www.archives.gov/founding-docs/constitution-transcript",
            "date": "1787-09-17",
            "authors": ["Constitutional Convention"],
            "type": "founding_document"
        },
        {
            "title": "The Bill of Rights",
            "url": "https://www.archives.gov/founding-docs/bill-of-rights-transcript",
            "date": "1789-09-25",
            "authors": ["James Madison", "First Congress"],
            "type": "founding_document"
        }
    ],
    "speeches": [
        {
            "title": "Common Sense",
            "url": "https://www.gutenberg.org/cache/epub/147/pg147.txt",
            "date": "1776-01-10",
            "authors": ["Thomas Paine"],
            "type": "pamphlet"
        },
        {
            "title": "Give Me Liberty or Give Me Death",
            "url": "https://avalon.law.yale.edu/18th_century/patrick.asp",
            "date": "1775-03-23",
            "authors": ["Patrick Henry"],
            "type": "speech"
        }
    ],
    "letters": [
        {
            "title": "Letter from Abigail Adams to John Adams, 31 March - 5 April 1776",
            "url": "https://founders.archives.gov/documents/Adams/04-01-02-0241",
            "date": "1776-03-31",
            "authors": ["Abigail Adams"],
            "recipient": "John Adams",
            "type": "letter"
        },
        {
            "title": "From Thomas Jefferson to John Adams, 28 October 1813",
            "url": "https://founders.archives.gov/documents/Jefferson/03-06-02-0446",
            "date": "1813-10-28",
            "authors": ["Thomas Jefferson"],
            "recipient": "John Adams",
            "type": "letter"
        }
    ],
    "federalist_papers": [
        {
            "title": "Federalist No. 1",
            "url": "https://avalon.law.yale.edu/18th_century/fed01.asp",
            "date": "1787-10-27",
            "authors": ["Alexander Hamilton"],
            "type": "essay"
        },
        {
            "title": "Federalist No. 10",
            "url": "https://avalon.law.yale.edu/18th_century/fed10.asp",
            "date": "1787-11-22",
            "authors": ["James Madison"],
            "type": "essay"
        }
    ]
}

def get_all_sources():
    """Return a flat list of all document sources."""
    all_sources = []
    for source_type, documents in SOURCES.items():
        all_sources.extend(documents)
    return all_sources

def get_sources_by_type(source_type):
    """Return sources of a specific type."""
    return SOURCES.get(source_type, [])