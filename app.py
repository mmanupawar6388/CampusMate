from pathlib import Path
import os
import re

import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM

from tools import calculate, percentage, create_study_plan
from viva_mode import VIVA_BANK, get_topics, start_viva, evaluate_answer

MODEL_ID = "manupawar6388/campusmate-gpt2"

print("=" * 60)
print("CAMPUSMATE - DEPLOYMENT")
print("=" * 60)
print("Loading model:", MODEL_ID)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

model.to("cpu")
model.eval()

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Model loaded successfully.")
print("Device: CPU")


def clean_response(text):
    text = re.sub(
        r"###\s*(User|Assistant)\s*:?",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\bUser\s*:",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chat(message):
    message = message.strip()

    if not message:
        return "Please enter a message."

    text = message.lower()

    if text in {"hi", "hello", "hey"}:
        return "Hello! I'm CampusMate. What do you need help with?"

    if text in {"thanks", "thank you"}:
        return "You're welcome. Good luck with your studies."

    if text in {"bye", "goodbye"}:
        return "Good luck! See you later."

    calc_match = re.search(
        r"^(calculate|solve)\s+(.+)",
        text,
    )

    if calc_match:
        expression = calc_match.group(2)

        try:
            return f"🧮 {expression} = {calculate(expression)}"
        except Exception:
            return "I couldn't safely calculate that."

    percent_match = re.search(
        r"percentage\s+(\d+(?:\.\d+)?)\s+(?:of|out of)\s+(\d+(?:\.\d+)?)",
        text,
    )

    if percent_match:
        value = float(percent_match.group(1))
        total = float(percent_match.group(2))

        return (
            f"📊 {value} out of {total} = "
            f"{percentage(value, total)}"
        )

    prompt = (
        "### User:\n"
        + message
        + "\n\n### Assistant:\n"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=256,
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=30,
            do_sample=True,
            temperature=0.65,
            top_p=0.9,
            repetition_penalty=1.25,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    generated = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    if "### Assistant:" in generated:
        reply = generated.split(
            "### Assistant:",
            1,
        )[1]
    else:
        reply = generated

    if "### User:" in reply:
        reply = reply.split(
            "### User:",
            1,
        )[0]

    return clean_response(reply) or "I'm not sure how to respond."


def start_viva_clean(topic):
    index, question = start_viva(topic)

    return (
        question,
        int(index),
        "",
        "",
    )


def evaluate_viva_clean(topic, index, answer):
    feedback, current_index, _ = evaluate_answer(
        topic,
        int(index),
        answer,
    )

    return feedback, int(current_index)


def next_viva_clean(topic, index):
    bank = VIVA_BANK[topic]

    next_index = (
        int(index) + 1
    ) % len(bank)

    return (
        bank[next_index]["question"],
        next_index,
        "",
    )


with gr.Blocks(
    title="CampusMate"
) as demo:

    gr.Markdown(
        """
        # 🎓 CampusMate

        ### Your Local Student AI Assistant

        Fine-tuned GPT-2 + Python student tools
        """
    )

    with gr.Tabs():

        with gr.Tab("💬 Chat"):

            chat_input = gr.Textbox(
                label="Message",
                placeholder="Talk to CampusMate...",
                lines=4,
            )

            chat_output = gr.Textbox(
                label="CampusMate",
                lines=8,
            )

            gr.Button(
                "Send",
                variant="primary",
            ).click(
                chat,
                inputs=chat_input,
                outputs=chat_output,
            )

        with gr.Tab("📚 Study Mode"):

            subjects = gr.Textbox(
                label="Subjects",
                placeholder="Python, DBMS, Computer Networks",
            )

            days = gr.Number(
                label="Days",
                value=5,
                precision=0,
            )

            hours = gr.Number(
                label="Hours per day",
                value=3,
            )

            study_output = gr.Textbox(
                label="Study Plan",
                lines=15,
            )

            gr.Button(
                "Create Study Plan",
                variant="primary",
            ).click(
                create_study_plan,
                inputs=[
                    subjects,
                    days,
                    hours,
                ],
                outputs=study_output,
            )

        with gr.Tab("🎤 Viva Practice"):

            topic = gr.Dropdown(
                choices=get_topics(),
                value="Python",
                label="Topic",
            )

            question = gr.Textbox(
                label="Viva Question",
                lines=3,
            )

            answer = gr.Textbox(
                label="Your Answer",
                lines=6,
            )

            feedback = gr.Markdown()

            question_index = gr.State(0)

            with gr.Row():

                gr.Button(
                    "Start Viva",
                ).click(
                    start_viva_clean,
                    inputs=topic,
                    outputs=[
                        question,
                        question_index,
                        answer,
                        feedback,
                    ],
                )

                gr.Button(
                    "Evaluate My Answer",
                    variant="primary",
                ).click(
                    evaluate_viva_clean,
                    inputs=[
                        topic,
                        question_index,
                        answer,
                    ],
                    outputs=[
                        feedback,
                        question_index,
                    ],
                )

                gr.Button(
                    "Next Question",
                ).click(
                    next_viva_clean,
                    inputs=[
                        topic,
                        question_index,
                    ],
                    outputs=[
                        question,
                        question_index,
                        answer,
                    ],
                )

        with gr.Tab("🛠 Tools"):

            expression = gr.Textbox(
                label="Expression",
                placeholder="25 * 48 + 100",
            )

            result = gr.Textbox(
                label="Result",
            )

            gr.Button(
                "Calculate",
                variant="primary",
            ).click(
                calculate,
                inputs=expression,
                outputs=result,
            )


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            "7860",
        )
    )

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
    )
