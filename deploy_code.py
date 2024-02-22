import wikipediaapi
from fastapi import FastAPI, HTTPException
import openai

# Set up Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia('English')

# Set up OpenAI API key
openai.api_key = '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'

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to Wikipedia Summarization and Paraphrasing API"}


@app.get("/sections/{page_title}")
def get_sections(page_title: str):
    page_py = wiki_wiki.page(page_title)
    if not page_py.exists():
        raise HTTPException(status_code=404, detail="Page not found")
    return {"sections": [section.title for section in page_py.sections]}


@app.get("/summarize/{page_title}/{section_index}")
def summarize_section(page_title: str, section_index: int):
    page_py = wiki_wiki.page(page_title)
    if not page_py.exists():
        raise HTTPException(status_code=404, detail="Page not found")

    sections = page_py.sections
    if not (1 <= section_index <= len(sections)):
        raise HTTPException(status_code=400, detail="Invalid section index")

    selected_section = sections[section_index - 1].text

    # Use OpenAI GPT-3.5 Turbo for summarization
    summary = openai.Completion.create(
        engine="text-davinci-003",
        prompt=selected_section,
        max_tokens=150
    )["choices"][0]["text"].strip()

    return {"summary": summary}


@app.get("/paraphrase")
def paraphrase_text(text: str):
    # Use OpenAI GPT-3.5 Turbo for paraphrasing
    paraphrased_text = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150,
        temperature=0.7
    )["choices"][0]["text"].strip()

    return {"paraphrased_text": paraphrased_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(host="127.0.0.1", port="8001")
