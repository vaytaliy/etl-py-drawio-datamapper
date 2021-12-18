import configparser

rules_headers = [
    'Identifier',
    'RuleName',
    'RuleDescription',
    'RuleType',
    'DependentRule',
    'PreceedingRule']

mapping_headers = [
    'SourceSystemIdentifier',
    'SourceSystemTechnicalName',
    'SourceStorageName',
    'SourceStorageDescription',
    'SourceColumnName',
    'SourceColumnDescription',
    'SourceColumnLineage',
    'SourceDatatype',
    'SourceDataSensitiveFlag',
    'RulesReferences',
    'LogicalKeyFlag',
    'ProductDomain',
    'TargetColumnName',
    'TargetColumnDescription',
    'TargetDatatype',
    'TargetMode',
    'TargetDataSensitiveFlag']

def read_config(config_path):
    if config_path is None:
        print("couldn't read config")
        return
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        print(config['Rules']['Sheet'])
        return config
    except:
        print("some error occured")
    return -1
