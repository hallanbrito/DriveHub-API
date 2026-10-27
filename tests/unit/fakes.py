from core.domain.entities import Brand, SaleProposal, Vehicle
class InMemoryBrandRepository:
    def __init__(self) -> None:
        self.items: dict[int, Brand] = {}
        self.next_id = 1
    def get_or_create_by_name(self, name: str) -> Brand:
        for b in self.items.values():
            if b.name == name.strip(): return b
        b = Brand(id=self.next_id, name=name.strip())
        self.items[self.next_id] = b
        self.next_id += 1
        return b
class InMemoryVehicleRepository:
    def __init__(self) -> None:
        self.items: dict[int, Vehicle] = {}
        self.next_id = 1
    def get_by_id(self, i: int) -> Vehicle | None: return self.items.get(i)
    def list_all(self) -> list[Vehicle]: return list(self.items.values())
    def save(self, v: Vehicle) -> Vehicle:
        if v.id is None: v.id = self.next_id; self.next_id += 1
        self.items[v.id] = v
        return v
class InMemorySaleProposalRepository:
    def __init__(self) -> None:
        self.items: dict[int, SaleProposal] = {}
        self.next_id = 1
    def get_by_id(self, i: int) -> SaleProposal | None: return self.items.get(i)
    def list_all(self) -> list[SaleProposal]: return list(self.items.values())
    def save(self, p: SaleProposal) -> SaleProposal:
        if p.id is None: p.id = self.next_id; self.next_id += 1
        self.items[p.id] = p
        return p
