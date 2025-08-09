"""
LangGraph nodes for Wikipedia research workflow
"""
import wikipedia
from openai import OpenAI
import os
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikipediaSearchNode:
    """Node for searching Wikipedia articles based on user query"""
    
    def __init__(self, max_results: int = 3):
        self.max_results = max_results
        wikipedia.set_lang("en")  # Set language to English
    
    def __call__(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        query = inputs.get("query", "")
        
        if not query:
            return {"search_results": [], "error": "No query provided"}
        
        try:
            logger.info(f"Searching Wikipedia for: {query}")
            results = wikipedia.search(query, results=self.max_results)
            
            if not results:
                # Try with a more general search term
                simplified_query = query.split()[0] if query.split() else query
                results = wikipedia.search(simplified_query, results=self.max_results)
            
            logger.info(f"Found {len(results)} Wikipedia articles")
            return {"search_results": results, "query": query}
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation by taking the first few options
            logger.info(f"Disambiguation found, using first {self.max_results} options")
            return {"search_results": e.options[:self.max_results], "query": query}
            
        except Exception as e:
            logger.error(f"Wikipedia search error: {str(e)}")
            return {"search_results": [], "error": str(e), "query": query}


class WikipediaSummaryNode:
    """Node for retrieving and processing Wikipedia page content"""
    
    def __init__(self, max_content_length: int = 3000):
        self.max_content_length = max_content_length
    
    def __call__(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        search_results = inputs.get("search_results", [])
        query = inputs.get("query", "")
        
        if not search_results:
            return {"documents": [], "query": query, "error": "No search results to process"}
        
        documents = []
        
        for title in search_results:
            try:
                logger.info(f"Retrieving content for: {title}")
                page = wikipedia.page(title)
                
                # Truncate content to manage token limits
                content = page.content[:self.max_content_length]
                if len(page.content) > self.max_content_length:
                    content += "... [Content truncated]"
                
                documents.append({
                    "title": title,
                    "content": content,
                    "url": page.url,
                    "summary": page.summary[:500] if page.summary else ""
                })
                
            except wikipedia.exceptions.DisambiguationError as e:
                # Try the first disambiguation option
                try:
                    page = wikipedia.page(e.options[0])
                    content = page.content[:self.max_content_length]
                    if len(page.content) > self.max_content_length:
                        content += "... [Content truncated]"
                    
                    documents.append({
                        "title": e.options[0],
                        "content": content,
                        "url": page.url,
                        "summary": page.summary[:500] if page.summary else ""
                    })
                except:
                    logger.warning(f"Could not resolve disambiguation for: {title}")
                    continue
                    
            except wikipedia.exceptions.PageError:
                logger.warning(f"Page not found: {title}")
                continue
                
            except Exception as e:
                logger.error(f"Error retrieving page {title}: {str(e)}")
                continue
        
        logger.info(f"Successfully retrieved {len(documents)} documents")
        return {"documents": documents, "query": query}


class GPTSummarizerNode:
    """Node for generating answers using GPT-3.5 based on Wikipedia content"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def __call__(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        query = inputs.get("query", "")
        documents = inputs.get("documents", [])
        
        if not query:
            return {"answer": "No query provided", "sources": []}
        
        if not documents:
            return {
                "answer": "I couldn't find any relevant Wikipedia articles for your query. Please try rephrasing your question or using different keywords.",
                "sources": []
            }
        
        # Prepare context from documents
        context_parts = []
        sources = []
        
        for doc in documents:
            context_parts.append(f"**{doc['title']}**:\n{doc['content']}")
            sources.append({
                "title": doc['title'],
                "url": doc['url'],
                "summary": doc['summary']
            })
        
        context = "\n\n".join(context_parts)
        
        # Create the prompt
        prompt = f"""You are a knowledgeable Wikipedia research assistant. Answer the user's question based ONLY on the provided Wikipedia content. 

Guidelines:
- Provide a comprehensive but concise answer
- Use information from multiple sources when relevant
- If the information is insufficient, acknowledge the limitations
- Structure your response clearly with proper formatting
- Include specific details and examples when available

User Question: {query}

Wikipedia Content:
{context}

Please provide a detailed answer based on the above information:"""

        try:
            logger.info("Generating response with GPT-3.5")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": sources,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"GPT API error: {str(e)}")
            return {
                "answer": f"I encountered an error while processing your request: {str(e)}",
                "sources": sources,
                "query": query
            }
