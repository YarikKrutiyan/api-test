from src.config import USER_MY
from api.counterpartiesCase import Counterparties

class TestC:
    def test_con(self, set_environment):
        z = Counterparties.get(self,set_environment, USER_MY)
        print(z)
