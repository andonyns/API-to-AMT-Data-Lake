# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dagster import job

from edfi_amt_data_lake.api.api import validate_supported_api
from edfi_amt_data_lake.dagster_config.ops.api import (
    generate_parquet,
    get_api_data,
    not_supported_data_standard_version,
)


@job
def pipe_api_job():
    if validate_supported_api():
        generate_parquet(get_api_data())
    else:
        not_supported_data_standard_version()
