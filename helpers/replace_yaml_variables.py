import yaml

def replace_yaml_variables(yaml_content, replacements):
    """
    Replace template variables in the given YAML content using the replacements dictionary.
    Template variables are expected to be in the format {VAR_NAME}.
    """
    yaml_str = yaml.dump(yaml_content)
    for key, value in replacements.items():
        yaml_str = yaml_str.replace(f"{{ {key} }}", str(value))
    return yaml.safe_load(yaml_str)