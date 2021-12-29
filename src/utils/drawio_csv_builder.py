from entities.identity import Id
from entities.source_row import SourceRow
from entities.rule import Rule
from entities.target_row import TargetRow
from utils import constants
from entities.source_table import SourceTable
from entities.rules_container import RulesContainer
from entities.target_table import TargetTable


def create_csv(mapping_data_dict, target_table_name):
    upper_csv = """# labels: {"boldlabel": "%text%", "headerlabel": "<span style=\\u0022color:#0d6906;font-weight:600;padding-left:%identation%px\\u0022>%text%</span>"}
# labelname: labelType
# style: %entityStyle%
# parentstyle: %entityStyle%
# parent: parentEntity
# identity: name
# namespace: csvimport-
#
# connect: {"from": "refs", "to": "name", "style": "endArrow=classic;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;rounded=1;edgeStyle=orthogonalEdgeStyle;jumpStyle=arc;strokeColor=#6F0000;fillColor=#a20025;"}
## Node width and height, and padding for autosize
# width: auto
# height: auto
# padding: 0
# ignore: name, refs
#
## Column to be renamed to link attribute (used as link).
# link: url
#
## Spacing between nodes, heirarchical levels and parallel connections.
# nodespacing: 10
# levelspacing: 20
# edgespacing: 10
#
# layout: auto
#
## ---- CSV below this line. First line are column names. ----\n"""

    mapping_data = mapping_data_dict['mapping_data']
    rules_data = mapping_data_dict['rules_data']

    # transpose to change from dictionary format to CSV-like representation
    # so that each row has both source and target in it
    rules_data_transposed = prep_rows(rules_data)
    mapping_data_transposed = prep_rows(mapping_data)

    # jump through all rule ids so that ids assigned to
    # columns dont intersect with ids of rules
    # if theres are rules with id 1,2,3 that means anything else will start from id 4
    max_rule_id = get_max_rule_id(rules_data_transposed)
    Id.set_new_increment_position(max_rule_id)

    # Create data lineage for targets and assign ids to
    # unique targets, using target column as unique name
    # Using only target col name is insufficient in scenarios of nested data
    create_target_lineage(mapping_data_transposed)
    create_unique_target_identifiers(mapping_data_transposed)

    # connect rules to targets
    create_target_col_id_references_for_rules(
        mapping_data_transposed, rules_data_transposed)

    # sources, where key is system tech name (technical locaion, full name)
    # and value is instance of SourceTable with dictionary of SourceRows
    target: TargetTable = build_target(
        mapping_data_transposed, target_table_name)
    sources: dict[str, SourceTable] = build_sources(
        mapping_data_transposed, target_table_name, target)

    # rules represented as RulesContainer which
    # contains chains of rules (begins from first rule that has no preceeding rule and ends with max dependent (next) rule)
    # elements in each chain are linked in order so that's how
    # connections on diagram will be shown for rules

    rules_container = build_rules(rules_data_transposed)

    # if a source S references target T, and S references rule with id X
    # and rule X references target T, then S references only X

    for source in sources.values():
        source.add_rule_references(rules_container)

    # if target references itself
    # it must reference a rule but not field directly
    target.add_rule_references(rules_container)

    sources_out = "name,type,parentEntity,text,labelType,entityStyle,refs,identation\n"
    for source in sources.values():
        source.get_drawio_out()
        sources_out += source.drawio_out
    rules_container.get_drawio_out()
    sources_out += rules_container.drawio_out
    target.get_drawio_out()
    sources_out += target.drawio_out

    upper_csv += sources_out
    return upper_csv


def build_rules(rules_data):

    rules_container = RulesContainer()

    rule_id_loc = get_property_location_in_list(
        rules_data[-1], constants.RULE_ID)
    rule_name_loc = get_property_location_in_list(
        rules_data[-1], constants.RULE_NAME)
    rule_description_loc = get_property_location_in_list(
        rules_data[-1], constants.RULE_DESCRIPTION)
    rule_type_loc = get_property_location_in_list(
        rules_data[-1], constants.RULE_TYPE)
    dependent_rule_id_loc = get_property_location_in_list(
        rules_data[-1], constants.DEPENDENT_RULE)
    preceeding_rule_id_loc = get_property_location_in_list(
        rules_data[-1], constants.PRECEEDING_RULE)
    target_refs_loc = get_property_location_in_list(
        rules_data[-1], constants.TRGS_REFERENCED_BY_RULE)

    for rule_row in rules_data[:-1]:
        rule = Rule(rule_row[rule_id_loc],
                    rule_row[rule_name_loc],
                    rule_row[rule_description_loc],
                    rule_row[rule_type_loc],
                    rule_row[target_refs_loc],
                    rule_row[dependent_rule_id_loc],
                    rule_row[preceeding_rule_id_loc])

        rules_container.add_rule(rule)

    rules_container.create_rule_chains()
    rules_container.combine_target_refs_to_last()
    return rules_container


def create_target_col_id_references_for_rules(mapping_data, rules_data):
    rules_data[-1].append(constants.TRGS_REFERENCED_BY_RULE)

    src_rule_refs_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_RULE_REF_VAL)
    trg_id_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_IDENTIFIER)
    rule_id_loc = get_property_location_in_list(
        rules_data[-1], constants.RULE_ID)

    for row_from_rules in rules_data[:-1]:
        refs_set = set()  # targets which exist for this rule
        for row_from_mapping in mapping_data:
            mapping_rule_refs = row_from_mapping[src_rule_refs_loc]
            if mapping_rule_refs is not None:
                split_rule_refs = str.split(str(mapping_rule_refs), ',')
                if str(row_from_rules[rule_id_loc]) in split_rule_refs:
                    refs_set.add(row_from_mapping[trg_id_loc])

        row_from_rules.append(refs_set)


