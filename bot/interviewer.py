# bot/interviewer.py

import sys
import os
sys.path.append(".")

from groq import Groq
from dotenv import load_dotenv
from retrieval.retriever import retrieve_context

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Topics that have external resources in data/ folder ──
# Add topic name here whenever you add a new PDF/URL resource
TOPICS_WITH_RESOURCES = [
    "python",
    "java",
    "sql",
]

# ── All available topics ──
TOPICS = {
    "1": "Python",
    "2": "Java",
    "3": "JavaScript",
    "4": "C++",
    "5": "SQL",
    "6": "Data Science",
    "7": "Machine Learning",
    "8": "System Design",
    "9": "Django",
    "10": "React",
    "11": "RAG",
    "12": "LangChain",
    "13": "Deep Learning",
    "14": "DevOps",
    "15": "Docker",
}

DIFFICULTY = {
    "1": "Beginner",
    "2": "Intermediate",
    "3": "Advanced"
}

SKIP_COMMANDS = ["pass", "skip", "next", "idk",
                 "i don't know", "i dont know", "not sure"]

# ── System prompt when RAG resources are available ──
RAG_SYSTEM_PROMPT = """You are a professional technical interviewer conducting a {topic} interview.

You have access to verified reference material for {topic} in the context below.

YOUR BEHAVIOR:
- Ask questions strictly based on the context provided
- After the candidate answers, compare their answer with the context
- Give feedback like: "✅ Correct!", "⚠️ Partially correct", "❌ Incorrect"
- If incorrect, show the correct answer from the context
- If candidate says pass/skip/idk → reveal the correct answer from context, then move on
- Ask one question at a time
- After 5 questions give score out of 10 with summary

Difficulty: {difficulty}

✅ Reference Material (use this to ask questions AND verify answers):
{context}
"""

# ── System prompt when NO resources available (LLM knowledge only) ──
LLM_SYSTEM_PROMPT = """You are a professional technical interviewer conducting a {topic} interview.

You are using your own trained knowledge to conduct this interview.

YOUR BEHAVIOR:
- Ask relevant {topic} interview questions based on your knowledge
- After the candidate answers, evaluate using your own knowledge
- Give feedback like: "✅ Correct!", "⚠️ Partially correct", "❌ Incorrect"
- If incorrect, explain the correct answer from your knowledge
- If candidate says pass/skip/idk → reveal the correct answer, then move on
- Ask one question at a time
- After 5 questions give score out of 10 with summary

Difficulty: {difficulty}

Note: No external resources loaded for this topic. Using trained knowledge only.
"""

def has_resources(topic: str) -> bool:
    """Check if topic has external resources in vector store"""
    return topic.lower() in TOPICS_WITH_RESOURCES


def select_topic():
    print("\n📚 Select Interview Topic:")
    print("-" * 40)
    for key, value in TOPICS.items():
        # Show resource indicator
        tag = "📄" if has_resources(value) else "🧠"
        print(f"  {key}. {tag} {value}")
    print("  0. Custom topic (type your own)")
    print("-" * 40)
    print("  📄 = Has external resources | 🧠 = Uses LLM knowledge")
    print("-" * 40)

    choice = input("Enter number: ").strip()

    if choice == "0":
        topic = input("Enter your custom topic: ").strip()
    elif choice in TOPICS:
        topic = TOPICS[choice]
    else:
        print("Invalid choice, defaulting to Python")
        topic = "Python"

    return topic


def select_difficulty():
    print("\n🎯 Select Difficulty Level:")
    print("-" * 30)
    for key, value in DIFFICULTY.items():
        print(f"  {key}. {value}")
    print("-" * 30)

    choice = input("Enter number: ").strip()
    return DIFFICULTY.get(choice, "Intermediate")


def get_context_and_prompt(user_input: str, topic: str, difficulty: str):
    """
    Smart context fetcher:
    - If topic has resources → fetch from vector store
    - If not → use LLM knowledge only
    """

    if has_resources(topic):
        # ── RAG Mode: fetch from vector store ──
        if user_input.lower().strip() in SKIP_COMMANDS:
            search_query = f"{topic} interview question answer"
        else:
            search_query = f"{topic} {user_input}"

        context = retrieve_context(search_query, k=5)

        system = RAG_SYSTEM_PROMPT.format(
            topic=topic,
            difficulty=difficulty,
            context=context
        )
        mode = "📄 RAG Mode"

    else:
        # ── LLM Mode: use trained knowledge ──
        system = LLM_SYSTEM_PROMPT.format(
            topic=topic,
            difficulty=difficulty
        )
        mode = "🧠 LLM Mode"

    return system, mode


def run_interview(user_input: str, history: list, topic: str, difficulty: str):
    """Run one turn of the interview"""

    system, mode = get_context_and_prompt(user_input, topic, difficulty)

    # Add user message to history
    history.append({"role": "user", "content": user_input})

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "system", "content": system}] + history
    )

    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    return assistant_message, history, mode


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI Interview Bot")
    print("💡 Powered by Groq + RAG")
    print("=" * 50)

    topic = select_topic()
    difficulty = select_difficulty()

    # Show which mode will be used
    if has_resources(topic):
        print(f"\n📄 RAG Mode: Using external resources for {topic}")
    else:
        print(f"\n🧠 LLM Mode: Using trained knowledge for {topic}")

    print(f"✅ Starting {difficulty} level {topic} interview...")
    print("📝 Commands: 'pass'=skip | 'quit'=exit | 'restart'=new topic")
    print("=" * 50)

    history = []

    print("\n⏳ Preparing your interview...\n")
    first_response, history, mode = run_interview(
        f"Start a {difficulty} level {topic} interview. Ask the first question.",
        history,
        topic,
        difficulty
    )
    print(f"[{mode}]")
    print(f"🎙️  Interviewer: {first_response}\n")
    print("-" * 50)

    while True:
        user_input = input("👤 You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("\n👋 Interview ended. Good luck!")
            break

        if user_input.lower() == "restart":
            print("\n🔄 Restarting...\n")
            history = []
            topic = select_topic()
            difficulty = select_difficulty()
            user_input = f"Start a {difficulty} level {topic} interview. Ask the first question."

        print("\n⏳ Thinking...\n")
        response, history, mode = run_interview(user_input, history, topic, difficulty)
        print(f"[{mode}]")
        print(f"🎙️  Interviewer: {response}\n")
        print("-" * 50)