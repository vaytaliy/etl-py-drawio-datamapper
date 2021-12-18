from entities.rules_container import RulesContainer
from entities.identity import Id

from entities.rules_container import RulesContainer
from entities.table_row import TableRow


class Table():
    def __init__(self, table_name, style):
        self.table_name = table_name
        self.rows : dict[str, TableRow] = {}
        self.id = Id.get_id()
        self.style = style
        self.drawio_out = ""
    
    def get_row_by_name_and_lineage(self, name, lineage):

        clean_lineage = ""
        if lineage is not None:
            clean_lineage = lineage

        key = clean_lineage + '#' + name
        if key in self.rows:
            return self.rows[key]
        return None

    def append_row(self, row : TableRow):
        if row.col_lineage is None:
            row.col_lineage = ""
        self.rows[row.col_lineage + '#' + row.col_name] = row

    def add_rule_references(self, rules_container : RulesContainer):
        for row in self.rows.values():
            row_rule_refs : set = row.rule_set
            row_trg_refs : set = row.target_col_set
            for rule in row_rule_refs:
                found_rule = rules_container.get_rule_by_internal_id(rule)
                if found_rule:
                    last_rule_in_chain = rules_container.get_last_rule_in_chain_for_rule(found_rule)
                    for rule_trg_ref in last_rule_in_chain.target_refs:
                        if str(rule_trg_ref) in row_trg_refs:
                            row.remove_target_ref(rule_trg_ref)
    
    def get_drawio_out(self):
        out_from_rows = f"""{self.id},table,,{self.table_name},boldlabel,{self.style},,0\n"""
        for row in self.rows.values():
            out_from_rows += row.create_drawio_out() + '\n';
        self.drawio_out = out_from_rows