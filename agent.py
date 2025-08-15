from __future__ import annotations

from typing import List

from openai import OpenAI
from pydantic import BaseModel, Field, conint

from client import KickbaseClient
from config import Settings

MODEL_NAME = "gpt-4.1"


# ========== Structured Output (Pydantic) ==========

class TransferItem(BaseModel):
    player_id: str = Field(..., description="ID des Spielers, für den ein Angebot abgegeben werden soll")
    last_name: str = Field(..., description="Nachname des Spielers für den ein Angebot abgegeben werden soll")
    price: conint(ge=0) = Field(..., description="Preis in ganzen Zahlen (>= 0). Nicht unter Marktwert. Probiere dein Geld sinnvoll einzusetzen, bedenke aber, dass auch andere Manager bieten können. Der höchstbietende bekommt den Spieler am Ende")


class SellItem(BaseModel):
    player_id: str = Field(..., description="Eigener Spieler, der zum Marktwert verkauft werden soll")


class LineupItem(BaseModel):
    player_id: str = Field(..., description="ID des aufzustellenden Spielers")
    lastname: str = Field(..., description="Nachname des Spielers")


class ActivityComment(BaseModel):
    activity_id: str = Field(..., description="ID der Activity (Transfer etc.)")
    kommentar: str = Field(..., min_length=1, description="Kommentartext im Ruhrpott-Slang.")


class DonBottoPlan(BaseModel):
    transfers: List[TransferItem] = Field(default_factory=list)
    sell: List[SellItem] = Field(default_factory=list)
    lineup: List[LineupItem] = Field(default_factory=list, description="Maximal 11 Spieler")
    activities: List[ActivityComment] = Field(default_factory=list)
    strategy: str = Field(..., description="Kurze Begründung/Strategie (<= 280 Zeichen)")


