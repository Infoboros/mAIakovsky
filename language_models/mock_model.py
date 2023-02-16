from .base_model import BaseModel


class MockModel(BaseModel):
    def predict_next_word(self, context: [str], count: int = None) -> [str]:
        count = count if count is not None else 10
        return ['1' for _ in range(count)]
