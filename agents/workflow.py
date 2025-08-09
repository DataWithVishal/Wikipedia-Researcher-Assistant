"""
LangGraph workflow definition for Wikipedia research agent
"""
from langgraph.graph import StateGraph, START, END
from typing import Dict, Any, TypedDict
from .nodes import WikipediaSearchNode, WikipediaSummaryNode, GPTSummarizerNode
import logging

logger = logging.getLogger(__name__)


class ResearchState(TypedDict):
    """State schema for the research workflow"""
    query: str
    search_results: list
    documents: list
    answer: str
    sources: list
    error: str


class WikipediaResearchWorkflow:
    """Main workflow class for Wikipedia research agent"""
    
    def __init__(self, max_results: int = 3, max_content_length: int = 3000):
        self.max_results = max_results
        self.max_content_length = max_content_length
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Initialize nodes
        search_node = WikipediaSearchNode(max_results=self.max_results)
        summary_node = WikipediaSummaryNode(max_content_length=self.max_content_length)
        gpt_node = GPTSummarizerNode()
        
        # Create the state graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes to the graph
        workflow.add_node("search", search_node)
        workflow.add_node("summarize", summary_node)
        workflow.add_node("generate_answer", gpt_node)
        
        # Define the workflow edges
        workflow.add_edge(START, "search")
        workflow.add_edge("search", "summarize")
        workflow.add_edge("summarize", "generate_answer")
        workflow.add_edge("generate_answer", END)
        
        return workflow.compile()
    
    def research(self, query: str) -> Dict[str, Any]:
        """
        Execute the research workflow for a given query
        
        Args:
            query (str): The research question
            
        Returns:
            Dict[str, Any]: Research results including answer and sources
        """
        try:
            logger.info(f"Starting research workflow for query: {query}")
            
            # Initialize the state
            initial_state = {
                "query": query,
                "search_results": [],
                "documents": [],
                "answer": "",
                "sources": [],
                "error": ""
            }
            
            # Execute the workflow
            result = self.workflow.invoke(initial_state)
            
            logger.info("Research workflow completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}")
            return {
                "query": query,
                "search_results": [],
                "documents": [],
                "answer": f"An error occurred during research: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def get_workflow_graph(self):
        """Return the compiled workflow graph"""
        return self.workflow


# Factory function to create a research agent
def create_wikipedia_agent(max_results: int = 3, max_content_length: int = 3000) -> WikipediaResearchWorkflow:
    """
    Factory function to create a Wikipedia research agent
    
    Args:
        max_results (int): Maximum number of Wikipedia articles to search
        max_content_length (int): Maximum content length per article
        
    Returns:
        WikipediaResearchWorkflow: Configured research workflow
    """
    return WikipediaResearchWorkflow(
        max_results=max_results,
        max_content_length=max_content_length
    )
