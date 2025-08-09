"""
Wikipedia Researcher Agent - Streamlit Application
"""
import streamlit as st
import os
from datetime import datetime
from agents.workflow import create_wikipedia_agent
from utils.helpers import (
    load_config, 
    validate_config, 
    display_research_results,
    create_sidebar_info,
    initialize_session_state,
    add_to_history,
    display_search_history
)

# Page configuration
st.set_page_config(
    page_title="Wikipedia Researcher Agent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .search-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .result-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Load configuration
    config = load_config()
    
    # Main header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("📚 Wikipedia Researcher Agent")
    st.markdown("*Powered by LangGraph, Wikipedia API, and GPT-3.5*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create sidebar
    create_sidebar_info()
    display_search_history()
    
    # Validate configuration
    if not validate_config(config):
        st.stop()
    
    # Create the research agent
    try:
        agent = create_wikipedia_agent(
            max_results=config["max_search_results"],
            max_content_length=config["max_content_length"]
        )
    except Exception as e:
        st.error(f"Failed to initialize research agent: {str(e)}")
        st.stop()
    
    # Main search interface
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # Query input
        query = st.text_input(
            "🔍 Enter your research question:",
            value=st.session_state.get("current_query", ""),
            placeholder="e.g., What is quantum computing and how does it work?",
            help="Ask any question that might have information available on Wikipedia"
        )
        
        # Search button and options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_button = st.button("🚀 Research", type="primary")
        
        with col2:
            if st.button("🗑️ Clear"):
                st.session_state.current_query = ""
                st.rerun()
        
        with col3:
            show_advanced = st.checkbox("⚙️ Advanced")
        
        # Advanced options
        if show_advanced:
            st.markdown("**Advanced Options:**")
            col1, col2 = st.columns(2)
            
            with col1:
                max_results = st.slider(
                    "Max Wikipedia articles",
                    min_value=1,
                    max_value=5,
                    value=config["max_search_results"],
                    help="Number of Wikipedia articles to search"
                )
            
            with col2:
                max_content = st.slider(
                    "Max content length per article",
                    min_value=1000,
                    max_value=5000,
                    value=config["max_content_length"],
                    step=500,
                    help="Maximum characters to extract from each article"
                )
            
            # Update agent with new settings
            if max_results != config["max_search_results"] or max_content != config["max_content_length"]:
                agent = create_wikipedia_agent(
                    max_results=max_results,
                    max_content_length=max_content
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Process search request
    if search_button and query.strip():
        
        # Update current query in session state
        st.session_state.current_query = query
        
        # Show progress
        with st.spinner("🔍 Searching Wikipedia and analyzing content..."):
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Search
                status_text.text("🔍 Searching Wikipedia articles...")
                progress_bar.progress(25)
                
                # Step 2: Extract
                status_text.text("📄 Extracting article content...")
                progress_bar.progress(50)
                
                # Step 3: Analyze
                status_text.text("🤖 Analyzing with GPT-3.5...")
                progress_bar.progress(75)
                
                # Execute research
                result = agent.research(query)
                
                # Step 4: Complete
                status_text.text("✅ Research complete!")
                progress_bar.progress(100)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Add to history
                add_to_history(query, result)
                
            except Exception as e:
                st.error(f"Research failed: {str(e)}")
                st.stop()
        
        # Display results
        if result:
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            display_research_results(result)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Copy Answer"):
                    st.write("Answer copied to clipboard!")
            
            with col2:
                # Create downloadable content
                download_content = f"""# Research Query: {query}

## Answer:
{result.get('answer', 'No answer available')}

## Sources:
"""
                for i, source in enumerate(result.get('sources', []), 1):
                    download_content += f"{i}. {source.get('title', 'Unknown')} - {source.get('url', '#')}\n"
                
                st.download_button(
                    label="💾 Download Results",
                    data=download_content,
                    file_name=f"wikipedia_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
            
            with col3:
                if st.button("🔄 New Search"):
                    st.session_state.current_query = ""
                    st.rerun()
    
    elif search_button and not query.strip():
        st.warning("⚠️ Please enter a research question.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            Built with ❤️ using Streamlit, LangGraph, and OpenAI GPT-3.5<br>
            Data sourced from Wikipedia under Creative Commons license
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
