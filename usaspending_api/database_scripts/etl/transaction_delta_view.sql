DROP VIEW IF EXISTS transaction_delta_view;

CREATE VIEW transaction_delta_view AS
SELECT
  "transaction_id",
  "award_id",
  "modification_number",
  "detached_award_proc_unique",
  "afa_generated_unique",
  "generated_unique_award_id",
  "piid",
  "fain",
  "uri",
  CASE
    WHEN "detached_award_proc_unique" IS NOT NULL THEN 'CONT_TX_' || "detached_award_proc_unique"
    WHEN "afa_generated_unique" IS NOT NULL THEN 'ASST_TX_' || "afa_generated_unique"
    ELSE NULL
  END AS generated_unique_transaction_id,
  CASE
    WHEN "type" IN ('02', '03', '04', '05', '06', '10', '07', '08', '09', '11') AND "fain" IS NOT NULL THEN "fain"
    WHEN "piid" IS NOT NULL THEN "piid"  -- contracts. Did it this way to easily handle IDV contracts
    ELSE "uri"
  END AS display_award_id,
  "action_date",
  "fiscal_action_date",
  "last_modified_date",
  "fiscal_year",
  "award_certified_date",
  "award_fiscal_year",
  "award_date_signed",
  "update_date",
  "award_update_date",
  "etl_update_date",
  "period_of_performance_start_date",
  "period_of_performance_current_end_date",
  "ordering_period_end_date",
  "type",
  "type_description",
  "award_category",
  "transaction_description",
  "award_amount",
  "generated_pragmatic_obligation",
  "federal_action_obligation",
  "original_loan_subsidy_cost",
  "face_value_loan_guarantee",
  "business_categories",
  "naics_code",
  "naics_description",
  "product_or_service_code",
  "product_or_service_description",
  "type_of_contract_pricing",
  "type_set_aside",
  "extent_competed",
  "cfda_number",
  "cfda_title",
  "pop_country_name",
  "pop_country_code",
  "pop_state_name",
  "pop_state_code",
  "pop_state_fips",
  "pop_state_population",
  "pop_county_code",
  "pop_county_name",
  "pop_county_population",
  "pop_zip5",
  "pop_congressional_code",
  "pop_congressional_population",
  "pop_city_name",
  "recipient_location_country_code",
  "recipient_location_country_name",
  "recipient_location_state_name",
  "recipient_location_state_code",
  "recipient_location_state_fips",
  "recipient_location_state_population",
  "recipient_location_county_code",
  "recipient_location_county_name",
  "recipient_location_county_population",
  "recipient_location_congressional_code",
  "recipient_location_congressional_population",
  "recipient_location_zip5",
  "recipient_location_city_name",
  "recipient_hash",
  "recipient_name",
  "recipient_levels",
  "recipient_unique_id",
  "parent_recipient_hash",
  "parent_recipient_name",
  "parent_recipient_unique_id",
  "recipient_uei",
  "parent_uei",
  "awarding_agency_id",
  "funding_agency_id",
  "awarding_toptier_agency_id",
  "funding_toptier_agency_id",
  "awarding_agency_code",
  "awarding_toptier_agency_name",
  "funding_agency_code",
  "funding_toptier_agency_name",
  "awarding_sub_tier_agency_c",
  "awarding_subtier_agency_name",
  "funding_sub_tier_agency_co",
  "funding_subtier_agency_name",
  "awarding_office_code",
  "awarding_office_name",
  "funding_office_code",
  "funding_office_name",
  "awarding_toptier_agency_abbreviation",
  "funding_toptier_agency_abbreviation",
  "awarding_subtier_agency_abbreviation",
  "funding_subtier_agency_abbreviation",
  "tas_paths",
  "tas_components",
  "federal_accounts"::JSON,
  "disaster_emergency_fund_codes"
FROM "rpt.transaction_search"
WHERE "action_date" >= '2007-10-01';
