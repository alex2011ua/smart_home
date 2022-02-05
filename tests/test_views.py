import json
import unittest
from unittest.mock import Mock, patch

import pytest
import responses
from django.conf import settings

from house.core.tasks import tessty


class TestViews:
    @patch('Setting.objects.get(controller_name="poliv")')
    def test_tsssty(self, mockPoliv):
        poliv = mockPoliv()
        poliv.value.return_value = "включен"
        assert (tessty(), True)
