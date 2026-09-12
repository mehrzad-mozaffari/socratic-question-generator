from pathlib import Path
import gradio as gr
from socratic_tutor.config import ROOT, load_config, resolve_path
from socratic_tutor.model.loader import load_model
from socratic_tutor.tutor.socratic_agent import SocraticTutor
from socratic_tutor.tutor.conversation import gradio_history_to_turns, save_transcript


def create_app():
    cfg = load_config()
    model_cfg = cfg["model"]
    runtime = cfg["runtime"]
    adapter_dir = resolve_path(model_cfg["adapter_dir"])
    merged = resolve_path(model_cfg["merged_model_dir"]) if model_cfg["merged_model_dir"] else ""
    model, tokenizer = load_model(
        model_cfg["base_model"], str(adapter_dir), str(merged) if merged else "",
        use_merged=runtime["use_merged"], trust_remote_code=runtime["trust_remote_code"]
    )
    tutor = SocraticTutor(
        model, tokenizer,
        max_new_tokens=model_cfg["max_new_tokens"],
        greedy=runtime["greedy"],
        temperature=model_cfg["temperature"],
        top_p=model_cfg["top_p"],
    )
    log_dir = resolve_path(cfg["paths"]["chat_logs"])

    def chat_reply(user_msg, chat_history, problem, notes, greedy, max_new_tokens):
        history = gradio_history_to_turns(chat_history, user_msg)
        old_greedy, old_max = tutor.greedy, tutor.max_new_tokens
        tutor.greedy, tutor.max_new_tokens = greedy, int(max_new_tokens)
        try:
            reply = tutor.ask(history, problem=problem, notes=notes)
        finally:
            tutor.greedy, tutor.max_new_tokens = old_greedy, old_max
        chat_history = chat_history or []
        chat_history.append((user_msg, reply))
        return "", chat_history

    def save(chat_history, problem, notes):
        path = save_transcript(chat_history or [], problem, notes, log_dir)
        return f"Saved transcript to: {path}"

    with gr.Blocks(title="Socratic Debugging Tutor") as demo:
        gr.Markdown("## Socratic Debugging Tutor\nAsk the student **one short diagnostic question** at a time.")
        with gr.Row():
            problem = gr.Textbox(label="Problem (context)", placeholder="e.g., Fibonacci off-by-one bug")
            notes = gr.Textbox(label="Student notes (optional)", placeholder="e.g., Confused about range endpoints")
        with gr.Row():
            greedy = gr.Checkbox(value=True, label="Greedy decoding (precise & fast)")
            max_tokens = gr.Slider(16, 96, value=48, step=1, label="Max new tokens per turn")
        chat = gr.Chatbot(label="Chat", show_copy_button=True)
        msg = gr.Textbox(label="Your message")
        with gr.Row():
            send = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear chat")
            save_btn = gr.Button("Save transcript")
        send.click(chat_reply, [msg, chat, problem, notes, greedy, max_tokens], [msg, chat])
        msg.submit(chat_reply, [msg, chat, problem, notes, greedy, max_tokens], [msg, chat])
        clear.click(lambda: ([], ""), outputs=[chat, msg])
        save_btn.click(save, [chat, problem, notes], outputs=[])
    return demo


if __name__ == "__main__":
    create_app().launch()
