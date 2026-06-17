# Architecture

The framework is divided into several independent but composable modules.

## Distillation (`src/ai_distiller/distillation`)
- `TeacherConnector`: Interfaces with provider APIs (OpenAI, Anthropic) via LiteLLM.
- `DataGenerator`: Uses the Teacher to synthetically generate dialogue.
- `DataCleaner`: Removes duplicates, formats data to conversational formats (ShareGPT/Alpaca).
- `Trainer`: Handles integration with tools like Unsloth and Axolotl to actually fine-tune models.

## Orchestration (`src/ai_distiller/orchestration`)
Integrations with agentic frameworks to allow the generated data to be more than just Q&A (e.g. multi-step reasoning).
- `LangGraphBuilder`
- `CrewBuilder`

## Capabilities (`src/ai_distiller/capabilities`)
Modules that augment the LLM's raw knowledge:
- `RAGIntegration`: LlamaIndex wrappers.
- `WebSearcher`: Tavily integrations.
