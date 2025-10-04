# -*- coding: utf-8 -*-
# coding: utf-8

import time
from utils import card_utils, game_logic

def init_game(players):
    hands, community = card_utils.deal(len(players))
    st.session_state["game_state"] = {
        "players": players,
        "chips": {p: 10000 for p in players},
        "folded": {p: False for p in players},
        "pot": 0,
        "current_bet": 0,
        "turn_index": 0,
        "round": "preflop",
        "community": [],
        "hands": {p: hands[i] for i, p in enumerate(players)},
        "bet_this_round": {p: 0 for p in players},
        "full_community": community,
        "active": True
    }

def next_player():
    state = st.session_state["game_state"]
    players = state["players"]
    while True:
        state["turn_index"] = (state["turn_index"] + 1) % len(players)
        if not state["folded"][players[state["turn_index"]]]:
            break

def player_action(player, action, amount=0):
    s = st.session_state["game_state"]
    chips = s["chips"]
    pot = s["pot"]

    if action == "fold":
        s["folded"][player] = True
        st.toast(f"{player} 弃牌 ❌")

    elif action == "check":
        st.toast(f"{player} 让牌 ✅")

    elif action == "call":
        diff = s["current_bet"] - s["bet_this_round"][player]
        if diff > chips[player]:
            diff = chips[player]
        chips[player] -= diff
        s["pot"] += diff
        s["bet_this_round"][player] += diff
        st.toast(f"{player} 跟注 {s['current_bet']} 💵")

    elif action == "raise":
        diff = amount - s["bet_this_round"][player]
        if diff > chips[player]:
            diff = chips[player]
        chips[player] -= diff
        s["pot"] += diff
        s["current_bet"] = amount
        s["bet_this_round"][player] = amount
        st.toast(f"{player} 加注到 {amount} 💰")

    elif action == "allin":
        allin_amt = chips[player]
        chips[player] = 0
        s["pot"] += allin_amt
        s["bet_this_round"][player] += allin_amt
        st.toast(f"{player} 全下 ⚡️ {allin_amt}")
        if allin_amt > s["current_bet"]:
            s["current_bet"] = allin_amt

    next_player()

def next_round():
    """翻下一轮公共牌"""
    s = st.session_state["game_state"]
    if s["round"] == "preflop":
        s["community"] = s["full_community"][:3]
        s["round"] = "flop"
    elif s["round"] == "flop":
        s["community"] = s["full_community"][:4]
        s["round"] = "turn"
    elif s["round"] == "turn":
        s["community"] = s["full_community"][:5]
        s["round"] = "river"
    else:
        s["active"] = False
        determine_winner()

    # 重置每轮下注记录
    s["bet_this_round"] = {p: 0 for p in s["players"]}
    s["current_bet"] = 0
    s["turn_index"] = 0
    st.toast(f"进入下一轮：{s['round']}")

def determine_winner():
    """牌局结束：比牌"""
    s = st.session_state["game_state"]
    valid_players = [p for p in s["players"] if not s["folded"][p]]
    scores = {p: game_logic.best_hand(s["hands"][p] + s["community"]) for p in valid_players}
    winner = max(scores, key=scores.get)
    s["chips"][winner] += s["pot"]
    s["pot"] = 0
    s["winner"] = winner
    st.success(f"🎉 {winner} 获胜！赢得底池")
