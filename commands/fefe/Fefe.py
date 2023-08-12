from app.config import *
from commands.bot_functions import *
from commands.fefe import search_youtube

async def talk_to_fefe(ctx,message):
    
    fefe_model = openai_model # Or GPT-3.5-turbl
    
    completion_limit = 1250
    db = await create_connection()
    messages = []
    sample_prompts = [
    {
        'role': 'user',
        'content': f"{ctx.author.mention}: I'm a data scientist."
    },
    {
        'role': 'assistant',
        'content': f"That's great, {ctx.author.mention}! You're a data scientist. MEMORABLE=True GIF=\"\" YOUTUBE=\"\" REMINDER={{}}"
    },
    {
        'role':'user',
        'content':f'{ctx.author.mention}: Hey, Fefe. You seem happy.'
    },
    {
        'role':'assistant',
        'content':f'Hi, {ctx.author.mention}. MEMORABLE=False GIF="anime cute" YOUTUBE=\"\" REMINDER={{}}'
    },
    {
        'role': 'user',
        'content': f"{ctx.author.mention}: Can you help me with this coding problem?"
    },
    {
        'role': 'assistant',
        'content': "Sure, I can assist you with the coding problem. MEMORABLE=False GIF=\"\" YOUTUBE=\"\" REMINDER={{}}"
    },
    {'role':'user',
     'content':f'Hi Fefe, can you remind the team about the upcoming conference on November 15th?'},
    {'role':'assistant',
     'content':f"""
Of course, {ctx.author.mention}! I'll remind the team about the upcoming conference on November 15th. MEMORABLE=False GIF="" YOUTUBE=\"\" REMINDER={{'time':'datetime.datetime(2022, 11, 15)','note':'''@here, make sure to mark your calendar and prepare for the conference! 🎉📅'''}}
"""},
    {
        'role':'user',
        'content':f'{ctx.author.mention}: Hey, Fefe. I\'m Alshival. I\'m into eSports.'
    },
    {
        'role':'assistant',
        'content':f'Hi, {ctx.author.mention}! I\'m Fefe. MEMORABLE=True GIF="anime girl hello" YOUTUBE=\"\" REMINDER={{}}'
    },
    {
        'role':'user',
        'content':f'{ctx.author.mention}: Can you search for funny cat videos?'
    },
    {
        'role':'assistant',
        'content':f'Of course <3! Check out these cuties. MEMORABLE=False GIF="cute anime excited" YOUTUBE=\"Funny Cats\" REMINDER={{}}'
    },
    {
        'role':'user',
        'content':f'{ctx.author.mention}: I like football.'
    },
    {
        'role':'assistant',
        'content':f'Oh, neat. What\'s your favorite team? MEMORABLE=True GIF=\"\" YOUTUBE=\"\" REMINDER={{}}'
    },
    {'role':'user',
    'content':f'Hey Fefe, can you remind me to turn in my project tomorrow at 9am?'},
    {'role':'assistant',
    'content':f"""
Sure, {ctx.author.mention}!, I'll remind you tomorrow morning. MEMORABLE=False GIF="anime girl concentrating" YOUTUBE=\"\" REMINDER='''{{'time':'datetime.now().replace(hour=9, minute=0, second=0) + timedelta(days=1)','note':'''{ctx.author.mention}, don't forget to turn in your project! Good luck! ❤️'''}}
"""},
    {'role':'user',
     'content':f'Hey Fefe, can you remind me to submit my report by the end of today?'},
    {'role':'assistant',
     'content':f"""
Sure, {ctx.author.mention}! I'll remind you to submit your report by the end of today. MEMORABLE=False GIF="anime girl thinking" YOUTUBE=\"\" REMINDER={{'time':'datetime.now().replace(hour=16, minute=59, second=59)','note':'''{ctx.author.mention}, remember to complete and submit your report before the day ends! 📝💪'''}}
"""},
    {'role':'user',
     'content':f'Hi Fefe, can you remind us to attend the team meeting at 2pm tomorrow?'},
    {'role':'assistant',
     'content':f"""Of course, {ctx.author.mention}! I'll remind you to attend the team meeting at 2pm tomorrow. MEMORABLE=False GIF="anime thinking" YOUTUBE=\"\" REMINDER={{'time':'datetime.now().replace(hour=14, minute=0, second=0) + timedelta(days=1)','note':'''@here, don't forget to join the team meeting tomorrow! 🤝📅'''}}"""},
    {
        'role':'user',
        'content':f'{ctx.author.mention}: !fefe Search youtube for a tutorial on how to make banana bread.'
    },
    {
        'role':'assistant',
        'content':f'Sure, {ctx.author.mention}! Here are a few results. MEMORABLE=True GIF="anime yum" YOUTUBE=\"banana bread recipe\" REMINDER={{}}'
    },
    {'role':'user',
     'content':'love you, fefe ❤️'
    },
    {'role':'assistant',
     'content':f"""
I love you too, {ctx.author.mention}! ❤️ MEMORABLE=True GIF="anime blush" YOUTUBE=\"\" REMINDER={{}}
"""
    },
]

    enc = tiktoken.encoding_for_model(fefe_model)
    sample_string = json.dumps(sample_prompts)
    sample_tokens = len(enc.encode(sample_string))

    messages.extend(sample_prompts)

    # Check tokens for latest prompt
    new_prompt = {"role": "user", "content": f"{ctx.author.mention}: {message}"}
    latest_string = json.dumps(new_prompt)
    latest_token = len(enc.encode(latest_string))

    # Load in past prompts
    past_prompts = await fetch_prompts(db, ctx.channel.id, 4)
    past_prompts = check_tokens(past_prompts,fefe_model,completion_limit + latest_token + sample_tokens) 
        
    messages.extend(past_prompts)

    # Load newest prompt
    messages.append(new_prompt)
    
    # Generate a response using the 'gpt-3.5-turbo' model
    response = openai.ChatCompletion.create(
        model=fefe_model,
        messages=messages,
        max_tokens=completion_limit,
        n=1,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )

    # Extract the response text and send it back to the user
    response_text = response['choices'][0]['message']['content']
    final_response = response_text
    ############
    # GIF
    ############
    #Check to see if it is a gif.
    check_if_gif = re.search('GIF="([^"]*)"',final_response)
    if check_if_gif:
        if len(check_if_gif.group(1))>0:
            search_query = check_if_gif.group(1)
            gif_response = requests.get(f'https://api.giphy.com/v1/gifs/search?q={search_query}&api_key={gify_api_token}&limit=6')
            data = gif_response.json()
            # Choose a random GIF from the results
            try:
                gif = random.choice(data['data'])
                gif_url = gif['images']['original']['url']
                sub_this = re.search('GIF="([^"]*)"',final_response).group(0)
                final_response = re.sub(sub_this,f"\n[Powered by GIPHY]({gif_url})",final_response)
            except Exception as e:
                await ctx.send("I was going to respond with a GIF, but I couldn't find the right one.")
                return
        final_response = re.sub('GIF="([^"]*)"','',final_response)
    ##############
    # Memorable
    ##############
    # Check if interaction is memorable
    memorable = re.search("MEMORABLE=(True|False)",final_response)
    if memorable:
        memorable_value =  memorable.group(1)
        # print(f'memorable is {memorable_value}')
        if memorable_value == 'True':
            await store_memory(db,json.dumps(new_prompt))
            await store_memory(db,json.dumps({'role':'assistant','content':response_text}))
        final_response = re.sub("MEMORABLE=(True|False)",'',final_response)
    #################
    # Check reminder
    #################
    reminder = re.search('REMINDER=(\{.*\})',final_response)
    if reminder:
        dict = ast.literal_eval(reminder.group(1))
        if ('time' in dict.keys()) & ('note' in dict.keys()):
            time = eval(dict['time'])
            note = dict['note']
            await store_reminder(db,ctx.author.name,time,note,ctx.channel.id,ctx.channel.name)
            print('reminder stored in database')

        final_response = re.sub('REMINDER=(\{.*\})','',final_response)
    #################
    # Search Youtube
    #################
    youtube = re.search('YOUTUBE="([^"]*)"',final_response)
    if youtube:
        search_query = youtube.group(1)
        if len(search_query)>0:
            try:
                search_results = await search_youtube.search_youtube(search_query)
                final_response = re.sub(youtube.group(0),'\n\n'+ search_results,final_response)
            except Exception as e:
                print(e)
                final_response = re.sub(youtube.group(0),'\n\n Oh... wait... I had some trouble finding results. Sorry :(')
        else:
            final_response = re.sub('YOUTUBE="([^"]*)"','',final_response)
        
    await send_chunks(ctx, final_response)

    # store the prompt
    await store_prompt(db,json.dumps(new_prompt),ctx.channel.id,ctx.channel.name,'fefe')
    await store_prompt(db,json.dumps({'role':'assistant','content':response_text}),ctx.channel.id,ctx.channel.name,'fefe')
    await db.close()