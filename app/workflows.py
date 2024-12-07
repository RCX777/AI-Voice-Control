from app.globals import cards

def disable_subscription(param: str):
    return "disabled subscription!!"

def activate_subscription(param: str):
    return 'activated subscription!!'

def remove_card_with_id(param: str):
    for card_id in cards.keys():
        if param in card_id:
            cards.pop(card_id)
            break
    print(cards)
    return f'removed card with {param}'

actions = [
    {'id': 0, 'desc': 'Disable subscription', 'func': disable_subscription},
    {'id': 1, 'desc': 'Activate subscription', 'func': activate_subscription},
    {'id': 2, 'desc': 'Remove card with given ID', 'func': remove_card_with_id},
]
