#!/usr/bin/env python3
"""
ITB Chatbot Setup Script
========================

Automated setup script for ITB Chatbot with Advanced Fuzzy Matching.
This script will install dependencies and perform initial setup.

Usage:
    python setup.py install
    python setup.py dev  # For development setup
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description=""):
    """Run shell command with error handling"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    major, minor = sys.version_info[:2]
    
    if major < 3 or (major == 3 and minor < 8):
        print(f"❌ Python {major}.{minor} detected. Python 3.8+ required!")
        return False
    
    print(f"✅ Python {major}.{minor} - Compatible")
    return True

def install_requirements():
    """Install requirements from requirements.txt"""
    # Try minimal requirements first
    minimal_req = Path("requirements_minimal.txt")
    main_req = Path("requirement.txt")
    
    req_file = minimal_req if minimal_req.exists() else main_req
    
    if not req_file.exists():
        print("❌ No requirements file found!")
        return False
    
    print(f"📦 Installing Python dependencies from {req_file.name}...")
    return run_command(
        f"{sys.executable} -m pip install -r {req_file}",
        "Installing requirements"
    )

def setup_nltk_data():
    """Download NLTK data if needed"""
    print("📚 Setting up NLTK data...")
    
    nltk_commands = [
        "import nltk; nltk.download('punkt', quiet=True)",
        "import nltk; nltk.download('stopwords', quiet=True)",
        "import nltk; nltk.download('wordnet', quiet=True)"
    ]
    
    for cmd in nltk_commands:
        data_name = cmd.split("'")[1]  # Extract data name from command
        run_command(
            f"{sys.executable} -c \"{cmd}\"",
            f"Downloading NLTK data: {data_name}"
        )

def verify_installation():
    """Verify that key components can be imported"""
    print("🧪 Verifying installation...")
    
    test_imports = [
        ("flask", "Flask web framework"),
        ("pandas", "Data processing"),
        ("numpy", "Numerical computing"),
        ("sklearn", "Machine learning"),
        ("nltk", "Natural language processing")
    ]
    
    all_passed = True
    
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"✅ {description} - OK")
        except ImportError:
            print(f"❌ {description} - Failed to import {module}")
            all_passed = False
    
    return all_passed

def test_basic_functionality():
    """Test basic chatbot functionality"""
    print("🚀 Testing basic functionality...")
    
    try:
        # Test data loading
        sys.path.append("machinelearning")
        from machinelearning.dataLoader import load_csv_data
        
        data = load_csv_data()
        if data and len(data) > 0:
            print(f"✅ Data loading - OK ({len(data)} entries)")
        else:
            print("⚠️  Data loading - No data found")
            return False
            
        # Test matching function
        from machinelearning.matching import matchIntent
        
        test_result = matchIntent("test ITB")
        if test_result:
            print("✅ Matching function - OK")
        else:
            print("⚠️  Matching function - Returned empty result")
            
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def setup_development():
    """Setup development environment"""
    print("🛠️  Setting up development environment...")
    
    # Install development dependencies
    dev_packages = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=22.0.0",
        "flake8>=5.0.0"
    ]
    
    for package in dev_packages:
        run_command(
            f"{sys.executable} -m pip install {package}",
            f"Installing {package.split('>=')[0]}"
        )

def check_nodejs_version():
    """Check if Node.js and npm are installed"""
    print("🔍 Checking Node.js and npm...")
    
    # Check Node.js
    node_result = subprocess.run("node --version", shell=True, capture_output=True, text=True)
    if node_result.returncode != 0:
        print("❌ Node.js not found! Please install Node.js 16+ from https://nodejs.org")
        return False
    
    node_version = node_result.stdout.strip()
    print(f"✅ Node.js {node_version} - Found")
    
    # Check npm
    npm_result = subprocess.run("npm --version", shell=True, capture_output=True, text=True)
    if npm_result.returncode != 0:
        print("❌ npm not found! Please install npm")
        return False
    
    npm_version = npm_result.stdout.strip()
    print(f"✅ npm {npm_version} - Found")
    
    return True

def install_npm_dependencies():
    """Install npm dependencies for frontend"""
    package_json = Path("package.json")
    
    if not package_json.exists():
        print("⚠️  package.json not found - skipping npm install")
        return True
    
    print("📦 Installing npm dependencies...")
    return run_command(
        "npm install",
        "Installing npm packages"
    )

def build_frontend():
    """Build frontend for production"""
    print("🏗️  Building frontend...")
    return run_command(
        "npm run build",
        "Building React frontend"
    )

def main():
    """Main setup function"""
    print("=" * 60)
    print("🤖 ITB CHATBOT SETUP")
    print("=" * 60)
    
    mode = "install"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
      # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Node.js and npm for frontend
    frontend_available = check_nodejs_version()
    
    # Install Python requirements
    if not install_requirements():
        print("❌ Failed to install Python requirements!")
        sys.exit(1)
    
    # Install npm dependencies if Node.js is available
    if frontend_available:
        if not install_npm_dependencies():
            print("⚠️  Failed to install npm dependencies!")
            print("💡 Frontend may not work properly")
    
    # Setup NLTK data
    setup_nltk_data()
    
    # Verify installation
    if not verify_installation():
        print("⚠️  Some components failed to install properly!")
        print("💡 Try running: pip install -r requirement.txt")
    
    # Test basic functionality
    if not test_basic_functionality():
        print("⚠️  Basic functionality test failed!")
        print("💡 Check that all CSV data files are present")
      # Development setup
    if mode == "dev":
        setup_development()
        if frontend_available:
            print("🛠️  Frontend development mode - use 'npm run dev' to start")
    
    # Build frontend for production if not in dev mode
    if mode != "dev" and frontend_available:
        build_frontend()
    
    # Check Node.js and npm
    if not check_nodejs_version():
        sys.exit(1)
    
    # Install npm dependencies
    install_npm_dependencies()
    
    # Build frontend
    build_frontend()
    
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED!")
    print("=" * 60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Run backend server:")
    print("   cd backend && python app.py")
    
    if frontend_available:
        if mode == "dev":
            print("\n2. Run frontend development server:")
            print("   npm run dev")
            print("\n3. Open browser:")
            print("   Frontend: http://localhost:5173")
            print("   Backend API: http://localhost:5000")
        else:
            print("\n2. Serve built frontend:")
            print("   npm run preview")
            print("   Or use any web server to serve dist/ folder")
    
    print(f"\n3. Test chatbot functionality:")
    print("   python debug/testDirectMatching.py")
    print("\n4. Run comprehensive tests:")
    print("   python debug/masterTestRunner.py")
    
    print("\n📚 DOCUMENTATION:")
    print("- README.md - General information")
    print("- RESPONSE_MECHANISM_ANALYSIS.md - How bot answers questions")
    print("- ADVANCED_FUZZY_MATCHING_SUCCESS_REPORT.md - Fuzzy matching details")
    
    print("\n🆘 TROUBLESHOOTING:")
    print("- If imports fail: pip install -r requirement.txt")
    print("- If NLTK errors: python -c \"import nltk; nltk.download('all')\"")
    print("- If data loading fails: Check machinelearning/database/ folder")
    
    if frontend_available:
        print("- If npm install fails: Delete node_modules and try again")
        print("- If frontend won't start: npm run dev")
    else:
        print("- To use frontend: Install Node.js 16+ from https://nodejs.org")
        print("- Then run: npm install && npm run dev")

if __name__ == "__main__":
    main()
