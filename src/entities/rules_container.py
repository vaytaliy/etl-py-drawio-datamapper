from entities.rule import Rule
from entities.identity import Id

"""
Just keeps unique rules here
"""
class RulesContainer:
    def __init__(self) -> None:
        self.rule_dict : dict[int, Rule] = {}
        self.rule_chains : dict[int, list[Rule]] = {} #changed from list to list[Rule]
        self.drawio_out = ""
    
    def add_rule(self, new_rule : Rule):       
       if new_rule.rule_id:
           self.rule_dict[int(new_rule.rule_id)] = new_rule
    
    '''
    builds chains with rule sequences
    '''
    def create_rule_chains(self):
        
        for rule in self.rule_dict.values():
            dependent_rule = self.get_rule_by_internal_id(rule.dependent_rule_id)
            preceeding_rule = self.get_rule_by_internal_id(rule.preceeding_rule_id)
            if dependent_rule is None:
                rule_id = int(rule.rule_id)
                self.rule_chains[rule_id] = [rule]

                if preceeding_rule:
                    self.rule_chains[rule_id].append(preceeding_rule)

                current_rule = preceeding_rule
                while current_rule and current_rule.preceeding_rule_id:
                    current_rule = self.get_rule_by_internal_id(current_rule.preceeding_rule_id)    
                    self.rule_chains[rule_id].append(current_rule)

    def get_rule_by_internal_id(self, id):
        if id and int(id) in self.rule_dict:
            return self.rule_dict[int(id)]
        return None
    
    def get_last_rule_in_chain_for_rule(self, searched_rule : Rule):
        for chain in self.rule_chains.values():
            for rule in chain:
                if rule.rule_id == searched_rule.rule_id:
                    return chain[-1]
        return None

    def combine_target_refs_to_last(self):
        for chain in self.rule_chains.values():
            last_in_chain = chain[-1]
            for rule in chain[:-1]:
                for target_ref in rule.target_refs:
                    last_in_chain.target_refs.add(target_ref)

    def get_drawio_out(self):
        out = ""
        for rule in self.rule_dict.values():
            out += rule.create_drawio_out() + '\n'
        self.drawio_out = out