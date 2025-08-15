from agent import ActivityComment, DonBotto, DonBottoPlan, LineupItem, SellItem, TransferItem
from client import KickbaseClient
from typing import List

def main():
    don_botto = DonBotto()
    kickbase = KickbaseClient()
    plan: DonBottoPlan = don_botto.trigger()
    make_transfers(kickbase, plan.transfers)
    sell_players(kickbase, plan.sell)
    make_comments(kickbase, plan.activities)
    print_lineup(plan.lineup)

    if plan.strategy:
            print(f"[STRATEGY] {plan.strategy}")


def print_lineup(players: List[LineupItem]):
    print("===========LINE UP============")
    for player in players:
        print(player.lastname)

def make_transfers(kickbase: KickbaseClient, transfers: List[TransferItem]):
    for t in transfers:
        try:
            kickbase.market_api.place_an_offer(t.player_id, t.price)
            print(f"Offer placed: player={t.player_id}, price={t.price}")
        except Exception as e:
                    print(f"[ERROR] place_an_offer({t.player_id}, {t.price}): {e}")

def sell_players(kickbase: KickbaseClient, sell: List[SellItem]):
    for t in sell:
        try:
            kickbase.market_api.accept_kickbase_offer(t.player_id)
            print("Sold player to kickbase")
        except Exception as e:
                    print(f"[ERROR] sell/list player {t.player_id}: {e}")

def make_comments(kickbase: KickbaseClient, activities: List[ActivityComment]):
    for a in activities:
        try:
            kickbase.activities_api.send_feed_item_comment(a.activity_id, a.kommentar)
            print(f"Kommentar: {a.kommentar} getätigt")
        except Exception as e:
                    print(f"[ERROR] comment activity {a.activity_id}: {e}")




if __name__ == "__main__":
    main()
