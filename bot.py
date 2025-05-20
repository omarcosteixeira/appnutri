import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from report import gerar_relatorio_pdf

TOKEN = "7644187891:AAEo8AqDA1MvUnp0-klC3Z2ZtZXFElEjhjM"
WEBHOOK_URL = "https://appnutri-j31s.onrender.com/webhook"
PORT = int(os.getenv("PORT", "8443"))

(SEXO, IDADE, PESO, ALTURA, CINTURA, QUADRIL, TRICEPS, BICEPS, ATIVIDADE) = range(9)

dados = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Vamos começar a avaliação.\nQual o sexo do paciente? (m/f)"
    )
    return SEXO

async def receber_sexo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["sexo"] = update.message.text.lower()
    await update.message.reply_text("Idade?")
    return IDADE

async def receber_idade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["idade"] = int(update.message.text)
    await update.message.reply_text("Peso (kg)?")
    return PESO

async def receber_peso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["peso"] = float(update.message.text)
    await update.message.reply_text("Altura (cm)?")
    return ALTURA

async def receber_altura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["altura"] = float(update.message.text)
    await update.message.reply_text("Circunferência da cintura (cm)?")
    return CINTURA

async def receber_cintura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["cintura"] = float(update.message.text)
    await update.message.reply_text("Circunferência do quadril (cm)?")
    return QUADRIL

async def receber_quadril(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["quadril"] = float(update.message.text)
    await update.message.reply_text("Dobra cutânea: Tríceps (mm)?")
    return TRICEPS

async def receber_triceps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["triceps"] = float(update.message.text)
    await update.message.reply_text("Dobra cutânea: Bíceps (mm)?")
    return BICEPS

async def receber_biceps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["biceps"] = float(update.message.text)
    await update.message.reply_text("Nível de atividade (sedentario, leve, moderado, intenso)?")
    return ATIVIDADE

async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados["atividade"] = update.message.text.lower()
    path_pdf = gerar_relatorio_pdf(dados)
    await update.message.reply_document(open(path_pdf, "rb"))
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SEXO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_sexo)],
            IDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_idade)],
            PESO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_peso)],
            ALTURA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_altura)],
            CINTURA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_cintura)],
            QUADRIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_quadril)],
            TRICEPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_triceps)],
            BICEPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_biceps)],
            ATIVIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, calcular)],
        },
        fallbacks=[],
    )

    app.add_handler(conv)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
    )


if __name__ == "__main__":
    main()
