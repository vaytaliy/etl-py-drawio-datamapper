import re
from entities.identity import Id

class TableRow:
    def __init__(self, col_name, col_datatype, col_description, table_id, col_lineage):
        self.col_name = col_name
        self.col_datatype = col_datatype
        self.description = col_description
        self.table_id = table_id
        self.col_lineage = col_lineage
        self.identation = 0
        self.id = -1
        self.target_col_set : set = set()
        self.rule_set : set = set()
        self.drawio_out = ""
        self.container_style = "rounded=0;whiteSpace=wrap;html=1;align=left;"
        self.table_cell_style = "rounded=0;whiteSpace=wrap;html=1;align=left;"

    def create_set_refs(self, refs):
        refs_set = set()
        if refs:
            split_refs = str(refs).split(',')
            if split_refs:
                for ref in split_refs:
                    refs_set.add(ref)
        return refs_set

    def remove_target_ref(self, target_ref):
        if str(target_ref) in self.target_col_set:
            self.target_col_set.remove(str(target_ref))
        self.refs = ""
    
    def add_rule_refs(self, ids):        
        ids_list = str(ids).split(',')
        for id in ids_list:
            self.rule_set.add(int(id))