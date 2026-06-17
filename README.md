<p align="center">
  <h1 align="center">🚀 AI-Distiller</h1>
  <p align="center">
    <strong>Create specialized AI assistants through knowledge distillation — from powerful models to lightweight, deployable agents.</strong>
  </p>
  <p align="center">
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-how-it-works">How It Works</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-usage">Usage</a> •
    <a href="#-contributing">Contributing</a>
  </p>
</p>

---

## ✨ What is AI-Distiller?

AI-Distiller is a **complete Python framework** that automates the creation of specialized AI assistants. Instead of using expensive, powerful models (Claude, GPT-4o) in production, AI-Distiller lets you:

1. **Generate** high-quality synthetic training data using a powerful "Teacher" model.
2. **Filter** that data using Constitutional AI (LLM-as-a-Judge + Rejection Sampling).
3. **Fine-tune** a small, cheap "Student" model using DPO (Direct Preference Optimization).
4. **Export** the Student as a `.gguf` file that runs locally — on CPU, without cloud costs.

> **TL;DR**: Use Claude/GPT to teach a small model → Deploy it locally for free.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        AI-Distiller                          │
├──────────────┬──────────────┬──────────────┬─────────────────┤
│ Distillation │ Orchestration│ Capabilities │    Interface    │
│              │              │              │                 │
│ • Teacher    │ • LangGraph  │ • RAG        │ • CLI (Typer)   │
│ • Generator  │ • CrewAI     │ • Web Search │ • API (FastAPI) │
│ • Cleaner    │ • OpenHands  │ • Thinking   │ • UI (Gradio)   │
│ • Trainer    │              │ • Tools      │                 │
│ • Evaluator  │              │              │                 │
└──────────────┴──────────────┴──────────────┴─────────────────┘
```

---

## 🔧 Installation

### Prerequisites
- Python 3.10+
- An API key from at least one provider: [Anthropic](https://console.anthropic.com/), [OpenAI](https://platform.openai.com/), or a local [Ollama](https://ollama.com/) instance.

### Step 1: Clone the Repository

```bash
git clone https://github.com/anonyme-afk/ai-distiller.git
cd ai-distiller
```

### Step 2: Install Dependencies

```bash
# Option A: Using make (recommended)
make install

# Option B: Manual pip
pip install -r requirements.txt
pip install -e .
```

### Step 3: Configure Your API Keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:
```env
ANTHROPIC_API_KEY=sk-ant-...        # Required for Claude Teacher
OPENAI_API_KEY=sk-...               # Required for GPT Teacher
TAVILY_API_KEY=tvly-...             # Optional: enables web search
HF_TOKEN=hf_...                     # Optional: push models to HuggingFace
```

### Step 4: Verify Installation

```bash
python -c "from ai_distiller.distillation.teacher import TeacherConnector; print('✅ Ready!')"
```

---

## ⚡ Quick Start

### Interactive Wizard (Easiest)
```bash
ai-distiller wizard
```
This will guide you step by step to configure a domain, generate data, and train.

### Full Pipeline (Command Line)
```bash
# 1. Initialize a domain
ai-distiller init --domain support_client

# 2. Generate DPO training data (async, with Constitutional AI filtering)
ai-distiller generate --domain support_client --examples 500 --with-cot

# 3. Clean the generated dataset
ai-distiller clean --input-file outputs/dpo_dataset.json

# 4. Train (exports to GGUF automatically)
ai-distiller train --input-file outputs/cleaned_dataset.json

# 5. Start the API server
ai-distiller serve
```

### Docker (Zero Setup)
```bash
docker-compose up --build
```
This starts both the **FastAPI server** (port 8000) and the **Gradio Dashboard** (port 7860).

---

## 🧠 How It Works

### The Distillation Pipeline

```
Step 1: GENERATE                Step 2: JUDGE                  Step 3: TRAIN
┌─────────────┐                ┌──────────────────┐           ┌──────────────────┐
│   Teacher    │──generates──▶ │  3 Responses per  │──best──▶ │  DPO Training    │
│ (Claude/GPT) │   3 answers   │  prompt + Judge   │  /worst  │  (TRL/Unsloth)   │
└─────────────┘                │  picks best/worst │           └──────┬───────────┘
                               └──────────────────┘                  │
                                                              ┌──────▼───────────┐
                                                              │  GGUF Export     │
                                                              │  (llama.cpp)     │
                                                              │  + Dockerfile    │
                                                              └──────────────────┘
