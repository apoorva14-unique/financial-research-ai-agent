"""
Interactive Streamlit Chat Interface for the Financial Research & Analytics AI Agent.

This module provides a clean, professional conversational UI that allows users to ask
questions about Indian stocks (NSE/BSE) including live price, technical indicators,
fundamentals, and financial news.
"""

import streamlit as st
from agent.agent_core import run_agent

DISCLAIMER_TEXT = (
    "Educational & Research Purpose Only. This tool is not a SEBI registered investment advisor. "
    "The information and AI-generated analysis presented do not constitute financial advice "
    "or a recommendation to buy or sell securities."
)


def render_chat_interface(show_disclaimer: bool = True):
    """Renders the AI Financial Research Assistant chat interface."""
    st.subheader("💬 AI Financial Research Assistant")

    # Introductory description
    st.markdown(
        """
        Welcome to the **Financial Research & Analytics AI Agent**. You can ask questions about any Indian equity (NSE/BSE) across 5 core research areas:
        - 📈 **Current Stock Price:** Real-time price, day high/low, trading volume
        - 📊 **Technical Indicators:** RSI (14-day), SMA 20/50, EMA 20, and MACD
        - 🏢 **Fundamental Valuation:** P/E ratio, P/B ratio, ROE, Profit Margin, Market Cap
        - 📰 **Recent Financial News:** Latest market headlines and development sentiment
        - 📑 **Comprehensive Research Summary:** Combined multi-factor analysis
        """
    )

    # Example question chips for fast testing and viva demonstration
    st.write("**Suggested Questions:**")
    col1, col2, col3 = st.columns(3)
    col4, col5, _ = st.columns(3)

    suggested_query = None
    if col1.button("💵 Current Price: Reliance", use_container_width=True):
        suggested_query = "What is the current price of Reliance?"
    if col2.button("📈 Technicals: Reliance", use_container_width=True):
        suggested_query = "Analyze the technical indicators of Reliance."
    if col3.button("🏢 Fundamentals: TCS", use_container_width=True):
        suggested_query = "What are the fundamentals of TCS?"
    if col4.button("📰 Latest News: Infosys", use_container_width=True):
        suggested_query = "What are the latest news about Infosys?"
    if col5.button("📑 Research Summary: Reliance", use_container_width=True):
        suggested_query = "Give me a brief research summary of Reliance."

    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am your AI Financial Research Assistant. "
                    "How can I assist your Indian equity research today? "
                    "You can ask about stock prices, technical indicators, fundamentals, or recent news."
                ),
            }
        ]

    # Render previous conversation history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input via chat_input or suggested chip
    user_input = st.chat_input("Ask a question (e.g. 'What is the current price of Reliance?')...")
    active_query = suggested_query or user_input

    if active_query:
        # Display user question
        st.session_state.chat_messages.append({"role": "user", "content": active_query})
        with st.chat_message("user"):
            st.markdown(active_query)

        # Call AI agent loop and render response
        with st.chat_message("assistant"):
            with st.spinner("AI Agent is analyzing live market data and news..."):
                try:
                    response = run_agent(active_query)
                except Exception as err:
                    response = (
                        f"An unexpected error occurred while processing your request: {str(err)}. "
                        "Please verify your connection and try again."
                    )
                st.markdown(response)

        # Save assistant answer to session state
        st.session_state.chat_messages.append({"role": "assistant", "content": response})

    # Educational & Compliance Disclaimer
    if show_disclaimer:
        st.divider()
        st.caption(f"⚠️ **Disclaimer:** {DISCLAIMER_TEXT}")


# Backward compatibility alias
render_agent_chat = render_chat_interface


# Standalone runner support: `streamlit run ui/chat.py`
if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Financial Research Agent Chat",
        page_icon="🤖",
        layout="wide",
    )
    render_chat_interface()
