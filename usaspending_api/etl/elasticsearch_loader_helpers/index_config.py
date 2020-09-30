import json
import logging

from django.conf import settings

from usaspending_api.awards.v2.lookups.elasticsearch_lookups import INDEX_ALIASES_TO_AWARD_TYPES
from usaspending_api.etl.elasticsearch_loader_helpers.utilities import format_log


logger = logging.getLogger("script")


def put_alias(client, index, alias_name, alias_body):
    client.indices.put_alias(index, alias_name, body=alias_body)


def create_aliases(client, config):
    for award_type, award_type_codes in INDEX_ALIASES_TO_AWARD_TYPES.items():

        alias_name = f"{config['query_alias_prefix']}-{award_type}"
        if config["verbose"]:
            msg = f"Putting alias '{alias_name}' on {config['index_name']} with award codes {award_type_codes}"
            logger.info(format_log(msg, process="ES Alias"))
        alias_body = {"filter": {"terms": {"type": award_type_codes}}}
        put_alias(client, config["index_name"], alias_name, alias_body)

    # ensure the new index is added to the alias used for incremental loads.
    # If the alias is on multiple indexes, the loads will fail!
    logger.info(format_log(f"Putting alias '{config['write_alias']}' on {config['index_name']}", process="ES Alias"))
    put_alias(client, config["index_name"], config["write_alias"], {})


def set_final_index_config(client, index):
    es_settingsfile = str(settings.APP_DIR / "etl" / "es_config_objects.json")
    with open(es_settingsfile) as f:
        settings_dict = json.load(f)
    final_index_settings = settings_dict["final_index_settings"]

    current_settings = client.indices.get(index)[index]["settings"]["index"]

    client.indices.put_settings(final_index_settings, index)
    client.indices.refresh(index)
    for setting, value in final_index_settings.items():
        message = f'Changing "{setting}" from {current_settings.get(setting)} to {value}'
        logger.info(format_log(message, process="ES Settings"))


def swap_aliases(client, config):
    if client.indices.get_alias(config["index_name"], "*"):
        logger.info(format_log(f"Removing old aliases for index '{config['index_name']}'", process="ES Alias"))
        client.indices.delete_alias(config["index_name"], "_all")

    alias_patterns = config["query_alias_prefix"] + "*"
    old_indexes = []

    try:
        old_indexes = list(client.indices.get_alias("*", alias_patterns).keys())
        for old_index in old_indexes:
            client.indices.delete_alias(old_index, "_all")
            logger.info(format_log(f"Removing aliases from '{old_index}'", process="ES Alias"))
    except Exception:
        logger.exception(format_log(f"No aliases found for {alias_patterns}", process="ES Alias"))

    create_aliases(client, config)

    try:
        if old_indexes:
            client.indices.delete(index=old_indexes, ignore_unavailable=False)
            logger.info(format_log(f"Deleted index(es) '{old_indexes}'", process="ES Alias"))
    except Exception:
        logger.exception(format_log(f"Unable to delete indexes: {old_indexes}", process="ES Alias"))
