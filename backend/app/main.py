# app/main.py
from fastapi import FastAPI, HTTPException
from app.models import RuleInput, CombineRulesInput, EvaluateRuleInput
from app.parser import parse_rule
from app.database import insert_rule, get_rule, get_rules
from app.evaluator import evaluate_ast
from app.utils import combine_asts

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Rule Engine Backend is running"}

@app.post('/create_rule')
def create_rule(rule_input: RuleInput):
    try:
        ast = parse_rule(rule_input.rule_string)
        rule_data = {
            'rule_string': rule_input.rule_string,
            'ast': ast,
            'combined': False
        }
        rule_id = insert_rule(rule_data)
        return {'message': 'Rule created', 'rule_id': str(rule_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post('/combine_rules')
def combine_rules(input_data: CombineRulesInput):
    rules = get_rules(input_data.rule_ids)
    if not rules:
        raise HTTPException(status_code=404, detail="No rules found")
    asts = [rule['ast'] for rule in rules]
    combined_ast = combine_asts(asts)
    rule_data = {
        'rule_string': None,
        'ast': combined_ast,
        'combined': True
    }
    combined_rule_id = insert_rule(rule_data)
    return {'message': 'Rules combined', 'combined_rule_id': str(combined_rule_id)}


@app.post('/evaluate_rule')
def evaluate_rule(input_data: EvaluateRuleInput):
    rule = get_rule(input_data.rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    result = evaluate_ast(rule['ast'], input_data.user_data)
    return {'eligible': result}