import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel
from typing import List, Optional

# ------------------ Page Configuration ------------------
st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered"
)

# ------------------ Load Environment ------------------
load_dotenv()

# ------------------ Model ------------------
model = ChatMistralAI(model="mistral-small-2506")

# ------------------ Pydantic Model ------------------
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[str]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

# ------------------ Prompt ------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Extract Movie Information from the paragraph.

{format_instructions}
            """,
        ),
        (
            "human",
            "{paragraph}",
        ),
    ]
)

# ------------------ UI ------------------
st.title("🎬 Movie Information Extractor")
st.markdown(
    "Paste a movie-related paragraph below to extract structured movie information."
)

paragraph = st.text_area(
    "Movie Paragraph",
    height=250,
    placeholder="Enter your movie paragraph here..."
)

if st.button("Extract Information", use_container_width=True):

    if not paragraph.strip():
        st.warning("Please enter a movie paragraph.")
    else:
        with st.spinner("Extracting information..."):

            final_prompt = prompt.invoke(
                {
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions(),
                }
            )

            response = model.invoke(final_prompt)

        st.success("Extraction Completed!")

        st.subheader("Extracted Information")
        st.code(response.content, language="json")