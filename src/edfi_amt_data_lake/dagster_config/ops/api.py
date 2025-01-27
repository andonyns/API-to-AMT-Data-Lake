# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import traceback

from dagster import get_dagster_logger, op
from decouple import config

from edfi_amt_data_lake.api.api import api_async
from edfi_amt_data_lake.api.changeVersion import get_change_version_updated
from edfi_amt_data_lake.helper.helper import get_school_year
from edfi_amt_data_lake.helper.utils import delete_path_content
from edfi_amt_data_lake.parquet.amt_parquet import generate_amt_parquet


@op(description="API Data Standard Version is not supported.")
def not_supported_data_standard_version():
    logger = get_dagster_logger()
    logger.error("Data Standard Version not supported.")


@op(description="Get JSON Data from API.")
def get_api_data() -> bool:
    if (config('GENERATE_SILVER_DATA', default=True, cast=bool)):
        logger = get_dagster_logger()
        try:
            delete_path_content(config("SILVER_DATA_LOCATION"))
            for school_year in get_school_year():
                if get_change_version_updated(school_year):
                    api_async(school_year)
                return True
        except Exception as ex:
            logger.error(f"An unhandled exception occured: {ex}, Traceback: {traceback.format_exc()}")
        return False
    return True


@op(description="Generate Parquet Files.")
def generate_parquet(api_result_sucess) -> bool:
    if (config('GENERATE_GOLD_DATA', default=True, cast=bool)):
        logger = get_dagster_logger()
        try:
            if api_result_sucess:
                for school_year in get_school_year():
                    generate_amt_parquet(school_year)
            return True
        except Exception as ex:
            logger.error(f"An unhandled exception occured: {ex}, Traceback: {traceback.format_exc()}")
        return False
    return True
