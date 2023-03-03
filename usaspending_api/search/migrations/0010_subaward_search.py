# Generated by Django 3.2.13 on 2022-08-08 21:00

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0095_auto_20220617_1620'),
        ('references', '0058_bureautitlelookup'),
        ('search', '0009_awardsearch_view_drop'),
    ]

    operations = [
        CreateExtension('intarray'),
        CreateExtension('pg_trgm'),
        migrations.CreateModel(
            name='SubawardSearch',
            fields=[
                ('broker_created_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('broker_updated_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('broker_subaward_id', models.BigIntegerField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('unique_award_key', models.TextField(blank=True, db_index=True, null=True)),
                ('award_piid_fain', models.TextField(blank=True, null=True)),
                ('parent_award_id', models.TextField(blank=True, null=True)),
                ('award_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('action_date', models.DateField(blank=True, null=True)),
                ('fy', models.TextField(blank=True, null=True)),
                ('awarding_agency_code', models.TextField(blank=True, null=True)),
                ('awarding_agency_name', models.TextField(blank=True, null=True)),
                ('awarding_sub_tier_agency_c', models.TextField(blank=True, null=True)),
                ('awarding_sub_tier_agency_n', models.TextField(blank=True, null=True)),
                ('awarding_office_code', models.TextField(blank=True, null=True)),
                ('awarding_office_name', models.TextField(blank=True, null=True)),
                ('funding_agency_code', models.TextField(blank=True, null=True)),
                ('funding_agency_name', models.TextField(blank=True, null=True)),
                ('funding_sub_tier_agency_co', models.TextField(blank=True, null=True)),
                ('funding_sub_tier_agency_na', models.TextField(blank=True, null=True)),
                ('funding_office_code', models.TextField(blank=True, null=True)),
                ('funding_office_name', models.TextField(blank=True, null=True)),
                ('awardee_or_recipient_uniqu', models.TextField(blank=True, null=True)),
                ('awardee_or_recipient_uei', models.TextField(blank=True, null=True)),
                ('awardee_or_recipient_legal', models.TextField(blank=True, null=True)),
                ('dba_name', models.TextField(blank=True, null=True)),
                ('ultimate_parent_unique_ide', models.TextField(blank=True, null=True)),
                ('ultimate_parent_uei', models.TextField(blank=True, null=True)),
                ('ultimate_parent_legal_enti', models.TextField(blank=True, null=True)),
                ('legal_entity_country_code', models.TextField(blank=True, null=True)),
                ('legal_entity_country_name', models.TextField(blank=True, null=True)),
                ('legal_entity_state_code', models.TextField(blank=True, null=True)),
                ('legal_entity_state_name', models.TextField(blank=True, null=True)),
                ('legal_entity_zip', models.TextField(blank=True, null=True)),
                ('legal_entity_congressional', models.TextField(blank=True, null=True)),
                ('legal_entity_foreign_posta', models.TextField(blank=True, null=True)),
                ('legal_entity_city_name', models.TextField(blank=True, null=True)),
                ('legal_entity_address_line1', models.TextField(blank=True, null=True)),
                ('business_types', models.TextField(blank=True, null=True)),
                ('place_of_perform_country_co', models.TextField(blank=True, null=True)),
                ('place_of_perform_country_na', models.TextField(blank=True, null=True)),
                ('place_of_perform_state_code', models.TextField(blank=True, null=True)),
                ('place_of_perform_state_name', models.TextField(blank=True, null=True)),
                ('place_of_performance_zip', models.TextField(blank=True, null=True)),
                ('place_of_perform_congressio', models.TextField(blank=True, null=True)),
                ('place_of_perform_city_name', models.TextField(blank=True, null=True)),
                ('place_of_perform_street', models.TextField(blank=True, null=True)),
                ('award_description', models.TextField(blank=True, null=True)),
                ('naics', models.TextField(blank=True, null=True)),
                ('naics_description', models.TextField(blank=True, null=True)),
                ('cfda_numbers', models.TextField(blank=True, null=True)),
                ('cfda_titles', models.TextField(blank=True, null=True)),
                ('subaward_type', models.TextField(blank=True, null=True)),
                ('subaward_report_year', models.SmallIntegerField()),
                ('subaward_report_month', models.SmallIntegerField()),
                ('subaward_number', models.TextField(blank=True, null=True)),
                ('subaward_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('sub_action_date', models.DateField(blank=True, null=True)),
                ('sub_awardee_or_recipient_uniqu', models.TextField(blank=True, null=True)),
                ('sub_awardee_or_recipient_uei', models.TextField(blank=True, null=True)),
                ('sub_awardee_or_recipient_legal_raw', models.TextField(blank=True, null=True)),
                ('sub_dba_name', models.TextField(blank=True, null=True)),
                ('sub_ultimate_parent_unique_ide', models.TextField(blank=True, null=True)),
                ('sub_ultimate_parent_uei', models.TextField(blank=True, null=True)),
                ('sub_ultimate_parent_legal_enti_raw', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_country_code_raw', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_country_name_raw', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_state_code', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_state_name', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_zip', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_congressional_raw', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_foreign_posta', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_city_name', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_address_line1', models.TextField(blank=True, null=True)),
                ('sub_business_types', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_country_co_raw', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_country_na', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_state_code', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_state_name', models.TextField(blank=True, null=True)),
                ('sub_place_of_performance_zip', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_congressio_raw', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_city_name', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_street', models.TextField(blank=True, null=True)),
                ('subaward_description', models.TextField(blank=True, null=True)),
                ('sub_high_comp_officer1_full_na', models.TextField(blank=True, null=True)),
                ('sub_high_comp_officer1_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('sub_high_comp_officer2_full_na', models.TextField(blank=True, null=True)),
                ('sub_high_comp_officer2_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('sub_high_comp_officer3_full_na', models.TextField(blank=True, null=True)),
                ('sub_high_comp_officer3_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('sub_high_comp_officer4_full_na', models.TextField(blank=True, null=True)),
                ('sub_high_comp_officer4_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('sub_high_comp_officer5_full_na', models.TextField(blank=True, null=True)),
                ('sub_high_comp_officer5_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('prime_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('internal_id', models.TextField(blank=True, db_index=True, null=True)),
                ('date_submitted', models.DateTimeField(blank=True, null=True)),
                ('report_type', models.TextField(blank=True, null=True)),
                ('transaction_type', models.TextField(blank=True, null=True)),
                ('program_title', models.TextField(blank=True, null=True)),
                ('contract_agency_code', models.TextField(blank=True, null=True)),
                ('contract_idv_agency_code', models.TextField(blank=True, null=True)),
                ('grant_funding_agency_id', models.TextField(blank=True, null=True)),
                ('grant_funding_agency_name', models.TextField(blank=True, null=True)),
                ('federal_agency_name', models.TextField(blank=True, null=True)),
                ('treasury_symbol', models.TextField(blank=True, null=True)),
                ('dunsplus4', models.TextField(blank=True, null=True)),
                ('recovery_model_q1', models.BooleanField(blank=True, null=True)),
                ('recovery_model_q2', models.BooleanField(blank=True, null=True)),
                ('compensation_q1', models.BooleanField(blank=True, null=True)),
                ('compensation_q2', models.BooleanField(blank=True, null=True)),
                ('high_comp_officer1_full_na', models.TextField(blank=True, null=True)),
                ('high_comp_officer1_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('high_comp_officer2_full_na', models.TextField(blank=True, null=True)),
                ('high_comp_officer2_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('high_comp_officer3_full_na', models.TextField(blank=True, null=True)),
                ('high_comp_officer3_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('high_comp_officer4_full_na', models.TextField(blank=True, null=True)),
                ('high_comp_officer4_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('high_comp_officer5_full_na', models.TextField(blank=True, null=True)),
                ('high_comp_officer5_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=23, null=True)),
                ('sub_id', models.IntegerField(blank=True, null=True)),
                ('sub_parent_id', models.IntegerField(blank=True, null=True)),
                ('sub_federal_agency_id', models.TextField(blank=True, null=True)),
                ('sub_federal_agency_name', models.TextField(blank=True, null=True)),
                ('sub_funding_agency_id', models.TextField(blank=True, null=True)),
                ('sub_funding_agency_name', models.TextField(blank=True, null=True)),
                ('sub_funding_office_id', models.TextField(blank=True, null=True)),
                ('sub_funding_office_name', models.TextField(blank=True, null=True)),
                ('sub_naics', models.TextField(blank=True, null=True)),
                ('sub_cfda_numbers', models.TextField(blank=True, null=True)),
                ('sub_dunsplus4', models.TextField(blank=True, null=True)),
                ('sub_recovery_subcontract_amt', models.TextField(blank=True, null=True)),
                ('sub_recovery_model_q1', models.BooleanField(blank=True, null=True)),
                ('sub_recovery_model_q2', models.BooleanField(blank=True, null=True)),
                ('sub_compensation_q1', models.BooleanField(blank=True, null=True)),
                ('sub_compensation_q2', models.BooleanField(blank=True, null=True)),
                ('prime_award_group', models.TextField(blank=True, null=True)),
                ('prime_award_type', models.TextField(blank=True, null=True)),
                ('piid', models.TextField(blank=True, null=True)),
                ('fain', models.TextField(blank=True, null=True)),
                ('latest_transaction_id', models.BigIntegerField(blank=True, null=True)),
                ('last_modified_date', models.DateField(blank=True, null=True)),
                ('awarding_toptier_agency_name', models.TextField(blank=True, null=True)),
                ('awarding_toptier_agency_abbreviation', models.TextField(blank=True, null=True)),
                ('awarding_subtier_agency_name', models.TextField(blank=True, null=True)),
                ('awarding_subtier_agency_abbreviation', models.TextField(blank=True, null=True)),
                ('funding_toptier_agency_name', models.TextField(blank=True, null=True)),
                ('funding_toptier_agency_abbreviation', models.TextField(blank=True, null=True)),
                ('funding_subtier_agency_name', models.TextField(blank=True, null=True)),
                ('funding_subtier_agency_abbreviation', models.TextField(blank=True, null=True)),
                ('cfda_number', models.TextField(blank=True, null=True)),
                ('cfda_title', models.TextField(blank=True, null=True)),
                ('sub_fiscal_year', models.IntegerField()),
                ('sub_total_obl_bin', models.TextField()),
                ('sub_awardee_or_recipient_legal', models.TextField(blank=True, null=True)),
                ('sub_ultimate_parent_legal_enti', models.TextField(blank=True, null=True)),
                ('business_type_code', models.TextField(blank=True, null=True)),
                ('business_categories', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None, null=True)),
                ('treasury_account_identifiers', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=None, null=True, size=None)),
                ('pulled_from', models.TextField(blank=True, null=True)),
                ('type_of_contract_pricing', models.TextField(blank=True, null=True)),
                ('type_set_aside', models.TextField(blank=True, null=True)),
                ('extent_competed', models.TextField(blank=True, null=True)),
                ('product_or_service_code', models.TextField(blank=True, null=True)),
                ('product_or_service_description', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_country_code', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_country_name', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_county_code', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_county_name', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_zip5', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_city_code', models.TextField(blank=True, null=True)),
                ('sub_legal_entity_congressional', models.TextField(blank=True, null=True)),
                ('place_of_perform_scope', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_country_co', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_country_name', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_county_code', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_county_name', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_zip5', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_city_code', models.TextField(blank=True, null=True)),
                ('sub_place_of_perform_congressio', models.TextField(blank=True, null=True)),
                ('keyword_ts_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('award_ts_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('recipient_name_ts_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('award', models.BigIntegerField(null=True, db_column="award_id")),
                ('awarding_agency', models.IntegerField(null=True, db_column="awarding_agency_id")),
                ('cfda', models.IntegerField(null=True, db_column="cfda_id")),
                ('funding_agency', models.IntegerField(null=True, db_column="funding_agency_id")),
            ],
            options={
                'db_table': 'subaward_search',
            },
        ),
        # Trick Django into believing this is a foreign primary key for purposes of using the ORM,
        # but avoid the headache that comes with foreign keys and the primary key constraint
        migrations.RunSQL(
            sql='',
            reverse_sql="",
            state_operations=[
                migrations.AlterField(
                    model_name='subawardsearch',
                    name='award',
                    field=models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='subawardsearch',
                        to='awards.award'
                    )
                )
            ]
        ),
        migrations.RunSQL(
            sql='',
            reverse_sql="",
            state_operations=[
                migrations.AlterField(
                    model_name='subawardsearch',
                    name='awarding_agency',
                    field=models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='awarding_subawardsearch',
                        to='references.agency'
                    )
                )
            ]
        ),
        migrations.RunSQL(
            sql='',
            reverse_sql="",
            state_operations=[
                migrations.AlterField(
                    model_name='subawardsearch',
                    name='funding_agency',
                    field=models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='funding_subawardsearch',
                        to='references.agency'
                    )
                )
            ]
        ),
        migrations.RunSQL(
            sql='',
            reverse_sql="",
            state_operations=[
                migrations.AlterField(
                    model_name='subawardsearch',
                    name='cfda',
                    field=models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='related_subawardsearch',
                        to='references.cfda'
                    )
                )
            ]
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(fields=['award_id'], name='ss_idx_award_id'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('prime_award_type__isnull', False)), fields=['prime_award_type'], name='ss_idx_prime_award_type'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('subaward_number'), descending=True, nulls_last=True), name='ss_idx_ordered_subaward_number'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('prime_award_type'), descending=True, nulls_last=True), name='ss_idx_order_prime_award_type'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.functions.text.Upper('fain'), descending=True, nulls_last=True), condition=models.Q(('fain__isnull', False)), name='ss_idx_ordered_fain'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.functions.text.Upper('piid'), descending=True, nulls_last=True), condition=models.Q(('piid__isnull', False)), name='ss_idx_ordered_piid'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('subaward_amount__isnull', False)), fields=['subaward_amount'], name='ss_idx_subaward_amount'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('subaward_amount'), descending=True, nulls_last=True), name='ss_idx_ordered_subaward_amount'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(fields=['sub_total_obl_bin'], name='ss_idx_sub_total_obl_bin'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['sub_awardee_or_recipient_legal'], name='ss_idx_gin_sub_recp_name', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_awardee_or_recipient_legal__isnull', False)), fields=['sub_awardee_or_recipient_legal'], name='ss_idx_sub_recp_name'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_awardee_or_recipient_uniqu__isnull', False)), fields=['sub_awardee_or_recipient_uniqu'], name='ss_idx_sub_duns'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_awardee_or_recipient_uei__isnull', False)), fields=['sub_awardee_or_recipient_uei'], name='ss_idx_sub_uei'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_ultimate_parent_unique_ide__isnull', False)), fields=['sub_ultimate_parent_unique_ide'], name='ss_idx_sub_parent_duns'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_ultimate_parent_uei__isnull', False)), fields=['sub_ultimate_parent_uei'], name='ss_idx_sub_parent_uei'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('sub_action_date'), descending=True, nulls_last=True), name='ss_idx_sub_action_date'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('last_modified_date'), descending=True, nulls_last=True), name='ss_idx_last_modified_date'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('sub_fiscal_year'), descending=True, nulls_last=True), name='ss_idx_sub_fiscal_year'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('awarding_agency_id'), nulls_last=True), condition=models.Q(('awarding_agency_id__isnull', False)), name='ss_idx_awarding_agency_id'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('funding_agency_id'), nulls_last=True), condition=models.Q(('funding_agency_id__isnull', False)), name='ss_idx_funding_agency_id'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('awarding_toptier_agency_name'), descending=True, nulls_last=True), name='ss_idx_order_awarding_top_name'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.F('awarding_subtier_agency_name'), descending=True, nulls_last=True), name='ss_idx_order_awarding_sub_name'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('awarding_toptier_agency_name__isnull', False)), fields=['awarding_toptier_agency_name'], name='ss_idx_awarding_top_agency_nam'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('awarding_subtier_agency_name__isnull', False)), fields=['awarding_subtier_agency_name'], name='ss_idx_awarding_sub_agency_nam'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('funding_toptier_agency_name__isnull', False)), fields=['funding_toptier_agency_name'], name='ss_idx_funding_top_agency_name'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('funding_subtier_agency_name__isnull', False)), fields=['funding_subtier_agency_name'], name='ss_idx_funding_sub_agency_name'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_legal_entity_country_code__isnull', False)), fields=['sub_legal_entity_country_code'], name='ss_idx_sub_le_country_code'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_legal_entity_state_code__isnull', False)), fields=['sub_legal_entity_state_code'], name='ss_idx_sub_le_state_code'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_legal_entity_county_code__isnull', False)), fields=['sub_legal_entity_county_code'], name='ss_idx_sub_le_county_code'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_legal_entity_zip5__isnull', False)), fields=['sub_legal_entity_zip5'], name='ss_idx_sub_le_zip5'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_legal_entity_congressional__isnull', False)), fields=['sub_legal_entity_congressional'], name='ss_idx_sub_le_congressional'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_legal_entity_city_name__isnull', False)), fields=['sub_legal_entity_city_name'], name='ss_idx_sub_le_city_name'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_place_of_perform_country_co__isnull', False)), fields=['sub_place_of_perform_country_co'], name='ss_idx_sub_ppop_country_co'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_place_of_perform_state_code__isnull', False)), fields=['sub_place_of_perform_state_code'], name='ss_idx_sub_ppop_state_code'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_place_of_perform_county_code__isnull', False)), fields=['sub_place_of_perform_county_code'], name='ss_idx_sub_ppop_county_code'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_place_of_perform_zip5__isnull', False)), fields=['sub_place_of_perform_zip5'], name='ss_idx_sub_ppop_zip5'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_place_of_perform_congressio__isnull', False)), fields=['sub_place_of_perform_congressio'], name='ss_idx_sub_ppop_congressio'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('sub_place_of_perform_city_name__isnull', False)), fields=['sub_place_of_perform_city_name'], name='ss_idx_sub_ppop_city_name'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('cfda_number__isnull', False)), fields=['cfda_number'], name='ss_idx_cfda_number'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('type_of_contract_pricing__isnull', False)), fields=['type_of_contract_pricing'], name='ss_idx_type_of_contract_pricin'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('extent_competed__isnull', False)), fields=['extent_competed'], name='ss_idx_extent_competed'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('type_set_aside__isnull', False)), fields=['type_set_aside'], name='ss_idx_type_set_aside'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(condition=models.Q(('product_or_service_code__isnull', False)), fields=['product_or_service_code'], name='ss_idx_product_service_code'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['product_or_service_description'], name='ss_idx_gin_product_service_des', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['business_categories'], name='ss_idx_gin_business_categories'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['keyword_ts_vector'], name='ss_idx_gin_keyword_ts_vector'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['award_ts_vector'], name='ss_idx_gin_award_ts_vector'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['recipient_name_ts_vector'], name='ss_idx_gin_recip_name_ts_vecto'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['treasury_account_identifiers'], name='ss_idx_gin_treasury_account_id', opclasses=['gin__int_ops']),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(fields=['product_or_service_code', 'sub_action_date'], name='ss_idx_comp_psc_sub_action_dat'),
        ),
        migrations.AddIndex(
            model_name='subawardsearch',
            index=models.Index(fields=['cfda_number', 'sub_action_date'], name='ss_idx_comp_cfda_sub_action_da'),
        ),
    ]
