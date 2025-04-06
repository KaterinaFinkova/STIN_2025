import unittest
from datetime import datetime, timedelta, timezone
from models.CompanySymbolMapper import CompanySymbolMapper

class TestCompanySymbolMapper(unittest.TestCase):

    def test_add_and_get_mapping(self):
        mapper = CompanySymbolMapper()
        mapper.addMapping("OpenAI", ["OAI", "OPEN"])
        self.assertEqual(mapper.getCompany("OAI"), "OpenAI")
        self.assertIn("OAI", mapper.getSymbols("OpenAI"))

    def test_has_symbol(self):
        mapper = CompanySymbolMapper()
        mapper.addMapping("Tesla", ["TSLA"])
        self.assertTrue(mapper.hasSymbol("TSLA"))
        self.assertFalse(mapper.hasSymbol("XYZ"))

    def test_get_symbols_empty_if_unknown_company(self):
        mapper = CompanySymbolMapper()
        self.assertEqual(mapper.getSymbols("UnknownCo"), set())

    def test_get_unknown_companies(self):
        mapper = CompanySymbolMapper()
        mapper.addMapping("OpenAI", ["OAI"])
        unknown = mapper.getUnknownCompanies({"OpenAI", "DeepMind"})
        self.assertEqual(unknown, {"DeepMind"})

    def test_expired_symbol_is_removed(self):
        mapper = CompanySymbolMapper(expiry_days=1)
        now = datetime.now(timezone.utc)
        old_timestamp = now - timedelta(days=2)

        mapper.symbol_to_company["OLD"] = "OldCorp"
        mapper.company_to_symbol["OldCorp"].add("OLD")
        mapper.symbol_timestamp["OLD"] = old_timestamp

        mapper.getUnknownCompanies(set())

        self.assertIsNone(mapper.getCompany("OLD"))
        self.assertNotIn("OLD", mapper.symbol_to_company)
        self.assertNotIn("OLD", mapper.getSymbols("OldCorp"))