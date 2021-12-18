from __future__ import annotations
from utils import tools
from entities.target_row import TargetRow
import re

class Rule():
    def __init__(self, rule_id, rule_name, rule_description, rule_type, target_refs : set, dependent_rule_id = None, preceeding_rule_id = None):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.description = rule_description
        self.rule_type = rule_type
        self.dependent_rule_id = dependent_rule_id
        self.preceeding_rule_id = preceeding_rule_id
        self.target_refs : set = target_refs #if dependent rule, then no refs, otherwise has target refs
        self.target_arrow_labels :dict[str, TargetRow] = {} #goes in order to each target_ref
        self.style = "rounded=0;whiteSpace=wrap;html=1;"
        self.drawio_out = ""

    def equals(self, value_to_compare : Rule):
        if self.rule_id == value_to_compare:
            return True
        return False

    def add_table_ref(self, id):
        self.target_refs = tools.add_to_comma_separated_list(self.target_refs, id)
    

    def create_drawio_out(self):
        
        refs = ""
        descr_without_linebreaks = re.sub(r'\n', ' ', self.description, flags = re.MULTILINE)
        clean_descr = re.sub(r'"', ' ', descr_without_linebreaks, flags = re.MULTILINE)
        if self.preceeding_rule_id:
            refs = self.preceeding_rule_id
        else:
            if len(self.target_refs) > 0:
                for target_ref in self.target_refs:
                    refs += str(target_ref) + ','
            refs = refs[:-1]
        
        return f'{self.rule_id},rule,,"{clean_descr}",boldlabel,{self.style},"{refs}",0'