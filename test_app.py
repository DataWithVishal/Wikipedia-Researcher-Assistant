"""
Simple test script to verify the Wikipedia Researcher Agent setup
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test core dependencies
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        import wikipedia
        print("✅ Wikipedia module imported successfully")
        
        from openai import OpenAI
        print("✅ OpenAI module imported successfully")
        
        # Test LangGraph (might not be installed yet)
        try:
            from langgraph.graph import StateGraph
            print("✅ LangGraph imported successfully")
        except ImportError:
            print("⚠️ LangGraph not installed - run 'pip install -r requirements.txt'")
        
        # Test project modules
        from agents.nodes import WikipediaSearchNode, WikipediaSummaryNode, GPTSummarizerNode
        print("✅ Agent nodes imported successfully")
        
        from agents.workflow import create_wikipedia_agent
        print("✅ Workflow module imported successfully")
        
        from utils.helpers import load_config, validate_config
        print("✅ Helper utilities imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "agents/__init__.py",
        "agents/nodes.py",
        "agents/workflow.py",
        "utils/__init__.py",
        "utils/helpers.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_environment():
    """Test environment configuration"""
    print("\nTesting environment...")
    
    # Check if .env.example exists
    if os.path.exists(".env.example"):
        print("✅ .env.example file exists")
    else:
        print("❌ .env.example file missing")
        return False
    
    # Check if .env file exists (optional)
    if os.path.exists(".env"):
        print("✅ .env file exists")
        
        # Try to load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                print("✅ OPENAI_API_KEY is set")
            else:
                print("⚠️ OPENAI_API_KEY not set in .env file")
                
        except ImportError:
            print("⚠️ python-dotenv not installed")
    else:
        print("⚠️ .env file not found - copy from .env.example and add your API key")
    
    return True

def main():
    """Run all tests"""
    print("🧪 Wikipedia Researcher Agent - Setup Test\n")
    print("=" * 50)
    
    # Test file structure first
    structure_ok = test_file_structure()
    
    # Test imports (only if structure is OK)
    if structure_ok:
        imports_ok = test_imports()
    else:
        imports_ok = False
        print("\n⚠️ Skipping import tests due to missing files")
    
    # Test environment
    env_ok = test_environment()
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if structure_ok and imports_ok and env_ok:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Copy .env.example to .env and add your OpenAI API key")
        print("3. Run the app: streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        
        if not structure_ok:
            print("- Fix missing files")
        if not imports_ok:
            print("- Install required dependencies")
        if not env_ok:
            print("- Set up environment variables")

if __name__ == "__main__":
    main()
