from typing import Any, Dict, List, Union

from coppyr.config import TOMLConfig
from crossplane import analyzer

from engin.nginx import objects as ngxo


# any # of args | block conf | any context
DEFAULT_MASK = analyzer.NGX_CONF_ANY | analyzer.NGX_CONF_BLOCK | analyzer.NGX_ANY_CONF


def _parse_directive(
    name: str,
    definition: Union[Dict[str, Any], Any]
) -> ngxo.NginxDirective:
    is_block = isinstance(definition, dict)
    is_list = isinstance(definition, list)

    directive = ngxo.NginxDirective(
        directive=name,
        args=definition.get("args", []) if is_block \
            else definition if is_list \
            else [definition]
    )

    # Convert args to str as that is crossplane standard
    directive.args = [str(arg) for arg in directive.args]

    # If not a block or the block is empty, just return the directive as a k-v
    # pair.
    if not is_block or not len(definition) > 0:
        return directive

    # Recursive block handling
    directive.block = []
    for name, definition in definition.items():
        # skip "args" as that is handled above
        if name == "args":
            continue

        if isinstance(definition, dict):
            directive.block += _parse_block(name, definition)
        elif isinstance(definition, list):
            directive.block += _parse_directive_list(name, definition)
        else:
            directive.block.append(
                _parse_directive(name, definition)
            )

    return directive


def _parse_directive_list(
    name: str,
    definitions: List[Any]
) -> List[ngxo.NginxDirective]:
    mask = analyzer.DIRECTIVES.get(name, [DEFAULT_MASK])[0]

    # If the block is a list of things and the directive supports NGX config
    # blocks, then parse it as a list of sub-directives
    if mask & analyzer.NGX_CONF_BLOCK:
        return [
            _parse_directive(name, definition) for definition in definitions
        ]
    else:
        return [_parse_directive(name, definitions)]


def _parse_block(
    name: str,
    block: Union[List[Any], Dict[str, Any]]
) -> List[ngxo.NginxDirective]:
    if isinstance(block, list):
        return _parse_directive_list(name, block)
    else:
        return [_parse_directive(name, block)]


def load(file_path: str) -> ngxo.CrossplaneParsePayload:
    toml_config = TOMLConfig(file_path)
    crossplane = ngxo.CrossplaneParsePayload()

    for file_block in toml_config.values():
        ngx_conf = ngxo.NginxConfig(file=file_block.filename)

        for name, definition in file_block.items():
            if name != "filename":
                ngx_conf.parsed += _parse_block(name, definition)

        crossplane.config.append(ngx_conf)

    return crossplane
