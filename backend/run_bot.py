#!/usr/bin/env python
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
from database import SessionLocal
import crud

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8671439867:AAELj__eiVFoie65jw3e2tQQkr_WJIawoDY"

# НАСТРОЙКА ПРОКСИ (выберите один вариант)
# Вариант 1: SOCKS5 прокси (например, через Tor или VPN)
PROXY_URL = "socks5://127.0.0.1:1080"  # Замените на ваш прокси

# Вариант 2: HTTP прокси
# PROXY_URL = "http://45.144.53.89:80"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 <b>Jade Archive Bot</b>\n\n"
        "/contacts - Список контактов\n"
        "/search <имя> - Поиск\n"
        "/view <id> - Просмотр\n"
        "/help - Помощь",
        parse_mode="HTML"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 <b>Команды:</b>\n"
        "/contacts - Все контакты\n"
        "/search Иван - Поиск\n"
        "/view 1 - Досье",
        parse_mode="HTML"
    )

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Загрузка...")
    db = next(get_db())
    persons = crud.get_persons(db)
    
    if not persons:
        await update.message.reply_text("📭 Нет контактов")
        return
    
    message = "📋 <b>Контакты</b>\n\n"
    for p in persons[:20]:
        message += f"🆔 {p.id}. {p.full_name} (@{p.short_name})\n"
    
    if len(persons) > 20:
        message += f"\n... и еще {len(persons) - 20}"
    
    await update.message.reply_text(message, parse_mode="HTML")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Пример: /search Иван")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Ищу: {query}...")
    
    db = next(get_db())
    persons = crud.search_persons(db, query)
    
    if not persons:
        await update.message.reply_text(f"❌ Не найдено: {query}")
        return
    
    message = f"🔍 <b>Результаты ({len(persons)})</b>\n\n"
    for p in persons[:10]:
        message += f"🆔 {p.id}. {p.full_name}\n"
    
    await update.message.reply_text(message, parse_mode="HTML")

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Пример: /view 1")
        return
    
    try:
        person_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")
        return
    
    db = next(get_db())
    person = crud.get_person(db, person_id)
    
    if not person:
        await update.message.reply_text(f"❌ Контакт {person_id} не найден")
        return
    
    person.social_media = crud.get_social_media(db, person_id)
    
    message = f"👤 <b>{person.full_name}</b>\n"
    message += f"└ @{person.short_name}\n"
    message += f"🆔 ID: {person.id}\n\n"
    message += f"📞 Телефон: {person.phone or '—'}\n"
    message += f"📧 Email: {person.email or '—'}\n"
    message += f"📍 Адрес: {person.address or '—'}\n"
    
    if person.social_media:
        message += "\n🌐 <b>Соцсети:</b>\n"
        for sm in person.social_media:
            message += f"• {sm.platform}: {sm.link}\n"
    
    await update.message.reply_text(message, parse_mode="HTML")

def run():
    """Запуск бота с прокси"""
    print("🤖 Запуск Telegram бота...")
    print(f"Токен: {BOT_TOKEN[:10]}...")
    
    try:
        # Создаем request с прокси (если PROXY_URL задан)
        if PROXY_URL:
            print(f"🔄 Используется прокси: {PROXY_URL}")
            request = HTTPXRequest(proxy_url=PROXY_URL)
            application = Application.builder().token(BOT_TOKEN).request(request).build()
        else:
            application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("contacts", contacts))
        application.add_handler(CommandHandler("search", search))
        application.add_handler(CommandHandler("view", view))
        
        # Запускаем polling
        print("✅ Бот запущен! Нажмите Ctrl+C для остановки.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    run()