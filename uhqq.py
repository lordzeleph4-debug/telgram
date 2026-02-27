import csv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIG
# =========================
TOKEN = "8752436181:AAGRBzSlm-sSgL8CQMIRbScbReImpGj5eJo"  # Remplace par ton token
CSV_FILE = "caf.csv"

# Mode discret (désactive logs)
logging.basicConfig(level=logging.CRITICAL)

# =========================
# CHARGEMENT RAPIDE
# =========================
DATA = []

def load_csv():
    global DATA
    with open(CSV_FILE, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Champ recherche optimisé
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
    message = """
👋 Bonjour et bienvenue sur **le Bot Recherche CSV** !

Ce bot te permet de rechercher facilement des informations dans le fichier `caf.csv`.

━━━━━━━━━━━━━━━━━━
🔎 QUE PEUT-IL FAIRE ?
━━━━━━━━━━━━━━━━━━
• Recherche dans TOUTES les colonnes : nom, prénom, email, téléphone, adresse…
• Recherche multi-mots intelligente
• Insensible à la casse

━━━━━━━━━━━━━━━━━━
📌 COMMANDES PRINCIPALES
━━━━━━━━━━━━━━━━━━
/lookup <mots clés> → Recherche intelligente
/help               → Affiche l’aide complète

━━━━━━━━━━━━━━━━━━
🧠 ASTUCE
━━━━━━━━━━━━━━━━━━
Tu peux taper juste un nom, un prénom, un code postal ou même un email :
Exemples : 
/lookup jean dupont
/lookup dupont
/lookup 75001
/lookup jean.dupont@gmail.com

━━━━━━━━━━━━━━━━━━
🚀 CONSEIL
━━━━━━━━━━━━━━━━━━
Le bot limite l’affichage à 15 résultats pour ne pas spammer.
Si besoin, fais plusieurs recherches plus ciblées.
"""
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
📖 AIDE COMPLÈTE — Bot Recherche CSV

━━━━━━━━━━━━━━━━━━
🤖 DESCRIPTION
━━━━━━━━━━━━━━━━━━
Ce bot permet de rechercher des informations dans le fichier caf.csv.

La recherche est intelligente :
• Insensible aux majuscules/minuscules
• Recherche dans TOUTES les colonnes
• Support multi-mots
• Peu importe l'ordre des mots

━━━━━━━━━━━━━━━━━━
🔎 UTILISATION
━━━━━━━━━━━━━━━━━━
Commande principale :

/lookup <mots clés>

━━━━━━━━━━━━━━━━━━
🧠 EXEMPLES RÉELS
━━━━━━━━━━━━━━━━━━
Recherche prénom + nom :
/lookup jean dupont

Recherche par nom uniquement :
/lookup dupont

Recherche par code postal :
/lookup 75001

Recherche par email :
/lookup jean.dupont@gmail.com

Recherche combinée :
/lookup dupont 75001

━━━━━━━━━━━━━━━━━━
📂 CHAMPS RECHERCHÉS
━━━━━━━━━━━━━━━━━━
• ID
• Nom
• Prénom
• Date de naissance
• Email
• Téléphone
• Adresse
• Code postal
• Commune

━━━━━━━━━━━━━━━━━━
⚡ PERFORMANCE
━━━━━━━━━━━━━━━━━━
Le fichier est chargé en mémoire au démarrage.
Les recherches sont instantanées.

━━━━━━━━━━━━━━━━━━
ℹ️ AUTRES COMMANDES
━━━━━━━━━━━━━━━━━━
/start → Message d'accueil
/help  → Afficher cette aide
"""
    await update.message.reply_text(message)


async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Utilisation : /lookup noe roubaud")
        return

    words = [w.lower() for w in context.args]
    results = search_smart(words)

    if not results:
        await update.message.reply_text("🔎 Aucun résultat trouvé.")
        return

    for row in results[:15]:  # limite anti-spam
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
load_csv()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("lookup", lookup))

print("🚀 Bot lancé...")
app.run_polling(drop_pending_updates=True)