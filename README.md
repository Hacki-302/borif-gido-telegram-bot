# 🤖 Borif Gido — Personal Portfolio Telegram Bot

<p align="center">
  <strong>A conversational Telegram bot that introduces Borif Gido, showcases his software engineering projects, and answers general programming and technology questions.</strong>
</p>

<p align="center">
  <a href="https://github.com/Hacki-302/borif-gido-telegram-bot">GitHub Repository</a> •
  <a href="https://hacki-302.github.io/MyPortfolio/">Personal Portfolio</a> •
  <a href="https://t.me/MaadiiB9">Telegram Contact</a>
</p>

---

## 📌 About the Project

**Borif Gido Telegram Bot** is a Python-powered conversational portfolio assistant designed to provide information about Borif Gido's background, education, technical skills, interests, and software development projects.

Beyond serving as a digital portfolio, the bot includes a structured knowledge base that helps users explore programming, web development, computer science, and modern technology topics.

The project focuses on providing a simple, accessible, and interactive way to discover personal portfolio information and learn about technology through Telegram.

## ✨ Features

### 👤 Personal Portfolio Assistant
- Provides personal information and introduction.
- Displays educational background.
- Explains technical skills and interests.
- Shares future goals and professional ambitions.
- Presents software development projects.
- Provides portfolio and contact links.

### 📚 General Knowledge Assistant
- Answers supported programming questions.
- Provides information about programming languages.
- Explains frontend and backend development.
- Covers web development technologies and frameworks.
- Introduces computer science concepts.
- Covers technology topics such as artificial intelligence and cybersecurity.

### 💬 Conversational Experience
- Accepts natural-language text questions.
- Uses keyword matching to identify relevant answers.
- Supports selected follow-up questions using conversation context.
- Provides a simple text-based interface without inline menu buttons.

### ⚙️ Additional Capabilities
- Separate profile and knowledge-base JSON files.
- Basic usage statistics.
- Administrator-related functionality.
- Error handling and application logging.
- Environment-variable configuration.

> **Note:** The general knowledge assistant uses a curated JSON knowledge base and keyword matching. It is not an unrestricted AI language model.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| python-telegram-bot | Telegram Bot API integration |
| python-dotenv | Environment variable management |
| JSON | Profile, knowledge base, and statistics storage |
| Git & GitHub | Version control and source-code hosting |
| FadeHost | Bot deployment and hosting |

## 📂 Project Structure

```text
telegram-bot/
│
├── bot.py                  # Main Telegram bot application
├── profile.json            # Personal portfolio information
├── knowledge_base.json     # General knowledge questions and answers
├── .env                    # Private environment configuration
├── .gitignore              # Git exclusion rules
├── requirements.txt        # Python dependencies
├── stats.json              # Bot usage statistics (if generated)
├── README.md               # Project documentation
│
└── .venv/                  # Python virtual environment
```

*Some files, such as `stats.json`, may be created automatically when the bot runs.*

## 🚀 Getting Started

Follow these instructions to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Hacki-302/borif-gido-telegram-bot.git
```

### 2. Navigate to the Project Directory

```bash
cd borif-gido-telegram-bot
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ADMIN_USER_ID=YOUR_TELEGRAM_USER_ID
```

Replace the placeholder values with your own credentials.

**Security warning:** Never publish your `.env` file, bot token, or private credentials to GitHub.

### 7. Run the Bot

```bash
python bot.py
```

The bot should start and connect to Telegram.

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Start the bot and display its welcome message |
| `/help` | Display available help information |
| `/stats` | View bot usage statistics (administrator functionality) |
| `/about` | Learn about Borif Gido |
| `/education` | View educational background |
| `/skills` | Explore technical skills |
| `/projects` | View software development projects |
| `/goals` | Explore future goals |
| `/interests` | View personal and professional interests |
| `/contact` | Get contact and portfolio information |

Users can also ask questions directly using ordinary text.

## 💬 Example Questions

Try asking the bot:

**Personal Portfolio Questions**
- Who is Borif Gido?
- What does Borif study?
- What programming languages does Borif know?
- What projects has Borif developed?
- How can I contact Borif?

**Programming and Technology Questions**
- What is programming?
- Explain Python.
- What is JavaScript?
- What is React?
- What is a database?
- What is artificial intelligence?
- What is cybersecurity?
- What is cloud computing?

**Follow-up Questions**
- Tell me more.
- Explain further.
- What are its advantages?
- How does it work?

The bot answers topics covered by its knowledge base and configured conversational logic.

## 🔐 Security

Security is an important part of this project.

- Store Telegram credentials in `.env`.
- Keep `.env` excluded from Git.
- Never share your bot token publicly.
- Avoid committing virtual environments and Python cache files.
- Restrict administrator functionality to authorized users.

## 🌐 Deployment

The project can be hosted using **FadeHost**.

General deployment workflow:

1. Push the latest project changes to the GitHub `main` branch.
2. Open your FadeHost dashboard.
3. Check the bot's deployment status.
4. Review deployment logs for errors.
5. Test the live bot through Telegram.

GitHub repository:

https://github.com/Hacki-302/borif-gido-telegram-bot

## 🗺️ Future Improvements

Potential future development ideas include:

- More comprehensive programming knowledge.
- Improved natural-language understanding.
- More advanced conversational memory.
- Additional educational topics.
- Multilingual support.
- Improved administrator dashboard and analytics.
- Optional AI-powered responses.

These are potential enhancements and are not necessarily implemented in the current version.

## 👨‍💻 Developer

**Borif Gido**

Software Engineering Student | Aspiring Full-Stack Developer | Cybersecurity Enthusiast | AI Engineer

- **GitHub:** https://github.com/Hacki-302
- **Portfolio:** https://hacki-302.github.io/my-portfolio/
- **Telegram:** https://t.me/MaadiiB9

## 📄 License

No license has been specified for this project yet. All rights and permissions should be clarified before others reuse, modify, or distribute the source code.

---

<p align="center">
  <strong>Built with Python and a passion for software engineering. 🚀</strong>
</p>