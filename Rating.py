import discord
from discord.ext import commands
import json
import os

# インテント設定
intents = discord.Intents.default()
intents.message_content = True

# Botの初期設定
bot = commands.Bot(command_prefix="!", intents=intents)

# ユーザーのレートを保存する辞書
user_ratings = {}

# レートデータを保存するファイル名
RATING_FILE = "user_ratings.json"

# データをファイルに保存する関数
def save_ratings():
    with open(RATING_FILE, "w") as file:
        json.dump(user_ratings, file)

# データをファイルから読み込む関数
def load_ratings():
    global user_ratings
    if os.path.exists(RATING_FILE):
        with open(RATING_FILE, "r") as file:
            user_ratings = json.load(file)

# Botが起動したときの処理
@bot.event
async def on_ready():
    load_ratings()  # 起動時にレートデータを読み込む
    print(f'Botがログインしました: {bot.user}')

# `!res`コマンドで全ユーザーのレートを表示する
@bot.command()
async def res(ctx):
    if not user_ratings:
        await ctx.send("現在、登録されているユーザーはいません。")
        return

    # 各ユーザーのレートをフォーマットして表示
    result = "登録されている全ユーザーのレート:\n"
    for user, rating in user_ratings.items():
        result += f"{user}: {rating}\n"
    await ctx.send(result)

# テスト用のユーザー追加コマンド（例えば、初期レートを1000に設定する）
@bot.command()
async def add_user(ctx, username: str):
    if username in user_ratings:
        await ctx.send(f"{username} は既に登録されています。")
    else:
        user_ratings[username] = 1000  # 初期レートを1000に設定
        save_ratings()
        await ctx.send(f"{username} を追加しました。初期レートは 1000 です。")

# Botのトークンを使って起動
bot.run("MY_BOT_TOKEN")
