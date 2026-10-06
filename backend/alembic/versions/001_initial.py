"""initial_migration_with_all_fields

Revision ID: 001_initial
Revises: 
Create Date: 2026-06-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу persons со всеми полями
    op.create_table(
        'persons',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('short_name', sa.String(length=100), nullable=False),
        sa.Column('photo_path', sa.String(length=500), nullable=True),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('weight', sa.Integer(), nullable=True),
        sa.Column('clothing_size', sa.String(length=50), nullable=True),
        sa.Column('shoe_size', sa.Integer(), nullable=True),
        sa.Column('chest_size', sa.Integer(), nullable=True),
        sa.Column('waist_size', sa.Integer(), nullable=True),
        sa.Column('hip_size', sa.Integer(), nullable=True),
        sa.Column('blood_type', sa.String(length=10), nullable=True),
        sa.Column('rh_factor', sa.String(length=5), nullable=True),
        sa.Column('allergies', sa.Text(), nullable=True),
        sa.Column('chronic_diseases', sa.Text(), nullable=True),
        sa.Column('medications', sa.Text(), nullable=True),
        sa.Column('blood_pressure', sa.String(length=50), nullable=True),
        sa.Column('heart_rate', sa.Integer(), nullable=True),
        sa.Column('passport_number', sa.String(length=50), nullable=True),
        sa.Column('inn', sa.String(length=50), nullable=True),
        sa.Column('snils', sa.String(length=50), nullable=True),
        sa.Column('driver_license_category', sa.String(length=50), nullable=True),
        sa.Column('driver_license_number', sa.String(length=50), nullable=True),
        sa.Column('marital_status', sa.String(length=50), nullable=True),
        sa.Column('children_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('education', sa.String(length=255), nullable=True),
        sa.Column('profession', sa.String(length=255), nullable=True),
        sa.Column('workplace', sa.String(length=255), nullable=True),
        sa.Column('favorite_color', sa.String(length=100), nullable=True),
        sa.Column('favorite_flowers', sa.String(length=255), nullable=True),
        sa.Column('favorite_food', sa.String(length=255), nullable=True),
        sa.Column('favorite_music', sa.String(length=255), nullable=True),
        sa.Column('favorite_movies', sa.String(length=255), nullable=True),
        sa.Column('hobbies', sa.Text(), nullable=True),
        sa.Column('importance', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('importance_level', sa.String(length=20), nullable=True, server_default='medium'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        # Новые поля
        sa.Column('alcohol_habit', sa.Boolean(), nullable=True),
        sa.Column('alcohol_preference', sa.Text(), nullable=True),
        sa.Column('alcohol_frequency', sa.String(length=20), nullable=True),
        sa.Column('appearance_build', sa.String(length=30), nullable=True),
        sa.Column('appearance_posture', sa.String(length=30), nullable=True),
        sa.Column('appearance_gait', sa.String(length=30), nullable=True),
        sa.Column('tattoos', mysql.JSON(), nullable=True),
        sa.Column('piercings', mysql.JSON(), nullable=True),
        sa.Column('scars', mysql.JSON(), nullable=True),
        sa.Column('special_marks', sa.Text(), nullable=True),
        sa.Column('scent', sa.Text(), nullable=True),
        sa.Column('voice', sa.Text(), nullable=True),
        sa.Column('sexual_orientation', sa.String(length=50), nullable=True),
        sa.Column('relationship_style', sa.String(length=50), nullable=True),
        sa.Column('relationship_start_date', sa.Date(), nullable=True),
        sa.Column('relationship_commitment_level', sa.String(length=20), nullable=True),
        sa.Column('children_ages', mysql.JSON(), nullable=True),
        sa.Column('children_plans', sa.String(length=50), nullable=True),
        sa.Column('marriage_plans', sa.String(length=50), nullable=True),
        sa.Column('living_together', sa.Boolean(), nullable=True),
        sa.Column('breast_size', sa.String(length=10), nullable=True),
        sa.Column('breast_cup', sa.String(length=5), nullable=True),
        sa.Column('breast_band', sa.Integer(), nullable=True),
        sa.Column('breast_volume', sa.String(length=20), nullable=True),
        sa.Column('breast_shape', sa.String(length=30), nullable=True),
        sa.Column('nipple_type', sa.String(length=30), nullable=True),
        sa.Column('nipple_color', sa.String(length=20), nullable=True),
        sa.Column('breast_sensitivity', sa.String(length=20), nullable=True),
        sa.Column('breast_piercing', sa.Boolean(), nullable=True),
        sa.Column('breast_implants', sa.Boolean(), nullable=True),
        sa.Column('penis_length_erect', sa.Float(), nullable=True),
        sa.Column('penis_girth_erect', sa.Float(), nullable=True),
        sa.Column('penis_length_flaccid', sa.Float(), nullable=True),
        sa.Column('penis_girth_flaccid', sa.Float(), nullable=True),
        sa.Column('penis_shape', sa.String(length=30), nullable=True),
        sa.Column('foreskin', sa.String(length=20), nullable=True),
        sa.Column('testicles_size', sa.String(length=20), nullable=True),
        sa.Column('ejaculation_volume', sa.String(length=20), nullable=True),
        sa.Column('ejaculation_control', sa.String(length=20), nullable=True),
        sa.Column('refractory_period', sa.String(length=30), nullable=True),
        sa.Column('body_hair', sa.String(length=30), nullable=True),
        sa.Column('body_hair_locations', mysql.JSON(), nullable=True),
        sa.Column('skin_sensitivity', sa.String(length=20), nullable=True),
        sa.Column('erogenous_zones', mysql.JSON(), nullable=True),
        sa.Column('tattoos_intimate', mysql.JSON(), nullable=True),
        sa.Column('piercing_intimate', mysql.JSON(), nullable=True),
        sa.Column('sex_role', sa.String(length=30), nullable=True),
        sa.Column('sex_role_description', sa.Text(), nullable=True),
        sa.Column('sex_libido', sa.String(length=20), nullable=True),
        sa.Column('sex_libido_notes', sa.Text(), nullable=True),
        sa.Column('sex_experience_level', sa.String(length=20), nullable=True),
        sa.Column('sex_energy', sa.String(length=20), nullable=True),
        sa.Column('sex_openness', sa.String(length=20), nullable=True),
        sa.Column('sex_communication', sa.String(length=20), nullable=True),
        sa.Column('sex_positions_liked', mysql.JSON(), nullable=True),
        sa.Column('sex_positions_disliked', mysql.JSON(), nullable=True),
        sa.Column('sex_positions_want_try', mysql.JSON(), nullable=True),
        sa.Column('sex_positions_rating', mysql.JSON(), nullable=True),
        sa.Column('sex_caress_liked', mysql.JSON(), nullable=True),
        sa.Column('sex_caress_disliked', mysql.JSON(), nullable=True),
        sa.Column('sex_caress_sensitive_areas', mysql.JSON(), nullable=True),
        sa.Column('sex_caress_techniques', sa.Text(), nullable=True),
        sa.Column('sex_fetishes', mysql.JSON(), nullable=True),
        sa.Column('sex_fetishes_level', sa.String(length=20), nullable=True),
        sa.Column('sex_kinks', mysql.JSON(), nullable=True),
        sa.Column('sex_taboos', mysql.JSON(), nullable=True),
        sa.Column('sex_triggers', sa.Text(), nullable=True),
        sa.Column('sex_aversions', sa.Text(), nullable=True),
        sa.Column('sex_fantasy', sa.Text(), nullable=True),
        sa.Column('sex_toys_has', sa.Boolean(), nullable=True),
        sa.Column('sex_toys_list', mysql.JSON(), nullable=True),
        sa.Column('sex_toys_want', mysql.JSON(), nullable=True),
        sa.Column('sex_toys_rating', mysql.JSON(), nullable=True),
        sa.Column('sex_condoms', sa.String(length=20), nullable=True),
        sa.Column('sex_contraception', sa.String(length=50), nullable=True),
        sa.Column('sex_std_status', sa.String(length=20), nullable=True),
        sa.Column('sex_std_test_date', sa.Date(), nullable=True),
        sa.Column('sex_std_test_result', sa.Text(), nullable=True),
        sa.Column('sex_std_notes', sa.Text(), nullable=True),
        sa.Column('sex_pain', sa.Boolean(), nullable=True),
        sa.Column('sex_pain_description', sa.Text(), nullable=True),
        sa.Column('sex_lubricant', sa.String(length=20), nullable=True),
        sa.Column('sex_lubricant_type', sa.String(length=50), nullable=True),
        sa.Column('travel_countries_visited', mysql.JSON(), nullable=True),
        sa.Column('travel_countries_want', mysql.JSON(), nullable=True),
        sa.Column('travel_favorite_places', sa.Text(), nullable=True),
        sa.Column('travel_style', sa.String(length=30), nullable=True),
        sa.Column('travel_countries_count', sa.Integer(), nullable=True),
        sa.Column('gifts_favorite_brands', mysql.JSON(), nullable=True),
        sa.Column('gifts_collects', sa.Text(), nullable=True),
        sa.Column('gifts_dream', sa.Text(), nullable=True),
        sa.Column('gifts_color_scheme', sa.String(length=100), nullable=True),
        sa.Column('gifts_hobby_supplies', sa.Text(), nullable=True),
        sa.Column('skills_languages', mysql.JSON(), nullable=True),
        sa.Column('skills_programming', mysql.JSON(), nullable=True),
        sa.Column('skills_repair', sa.Text(), nullable=True),
        sa.Column('skills_medical', sa.Text(), nullable=True),
        sa.Column('skills_driving_experience', sa.Integer(), nullable=True),
        sa.Column('skills_driving_car', sa.String(length=100), nullable=True),
        sa.Column('skills_cooking', sa.Text(), nullable=True),
        sa.Column('skills_cooking_favorites', sa.Text(), nullable=True),
        sa.Column('skills_craft', sa.Text(), nullable=True),
        sa.Column('skills_music', mysql.JSON(), nullable=True),
        sa.Column('skills_sport', mysql.JSON(), nullable=True),
        sa.Column('skills_certificates', mysql.JSON(), nullable=True),
        sa.Column('character_type', sa.String(length=30), nullable=True),
        sa.Column('character_mbti', sa.String(length=10), nullable=True),
        sa.Column('character_features', sa.Text(), nullable=True),
        sa.Column('habits_snoring', sa.Boolean(), nullable=True),
        sa.Column('habits_snoring_solution', sa.Text(), nullable=True),
        sa.Column('habits_bruxism', sa.Boolean(), nullable=True),
        sa.Column('habits_sleepwalking', sa.Boolean(), nullable=True),
        sa.Column('habits_sleep_medication', sa.String(length=50), nullable=True),
        sa.Column('habits_caffeine', sa.Integer(), nullable=True),
        sa.Column('habits_sugar', sa.Boolean(), nullable=True),
        sa.Column('habits_smoking', sa.Boolean(), nullable=True),
        sa.Column('habits_drugs', sa.Boolean(), nullable=True),
        sa.Column('sleep_schedule', sa.String(length=50), nullable=True),
        sa.Column('work_schedule', sa.String(length=30), nullable=True),
        sa.Column('work_shifts', sa.Text(), nullable=True),
        sa.Column('work_career_plans', sa.Text(), nullable=True),
        sa.Column('work_salary', sa.Float(), nullable=True),
        sa.Column('work_salary_desired', sa.Float(), nullable=True),
        sa.Column('work_colleagues', sa.Text(), nullable=True),
        sa.Column('work_manager', sa.String(length=255), nullable=True),
        sa.Column('work_projects', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('short_name')
    )
    op.create_index('ix_persons_id', 'persons', ['id'])

    # Создаем остальные таблицы (кратко)
    op.create_table(
        'relations',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('parent_id', sa.Integer(), nullable=False),
        sa.Column('child_id', sa.Integer(), nullable=False),
        sa.Column('relation_type', sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(['child_id'], ['persons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_relations_id', 'relations', ['id'])

    op.create_table(
        'social_media',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('link', sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_social_media_id', 'social_media', ['id'])

    op.create_table(
        'tags_and_prefs',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tags_and_prefs_id', 'tags_and_prefs', ['id'])

    op.create_table(
        'digital_accounts',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('platform_type', sa.String(length=50), nullable=False),
        sa.Column('platform_name', sa.String(length=100), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('password', sa.Text(), nullable=True),
        sa.Column('backup_codes', sa.Text(), nullable=True),
        sa.Column('security_questions', sa.Text(), nullable=True),
        sa.Column('account_id', sa.String(length=255), nullable=True),
        sa.Column('uid', sa.String(length=255), nullable=True),
        sa.Column('user_id', sa.String(length=255), nullable=True),
        sa.Column('friend_code', sa.String(length=255), nullable=True),
        sa.Column('server_id', sa.String(length=100), nullable=True),
        sa.Column('server_name', sa.String(length=255), nullable=True),
        sa.Column('region', sa.String(length=100), nullable=True),
        sa.Column('nickname', sa.String(length=255), nullable=True),
        sa.Column('server', sa.String(length=100), nullable=True),
        sa.Column('level', sa.Integer(), nullable=True),
        sa.Column('rank', sa.String(length=100), nullable=True),
        sa.Column('guild', sa.String(length=255), nullable=True),
        sa.Column('characters', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_digital_accounts_id', 'digital_accounts', ['id'])

    op.create_table(
        'person_cases',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('case_type', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=True, server_default='medium'),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='active'),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_person_cases_id', 'person_cases', ['id'])

    op.create_table(
        'medical_records',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('record_type', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('record_date', sa.DateTime(), nullable=True),
        sa.Column('doctor_name', sa.String(length=255), nullable=True),
        sa.Column('attachments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_medical_records_id', 'medical_records', ['id'])

    op.create_table(
        'real_estate',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('property_type', sa.String(length=50), nullable=False),
        sa.Column('property_name', sa.String(length=255), nullable=True),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('total_area', sa.Float(), nullable=True),
        sa.Column('living_area', sa.Float(), nullable=True),
        sa.Column('land_area', sa.Float(), nullable=True),
        sa.Column('floor', sa.Integer(), nullable=True),
        sa.Column('total_floors', sa.Integer(), nullable=True),
        sa.Column('rooms_count', sa.Integer(), nullable=True),
        sa.Column('bathroom_count', sa.Integer(), nullable=True),
        sa.Column('balcony_count', sa.Integer(), nullable=True),
        sa.Column('ownership_type', sa.String(length=50), nullable=True),
        sa.Column('ownership_percent', sa.Float(), nullable=True, server_default='100.0'),
        sa.Column('cadastral_number', sa.String(length=50), nullable=True),
        sa.Column('registration_date', sa.Date(), nullable=True),
        sa.Column('purchase_price', sa.Float(), nullable=True),
        sa.Column('current_value', sa.Float(), nullable=True),
        sa.Column('mortgage_bank', sa.String(length=255), nullable=True),
        sa.Column('mortgage_amount', sa.Float(), nullable=True),
        sa.Column('mortgage_left', sa.Float(), nullable=True),
        sa.Column('condition', sa.String(length=50), nullable=True),
        sa.Column('year_built', sa.Integer(), nullable=True),
        sa.Column('renovation_year', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_real_estate_id', 'real_estate', ['id'])

    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('vehicle_type', sa.String(length=50), nullable=False),
        sa.Column('brand', sa.String(length=100), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('license_plate', sa.String(length=50), nullable=True),
        sa.Column('vin', sa.String(length=50), nullable=True),
        sa.Column('engine_number', sa.String(length=100), nullable=True),
        sa.Column('chassis_number', sa.String(length=100), nullable=True),
        sa.Column('engine_capacity', sa.Float(), nullable=True),
        sa.Column('horsepower', sa.Integer(), nullable=True),
        sa.Column('mileage', sa.Integer(), nullable=True),
        sa.Column('transmission', sa.String(length=50), nullable=True),
        sa.Column('drive_type', sa.String(length=50), nullable=True),
        sa.Column('fuel_type', sa.String(length=50), nullable=True),
        sa.Column('ownership_type', sa.String(length=50), nullable=True),
        sa.Column('registration_date', sa.Date(), nullable=True),
        sa.Column('registration_number', sa.String(length=100), nullable=True),
        sa.Column('purchase_price', sa.Float(), nullable=True),
        sa.Column('current_value', sa.Float(), nullable=True),
        sa.Column('loan_bank', sa.String(length=255), nullable=True),
        sa.Column('loan_amount', sa.Float(), nullable=True),
        sa.Column('loan_left', sa.Float(), nullable=True),
        sa.Column('insurance_company', sa.String(length=255), nullable=True),
        sa.Column('insurance_policy', sa.String(length=100), nullable=True),
        sa.Column('insurance_until', sa.Date(), nullable=True),
        sa.Column('osago_until', sa.Date(), nullable=True),
        sa.Column('last_maintenance', sa.Date(), nullable=True),
        sa.Column('next_maintenance', sa.Date(), nullable=True),
        sa.Column('maintenance_notes', sa.Text(), nullable=True),
        sa.Column('condition', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_vehicles_id', 'vehicles', ['id'])

    # Создаем расширенные таблицы
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('is_system', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('sort_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['parent_id'], ['categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_categories_id', 'categories', ['id'])

    op.create_table(
        'record_tags',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_record_tags_id', 'record_tags', ['id'])

    op.create_table(
        'cross_records',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('record_type', sa.String(length=50), nullable=False),
        sa.Column('primary_category_id', sa.Integer(), nullable=False),
        sa.Column('data', mysql.JSON(), nullable=True),
        sa.Column('record_date', sa.Date(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='active'),
        sa.Column('importance', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_private', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['created_by'], ['persons.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['primary_category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cross_records_id', 'cross_records', ['id'])

    op.create_table(
        'record_tag_relations',
        sa.Column('record_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['record_id'], ['cross_records.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['record_tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('record_id', 'tag_id')
    )

    op.create_table(
        'partners',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('partner_id', sa.Integer(), nullable=False),
        sa.Column('relationship_type', sa.String(length=50), nullable=True),
        sa.Column('relationship_status', sa.String(length=20), nullable=True),
        sa.Column('relationship_label', sa.String(length=50), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('breakup_reason', sa.Text(), nullable=True),
        sa.Column('emotional_connection', sa.String(length=20), nullable=True),
        sa.Column('physical_connection', sa.String(length=20), nullable=True),
        sa.Column('relationship_rating', sa.Integer(), nullable=True),
        sa.Column('relationship_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['partner_id'], ['persons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_partners_id', 'partners', ['id'])

    op.create_table(
        'devices',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('device_type', sa.String(length=50), nullable=False),
        sa.Column('brand', sa.String(length=100), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('specs', sa.Text(), nullable=True),
        sa.Column('imei', sa.String(length=50), nullable=True),
        sa.Column('serial_number', sa.String(length=50), nullable=True),
        sa.Column('purchase_date', sa.Date(), nullable=True),
        sa.Column('purchase_price', sa.Float(), nullable=True),
        sa.Column('purchase_place', sa.String(length=255), nullable=True),
        sa.Column('warranty_until', sa.Date(), nullable=True),
        sa.Column('accessories', sa.Text(), nullable=True),
        sa.Column('condition', sa.String(length=30), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_devices_id', 'devices', ['id'])

    op.create_table(
        'audit',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('changed_by', sa.Integer(), nullable=True),
        sa.Column('changed_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('field_name', sa.String(length=100), nullable=True),
        sa.Column('old_value', sa.Text(), nullable=True),
        sa.Column('new_value', sa.Text(), nullable=True),
        sa.Column('change_reason', sa.Text(), nullable=True),
        sa.Column('viewed_by', sa.Integer(), nullable=True),
        sa.Column('viewed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['changed_by'], ['persons.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['viewed_by'], ['persons.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_audit_id', 'audit', ['id'])

    # Вставляем начальные категории
    op.execute("""
        INSERT INTO categories (name, slug, icon, color, is_system, sort_order) VALUES
        ('Общее', 'general', '📌', '#888888', 1, 0),
        ('Секс и отношения', 'sex', '❤️', '#ff6b6b', 1, 1),
        ('Медицина', 'medicine', '🩺', '#4ecdc4', 1, 2),
        ('Подарки', 'gifts', '🎁', '#ffd93d', 1, 3),
        ('Навыки', 'skills', '🔧', '#6c5ce7', 1, 4),
        ('Путешествия', 'travel', '✈️', '#74b9ff', 1, 5),
        ('Техника', 'devices', '📱', '#00b894', 1, 6),
        ('Работа', 'work', '💼', '#fdcb6e', 1, 7),
        ('Характер', 'character', '😊', '#fd79a8', 1, 8),
        ('Важные даты', 'dates', '📅', '#a29bfe', 1, 9)
    """)


def downgrade() -> None:
    op.drop_table('audit')
    op.drop_table('devices')
    op.drop_table('partners')
    op.drop_table('record_tag_relations')
    op.drop_table('cross_records')
    op.drop_table('record_tags')
    op.drop_table('categories')
    op.drop_table('vehicles')
    op.drop_table('real_estate')
    op.drop_table('medical_records')
    op.drop_table('person_cases')
    op.drop_table('digital_accounts')
    op.drop_table('tags_and_prefs')
    op.drop_table('social_media')
    op.drop_table('relations')
    op.drop_table('persons')