import discord
from discord.ext import commands
import os

# インテントとBotのコマンドプレフィックス設定
intents = discord.Intents.default()
intents.message_content = True  # discord.py v2.xではメッセージを受け取るのに必要
intents.members = True  # メンバー関連のイベントを受け取るのに必要

bot = commands.Bot(command_prefix='!', intents=intents)

# 正しいパスワード (この例では 'secret_password')
CORRECT_PASSWORD = "secret_password"

# helloコマンド
@bot.command()
async def hello(ctx):
    await ctx.send('我が君')

# ユーザーをBANするコマンド（!avadaで実行）
@bot.command(name='avada')
async def avada(ctx, member: discord.Member, *, reason=None):
    # パスワードを要求するメッセージを送信
    try:
        await ctx.author.send('アバダケダブラを実行するにはパスワードを入力してください。')

        # パスワードの応答を待つ
        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
        
        password_message = await bot.wait_for('message', check=check)

        # パスワードが正しいか確認
        if password_message.content == CORRECT_PASSWORD:
            # パスワードが正しい場合、ユーザーをBAN
            await member.ban(reason=reason)
            await ctx.send(f'アバタケダブラー！ {member}')

            # 音声ファイルを再生
            if ctx.author.voice:  # コマンドを実行したユーザーがボイスチャンネルに接続しているか確認
                channel = ctx.author.voice.channel  # ボイスチャンネルを取得
                voice_client = await channel.connect()  # ボイスチャンネルに接続

                # 任意の音声ファイルを再生 (例: "ban_sound.mp3")
                audio_source = discord.FFmpegPCMAudio('ban_sound.mp3')
                if not voice_client.is_playing():
                    voice_client.play(audio_source)

                # 音声が終了後、ボイスチャンネルから切断
                while voice_client.is_playing():
                    await discord.utils.sleep_until(2)  # 再生中は待機
                await voice_client.disconnect()

        else:
            # パスワードが間違っている場合
            await ctx.author.send('パスワードが間違っています。BANはキャンセルされました。')

    except discord.Forbidden:
        await ctx.send('DMを送信できませんでした。ユーザーのDMが無効化されている可能性があります。')
    except Exception as e:
        await ctx.send(f'エラーが発生しました: {e}')

# Botをトークンで起動
bot.run('YOUR_BOT_TOKEN')
