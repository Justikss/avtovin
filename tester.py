a = ['6', '8']
active_non_confirm_offers = {'4072': '4:5:6', '4514': '6:8'}
b = need_message_id = next((key for key, value in active_non_confirm_offers.items() if value == ':'.join(a)), None)

print(b)