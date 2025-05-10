#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from docx import Document
from docx.shared import Inches
from datetime import date
import openai

# -------------------
# App Setup
# -------------------
st.image("coursemon_pic_logo.jpg", width=150)
st.title("📄 Coursemon Letter Generator")

# Use API key from secrets
if "openai" not in st.secrets:
    st.error("❌ OpenAI API Key not found in secrets.")
    st.stop()

openai.api_key = st.secrets["openai"]["api_key"]

# Inputs
letter_type = st.selectbox("Letter Type", ["Employment Letter", "Business Proposal", "Notice Letter"])
name = st.text_input("Recipient Name", "Malaika Khan")
email = st.text_input("Recipient Email", "malaika@example.com")
position = st.text_input("Position/Role", "Business Development Specialist")
equity = st.text_input("Equity % (only if needed)", "5")
letter_date = st.date_input("Date", date.today())

# -------------------
# Generate with GPT
# -------------------
def get_letter_from_gpt(letter_type, name, position, equity, letter_date):
    prompt = f"""
You are a professional business assistant writing letters on behalf of Coursemon's CEO, Ammar Jamshed.

Write a {letter_type.lower()} addressed to {name}, whose role is {position}, dated {letter_date.strftime('%B %d, %Y')}.

Include equity offering of {equity}% only if it's an Employment Letter. 
Tone should be professional and warm. End the letter with:
"Ammar Jamshed, Founder & CEO, Coursemon"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes formal letters for a startup."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response["choices"][0]["message"]["content"]

# -------------------
# Generate Letter
# -------------------
if st.button("Generate Letter with GPT"):
    with st.spinner("Generating letter with GPT..."):
        letter_text = get_letter_from_gpt(letter_type, name, position, equity, letter_date)

        doc = Document()
        doc.add_picture("coursemon_pic_logo.jpg", width=Inches(1.5))
        doc.add_paragraph()
        doc.add_paragraph("COURSEMON", style='Title')
        doc.add_paragraph("Empowering Learning Journeys", style='Intense Quote')
        doc.add_paragraph()
        doc.add_paragraph(f"Date: {letter_date.strftime('%B %d, %Y')}")
        doc.add_paragraph(f"To:\n{name}\n{email}")
        doc.add_paragraph()
        doc.add_paragraph(f"Subject: {letter_type} for {position}", style='Heading 2')
        doc.add_paragraph(letter_text)

        file_name = f"{name.replace(' ', '_')}_{letter_type.replace(' ', '_')}_Coursemon_Letter.docx"
        doc.save(file_name)

        with open(file_name, "rb") as f:
            st.success("✅ Letter Ready!")
            st.download_button(
                label="📥 Download Letter",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
