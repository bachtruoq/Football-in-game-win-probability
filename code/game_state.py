import os
import pandas as pd
import json
import ast

pregame_data = pd.read_csv('pregame_data/pregame_data.csv')
for i in pregame_data.index:
    game_data = [{
        'timestamp' : 0,
        'half' : 1,
        'ht_elo': pregame_data['home_team_elo'][i],
        'at_elo' : pregame_data['away_team_elo'][i],
        'ht_goal' : 0,
        'at_goal' : 0,
        'pass' : 0,
        'short_pass' : 0,
        'long_pass' : 0,
        'final_3rd_pass' : 0,
        'key_pass' : 0,
        'cross' : 0,
        'corner' : 0,
        'big_chance' : 0,
        'shot' : 0,
        'shot_6_yard_box' : 0,
        'shot_penalty_box' : 0,
        'shot_open_play' : 0,
        'shot_fast_break' : 0,
        'dispossessed' : 0,
        'turnover' : 0,
        'duel' : 0,
        'tackle' : 0,
        'interception' : 0,
        'clearance' : 0,
        'offside' : 0,
        'yellow' : 0,
        'red' : 0,
        'result' : 'D'
    }]
    ht_id = pregame_data['home_team_id'][i]
    at_id = pregame_data['away_team_id'][i]
    event_data = pd.read_csv('event_data/'+str(pregame_data['match_id'][i])+'.csv')
    event_data['period'] = event_data['period'].apply(ast.literal_eval)
    event_data['type'] = event_data['type'].apply(ast.literal_eval)
    event_data['satisfiedEventsTypes'] = event_data['satisfiedEventsTypes'].apply(ast.literal_eval)
    for ind, event in event_data.iterrows():
        new_event = game_data[-1].copy()
        if pd.isnull(event['second']):
            event['second'] = 0
        new_event['timestamp'] = event['minute']*60 + event['second']
        new_event['half'] = event['period']['value']
        update = False
        if event['type']['value'] == 16:
            update = True
            if 23 in event['satisfiedEventsTypes']:
                if event['teamId'] == ht_id:
                    new_event['at_goal'] += 1
                else:
                    new_event['ht_goal'] += 1
            else:
                if event['teamId'] == ht_id:
                    new_event['ht_goal'] += 1
                else:
                    new_event['at_goal'] += 1
        if 117 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['pass'] += 1
            else:
                new_event['pass'] -= 1
        if 30 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['short_pass'] += 1
            else:
                new_event['short_pass'] -= 1
        if 127 in event['satisfiedEventsTypes'] or 128 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['long_pass'] += 1
            else:
                new_event['long_pass'] -= 1
        if 217 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['final_3rd_pass'] += 1
            else:
                new_event['final_3rd_pass'] -= 1
        if 123 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['key_pass'] += 1
            else:
                new_event['key_pass'] -= 1
        if 125 in event['satisfiedEventsTypes'] or 126 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['cross'] += 1
            else:
                new_event['cross'] -= 1
        if 31 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['corner'] += 1
            else:
                new_event['corner'] -= 1
        if 203 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['big_chance'] += 1
            else:
                new_event['big_chance'] -= 1
        if 10 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['shot'] += 1
            else:
                new_event['shot'] -= 1
        if 0 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['shot_6_yard_box'] += 1
            else:
                new_event['shot_6_yard_box'] -= 1
        if 1 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['shot_penalty_box'] += 1
            else:
                new_event['shot_penalty_box'] -= 1
        if 3 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['shot_open_play'] += 1
            else:
                new_event['shot_open_play'] -= 1
        if 4 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['shot_fast_break'] += 1
            else:
                new_event['shot_fast_break'] -= 1
        if 70 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['dispossessed'] += 1
            else:
                new_event['dispossessed'] -= 1
        if 69 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['turnover'] += 1
            else:
                new_event['turnover'] -= 1
        if 197 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['duel'] += 1
            else:
                new_event['duel'] -= 1
        if 143 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['tackle'] += 1
            else:
                new_event['tackle'] -= 1
        if 101 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['interception'] += 1
            else:
                new_event['interception'] -= 1
        if 95 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['clearance'] += 1
            else:
                new_event['clearance'] -= 1
        if 61 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['offside'] += 1
            else:
                new_event['offside'] -= 1
        if 65 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['yellow'] += 1
            else:
                new_event['yellow'] -= 1
        if 68 in event['satisfiedEventsTypes']:
            update = True
            if event['teamId'] == ht_id:
                new_event['red'] += 1
            else:
                new_event['red'] -= 1
        if update: game_data.append(new_event)
    df = pd.DataFrame(game_data)
    diff = game_data[-1]['ht_goal'] - game_data[-1]['at_goal']    
    if diff > 0:
        df['result'] = 'W'
    elif diff < 0:
        df['result'] = 'L'
    df.to_csv('data/'+str(pregame_data['match_id'][i])+'.csv', index=False)
    with open('data/data.csv', 'a') as f:
        df.to_csv(f, header=f.tell()==0, index=False)