# LightRAG Simple Guide - Step by Step

## What is LightRAG?
LightRAG is a tool that helps AI understand and answer questions from your documents by creating a "knowledge graph" - like a map of all the important information.

---

## Simple 5-Step Process

### Step 1: Install LightRAG
```bash
# Install from PyPI
pip install lightrag-hku

# Or install from source
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
pip install -e .
```

### Step 2: Set Up Your API Keys
```bash
# Create a .env file or set environment variables
export OPENAI_API_KEY="sk-your-key-here"
```

### Step 3: Create a Simple Python Script

```python
import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed

# Step 3a: Create a folder for LightRAG to store data
WORKING_DIR = "./my_rag_storage"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# Step 3b: Initialize LightRAG
async def setup():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,           # How to convert text to numbers
        llm_model_func=gpt_4o_mini_complete,  # Which AI model to use
    )
    
    # IMPORTANT: Always initialize storage!
    await rag.initialize_storages()
    return rag

# Step 4: Add Your Documents
async def add_documents(rag):
    # Add text from a file or string
    with open("your_document.txt", "r") as f:
        text = f.read()
    
    await rag.ainsert(text)  # LightRAG will extract entities and relationships

# Step 5: Ask Questions
async def ask_questions(rag):
    # Ask a question
    answer = await rag.aquery(
        "What are the main topics in this document?",
        param=QueryParam(mode="hybrid")  # Use hybrid mode for best results
    )
    print(answer)

# Run everything
async def main():
    rag = await setup()
    await add_documents(rag)
    await ask_questions(rag)
    await rag.finalize_storages()  # Clean up

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Even Simpler Version (Copy-Paste Ready)

```python
import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed

async def main():
    # 1. Create storage folder
    WORKING_DIR = "./rag_storage"
    os.makedirs(WORKING_DIR, exist_ok=True)
    
    # 2. Initialize LightRAG
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
    )
    await rag.initialize_storages()
    
    # 3. Add your text
    rag.insert("Your text content goes here. It can be anything - documents, articles, etc.")
    
    # 4. Ask questions
    result = rag.query(
        "What is this text about?",
        param=QueryParam(mode="hybrid")
    )
    print(result)
    
    await rag.finalize_storages()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## What Each Step Does

1. **Install**: Get LightRAG on your computer
2. **Set API Key**: Tell LightRAG which AI service to use (OpenAI, etc.)
3. **Initialize**: Create a LightRAG instance and storage folder
4. **Insert**: Give LightRAG your documents - it automatically:
   - Extracts important entities (people, places, things)
   - Finds relationships between them
   - Creates a knowledge graph
5. **Query**: Ask questions and get answers based on your documents

---

## Query Modes (Choose One)

- **`mode="naive"`**: Simple search (fastest, basic)
- **`mode="local"`**: Focus on specific entities
- **`mode="global"`**: Use the knowledge graph relationships
- **`mode="hybrid"`**: Combine local + global (recommended)
- **`mode="mix"`**: Best of both worlds (best quality)

---

## Common Use Cases

### Use Case 1: Document Q&A
```python
rag.insert("Your long document text...")
answer = rag.query("What are the key points?", param=QueryParam(mode="hybrid"))
```

### Use Case 2: Multiple Documents
```python
documents = ["Document 1 text...", "Document 2 text...", "Document 3 text..."]
rag.insert(documents)  # Can insert multiple at once
```

### Use Case 3: File Upload
```python
with open("report.pdf", "r") as f:
    text = f.read()
rag.insert(text)
```

---

## Important Notes

✅ **DO**: Always call `await rag.initialize_storages()` after creating LightRAG  
✅ **DO**: Use `await rag.finalize_storages()` when done  
✅ **DO**: Set your API key before running  
❌ **DON'T**: Forget to initialize storage (you'll get errors)  
❌ **DON'T**: Switch embedding models without clearing the storage folder  

---

## Troubleshooting

**Error: "AttributeError: __aenter__"**
- **Fix**: Call `await rag.initialize_storages()` after creating LightRAG

**Error: "KeyError: 'history_messages'"**
- **Fix**: Same as above - initialize storage!

**Different answers when switching models?**
- **Fix**: Delete the `WORKING_DIR` folder and re-insert documents

---

## Next Steps

1. Try the simple example above
2. Read the full README for advanced features
3. Check `examples/` folder for more examples
4. Explore different storage backends (Neo4j, PostgreSQL, etc.)

---

## Quick Reference

```python
# Initialize
rag = LightRAG(working_dir="./storage", embedding_func=..., llm_model_func=...)
await rag.initialize_storages()

# Insert
rag.insert("Your text")

# Query
result = rag.query("Your question", param=QueryParam(mode="hybrid"))

# Clean up
await rag.finalize_storages()
```

That's it! LightRAG handles all the complex knowledge graph stuff automatically. 🚀

