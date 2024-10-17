# app/main.py
from fastapi import FastAPI, HTTPException
# from app.models import RuleInput, CombineRulesInput, EvaluateRuleInput
# from app.parser import parse_rule
# from app.database import insert_rule, get_rule, get_rules
# from app.evaluator import evaluate_ast
# from app.utils import combine_asts

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Rule Engine Backend is running"}