
from unittest.mock import Mock, patch




class TestViews:
    @patch('Setting.objects.get(controller_name="poliv")')
    def test_tsssty(self, mockPoliv):
        poliv = mockPoliv()
        poliv.value.return_value = "включен"
        assert (tessty(), True)
