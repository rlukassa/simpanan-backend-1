# Debug & Testing Files

Folder ini berisi semua file debug, testing, dan prototype yang diperlukan untuk development dan testing sistem ITB Chatbot.

## 📁 File Structure

### Testing Files
- `masterTestRunner.py` - Main test orchestrator dengan comprehensive test suite
- `masterTestReport20250621_210538.json` - Test report (older)
- `masterTestReport20250621_214833.json` - Latest test report dengan full results

### Prototype Files
- `langchainPrototype.py` - LangChain RAG implementation prototype

## 🚀 Usage

### Running Tests
```bash
# Dari root directory
python debug/masterTestRunner.py

# Atau dari debug directory
cd debug
python masterTestRunner.py
```

### LangChain Prototype
```bash
# Testing LangChain prototype
python debug/langchainPrototype.py
```

## 📋 File Naming Convention

Semua file di folder ini menggunakan **camelCase** naming convention:
- `masterTestRunner.py` (bukan `master_test_runner.py`)
- `langchainPrototype.py` (bukan `langchain_prototype.py`)
- `masterTestReport...json` (bukan `master_test_report...json`)

## 🧹 Organization

Folder ini membantu menjaga codebase tetap rapi dengan memisahkan:
- ✅ **Production files** di root directory
- ✅ **Debug/test files** di `debug/` directory
- ✅ **Documentation** di `doc/` directory

## 📈 Test Coverage

Master Test Runner mencakup:
- **Basic Questions**: Real user queries
- **Comprehensive Tests**: Academic categories
- **Edge Cases**: Robustness testing
- **Fuzzy Matching**: Typo tolerance
- **Performance Metrics**: Detailed scoring

---
*Updated: 2025-06-21*
*Convention: camelCase naming*  
*Status: Organized & Clean ✅*
