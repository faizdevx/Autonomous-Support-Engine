# Autonomous-Support-Engine

User → Supervisor → Router → Knowledge → Responder → Critic → (Loop / Exit)

everything revolve around **STATE**

| Layer         | Tool                                    |
| ------------- | --------------------------------------- |
| API           | FastAPI                                 |
| State         | Pydantic                                |
| Agents        | Python functions (don’t overcomplicate) |
| LLM           | HuggingFace (free)                      |
| Vector DB     | FAISS                                   |
| Storage       | Dict / SQLite                           |
| Orchestration | Manual flow (LangGraph later)           |




AUTONOMOUS-SUPPORT-SYSTEM/
│
├── app.py                # FastAPI entry
├── models/
│   └── state.py         # Pydantic models
├── agents/
│   ├── router.py
│   ├── knowledge.py
│   ├── responder.py
│   ├── critic.py
│
├── llm/
│   └── hf_model.py
│
├── rag/
│   ├── embed.py
│   ├── retriever.py
│
├── db/
│   └── memory.py



✔ Multi-agent pipeline
✔ SOP-driven flow
✔ Self-correction loop
✔ Confidence gating
✔ Async-ready backend