def build_sources(mapping_data, target_table_name, target_table: TargetTable):
    table_dict: dict[str, SourceTable] = {}

    src_sys_num_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_SYC_NUM_HEAD_VAL)
    src_sys_tech_nm_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_SYS_TECH_NAME_VAL)
    src_store_nm_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_STORE_NAME_VAL)
    src_store_desc_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_STORE_DESC_VAL)
    src_col_nm_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_NAME_HEAD_VAL)
    src_col_desc_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_DESC_HEAD_VAL)
    src_lineage_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_LINEAGE_HEAD_VAL)
    src_datatype_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_DATATYPE_HEAD_VAL)
    src_sensitive_flag_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_SENSITIVE_FLAG)
    src_rule_refs_loc = get_property_location_in_list(
        mapping_data[-1], constants.SRC_COL_RULE_REF_VAL)

    targ_col_id_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_IDENTIFIER)

    for row in mapping_data[:-1]:
        tbl_name = row[src_sys_tech_nm_loc]
        if tbl_name is None:
            continue
        elif row[src_store_nm_loc] == target_table_name:
            target_row = target_table.get_row_by_name_and_lineage(
                row[src_col_nm_loc], row[src_lineage_loc])
            target_row.add_rule_refs(row[src_rule_refs_loc])
            continue
        elif tbl_name not in table_dict:
            table_dict[tbl_name] = SourceTable(
                row[src_store_nm_loc], row[src_sys_tech_nm_loc], row[src_store_desc_loc])
        table_dict[tbl_name].add_row(SourceRow(
            row[src_sys_num_loc],
            row[src_col_nm_loc],
            row[src_col_desc_loc],
            row[src_lineage_loc],
            row[src_datatype_loc],
            row[src_rule_refs_loc],
            row[src_sensitive_flag_loc],
            row[targ_col_id_loc],
            table_dict[tbl_name].id))

    return table_dict


def build_target(mapping_data, table_name):

    table_desc = "test target description"
    trg_col_name_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_NAME_VAL)
    trg_col_descr_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_DESCR_VAL)
    trg_col_datatype_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_DATATYPE_VAL)
    trg_col_mode_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_MODE_VAL)
    trg_col_lineage_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_LINEAGE)
    trg_col_id_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_IDENTIFIER)

    target_table = TargetTable(table_name, table_desc)

    for row in mapping_data[:-1]:
        if row[trg_col_datatype_loc] != constants.RECORD_END:
            target_table.add_row(TargetRow(
                row[trg_col_name_loc],
                row[trg_col_datatype_loc],
                target_table.id,
                row[trg_col_id_loc],
                row[trg_col_mode_loc],
                row[trg_col_descr_loc],
                row[trg_col_lineage_loc]
            ))

    return target_table


def get_max_rule_id(rules_data):

    rule_id_loc = get_property_location_in_list(
        rules_data[-1], constants.RULE_ID)
    max_id = 0

    for row in rules_data[:-1]:
        rule_id = row[rule_id_loc]
        if rule_id > max_id:
            max_id = rule_id

    return max_id


def create_unique_target_identifiers(mapping_data):

    mapping_data[-1].append(constants.TRG_COL_IDENTIFIER)

    unique_attr_set = set()
    id = Id.get_id()  # default id

    target_name_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_NAME_VAL)
    lineage_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_LINEAGE)

    for row in mapping_data[:-1]:

        unique_field = row[lineage_loc] + '#' + row[target_name_loc]

        if unique_field not in unique_attr_set:
            unique_attr_set.add(unique_field)
            id = Id.get_id()  # make new id
        row.append(id)


"""
Helper method to work with lineage dot separation
"""


def gen_lineage_string(current_lineage_string, new_properties_list):
    mod_string = current_lineage_string
    for new_property in new_properties_list:
        if mod_string == "":
            mod_string = new_property
        else:
            mod_string += '.' + new_property
    return mod_string


"""
To identify what target attribute is unique, its full lineage is needed
lineage is also important for displaying nesting per given attribute
"""


def create_target_lineage(mapping_data):

    mapping_data[- 1].append(constants.TRG_COL_LINEAGE)

    target_name_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_NAME_VAL)
    datatype_loc = get_property_location_in_list(
        mapping_data[-1], constants.TRG_COL_DATATYPE_VAL)

    current_lineage = ""
    for row in mapping_data[:-1]:

        if row[datatype_loc] == constants.RECORD:
            row.append(current_lineage)
            current_lineage = gen_lineage_string(
                current_lineage, [row[target_name_loc]])
            continue
        elif row[datatype_loc] == constants.RECORD_END:
            lineage_split = current_lineage.split('.')
            if len(lineage_split) > 0:
                current_lineage = gen_lineage_string("", lineage_split[:-1])

        row.append(current_lineage)


"""
Searched for location of property by provided constant property name
returns index
"""


def get_property_location_in_list(prop_names_list, searched_constant_name):
    for i, prop_name in enumerate(prop_names_list):
        if prop_name == searched_constant_name:
            return i
    return ""


def prep_rows(mapping_data):

    def transpose(rows):
        transposed_list = []

        for i in range(len(rows[0])):
            transposed_list.append([None] * len(rows))

        for j, ypos in enumerate(rows):
            for i, elem in enumerate(ypos):
                transposed_list[i][j] = elem

        return transposed_list

    rows = []

    for key, value in mapping_data.items():
        row = []
        row = value
        row.append(key)
        rows.append(row)

    transposed_data = transpose(rows)
    return transposed_data
