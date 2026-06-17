"""
app.py
Gradio Web UI for AI-Distiller.
Features: Config UI, Monitoring, Chat, Metrics.
"""
import gradio as gr
import pandas as pd
import plotly.express as px
import random
import time

def generate_mock_metrics():
    """Generates mock training metrics for the dashboard."""
    steps = list(range(1, 101))
    loss = [max(0.1, 5.0 - (x * 0.04) + random.uniform(-0.2, 0.2)) for x in steps]
    eval_loss = [l + random.uniform(0.1, 0.5) for l in loss]
    
    df = pd.DataFrame({
        "Step": steps,
        "Training Loss": loss,
        "Evaluation Loss": eval_loss
    })
    
    fig = px.line(df, x="Step", y=["Training Loss", "Evaluation Loss"], title="Training Progress")
    return fig

def launch_training(domain, teacher):
    """Stub function to simulate starting a training process."""
    time.sleep(1)
    return f"🚀 Entraînement démarré pour le domaine '{domain}' avec le teacher '{teacher}'. Consultez l'onglet Monitoring."

def chat_interface(message, history):
    """Stub chat function."""
    response = f"Ceci est une réponse simulée de l'agent distillé (domaine courant) pour : {message}"
    time.sleep(0.5)
    return response

# Construction de l'interface Gradio
with gr.Blocks(title="AI-Distiller Dashboard", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 AI-Distiller Dashboard")
    gr.Markdown("Plateforme de création d'assistants IA spécialisés via distillation.")
    
    with gr.Tabs():
        # Tab 1: Configuration
        with gr.TabItem("⚙️ Configuration"):
            gr.Markdown("### Configurer une nouvelle distillation")
            with gr.Row():
                with gr.Column():
                    domain_input = gr.Textbox(label="Domaine", placeholder="Ex: support_client, droit_francais...")
                    teacher_input = gr.Dropdown(
                        choices=["claude-3-5-sonnet-20241022", "gpt-4o", "llama-3-70b"], 
                        label="Modèle Teacher", 
                        value="claude-3-5-sonnet-20241022"
                    )
                    orchestration_input = gr.Dropdown(
                        choices=["langgraph", "crewai", "none"],
                        label="Orchestration",
                        value="crewai"
                    )
                    examples_slider = gr.Slider(minimum=1000, maximum=100000, step=1000, value=10000, label="Nombre d'exemples")
                
                with gr.Column():
                    train_btn = gr.Button("Démarrer la Distillation", variant="primary")
                    status_output = gr.Textbox(label="Statut", interactive=False)
                    
            train_btn.click(launch_training, inputs=[domain_input, teacher_input], outputs=status_output)

        # Tab 2: Monitoring
        with gr.TabItem("📈 Monitoring"):
            gr.Markdown("### Suivi de l'entraînement en temps réel")
            refresh_btn = gr.Button("Actualiser les métriques")
            metrics_plot = gr.Plot()
            refresh_btn.click(generate_mock_metrics, inputs=[], outputs=metrics_plot)
            demo.load(generate_mock_metrics, inputs=[], outputs=metrics_plot)

        # Tab 3: Chat & Test
        with gr.TabItem("💬 Tester le Modèle"):
            gr.Markdown("### Discuter avec le modèle distillé")
            gr.ChatInterface(chat_interface)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
