from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain .chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

OPENAI_API_KEY = ""

if OPENAI_API_KEY == "":
    OPENAI_API_KEY = input("Bitte gebe deinen API-Key für OpenAI ein:");

app = FastAPI()
app.mount('/static', StaticFiles(directory="static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

class ConceptRequest(BaseModel):
    concept_idea: str

@app.api_route("/", methods=["GET", "OPTIONS"])
async def index():
    return RedirectResponse("/static/")

@app.api_route("/search_concept_with_sources", methods=["POST", "OPTIONS"])
async def search_concept_with_sources(request: ConceptRequest):
    concept_idea = request.concept_idea
    prompt_template = (
        "Ich habe ein Konzept, dass einen Namen hat aber ich weiß nicht, wie es heißen könnte. Bitte sage mir wie der Fachbegriff für das ist, was ich meine. Erkläre außerdem, wie du auf die Fachbegriffe gekommen bist. Es könnte mehrere Antworten geben und nenne dabei alle, die zutreffen könnten. Bitte gebe mir die Erklärung mit den Fachbegriffen aus. Anschließend liste am Ende deiner Antwort die Fachbegriffe in folgenden Schema auf:\n"
        "Fachbegriff 1: Name des 1 möglichen Fachbegriffs\n"
        "Fachbegriff 2: Name des 2 möglichen Fachbegriffs\n"
        "Fachbegriff 3: Name des 3 möglichen Fachbegriffs\n"
        "... weitere Auflistungen der möglichen Fachbegriffen nach oberen Schema\n\n"
        "Das ist das Konzept:\n{concept_idea}"
    )
    prompt = prompt_template.replace("{concept_idea}", concept_idea)

    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-4o"
    )   

    response = llm.invoke(
    [
        HumanMessage(
            content=prompt
        )
    ])

    return {"response": response.content}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)