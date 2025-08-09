"""
Utility functions for the Wikipedia Researcher Agent
"""
import os
from typing import Dict, Any, List
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "wikipedia_language": os.getenv("WIKIPEDIA_LANGUAGE", "en"),
        "max_search_results": int(os.getenv("MAX_SEARCH_RESULTS", "3")),
        "max_content_length": int(os.getenv("MAX_CONTENT_LENGTH", "3000"))
    }


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate that required configuration is present"""
    if not config.get("openai_api_key"):
        st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
        st.info("You can get an API key from: https://platform.openai.com/api-keys")
        return False
    return True


def format_sources(sources: List[Dict[str, Any]]) -> str:
    """Format sources for display in Streamlit"""
    if not sources:
        return "No sources available"
    
    formatted_sources = []
    for i, source in enumerate(sources, 1):
        title = source.get("title", "Unknown")
        url = source.get("url", "#")
        summary = source.get("summary", "")
        
        source_text = f"{i}. **[{title}]({url})**"
        if summary:
            source_text += f"\n   *{summary[:200]}{'...' if len(summary) > 200 else ''}*"
        
        formatted_sources.append(source_text)
    
    return "\n\n".join(formatted_sources)


def display_research_results(result: Dict[str, Any]) -> None:
    """Display research results in Streamlit interface"""
    
    # Display the main answer
    if result.get("answer"):
        st.subheader("📝 Research Answer")
        st.write(result["answer"])
    
    # Display sources
    sources = result.get("sources", [])
    if sources:
        st.subheader("📚 Sources")
        st.markdown(format_sources(sources))
    
    # Display any errors
    if result.get("error"):
        st.error(f"Error: {result['error']}")


def create_sidebar_info() -> None:
    """Create informational sidebar"""
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This Wikipedia Researcher Agent uses:
        - **LangGraph** for workflow orchestration
        - **Wikipedia API** for content retrieval
        - **GPT-3.5** for intelligent summarization
        """)
        
        st.header("🔧 How it works")
        st.write("""
        1. **Search**: Finds relevant Wikipedia articles
        2. **Extract**: Retrieves article content
        3. **Analyze**: Uses AI to generate comprehensive answers
        4. **Present**: Shows results with source citations
        """)
        
        st.header("💡 Tips")
        st.write("""
        - Be specific in your questions
        - Use proper nouns when relevant
        - Ask about topics likely to have Wikipedia coverage
        """)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables"""
    if "research_history" not in st.session_state:
        st.session_state.research_history = []
    
    if "current_query" not in st.session_state:
        st.session_state.current_query = ""


def add_to_history(query: str, result: Dict[str, Any]) -> None:
    """Add research result to session history"""
    if "research_history" not in st.session_state:
        st.session_state.research_history = []
    
    st.session_state.research_history.append({
        "query": query,
        "result": result,
        "timestamp": st.session_state.get("timestamp", "")
    })
    
    # Keep only last 10 searches
    if len(st.session_state.research_history) > 10:
        st.session_state.research_history = st.session_state.research_history[-10:]


def display_search_history() -> None:
    """Display search history in sidebar"""
    if st.session_state.get("research_history"):
        with st.sidebar:
            st.header("🕒 Recent Searches")
            for i, item in enumerate(reversed(st.session_state.research_history[-5:]), 1):
                query = item["query"]
                if len(query) > 50:
                    query = query[:47] + "..."
                
                if st.button(f"{i}. {query}", key=f"history_{i}"):
                    st.session_state.current_query = item["query"]
                    st.rerun()