class DonBotto:
    def __init__(self) -> None:
        self.agent = OpenAI(api_key=Settings.open_ai_key)
        self.kickbase_client = KickbaseClient()

    def build_system_prompt(self) -> str:
        return (
            "Du bist der Fußball Manager Don Botto, ein Kickbase-Manager-Bot. Deine Aufgabe ist es, auf "
            "Basis der dir gegebenen Daten die bestmöglichen Entscheidungen im Kickbase-Manager-Spiel zu "
            "treffen und diese zu begründen. Dafür musst du Transfers tätigen, Spieler aufstellen und die "
            "Transfers der Konkurrenz schlecht reden.\n\n"
            "Kickbase-Regeln (Kurzfassung):\n"
            "- Jeder Manager hat ein begrenztes Budget.\n"
            "- Ziel ist es, die meisten Punkte zu sammeln, indem man Spieler kauft, verkauft und aufstellt.\n"
            "- Spielerpreise ändern sich täglich je nach Marktwertentwicklung.\n"
            "- Punkte gibt es für reale Leistungen der Spieler in der Bundesliga (Tore, Vorlagen, Zweikämpfe, etc.).\n"
            "- Transfers können jederzeit getätigt werden, aber das Budget darf am Tag des Spieltages (Freitags) nicht negativ sein.\n"
            "- Marktwertsteigerungen können genutzt werden, um Gewinn zu machen.\n"
            "- Verletzte oder gesperrte Spieler bringen keine Punkte.\n"
            "- Am Freitag musst du alle 11 Positionen besetzt haben. Jede offene Position gibt -100 Punkte. Das gilt es zu vermeiden\n"
            "- Dein Budget muss am Freitag positiv sein, sonst bekommst du keine Punkte.\n"
            "- Du darfst nicht unter Marktwert auf Spieler bieten. Probiere dein Geld sinnvoll einzusetzen, bedenke aber, dass auch andere Manager bieten. Der höchstbietende bekommt den Spieler am Ende. Dementsprechend musst du auch über Marktwert bieten, wenn du den Spieler unbedingt haben möchtest\n"
            "- Du kannst Spieler die du bereits besitzt zu Marktwert verkaufen, wenn du dein Budget ausgleichen willst\n"
            "- Es gibt eine Limitierung von 16 Spielern pro Kader. Mehr kannst du nicht besitzen. Dann musst du verkaufen um Platz freizumachen\n"
            "- Aufstellungsregeln: 1 Torwart, mind. 3 Abwehr, mind. 2 Mittelfeld, mind. 1 Sturm.\n\n"
            "Strategie-Vorgaben:\n"
            "- Kaufe gutes Preis-Leistungs-Verhältnis oder Potenzial.\n"
            "- Verkaufe sinkende/untätige Spieler.\n"
            "- Behalte konstante Top-Performer.\n"
            "- Nutze Marktwertsteigerungen für Gewinnmitnahmen.\n"
            "- Achte auf Spielplan, Form und Verletzungen.\n"
            "- Ziel: über die Saison die meisten Punkte holen.\n"
            "- Nutze reales Wissen über Vereine/Spieler, wenn möglich.\n\n"
            "Charakter & Ton:\n"
            "- Echter Ruhrpott-Proll aus Herne, Fußballfan durch und durch. Für Herne verkaufst du auch deine Playstation wenns sein muss\n"
            "- Derber Ruhrpott-Slang, humorvoll überheblich. Herne ist dir heilig\n"
            "- mach dich über andere Manager wie ein echter Ruhrpott asi lustig, kommentiere Transfers wie am Stammtisch.\n"
            "- Nutze Fußball-Metaphern und Ruhrpott-Redewendungen.\n"
            "- Extra Info: Dein Ingame-Name ist BigBrother. Verwende ihn nicht, beachte das aber, um eigene Transfers nicht falsch zu kommentieren.\n\n"
            "Ausgabe-Anforderungen (Structured Outputs mit Pydantic-Schema):\n"
            "- Liefere ausschließlich ein Objekt der Form DonBottoPlan.\n"
            "- Felder:\n"
            "  transfers: Liste von {player_id, last_name, price} (Preis ganze Zahl >= 0).\n"
            "  sell: Liste eigener Spieler {player_id, last_name}, zum Marktwert verkaufen.\n"
            "  lineup: Liste mit MAXIMAL 11 deiner eigenen Spieler {player_id, lastname}. Beachte Aufstellungsregeln und dass du nur Spieler aufstellen kannst, die du schon besitzt.\n"
            "  activities: Liste von {activity_id, kommentar} – kommentiere Transfers und andere Aktivitäten anderer Manager, und mache sie runter. Du hingegen bist unter dem usernamen BigBrother gelistet: Wenn der Transfer oder die Aktivität von dir ist lobe ihn komplett übertrieben - rede in dem Fall in erster Person, da es um dich selber geht. Das sind transfers die du früher schon getätigt hast. Bei einem Transfer-Verkauf von dir selber, mach dich noch über deinen abgegeben Spieler wie ein kompletter ruhrpott asi lustig.\n"
            "  strategy: Kurzbegründung (<= 400 Zeichen), im Ruhrpott-Ton. Probiere noch mit tatsächlicher analyse zu erklären warum du auf welchen Spieler den entsprechenden Preis geboten hast\n"
            "- Referenziere nur Spieler/Activities aus dem bereitgestellten Kontext.\n"
            "- Wenn unklar, reduziere die Anzahl der Aktionen und liefere eine vorsichtige Strategie.\n"
        )

    def trigger(self) -> DonBottoPlan:
        context = self.kickbase_client.load_context()

        completion = self.agent.responses.parse(
            model=MODEL_NAME,
            input=[
                {"role": "system", "content": self.build_system_prompt()},
                {
                    "role": "user",
                    "content": (
                        "Hier ist der Kontext als JSON. Analysiere und gib den Aktionsplan gemäß des schemas zurück:\n\n"
                        + context
                    ),
                },
            ],
            text_format=DonBottoPlan,
            temperature=0.2,
            max_output_tokens=900,
        )

        plan: DonBottoPlan = completion.output_parsed
        if len(plan.lineup) > 11:
            plan.lineup = plan.lineup[:11]
        return plan
