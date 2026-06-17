# Getting Started

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/anonyme-afk/ai-distiller.git
cd ai-distiller
make install
```

## Configuration

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```
Edit `.env` and add:
`ANTHROPIC_API_KEY=your_key`
`OPENAI_API_KEY=your_key`

## Basic Usage

Run the wizard to bootstrap a new domain:
```bash
ai-distiller wizard
```

Generate data for your domain:
```bash
ai-distiller generate --domain support_client --examples 100
```

Start the Gradio Dashboard:
```bash
make run-ui
```
