
import json
import logging
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from telegram import (
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


# =========================================================
# 1. CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID", "").strip()

PROFILE_FILE = BASE_DIR / "profile.json"
STATS_FILE = BASE_DIR / "stats.json"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


# =========================================================
# 2. PROFILE DATA
# =========================================================

def load_profile():
    """Load and validate portfolio information from profile.json."""

    if not PROFILE_FILE.exists():
        raise FileNotFoundError(
            f"profile.json was not found at {PROFILE_FILE}"
        )

    with PROFILE_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    required_fields = [
        "name",
        "title",
        "bio",
        "education",
        "skills",
        "projects",
        "interests",
        "goals",
        "contact",
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(
                f"Missing required field '{field}' in profile.json"
            )

    return data


PROFILE = load_profile()

# =========================================================
# KNOWLEDGE BASE
# =========================================================

def load_knowledge_base():
    """Load general knowledge from the JSON file."""

    knowledge_file = BASE_DIR / "knowledge_base.json"

    try:
        with open(knowledge_file, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        logging.warning("Knowledge base file was not found.")
        return {}

    except json.JSONDecodeError as error:
        logging.error("Invalid knowledge base JSON: %s", error)
        return {}


KNOWLEDGE_BASE = load_knowledge_base()
# =========================================================
# 3. USAGE STATISTICS
# =========================================================

DEFAULT_STATS = {
    "starts": 0,
    "questions": 0,
    "menu_clicks": 0,
    "errors": 0,
}


def load_stats():
    """Load saved statistics or initialize default counters."""

    if not STATS_FILE.exists():
        return DEFAULT_STATS.copy()

    try:
        with STATS_FILE.open("r", encoding="utf-8") as file:
            saved = json.load(file)

        if not isinstance(saved, dict):
            logger.warning(
                "stats.json must contain a JSON object. Using defaults."
            )
            return DEFAULT_STATS.copy()

        result = DEFAULT_STATS.copy()

        for key in DEFAULT_STATS:
            value = saved.get(key, 0)

            if type(value) is int and value >= 0:
                result[key] = value

        return result

    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.warning(
            "stats.json is invalid. Using default statistics."
        )
        return DEFAULT_STATS.copy()

    except OSError:
        logger.exception("Could not read stats.json.")
        return DEFAULT_STATS.copy()


stats = load_stats()


def save_stats():
    """Save statistics safely using a temporary file."""

    temp_file = STATS_FILE.with_suffix(".tmp")

    try:
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(stats, file, indent=2)

        temp_file.replace(STATS_FILE)

    except OSError:
        logger.exception("Could not save usage statistics.")


def increment_stat(name):
    """Increase a known statistics counter."""

    if name not in stats:
        logger.warning("Unknown statistics counter: %s", name)
        return

    stats[name] += 1
    save_stats()


# =========================================================
# 4. KEYBOARDS
# =========================================================

def main_menu_text():
    """Return a conversational welcome message."""

    return (
        f"👋 Hello! Welcome to {PROFILE['name']}'s Portfolio Bot.\n\n"
        f"👨‍💻 {PROFILE['title']}\n\n"
        f"{PROFILE['bio']}\n\n"
        "💬 I'm here to answer your questions about Borif Gido.\n\n"
        "You can ask me about:\n"
        "• Personal information\n"
        "• Education and university\n"
        "• Programming skills\n"
        "• Projects and experience\n"
        "• Career goals and interests\n"
        "• Contact information\n\n"
        "Just type your question naturally. Let's chat! 🚀\n\n"
        "Example: What projects has Borif built?"
    )

# =========================================================
# 6. PROFILE SECTION FORMATTERS
# =========================================================


def format_projects():
    """Format all portfolio projects into a readable message."""

    projects = PROFILE.get("projects", [])

    if not projects:
        return "No projects have been added yet."

    lines = ["💻 Borif Gido's Projects\n"]

    for index, project in enumerate(projects, start=1):
        technologies = ", ".join(
            project.get("technologies", [])
        )

        lines.append(
            f"{index}. {project.get('name', 'Unnamed Project')}\n"
            f"📝 Description: {project.get('description', 'No description available.')}\n"
            f"🛠 Technologies: {technologies or 'Not specified'}\n"
            f"🔗 GitHub: {project.get('github', 'Not available')}\n"
        )

    return "\n".join(lines)


def format_contact():
    """Format contact information."""

    contact = PROFILE.get("contact", {})

    return (
        "📩 Contact Information\n\n"
        f"📱 Telegram: {contact.get('telegram', 'Not available')}\n"
        f"💻 GitHub: {contact.get('github', 'Not available')}\n"
        f"🌐 Portfolio: {contact.get('portfolio', 'Not available')}"
    )


def get_section(section):
    """Return the requested portfolio section."""

    if section == "about":
        return (
            f"👤 About {PROFILE['name']}\n\n"
            f"🎓 {PROFILE['title']}\n\n"
            f"{PROFILE['bio']}"
        )

    if section == "education":
        education = PROFILE["education"]

        return (
            "🎓 Education\n\n"
            f"🏫 University: {education['university']}\n"
            f"📚 Field: {education['field']}\n"
            f"📌 Level: {education['level']}"
        )

    if section == "skills":
        skills = PROFILE.get("skills", [])

        return (
            "🛠 Borif Gido's Skills\n\n"
            + "\n".join(f"• {skill}" for skill in skills)
        )

    if section == "projects":
        return format_projects()

    if section == "goals":
        goals = PROFILE.get("goals", [])

        return (
            "🎯 Career Goals\n\n"
            + "\n".join(f"• {goal}" for goal in goals)
        )

    if section == "interests":
        interests = PROFILE.get("interests", [])

        return (
            "💡 Interests\n\n"
            + "\n".join(f"• {interest}" for interest in interests)
        )

    if section == "contact":
        return format_contact()

    return "Sorry, this portfolio section is not available."

def answer_from_knowledge_base(question):
    """Find an answer from the general knowledge database."""

    text = normalize(question)

    for category, entries in KNOWLEDGE_BASE.items():

        for entry in entries:

            for keyword in entry.get("keywords", []):

                normalized_keyword = normalize(keyword)

                if re.search(
                    r"\b" + re.escape(normalized_keyword) + r"\b",
                    text
                ):
                    return (
                        f"📚 {entry['question']}\n\n"
                        f"{entry['answer']}"
                    )

    return None
# =========================================================
# 7. QUESTION MATCHING
# =========================================================

def normalize(text):
    """Normalize questions for more reliable matching."""

    text = text.lower()
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def answer_question(question):
    """Answer personal profile and general knowledge questions."""

    text = normalize(question)

    # Words that indicate the question is about Borif personally.
    personal_references = [
        "borif",
        "he",
        "him",
        "his",
        "you",
        "your",
    ]

    refers_to_borif = any(
        re.search(
            r"\b" + re.escape(word) + r"\b",
            text
        )
        for word in personal_references
    )

    # Search the general knowledge base for questions
    # that do not refer to Borif personally.
    if not refers_to_borif:
        knowledge_answer = answer_from_knowledge_base(question)

        if knowledge_answer:
            return knowledge_answer

    # Keep your existing matches() function and all
    # personal profile matching rules below this point.

    knowledge_answer = answer_from_knowledge_base(question)

    if knowledge_answer:
        return knowledge_answer

    def matches(words):
        return any(
            re.search(r"\b" + re.escape(word) + r"\b", text)
            for word in words
        )

    # 1. Contact information
    if matches([
        "contact",
        "contact information",
        "contact details",
        "contact him",
        "contact borif",
        "how can i contact",
        "how can i contact him",
        "how do i contact",
        "reach him",
        "reach borif",
        "get in touch",
        "email",
        "email address",
        "telegram",
        "telegram username",
        "social media",
        "social links",
        "website",
        "portfolio link",
        "github profile",
        "github link",
    ]):
        return get_section("contact")

    # 2. Projects and development work
    if matches([
        "project",
        "projects",
        "built",
        "build",
        "building",
        "developed",
        "develop",
        "created",
        "create",
        "made",
        "applications",
        "application",
        "apps",
        "software system",
        "systems",
        "repositories",
        "repository",
        "what have you made",
        "what have you built",
        "what has he built",
        "what did he build",
        "show me his work",
        "tell me about his work",
        "portfolio projects",
    ]):
        return get_section("projects")

    # 3. Skills and technologies
    if matches([
        "skill",
        "skills",
        "programming",
        "programming language",
        "programming languages",
        "language",
        "languages",
        "technology",
        "technologies",
        "tech stack",
        "tools",
        "coding",
        "framework",
        "frameworks",
        "python",
        "javascript",
        "java",
        "typescript",
        "html",
        "css",
        "c++",
        "node",
        "react",
        "database",
        "git",
        "github",
        "problem solving",
        "data structures",
        "what can you do",
        "what do you know",
        "what are you learning",
    ]):
        return get_section("skills")

    # 4. Education
    if matches([
        "university",
        "college",
        "education",
        "degree",
        "study",
        "studying",
        "student",
        "department",
        "academic",
        "course",
        "field of study",
        "where do you study",
        "where does he study",
        "what do you study",
        "what is he studying",
    ]):
        return get_section("education")

    # 5. Career goals
    if matches([
        "goal",
        "goals",
        "future",
        "ambition",
        "career",
        "dream",
        "aspiration",
        "plans",
        "want to become",
        "career plan",
        "future plan",
        "what does he want to become",
    ]):
        return get_section("goals")

    # 6. Interests
    if matches([
        "interest",
        "interests",
        "hobby",
        "hobbies",
        "passion",
        "like doing",
        "enjoy doing",
        "favorite activity",
        "what does he enjoy",
        "what does he like",
    ]):
        return get_section("interests")

    # 7. Personal information
    if matches([
        "who are you",
        "who is borif",
        "who is borif gido",
        "who is he",
        "personal information",
        "personal details",
        "about you",
        "about me",
        "about borif",
        "introduce",
        "introduction",
        "yourself",
        "your name",
        "tell me about borif",
        "tell me about him",
        "tell me about yourself",
        "biography",
        "bio",
    ]):
        return get_section("about")

    # 8. Name questions
    if matches(["name"]):
        return f"My name is {PROFILE['name']}."

    # 9. Friendly fallback without menu references
    return (
        "🤔 I couldn't find a matching answer in my portfolio yet.\n\n"
        "You can ask me questions such as:\n"
        "👤 Who is Borif Gido?\n"
        "🎓 Where does he study?\n"
        "🛠 What technologies does he know?\n"
        "💻 What projects has he built?\n"
        "🎯 What are his career goals?\n"
        "❤️ What are his interests?\n"
        "📩 How can I contact him?\n\n"
        "Try asking in a different way if I don't understand. 🚀"
    )


# =========================================================
# 8. TELEGRAM COMMAND HANDLERS
# =========================================================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle /start without displaying menu buttons."""

    increment_stat("starts")

    await update.effective_message.reply_text(
        text=main_menu_text(),
    )





async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Explain how to communicate with the conversational bot."""

    message = (
        "🤖 Borif Gido Portfolio Bot — Help\n\n"
        "You can communicate with me by typing questions naturally.\n\n"
        "Examples:\n"
        "• Who is Borif Gido?\n"
        "• Where does he study?\n"
        "• What programming languages does he know?\n"
        "• Tell me about his projects.\n"
        "• What are his career goals?\n"
        "• How can I contact him?\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/stats - View bot statistics (admin only)\n\n"
        "Just type your question and let's chat! 🚀"
    )

    await update.effective_message.reply_text(message)




async def section_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle profile section commands without menu buttons."""

    command = update.effective_message.text.split()[0]
    section = command.split("@")[0].lstrip("/").lower()

    await update.effective_message.reply_text(
        get_section(section),
    )


async def stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Show usage statistics to the configured administrator."""

    user = update.effective_user

    if (
        not ADMIN_USER_ID
        or user is None
        or str(user.id) != ADMIN_USER_ID
    ):
        await update.effective_message.reply_text(
            "⛔ You are not authorized to view usage statistics."
        )
        return

    report = (
        "📊 Borif Gido Bot Statistics\n\n"
        f"🚀 Bot starts: {stats['starts']}\n"
        f"💬 Profile questions: {stats['questions']}\n"
        f"🖱 Menu clicks: {stats['menu_clicks']}\n"
        f"⚠️ Recorded errors: {stats['errors']}"
    )

    await update.effective_message.reply_text(report)
# =========================================================
# 10. TEXT MESSAGE HANDLER
# =========================================================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Answer ordinary text questions."""

    message = update.effective_message

    if message is None or not message.text:
        return

    increment_stat("questions")

    answer = answer_question(message.text)

    await message.reply_text(
    text=answer,
)


# =========================================================
# 11. ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Log unexpected errors without crashing the bot."""

    error = context.error

    if error is None:
        logger.error("An unknown bot error occurred.")
    else:
        logger.error(
            "An unhandled bot error occurred.",
            exc_info=(
                type(error),
                error,
                error.__traceback__,
            ),
        )

    increment_stat("errors")


# =========================================================
# 12. START THE BOT
# =========================================================

def main():
    """Configure handlers and start polling Telegram."""

    if not TOKEN or TOKEN == "YOUR_ACTUAL_TELEGRAM_BOT_TOKEN":
        raise RuntimeError(
            "Set your real TELEGRAM_BOT_TOKEN in the .env file."
        )

    app = Application.builder().token(TOKEN).build()

    # Error handling
    app.add_error_handler(error_handler)

    # Main commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))

    # Portfolio section commands
    for command in [
        "about",
        "education",
        "skills",
        "projects",
        "goals",
        "interests",
        "contact",
    ]:
        app.add_handler(
            CommandHandler(command, section_command)
        )

    # Regular text questions
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    logger.info(
        "Starting %s Portfolio Bot",
        PROFILE["name"],
    )

    app.run_polling()


if __name__ == "__main__":
    main()
