import discord
from discord.ext import commands
import random
import colorama
from colorama import Fore
import time
import os


# Token du bot Discord
Token_bot_discord = os.getenv('TOKEN_BOT_DISCORD', 'votre_token_ici')

# Initialisation de Colorama pour la coloration des sorties dans le terminal
colorama.init(autoreset=True)

# Configuration des intents pour le bot Discord
intents_var = discord.Intents.default()
intents_var.message_content = True
bot = commands.Bot(command_prefix='disroll_', intents = intents_var)

# Initialisation des variables globales
synced = []
bot_start_time = None


@bot.event
async def on_ready():
    global bot_start_time, synced
    bot_start_time = time.time()
    print(Fore.GREEN + f"Bot connecté en tant que {bot.user.name} (ID: {bot.user.id})")

    try:
        synced = await bot.tree.sync()
        
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la synchronisation des commandes : {e}")
        inp_user = input(Fore.RED + "Réessayer la synchronisation des commandes ? (oui/non/stop_bot) :")
        if inp_user.lower() == "oui":
            try:
                synced = await bot.tree.sync()
            except Exception as e:
                print(Fore.RED + f"Erreur lors de la synchronisation des commandes : {e}\nSynchronisation des commandes annulée. Le bot continuera à fonctionner sans synchronisation.")
        elif inp_user.lower() == "stop_bot":
            print(Fore.YELLOW + "Arrêt du bot...")
            bot.loop.stop()
        else:
            print(Fore.RED + "Synchronisation des commandes annulée. Le bot continuera à fonctionner sans synchronisation.")

    print(Fore.GREEN + f"Bot prêt à recevoir des commandes.\nTemps de démarrage du bot : {time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(bot_start_time))}")
    await bot.change_presence(activity=discord.Game(name="lance des dés"))
    print(Fore.GREEN + "Présence du bot définie sur 'lance des dés'.")
    print("------")

# Commande slash
@bot.tree.command()
async def time_bot_use(interaction: discord.Interaction):
    current_time = time.time() # Obtenir le temps actuel en secondes depuis l'époque (timestamp)
    uptime_seconds = int(current_time - bot_start_time) # Calculer le temps de fonctionnement du bot en secondes en soustrayant du temps de démarrage

    days = uptime_seconds // (24 * 3600) # Calculer le nombre de jours
    hours = (uptime_seconds % (24 * 3600)) // 3600 # Calculer le nombre d'heures
    minutes = (uptime_seconds % 3600) // 60 # Calculer le nombre de minutes
    seconds = uptime_seconds % 60 # Calculer le nombre de secondes restantes
    
    embed = discord.Embed(
        title="Temps de fonctionnement du Bot depuis le dernier démarrage",
        description=f"Le bot est en ligne depuis {days} jours, {hours} heures, {minutes} minutes et {seconds} seconds.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.command(
    name="roll",
    description="Lance des dés selon le format 'XdY' (X dés à Y faces).",
    help="Utilisez cette commande pour lancer des dés. Par exemple, 'disroll_2d6' lance 2 dés à 6 faces.",
    aliases=["lancer", "dice"],
    hide_help=True,
)
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(f"Résultat du lancer de dés {dice}: {result}")
    except ValueError:
        await ctx.send("Format incorrect. Utilisez la syntaxe 'XdY' où X est le nombre de dés et Y est le nombre de faces.")


# Fonction principale pour démarrer le bot
def main():
    bot.run(Token_bot_discord)


# Fonction principale pour démarrer le bot
if __name__ == "__main__":
    print(Fore.GREEN + "Démarrage du bot...")
    main()