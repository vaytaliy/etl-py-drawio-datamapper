from entities.rules_container import RulesContainer
from entities.source_row import SourceRow
from entities.identity import Id
from entities.table import Table

class SourceTable(Table):
    
    def __init__(self, table_name, store_tech_name, store_description):
        super().__init__(table_name, "shape=table;childLayout=tableLayout;startSize=30;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;align=left;marginBottom=0;fillColor=#dae8fc;strokeColor=#6c8ebf;")
        self.rows : dict[str, SourceRow] = {}
        self.store_tech_name = store_tech_name
        self.store_description = store_description
        self.drawio_out = ""


    def add_row(self, new_row: SourceRow):
        
        if new_row.col_name is None:
            return

        same_existing_col : SourceRow = self.get_row_by_name_and_lineage(new_row.col_name, new_row.col_lineage)
        
        if same_existing_col is not None:
            same_existing_col.add_refs(new_row.refs)
            same_existing_col.add_rule_refs(new_row.rule_refs)
        else:
            new_row.id = Id.get_id() #add id when new row is created
            self.append_row(new_row)