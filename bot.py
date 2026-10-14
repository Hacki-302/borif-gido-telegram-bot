
import json
import logging
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ---------------- Configuration ----------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def load_profile():
    profile_path = BASE_DIR / "profile.json"

    with profile_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    required = ["name", "title", "bio", "education", "skills",
                "projects", "interests", "goals", "contact"]

    for field in required:
        if field not in data:
            raise ValueError(f"Missing '{field}' in profile.json")

    return data


PROFILE = load_profile()


# ---------------- Menu ----------------



def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("👤 About Me", callback_data="about"),
            InlineKeyboardButton("🎓 Education", callback_data="education"),
        ],
        [
            InlineKeyboardButton("💻 Skills", callback_data="skills"),
            InlineKeyboardButton("🚀 Projects", callback_data="projects"),
        ],
        [
            InlineKeyboardButton("🎯 Goals", callback_data="goals"),
            InlineKeyboardButton("📬 Contact", callback_data="contact"),
        ],
    ]

    contact = PROFILE.get("contact", {})

    github_url = contact.get("github", "").strip()
    portfolio_url = contact.get("portfolio", "").strip()

    links = []

    if github_url.startswith("https://github.com/"):
        links.append(
            InlineKeyboardButton(
                "🐙 GitHub Profile",
                url=github_url
            )
        )

    if portfolio_url.startswith("https://"):
        links.append(
            InlineKeyboardButton(
                "🌐 Portfolio Website",
                url=portfolio_url
            )
        )

    if links:
        keyboard.append(links)

    return InlineKeyboardMarkup(keyboard)


# ---------------- Profile answers ----------------

def format_projects():
    projects = PROFILE["projects"]
    lines = ["🚀 My Projects\n"]

    for item in projects:
        if isinstance(item, dict):
            name = item.get("name", "Untitled project")
            description = item.get("description", "")
            lines.append(f"• {name}\n  {description}")
        else:
            lines.append(f"• {item}")

    return "\n\n".join(lines)


def format_contact():
    contact = PROFILE["contact"]
    lines = ["📬 Find me online\n"]

    labels = {
        "telegram": "Telegram",
        "github": "GitHub",
        "portfolio": "Portfolio",
    }

    for key, label in labels.items():
        value = contact.get(key, "").strip()
        if value:
            lines.append(f"{label}: {value}")

    if len(lines) == 1:
        lines.append(
            "Public contact links have not been added yet."
        )

    return "\n".join(lines)


def get_section(section):
    if section == "about":
        return (
            f"👋 I'm {PROFILE['name']}.\n"
            f"{PROFILE['title']}\n\n"
            f"{PROFILE['bio']}"
        )

    if section == "education":
        education = PROFILE["education"]
        return (
            "🎓 Education\n\n"
            f"University: {education.get('university', 'Not provided')}\n"
            f"Field: {education.get('field', 'Not provided')}\n"
            f"Level: {education.get('level', 'Not provided')}"
        )

    if section == "skills":
        skills = PROFILE["skills"]
        return "💻 Skills I'm learning\n\n" + "\n".join(
            f"• {skill}" for skill in skills
        )

    if section == "projects":
        return format_projects()

    if section == "interests":
        return "✨ My Interests\n\n" + "\n".join(
            f"• {item}" for item in PROFILE["interests"]
        )

    if section == "goals":
        return "🎯 My Goals\n\n" + "\n".join(
            f"• {item}" for item in PROFILE["goals"]
        )

    if section == "contact":
        return format_contact()

    return "Sorry, I don't recognize that menu option."


def normalize(text):
    return re.sub(r"[^a-z0-9+#. ]", " ", text.lower()).strip()


def answer_question(question):
    text = normalize(question)

    # Check longer, more specific topics first.
    if any(word in text for word in [
        "contact", "github", "telegram", "website", "portfolio link"
    ]):
        return get_section("contact")

    if any(word in text for word in [
        "project", "projects", "what have you built",
        "what are you building", "systems"
    ]):
        return get_section("projects")

    if any(word in text for word in [
        "skill", "skills", "programming language",
        "languages", "what can you do", "what do you know"
    ]):
        return get_section("skills")

    if any(word in text for word in [
        "university", "education", "degree", "study",
        "studying", "student", "department"
    ]):
        return get_section("education")

    if any(word in text for word in [
        "goal", "goals", "future", "ambition", "career", "dream"
    ]):
        return get_section("goals")

    if any(word in text for word in [
        "interest", "interests", "hobby", "hobbies", "passion"
    ]):
        return get_section("interests")

    if any(word in text for word in [
        "who are you", "about you", "about me", "introduce",
        "yourself", "your name", "who is borif"
    ]):
        return get_section("about")

    if "name" in text:
        return f"My name is {PROFILE['name']}."

    return (
        "🤔 I couldn't match that question to my profile.\n\n"
        "Try asking about my education, skills, projects, goals, "
        "interests, or contact links. You can also use the buttons below."
    )


# ---------------- Commands and handlers ----------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = (
        f"👋 Welcome! I'm {PROFILE['name']}'s Portfolio Bot.\n\n"
        "Explore my education, programming skills, projects, "
        "and goals using the menu below.\n\n"
        "You can also type a question about my profile."
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_menu(),
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        "📚 Available commands:\n\n"
        "/start - Open the main menu\n"
        "/about - About me\n"
        "/skills - My skills\n"
        "/projects - My projects\n"
        "/goals - My goals\n"
        "/contact - My public links\n"
        "/help - Show this help message"
    )


async def section_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    section = update.message.text.split("@")[0].lstrip("/").lower()
    await update.effective_message.reply_text(get_section(section))


async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        get_section(query.data),
        reply_markup=main_menu(),
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    question = update.effective_message.text
    await update.effective_message.reply_text(
        answer_question(question),
        reply_markup=main_menu(),
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error("An error occurred while handling an update",
                 exc_info=context.error)


def main():
    if not TOKEN or TOKEN == "YOUR_ACTUAL_TELEGRAM_BOT_TOKEN":
        raise RuntimeError(
            "Set your real TELEGRAM_BOT_TOKEN in the .env file."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    for command in ["about", "education", "skills", "projects",
                    "goals", "contact"]:
        app.add_handler(CommandHandler(command, section_command))

    app.add_handler(CallbackQueryHandler(menu_callback))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    app.add_error_handler(error_handler)

    logger.info("Starting %s Portfolio Bot", PROFILE["name"])
    app.run_polling()


if __name__ == "__main__":
    main()
