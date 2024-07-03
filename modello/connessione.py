from dataclasses import dataclass

from modello.airport import Airport


@dataclass
class Connessione:
    v0: Airport
    v1: Airport
    N: int
