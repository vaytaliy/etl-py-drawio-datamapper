from entities.target_row import TargetRow
from entities.identity import Id
from entities.rules_container import RulesContainer
from entities.table import Table


class TargetTable(Table):
    def __init__(self, table_name, table_description):
        super().__init__(table_name, "shape=table;childLayout=tableLayout;startSize=30;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;align=left;marginBottom=0;fillColor=#d5e8d4;strokeColor=#82b366;")
        self.table_description = table_description
        self.rows : dict[str, TargetRow] = {}


    def add_row(self, new_row: TargetRow):
        
        if new_row.col_name is None:
            return

        same_existing_col : TargetRow = self.get_row_by_name_and_lineage(new_row.col_name, new_row.col_lineage)
        
        if same_existing_col is None:
            new_row.table_id = self.id
            self.append_row(new_row)