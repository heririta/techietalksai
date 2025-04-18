import os
import streamlit as st
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools

# --------- LOAD API KEYS ---------
openai_api_key = os.getenv("OPENAI_API_KEY")
exa_api_key = os.getenv("EXA_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY")
    st.stop()
if not exa_api_key:
    st.error("Exa API key not found. Please set EXA_API_KEY")
    st.stop()

# --------------- SETUP ---------------
cwd = Path(__file__).parent.resolve()
tmp = cwd.joinpath("tmp")
if not tmp.exists():
    tmp.mkdir(exist_ok=True, parents=True)

# --------------- TITLE AND INFO SECTION -------------------
st.title("🔍 AI Deep Research Agent")
st.write("Your advanced AI research assistant with academic-grade analysis capabilities")

# --------------- SIDEBAR CONTROLS -------------------
with st.sidebar:
    st.subheader("Research Prompt Ideas:")
    st.markdown("""
    - Quantum computing breakthroughs
    - CRISPR gene editing advances
    - Fusion energy developments
    - AI ethics frameworks
    - Neuroplasticity research
    - Climate change mitigation tech
    """)
    st.markdown("---")
    
    # Research counter
    if "counter" not in st.session_state:
        st.session_state["counter"] = 0
    st.caption(f"Research papers generated: {st.session_state['counter']}")

stream = st.sidebar.checkbox("Stream research process")
show_references = st.sidebar.checkbox("Show source references", True)

# --------------- AGENT INITIALIZATION -------------------
today = datetime.now().strftime("%Y-%m-%d")
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=openai_api_key),
    # model=xAI(id="grok-2", api_key=xai_api_key),
    # model=OpenAIChat(id="gpt-4o-mini"),
    # model=Groq(id="llama-3.3-70b-versatile"),
    # model=DeepSeek(id="deepseek-chat"),
    # model=Gemini(
    #     id="gemini-2.0-flash-exp",
    #     api_key=gemini_api_key,
    # ),
    # tools=[ExaTools(api_key=exa_api_key, start_published_date="2023-01-01")],
    tools=[ExaTools(api_key=exa_api_key, start_published_date=today)],
    instructions=dedent("""\
        You are Professor X-1000, an AI research scientist specializing in:
        - Cutting-edge technology analysis
        - Academic paper synthesis
        - Cross-disciplinary research
        
        **Research Protocol:**
        1. Conduct 3 distinct academic searches
        2. Cross-reference sources for validity
        3. Structure findings using academic standards
        4. Include verifiable citations
        5. Highlight practical applications
        6. End with future implications
        
        **Writing Style:**
        - Authoritative yet accessible
        - Data-driven insights
        - Clear technical explanations
        - Balanced perspective
        - Proper source attribution\
    """),
    expected_output=dedent(f"""\
        # {{title}}

        ## Executive Summary
        {{overview}}

        ## Key Findings
        {{bullet_points}}

        ## Technical Analysis
        {{detailed_analysis}}

        ## Applications & Implications
        {{real_world_impact}}

        ## References
        {{sources}}

        ---
        Generated by AI Research Agent v2.1
        Date: {datetime.now().strftime("%Y-%m-%d")}\
    """),
    markdown=True,
    show_tool_calls=show_references,
    save_response_to_file=str(tmp.joinpath("research_{datetime}.md")),
)

# --------------- USER INPUT HANDLING -------------------
prompt = st.text_input("Enter your research query:", placeholder="e.g., 'Recent advances in photonic computing'")

if prompt:
    st.session_state["counter"] += 1
    
    with st.spinner("🔬 Conducting deep research analysis..."):
        if stream:
            response_stream: Iterator[RunResponse] = agent.run(prompt, stream=True)
            response_text = ""
            placeholder = st.empty()
            
            for chunk in response_stream:
                response_text += chunk.content
                placeholder.markdown(response_text + "▌")
            
            placeholder.markdown(response_text)

        else:
            response = agent.run(prompt, stream=False)
            st.markdown(response.content)
            response_text = response.content #needed below

        # Save report download button
        with open(tmp / f"research_{datetime.now():%Y%m%d%H%M%S}.md", "w") as f:
            f.write(response_text)
    
        st.download_button(
            label="Download Research Report",
            data=response_text,
            file_name=f"research_report_{datetime.now():%Y%m%d}.md",
            mime="text/markdown"
        )

# --------------- FOOTER & INFO -------------------
st.markdown("---")
st.caption("""
**Research Agent Features:**
- Academic-grade source verification 📚
- Technical analysis with real-world applications 🌐
- Automatic reference generation 🔗
- Markdown report export 📥
- Cross-disciplinary synthesis 🔄
""")

st.caption(f"Note: I'm using {agent.model.id}!")

# Hidden dependency note
st.markdown("<!--- Run `pip install openai exa-py agno` -->", unsafe_allow_html=True)