from pydantic import BaseModel
from typing import Optional, List

class RuleInput(BaseModel):
    rule_string: str

class CombineRulesInput(BaseModel):
    rule_ids: List[str]

class EvaluateRuleInput(BaseModel):
    rule_id: str
    user_data: dict