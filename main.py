import csv
import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIG
# =========================
TOKEN = os.getenv("8752436181:AAGRBzSlm-sSgL8CQMIRbScbReImpGj5eJo")  # ⚠️ Mets ton token en variable d'environnement
CSV_FILE = "caf.csv"

# 🔽 Lien Dropbox direct
CSV_URL = "https://www.dropbox.com/scl/fi/6ybx9g96o27mcerubcq1w/caf.csv?rlkey=osilw7ai6k4pbaqapwkv4bfkb&dl=1"

logging.basicConfig(level=logging.CRITICAL)

# =========================
# TELECHARGEMENT AUTO CSV (AJOUT)
# =========================
def download_csv():
    if not os.path.exists(CSV_FILE):
        print("⬇️ Téléchargement du fichier CSV...")
        r = requests.get(CSV_URL)
        r.raise_for_status()
        with open(CSV_FILE, "wb") as f:
            f.write(r.content)
        print("✅ CSV téléchargé.")

# =========================
# CHARGEMENT RAPIDE
# =========================
DATA = []

def load_csv():
    global DATA
    with open(CSV_FILE, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["_fulltext"] = " ".join(str(v) for v in row.values()).lower()
            DATA.append(row)

    print(f"✅ {len(DATA)} lignes chargées.")

# =========================
# RECHERCHE INTELLIGENTE
# =========================
def search_smart(words):
    results = []
    for row in DATA:
        if all(word in row["_fulltext"] for word in words):
            results.append(row)
    return results

# =========================
# COMMANDES
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "👋 Bot opérationnel."
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Utilise /lookup <mots clés>")

async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Utilisation : /lookup noe roubaud")
        return

    words = [w.lower() for w in context.args]
    results = search_smart(words)

    if not results:
        await update.message.reply_text("🔎 Aucun résultat trouvé.")
        return

    for row in results[:15]:
        message = f"""
🆔 {row['id']}
👤 {row['nom']} {row['prenom']}
🎂 {row['date_naissance']}
📧 {row['courriel']}
📞 {row['telephone']}
🏠 {row['voie']} {row['cplt_adresse']}
📮 {row['code_postal']} {row['commune']}
"""
        await update.message.reply_text(message)

# =========================
# LANCEMENT DU BOT
# =========================
download_csv()  # AJOUT
load_csv()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("lookup", lookup))

print("🚀 Bot lancé...")
app.run_polling(drop_pending_updates=True)
