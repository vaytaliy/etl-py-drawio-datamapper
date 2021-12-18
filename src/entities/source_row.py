from entities.identity import Id
from entities.table_row import TableRow
from utils import tools
import re

class SourceRow(TableRow):
    def __init__(self, sys_number, col_name, col_description, col_lineage, col_datatype, rule_refs, sensitive_flag, target_refs, table_id):
        super().__init__(col_name, col_datatype, col_description, table_id, col_lineage)   
        self.sys_number = sys_number
        self.id = -1 #is set from source table class
        self.refs = target_refs
        self.rule_refs = rule_refs
        self.sensitive_flag = sensitive_flag
        self.target_col_set : set = self.create_set_refs(target_refs)
        self.rule_set : set = self.create_set_refs(rule_refs)
        self.identation = 0

    def add_refs(self, ids):        
        ids_list = str(ids).split(',')
        for id in ids_list:
            self.target_col_set.add(int(id))

    def create_drawio_out(self):
        
        full_col_name = ""
        if self.col_lineage is None or self.col_lineage == "":
            full_col_name = self.col_name
        else:
            full_col_name = f'{self.col_lineage}.{self.col_name}'

        full_refs = ""
        if len(self.rule_set) > 0:
            for rule_ref in self.rule_set:
                full_refs += str(rule_ref) + ','
        if len(self.target_col_set) > 0:
            for tbl_ref in self.target_col_set:
                full_refs += str(tbl_ref) + ','
        full_refs = full_refs[:-1]

        descr_without_linebreaks = re.sub(r'\n', ' ', self.description, flags = re.MULTILINE)
        descr_clean = re.sub(r'"', ' ', descr_without_linebreaks, flags = re.MULTILINE)
        return f"""{self.id},row_group,{self.table_id},"",boldlabel,{self.container_style},"{full_refs}",0
{Id.get_id()},col,{self.id},"{full_col_name}",headerlabel,{self.table_cell_style},"",{self.identation}
{Id.get_id()},col,{self.id},{self.col_datatype},boldlabel,{self.table_cell_style},"",0
{Id.get_id()},col,{self.id}," {descr_clean}",boldlabel,{self.table_cell_style},"",0"""
