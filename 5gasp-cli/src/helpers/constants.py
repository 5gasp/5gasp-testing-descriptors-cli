# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-13 15:17:29
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-20 10:57:49

from enum import Enum

CI_CD_SERVICE_URL = "https://ci-cd-service.5gasp.eu/manager"


class CI_CD_SERVICE_URL_ENDPOINTS(Enum):
    ALL_TESTS = "/tests/all"
    ALL_TESTBEDS = "/testbeds/all"
