from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool
from backend.expense_tools import (
    insert_expense,
    fetch_expenses_tool,
    fetch_latest_expense_tool,
    fetch_expenses_between_dates_tool,
    update_expense_tool,
    delete_expense_tool,
    fetch_category_summary_tool,
    fetch_daily_spending_tool,
    fetch_monthly_spending_tool
)
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Tools
tools = [
    fetch_expenses_tool,
    fetch_latest_expense_tool,
    fetch_expenses_between_dates_tool,
    fetch_category_summary_tool,
    fetch_daily_spending_tool,
    fetch_monthly_spending_tool
]
system_prompt = """You are a Personal Finance Advisor AI.

Your role is to give thoughtful, practical, and trustworthy financial advice
based on the user’s actual expense data.

Guidelines:
- Focus on advice, not raw analytics or statistics.
- Explain *why* a change is beneficial in simple terms.
- Recommend realistic actions the user can actually follow.
- Prioritize financial discipline, savings, and stability.
- Avoid extreme, risky, or speculative recommendations.
- Do not shame or judge spending behavior.
- Keep the tone supportive, calm, and responsible.
- Base advice only on the provided data; do not assume income or investments unless given.
- If data is insufficient, give cautious, general guidance and state limitations clearly.

Your goal is to help the user make better financial decisions step by step,
like a responsible financial mentor.

"""
# Create agent
advice_agent = create_agent(llm, tools=tools,system_prompt=system_prompt)




@tool
def analyze_finances_tool(
    user_id: str,
    start_date: str,
    end_date: str
):
    """
    Analyze user finances and provide insights and planning suggestions.
    """

    prompt = f"""
    user_id: {user_id}
    Analyze the user's expenses for the period: {start_date} to {end_date}.
    Provide practical money management suggestions.
    """

    response = advice_agent.invoke({
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    return response