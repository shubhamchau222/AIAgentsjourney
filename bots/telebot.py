import os 
from dotenv import load_dotenv
from telegram.ext import Application
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from telegram import Update

env_path = r"D:\common_credentials\.env"
load_dotenv(dotenv_path=env_path)


GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_content(full_prompt):
    try:
        response= model.generate_content(full_prompt)
        return response.text if hasattr(response, "text") else "Sorry, I can't generate a response"
    except Exception as e:
        return "There was error while generating the output.."

# generate_content("Hi")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.first_name
    system_message= f"Hello {user_id}! I am chabot. How can I assist you today?"
    await  update.message.reply_text(system_message)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response_text = generate_content(user_message)
    await update.message.reply_text(response_text)

# Build the application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()