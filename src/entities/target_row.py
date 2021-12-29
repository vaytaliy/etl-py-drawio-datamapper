from entities.identity import Id
from entities.table_row import TableRow
import re

class TargetRow(TableRow):
    def __init__(self, col_name, col_datatype, table_id, id, col_mode = "", col_description = "", col_lineage = None, col_domain_name = None,  sensitive_info_flag = None):
        super().__init__(col_name, col_datatype, col_description, table_id, "") 
        self.col_product_name = col_domain_name
        self.col_mode = col_mode
        self.col_lineage = col_lineage
        self.id = id
        self.sensitive_info_flag = sensitive_info_flag
        self.drawio_out = ""
        self.container_style = "rounded=0;whiteSpace=wrap;html=1;align=left;"
        self.table_cell_style = "rounded=0;whiteSpace=wrap;html=1;align=left;"
        self.identation = self.set_identation()
        self.target_col_set : set = set()
        self.rule_set : set = set()

    def set_identation(self):
        #default identation
        identation = 0
        
        if self.col_lineage == '':
            return identation
        
        #if there's at least one property in lineage, identation is increased
        identation = 50

        nesting_level = len(re.findall(r'\.|\[\]gm', self.col_lineage))
        
        if nesting_level is not None and nesting_level > 0:
            spaces = 0
            for num in range(nesting_level):
                spaces += 50

            identation += spaces
        
        return identation


    def create_drawio_out(self):
             
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
{Id.get_id()},col,{self.id},"{self.col_name}",headerlabel,{self.table_cell_style},"",{self.identation}
{Id.get_id()},col,{self.id},{self.col_datatype},boldlabel,{self.table_cell_style},"",0
{Id.get_id()},col,{self.id}," {descr_clean}",boldlabel,{self.table_cell_style},"",0"""