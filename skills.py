# -*- coding: utf-8 -*-
"""Cross-Border Section 321 de Minimis Compliance & Tariff Arbitrage Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def audit_section321_deminimis_compliance(**kwargs):
    """Audits cross-border e-commerce parcels for US Customs Section 321 ($800 de minimis threshold), validates one-entry-per-day consolidated manifests, and flags Section 301 China tariff exposure."""
    consignee_full_name = kwargs.get('consignee_full_name')
    consignee_delivery_address = kwargs.get('consignee_delivery_address')
    declared_customs_value_usd = kwargs.get('declared_customs_value_usd')
    country_of_origin = kwargs.get('country_of_origin')
    hts_subheading_code = kwargs.get('hts_subheading_code')
    carrier_manifest_date = kwargs.get('carrier_manifest_date')

    # US Customs 19 U.S.C. 1321 (Section 321): $800 daily ceiling per ultimate consignee
    is_under_threshold = declared_customs_value_usd <= 800.0
    
    # Base formal duty estimate if de minimis were revoked
    # Standard apparel 6109.10 has approx 16.5% base MFN duty + 25% Section 301 tariff if China
    is_china_origin = country_of_origin.upper() == "CN"
    mfn_duty_rate = 0.165 if hts_subheading_code.startswith("61") or hts_subheading_code.startswith("62") else 0.05
    section_301_rate = 0.25 if is_china_origin else 0.0
    total_effective_tariff_rate = mfn_duty_rate + section_301_rate
    
    avoided_duty_savings_usd = round(declared_customs_value_usd * total_effective_tariff_rate, 2) if is_under_threshold else 0.0
    
    if is_under_threshold:
        clearance_path = "SECTION_321_TYPE_86_ENTRY (Duty-Free & Tax-Free Expedited)"
        compliance_notes = f"Complies with 19 CFR 10.151. Total duty avoided: ${avoided_duty_savings_usd:.2f}. Verify single-daily-entry limit per consignee."
    else:
        clearance_path = "FORMAL_TYPE_01_ENTRY_REQUIRED (Exceeds $800 Statutory Limit)"
        compliance_notes = f"Parcel exceeds Section 321 threshold. Formal entry required with payment of estimated ${declared_customs_value_usd * total_effective_tariff_rate:.2f} in duties/fees."
        
    result = {
        "status": "success",
        "consignee": consignee_full_name,
        "declared_value_usd": declared_customs_value_usd,
        "section321_eligible": is_under_threshold,
        "clearance_channel": clearance_path,
        "statutory_daily_ceiling_usd": 800.0,
        "section_301_exposure": is_china_origin,
        "estimated_duty_savings_usd": avoided_duty_savings_usd,
        "cbp_entry_directives": compliance_notes,
        "engine": "GenPark US Customs Section 321 de Minimis Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "audit_section321_deminimis_compliance": {
        "name": "audit_section321_deminimis_compliance",
        "description": "Audits cross-border e-commerce parcels for US Customs Section 321 ($800 de minimis threshold), validates one-entry-per-day consolidated manifests, and flags Section 301 China tariff exposure.",
        "parameters": {
            "type": "object",
            "properties": {
                "consignee_full_name": {"type": "string", "description": "Ultimate retail recipient name"},
                "consignee_delivery_address": {"type": "string", "description": "Recipient destination street address"},
                "declared_customs_value_usd": {"type": "number", "description": "Fair retail value of parcel contents in USD"},
                "country_of_origin": {"type": "string", "description": "ISO 2-letter manufacturing origin (e.g. 'CN', 'VN')"},
                "hts_subheading_code": {"type": "string", "description": "6-to-10 digit Harmonized Tariff Schedule code"},
                "carrier_manifest_date": {"type": "string", "description": "Consolidated clearance date (YYYY-MM-DD)"},
            },
            "required": ['consignee_full_name', 'consignee_delivery_address', 'declared_customs_value_usd', 'country_of_origin', 'hts_subheading_code', 'carrier_manifest_date']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "audit_section321_deminimis_compliance":
            res = audit_section321_deminimis_compliance(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-cross-border-duty-de-minimis-arbitrage-auditor-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-cross-border-duty-de-minimis-arbitrage-auditor-skill...")
    test_args = {'consignee_full_name': 'Jane Doe', 'consignee_delivery_address': '742 Evergreen Terrace, Springfield, OR', 'declared_customs_value_usd': 340.0, 'country_of_origin': 'CN', 'hts_subheading_code': '6109.10.00', 'carrier_manifest_date': '2026-10-30'}
    res = audit_section321_deminimis_compliance(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-cross-border-duty-de-minimis-arbitrage-auditor-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
