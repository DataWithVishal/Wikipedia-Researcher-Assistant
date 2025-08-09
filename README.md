# Wikipedia Researcher Agent 📚

A powerful AI-powered research assistant that combines Wikipedia's vast knowledge base with GPT-3.5's intelligence to provide comprehensive answers to your questions.

## Features ✨

- **Intelligent Search**: Uses Wikipedia API to find the most relevant articles
- **AI-Powered Analysis**: Leverages GPT-3.5 to synthesize information from multiple sources
- **LangGraph Workflow**: Orchestrated agent flow for reliable and structured research
- **Interactive UI**: Clean Streamlit interface with real-time progress tracking
- **Source Citations**: Provides links and summaries of all Wikipedia sources used
- **Search History**: Keeps track of recent queries for easy reference
- **Export Options**: Download research results in Markdown format

## Architecture 🏗️

```
[Streamlit UI] → [LangGraph Workflow] → [Wikipedia API] → [GPT-3.5] → [Formatted Results]
                      ├─ Search Node
                      ├─ Summary Node
                      └─ GPT Analyzer Node
```

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wikipedia-researcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage 💡

1. **Start the app**: Run `streamlit run app.py`
2. **Enter your question**: Type any research question in the search box
3. **Get results**: The agent will search Wikipedia, analyze content, and provide a comprehensive answer
4. **Review sources**: Check the cited Wikipedia articles for additional information
5. **Export results**: Download your research in Markdown format

### Example Queries

- "What is quantum computing and how does it work?"
- "Explain the causes and effects of climate change"
- "Who was Marie Curie and what were her major contributions?"
- "What is the history of artificial intelligence?"

## Configuration ⚙️

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `WIKIPEDIA_LANGUAGE`: Wikipedia language code (default: "en")
- `MAX_SEARCH_RESULTS`: Number of articles to search (default: 3)
- `MAX_CONTENT_LENGTH`: Max characters per article (default: 3000)

### Advanced Options

The app includes advanced settings to customize:
- Number of Wikipedia articles to search (1-5)
- Maximum content length per article (1000-5000 characters)

## Project Structure 📁

```
wikipedia-researcher/
├── app.py                 # Main Streamlit application
├── agents/
│   ├── __init__.py
│   ├── nodes.py          # LangGraph node implementations
│   └── workflow.py       # LangGraph workflow definition
├── utils/
│   ├── __init__.py
│   └── helpers.py        # Utility functions
├── requirements.txt      # Project dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## How It Works 🔧

1. **Search Phase**: The Wikipedia Search Node finds relevant articles based on your query
2. **Extraction Phase**: The Summary Node retrieves and processes article content
3. **Analysis Phase**: The GPT Summarizer Node uses AI to generate comprehensive answers
4. **Presentation Phase**: Results are formatted and displayed with source citations

## Dependencies 📦

- **streamlit**: Web application framework
- **langgraph**: Agent workflow orchestration
- **openai**: GPT-3.5 API integration
- **wikipedia**: Wikipedia API wrapper
- **python-dotenv**: Environment variable management

## Error Handling 🛡️

The application includes robust error handling for:
- Wikipedia API failures and disambiguation
- OpenAI API errors with retry mechanisms
- Empty search results with suggestions
- Token limit management with content truncation

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- **Wikipedia**: For providing free access to human knowledge
- **OpenAI**: For the GPT-3.5 language model
- **LangGraph**: For the agent orchestration framework
- **Streamlit**: For the excellent web app framework

## Support 💬

If you encounter any issues or have questions:
1. Check the existing issues in the repository
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Built with ❤️ using Streamlit, LangGraph, and OpenAI GPT-3.5**
