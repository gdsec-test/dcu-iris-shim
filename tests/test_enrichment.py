from nose.tools import assert_equal

from enrichment import nutrition_label, dc_finder, os_finder, product_finder


class TestEnrichment:

    def test_nutrition_label_general_1(self):
        data = 'a2plwvnw0398'
        actual = nutrition_label(data)
        assert_equal(actual, ('A2', 'Linux', 'WPaaS'))

    def test_nutrition_label_general_2(self):
        data = 'n1pwcvnw0398'
        actual = nutrition_label(data)
        assert_equal(actual, ('N1', 'Windows', 'cPanel'))

    def test_nutrition_label_general_3(self):
        data = 'p3plvnw0398'
        actual = nutrition_label(data)
        assert_equal(actual, ('P3', 'Linux', 'Plesk'))

    def test_nutrition_label_sg2_1(self):
        data = 'sgpww8vw4536'
        actual = nutrition_label(data)
        assert_equal(actual, ('SG2', 'Windows', '4GH'))

    def test_nutrition_label_sg2_2(self):
        data = 'sgpwwvnw4536'
        actual = nutrition_label(data)
        assert_equal(actual, ('SG2', 'Windows', 'Plesk'))

    def test_nutrition_label_sg2_3(self):
        data = 'sgpwgvnq4536'
        actual = nutrition_label(data)
        assert_equal(actual, ('SG2', None, 'VPS'))

    def test_nutrition_label_sg2_4(self):
        data = 'sgpwgrnq4536'
        actual = nutrition_label(data)
        assert_equal(actual, ('SG2', None, None))

    def test_nutrition_label_check_vat(self):
        data = 'vepwgrnq4536'
        actual = nutrition_label(data)
        assert_equal(actual, ('Check VAT', 'Check VAT', 'Open'))

    def test_nutrition_label_dns(self):
        data = 'cnplcvnw0398'
        actual = nutrition_label(data)
        assert_equal(actual, ('DNS', 'Linux', 'Closed'))

    def test_nutrition_label_corp(self):
        data = 'fwplcvnw0398'
        actual = nutrition_label(data)
        assert_equal(actual, ('Corp', 'Linux', 'Closed'))

    def test_nutrition_label_vph(self):
        data = 'vpplcvnw0398'
        actual = nutrition_label(data)
        assert_equal(actual, ('VPH', 'Linux', 'Open'))

    def test_nutrition_label_failed(self):
        data = 'rtplcvnw0398'
        actual = nutrition_label(data)
        assert_equal(actual, ('Failed', 'Linux', 'Open'))

    def test_nutrition_label_broken(self):
        data = 'godaddy.com'
        actual = nutrition_label(data)
        assert_equal(actual, ('Failed', None, None))

    def test_dc_finder_p1(self):
        data = 'p1'
        actual = dc_finder(data)
        assert_equal(actual, 'P1')

    def test_dc_finder_s2(self):
        data = 's2'
        actual = dc_finder(data)
        assert_equal(actual, 'S2')

    def test_dc_finder_checkvat(self):
        data = 've'
        actual = dc_finder(data)
        assert_equal(actual, 'Check VAT')

    def test_dc_finder_dns(self):
        data = 'cn'
        actual = dc_finder(data)
        assert_equal(actual, 'DNS')

    def test_dc_finder_vph(self):
        data = 'vp'
        actual = dc_finder(data)
        assert_equal(actual, 'VPH')

    def test_dc_finder_corp(self):
        data = 'fw'
        actual = dc_finder(data)
        assert_equal(actual, 'Corp')

    def test_os_finder_corp(self):
        data = 'w'
        actual = os_finder(data)
        assert_equal(actual, 'Windows')

    def test_product_finder_4gh(self):
        data = 'hg'
        actual = product_finder(data)
        assert_equal(actual, '4GH')

    def test_product_finder_2gh(self):
        data = 'h*'
        actual = product_finder(data)
        assert_equal(actual, '2GH')

    def test_product_finder_vps(self):
        data = 'v-h'
        actual = product_finder(data)
        assert_equal(actual, 'VPS')