```

1. **Constitutional AI**: For each prompt, the Teacher generates **3 diverse responses**. An LLM Judge evaluates them for quality, accuracy, and safety, then picks the **best** (chosen) and **worst** (rejected).
2. **DPO Format**: The output is a dataset of `{prompt, chosen, rejected}` triplets — the gold standard for modern alignment training.
3. **GGUF Export**: After training, the model is automatically quantized to `.gguf` format and a ready-to-deploy `Dockerfile.agent` is generated.

---

## 🔌 Integrations & Related Projects

AI-Distiller is designed to work with the best tools in the ecosystem:

| Tool | Purpose | How to connect |
|------|---------|---------------|
| [Unsloth](https://github.com/unslothai/unsloth) | 2x faster fine-tuning, 80% less VRAM | Set `model_name="unsloth/llama-3-8b-bnb-4bit"` in Trainer |
| [TRL](https://github.com/huggingface/trl) | DPO/SFT training library by HuggingFace | Auto-detected in `trainer.py` if installed |
| [LiteLLM](https://github.com/BerriAI/litellm) | Unified API for 100+ LLM providers | Used in `teacher.py` for async calls |
| [Distilabel](https://github.com/argilla-io/distilabel) | Synthetic data pipeline (inspiration) | Compatible dataset formats |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Multi-step agent orchestration | See `orchestration/langgraph_builder.py` |
| [CrewAI](https://github.com/joaomdmoura/crewai) | Multi-agent collaboration | See `orchestration/crew_builder.py` |
| [LlamaIndex](https://github.com/run-llama/llama_index) | RAG (Retrieval Augmented Generation) | See `capabilities/rag.py` |
| [Ollama](https://github.com/ollama/ollama) | Run LLMs locally | Set `provider="ollama"` in TeacherConfig |
| [llama.cpp](https://github.com/ggerganov/llama.cpp) | Run GGUF models on CPU | Exports are compatible out-of-the-box |
| [EasyDistill](https://github.com/modelscope/easydistill) | Advanced distillation toolkit | Compatible architecture |
| [SWIFT](https://github.com/modelscope/swift) | Full training lifecycle | Alternative trainer backend |

### Connecting Unsloth (Example)

```python
# In your training script or after running `ai-distiller train`:
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3-8b-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

# Use AI-Distiller's generated dataset
# File: outputs/dataset.jsonl (auto-generated by the CLI)
from trl import DPOTrainer, DPOConfig

training_args = DPOConfig(output_dir="./results", num_train_epochs=1)
trainer = DPOTrainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()

# Export to GGUF for local deployment
model.save_pretrained_gguf("my_agent", tokenizer, quantization_method="q4_k_m")
```

### Deploying the GGUF Agent

After training, AI-Distiller generates a `Dockerfile.agent` in `outputs/`:

```bash
cd outputs/
docker build -f Dockerfile.agent -t my-agent .
docker run -p 8080:8080 my-agent

# Your agent is now serving at http://localhost:8080 !
# It's an OpenAI-compatible API (works with any client)
curl http://localhost:8080/v1/chat/completions \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'
```

---

## 📊 Gradio Dashboard

Launch the interactive web UI:
```bash
make run-ui
# or
python src/ai_distiller/ui/app.py
```
Open `http://localhost:7860` to access:
- **⚙️ DPO Generation & Training**: Configure and launch distillation runs.
- **📈 Monitoring**: Track training loss and benchmark scores.
- **💬 Chat**: Test your distilled agent interactively.

---

## 📁 Project Structure

```
ai-distiller/
├── .github/                    # CI/CD + Issue/PR templates
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── config/domains/             # YAML domain configs
│   ├── support_client.yaml
│   ├── droit_francais.yaml
│   ├── code_assistant.yaml
│   └── custom_template.yaml
├── docs/                       # MkDocs documentation site
├── src/ai_distiller/
│   ├── distillation/
│   │   ├── teacher.py          # LLM connectors (sync + async)
│   │   ├── data_generator.py   # DPO data generation pipeline
│   │   ├── cleaner.py          # Dataset cleaning & dedup
│   │   ├── trainer.py          # DPO/SFT training + GGUF export
│   │   └── evaluator.py       # LLM-as-a-Judge benchmarking
│   ├── orchestration/          # LangGraph, CrewAI integrations
│   ├── capabilities/           # RAG, Web Search, Tools
│   ├── api/                    # FastAPI server
│   ├── cli/                    # Typer CLI
│   └── ui/                     # Gradio dashboard
├── tests/                      # Pytest test suite
├── Dockerfile                  # Container for API + UI
├── docker-compose.yml          # Multi-service deployment
├── Makefile                    # Dev shortcuts
├── mkdocs.yml                  # Documentation config
└── requirements.txt
```

---

## 🧪 Development

```bash
# Install dev dependencies
make install

# Run tests
make test

# Format code
make format

# Lint
make lint

# Generate documentation site
mkdocs serve
```

---

## 📚 Resources & Inspiration

- [LLM Distillation Playbook](https://github.com/predibase/llm_distillation_playbook) — Best practices for production distillation
- [Awesome-LLM-Synthetic-Data](https://github.com/wasiahmad/Awesome-LLM-Synthetic-Data) — Curated list of synthetic data methods
- [DPO Paper](https://arxiv.org/abs/2305.18290) — Direct Preference Optimization
- [Constitutional AI Paper](https://arxiv.org/abs/2212.08073) — Anthropic's self-critique approach

---

## 📜 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/anonyme-afk">anonyme-afk</a>
</p>
