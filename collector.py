import time
def build_all_in_one_payload(cid):
 return {"system_name": "Bottrend", "cycle_id": cid, "timestamp": int(time.time()), "market_overview": {"btc_price": 81644.40}}