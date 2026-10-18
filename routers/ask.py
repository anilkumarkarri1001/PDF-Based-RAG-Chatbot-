
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")


class QuestionRequest(BaseModel):
    question: str


def text_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


@router.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    total_chunks = collection.count()

    if total_chunks == 0:
        raise HTTPException(
            status_code=400,
            detail="No PDF has been uploaded yet"
        )

    try:
        # 1. Convert the question into an embedding
        question_embedding = text_embedding(question)

        # 2. Retrieve the three closest chunks
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=min(3, total_chunks)
        )

        documents = (results.get("documents") or [[]])[0]

        if not documents:
            raise HTTPException(
                status_code=404,
                detail="No relevant document content found"
            )

        # 3. Combine retrieved chunks into context
        context = "\n\n".join(documents)

        # 4. Construct the RAG prompt
        prompt = f"""
You are a helpful PDF assistant.

Answer the question using only the supplied context.
If the answer is not present in the context, say:
"The information is not available in the document."

Context:
{context}

Question:
{question}
"""

        # 5. Generate the answer
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return {
            "question": question,
            "answer": response.text or "No answer was generated."
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(exc)}"
        ) from exc
