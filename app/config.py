import discord
from discord.ext import commands,tasks
from discord import app_commands
import os
import random
import sys
import subprocess
import io
import re 
import requests
import pandas as pd
import json
import jsonlines
import ast
from datetime import datetime,timedelta

discord_bot_token = os.environ.get("DISCORD_BOT_TOKEN")

############################################
# openai API config 
############################################
import openai
import tiktoken
# Set up the OpenAI API. The key is stored as an environment variable for security reasons.
openai_model = 'gpt-4'
# Abide to token limit:
data_viz_completion_limit = 1500
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Used to generate datalle finetune data
async def generate_dataviz_finetune_data(interaction):

    from commands.datalle import finetune as finetune_datalle
    from commands.discord_interpreter import finetune as finetune_interpreter

    data = finetune_datalle.finetune + finetune_interpreter.finetune

    result = []
    
    for i in range(0, len(data), 2):
        if data[i]['role'] == 'user' and data[i+1]['role'] == 'assistant':
            result.append({'prompt': data[i]['content'], 'completion': data[i+1]['content']})
    
    filename = "commands/finetune.jsonl"
    
    with jsonlines.open(filename, 'w') as fl:
        for item in result:
            fl.write(item)
            
    await interaction.followup.send("DATALL-E finetune data generation complete",file=discord.File(filename))

############################################
# GIFY API config 
############################################
gify_api_token = os.environ.get("GIPHY_API_KEY")

############################################
# Youtube Data API config
############################################
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# Set up the Google Youtube Data API key. For youtube searching and playback.
google_api_key = os.environ.get("google_api_key")

# Set up the YouTube Data API client
youtube = build("youtube", "v3", developerKey=google_api_key)
