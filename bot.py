import os
import requests
from telegram import Bot
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_1 = int(os.getenv("CHAT_ID"))
CHAT_ID_2 = int(os.getenv("CHAT_ID2"))  
API_KEY = os.getenv("FOOTBALL_API_KEY")

MY_TEAMS_IDS = {
    "3kq9cckrnlogidldtdie2fkbl",   # Real Madrid
    "apoawtpvac4zqlancmvw4nk4o",   # Bayern Munich
    "8lroq0cbhdxj8124qtxwrhvmm",   # Fenerbahce
    "c9swyor08g9pedxpe3n321svu",   # Al Hilal
    "57jcqe38hakh2hfit2zsogsb",    # Al Nassr
    "9q0arba2kbnywth8bkxlhgmdr",   # Chelsea
    "3vo5mpj7catp66nrwwqiuhuup",   # Inter
    "agh9ifb2mw3ivjusgedj7c3fe"    # Barcelona
    "d5m6k7n8p9q0r1s2t3u4v5w6x",  # Galatasaray
    "y7z8a9b0c1d2e3f4g5h6i7j8k"   # Roma
}

LEAGUE_FLAGS = {
    "LaLiga": "🇸",
    "Premier League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Bundesliga": "🇩🇪",
    "Serie A": "🇮🇹",
    "Ligue 1": "🇫🇷",
    "Super Lig": "🇹",
    "Saudi Pro League": "🇦",
    "Champions League": "🏆",
    "Europa League": "🇪🇺"
}

def convert_to_msk(utc_time_str):
    try:
        utc_time = datetime.strptime(utc_time_str, "%H:%M")
        msk_time = utc_time + timedelta(hours=3)
        return msk_time.strftime("%H:%M")
    except:
        return utc_time_str

def get_matches_for_today():
    today_obj = datetime.now()
    today = today_obj.strftime('%Y-%m-%d')
    date_display = today_obj.strftime('%d %B') 
    
    url = f"https://live-football-api.com/api/v1/matches?api_key={API_KEY}&date={today}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if not data.get('success'):
            return None, date_display
            
        all_matches = data['data']['matches']
        league_matches = defaultdict(list)
        
        for match in all_matches:
            home_id = match['home']['id']
            away_id = match['away']['id']
            
            if home_id in MY_TEAMS_IDS or away_id in MY_TEAMS_IDS:
                league_name = match['league']['name']
                home_name = match['home']['name']
                away_name = match['away']['name']
                kickoff = convert_to_msk(match['kickoff'])
                
                flag = LEAGUE_FLAGS.get(league_name, "🌍")
                
                match_line = f"{home_name} vs {away_name} • {kickoff}"
                league_matches[league_name].append((flag, match_line))
                
        return dict(league_matches) if league_matches else None, date_display
        
    except Exception as e:
        print(f"Error: {e}")
        return None, date_display

async def send_schedule():
    bot = Bot(token=TOKEN)
    matches_by_league, date_str = get_matches_for_today()
    
    if matches_by_league:
        text = f"📅 <b>Schedule for {date_str} (MSK):</b>\n\n"
        
        for league, matches in matches_by_league.items():
            flag = matches[0][0] 
            text += f"{flag} <b>{league}</b>\n"
            for _, match_line in matches:
                text += f"  • {match_line}\n"
            text += "\n"
    else:
        text = f"📅 No matches for our teams on {date_str}."

    for chat_id in [CHAT_ID_1, CHAT_ID_2]:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')

if __name__ == "__main__":
    asyncio.run(send_schedule())
