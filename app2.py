import gradio as gr
import PyPDF2
import os

pdf_text = ""

def upload_pdf(file):
    global pdf_text
    if file is None:
        return "Please upload PDF"
    reader = PyPDF2.PdfReader(file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() or ""
    return f"PDF Uploaded! {len(pdf_text)} characters read. Now you can ask question in Tab 2."

def ask_question(question):
    global pdf_text
    if not pdf_text:
        return "First upload PDF in Tab 1"
    if not question:
        return "Please type a question"
    # Simple search logic
    if question.lower() in pdf_text.lower():
        return "Answer found in PDF:\n\n" + pdf_text[:1500]
    else:
        return f"Your question: {question}\n\nPDF Content Preview:\n{pdf_text[:1500]}"

with gr.Blocks(title="AI Doc Search - 2 Separate APIs") as app:
    gr.Markdown("# AI Doc Search - 2 Separate APIs\nFor Website Integration: 1) Ingest first, 2) Then Ask")
    
    with gr.Tab("1. Upload / Ingest"):
        file_input = gr.File(label="Upload PDF")
        upload_btn = gr.Button("Ingest")
        out1 = gr.Textbox(label="Status")
        upload_btn.click(upload_pdf, inputs=file_input, outputs=out1)
    
    with gr.Tab("2. Chat / Ask"):
        q_input = gr.Textbox(label="Ask question from PDF")
        ask_btn = gr.Button("Ask")
        out2 = gr.Textbox(label="Answer")
        ask_btn.click(ask_question, inputs=q_input, outputs=out2)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port)