# Cross-Border Section 321 de Minimis Compliance & Tariff Arbitrage Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `audit_section321_deminimis_compliance`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Audits cross-border e-commerce parcels for US Customs Section 321 ($800 de minimis threshold), validates one-entry-per-day consolidated manifests, and flags Section 301 China tariff exposure.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Customs & International Trade)`

## MCP Tool Specification
### `audit_section321_deminimis_compliance`
Parameters:
- `consignee_full_name` (str): Ultimate retail recipient name
- `consignee_delivery_address` (str): Recipient destination street address
- `declared_customs_value_usd` (float): Fair retail value of parcel contents in USD
- `country_of_origin` (str): ISO 2-letter manufacturing origin (e.g. 'CN', 'VN')
- `hts_subheading_code` (str): 6-to-10 digit Harmonized Tariff Schedule code
- `carrier_manifest_date` (str): Consolidated clearance date (YYYY-MM-DD)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-cross-border-duty-de-minimis-arbitrage-auditor-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-cross-border-duty-de-minimis-arbitrage-auditor-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
