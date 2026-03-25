from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import GameSession, Decision
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def game_view(request):
    return render(request, 'game/index.html')

def clamp(x):
    return max(0, min(100, x))


def calculate_round1(choice, kpis, v):
    R, E, S, B, T, P, A = v["R"], v["E"], v["S"], v["B"], v["T"], v["P"], v["A"]

    Bn = (B - 1) / 4

    # base
    F_base = -0.02*R - 0.05*E - 0.04*S - 3*Bn - 0.03*T - 1.5*P - 0.06*A
    G_base = 0.08*R + 0.12*E + 0.10*S - Bn
    H_base = 0.10*T + 1.2*P + 0.02*A
    Re_base = 0.015*R + 0.04*E + 0.015*S + 10*Bn + 0.04*T + 0.5*P + 0.05*A
    D_base = 0.02*E + 0.02*S + 0.025*T + 0.12*A

    # option
    if choice == "A":
        F_opt, G_opt, H_opt, Re_opt, D_opt = -6, 2, 12, 8, 4
    elif choice == "B":
        F_opt, G_opt, H_opt, Re_opt, D_opt = -12, 1, 4, 5, 14
    else:
        F_opt, G_opt, H_opt, Re_opt, D_opt = -8, 0, 8, 6, 10

    return {
        "financial": clamp(kpis["financial"] + F_base + F_opt),
        "green": clamp(kpis["green"] + G_base + G_opt),
        "human": clamp(kpis["human"] + H_base + H_opt),
        "resilience": clamp(kpis["resilience"] + Re_base + Re_opt),
        "digital": clamp(kpis["digital"] + D_base + D_opt),
    }

def calculate_round1(choice, kpis, variables):
    kpis["human"] += 10
    kpis["green"] += 2
    return kpis


def calculate_round2(choice, kpis, variables):
    kpis["green"] += 15
    kpis["digital"] += 10
    return kpis


def calculate_round3(choice, kpis, variables):
    kpis["resilience"] += 20
    return kpis


def calculate_round4(choice, kpis, variables):
    kpis["green"] += 25
    kpis["resilience"] += 10
    return kpis


@csrf_exempt
def process_decision(request):
    if request.method == "POST":
        data = json.loads(request.body)

        round_number = data["round"]
        choice = data["choice"]
        kpis = data["kpis"]
        cash = data["cash"]
        variables = data["variables"]

        #  CORRECT FORMULA PER ROUND
        if round_number == 1:
            new_kpis = calculate_round1(choice, kpis, variables)
            cash -= 100000

        elif round_number == 2:
            new_kpis = calculate_round2(choice, kpis, variables)
            cash -= 120000

        elif round_number == 3:
            new_kpis = calculate_round3(choice, kpis, variables)
            cash -= 80000

        elif round_number == 4:
            new_kpis = calculate_round4(choice, kpis, variables)
            cash -= 90000

        # ✅ LIMIT VALUES
        for key in new_kpis:
            new_kpis[key] = max(0, min(100, new_kpis[key]))

        # ✅ SAVE GAME SESSION
        game = GameSession.objects.create(
            cash=cash,
            financial=new_kpis["financial"],
            human=new_kpis["human"],
            green=new_kpis["green"],
            resilience=new_kpis["resilience"],
            digital=new_kpis["digital"]
        )

        # ✅ SAVE DECISION CORRECTLY
        Decision.objects.create(
            game=game,
            round_number=round_number,   # ✅ FIXED
            choice=choice,
            **variables
        )

        return JsonResponse({
            "kpis": new_kpis,
            "cash": cash,
            "next_round": round_number + 1
        })