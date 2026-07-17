"""v0_2_architectural_migration

Revision ID: 257167865ef7
Revises: 615f76e823e4
Create Date: 2026-07-16 16:01:00.727066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '257167865ef7'
down_revision = '615f76e823e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add new nullable columns natively (no batch alter to avoid temp table conflicts)
    op.add_column('users', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.add_column('sites', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.add_column('assets', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.add_column('assets', sa.Column('project_id', sa.Integer(), nullable=True))
    op.add_column('scans', sa.Column('project_id', sa.Integer(), nullable=True))
    op.add_column('signals', sa.Column('asset_id', sa.Integer(), nullable=True))

    # 2. Copy the data from the old columns to the new columns
    op.execute("UPDATE users SET organization_id = company_id")
    op.execute("UPDATE sites SET organization_id = company_id")
    op.execute("UPDATE assets SET organization_id = company_id, project_id = site_id")
    op.execute("UPDATE scans SET project_id = site_id")

    # 3. Create new assets from sites url and name (do it before sites is renamed to projects)
    op.execute("""
        INSERT INTO assets (name, asset_type, value, description, is_active, organization_id, project_id, created_at, updated_at)
        SELECT name || ' - Web Application', 'web_application', url, 'Ativo gerado na migração do Site original', 1, organization_id, id, created_at, updated_at
        FROM sites
    """)

    # 4. Populate signals.asset_id and scans.asset_id from the new assets
    op.execute("""
        UPDATE signals
        SET asset_id = (
            SELECT id FROM assets 
            WHERE assets.project_id = signals.site_id AND assets.asset_type = 'web_application' 
            LIMIT 1
        )
        WHERE site_id IS NOT NULL
    """)

    op.execute("""
        UPDATE scans
        SET asset_id = (
            SELECT id FROM assets 
            WHERE assets.project_id = scans.project_id AND assets.asset_type = 'web_application' 
            LIMIT 1
        )
        WHERE asset_id IS NULL AND project_id IS NOT NULL
    """)

    # 5. Create dummy tables to satisfy reflection of new foreign keys pointing to organizations and projects
    op.create_table('organizations', sa.Column('id', sa.Integer(), primary_key=True))
    op.create_table('projects', sa.Column('id', sa.Integer(), primary_key=True))

    # Clear SQLAlchemy reflection cache
    sa.inspect(op.get_bind()).clear_cache()

    # 6. Run exactly ONE batch alter on each table to drop old columns, add foreign keys, and update indexes
    # users
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('ix_users_company_id')
        batch_op.drop_column('company_id')
        batch_op.create_foreign_key('fk_users_organization', 'organizations', ['organization_id'], ['id'])
        batch_op.create_index('ix_users_organization_id', ['organization_id'])

    # assets
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.drop_index('ix_assets_company_id')
        batch_op.drop_index('ix_assets_site_id')
        batch_op.drop_column('company_id')
        batch_op.drop_column('site_id')
        batch_op.create_foreign_key('fk_assets_organization', 'organizations', ['organization_id'], ['id'])
        batch_op.create_foreign_key('fk_assets_project', 'projects', ['project_id'], ['id'])
        batch_op.create_index('ix_assets_organization_id', ['organization_id'])
        batch_op.create_index('ix_assets_project_id', ['project_id'])

    # scans
    with op.batch_alter_table('scans', schema=None) as batch_op:
        batch_op.drop_index('ix_scans_site_id')
        batch_op.drop_column('site_id')
        batch_op.create_foreign_key('fk_scans_project', 'projects', ['project_id'], ['id'])
        batch_op.create_index('ix_scans_project_id', ['project_id'])

    # signals
    with op.batch_alter_table('signals', schema=None) as batch_op:
        batch_op.drop_column('site_id')
        batch_op.create_foreign_key('fk_signals_asset', 'assets', ['asset_id'], ['id'])

    # companies
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_index('ix_companies_id')
        batch_op.create_index('ix_organizations_id', ['id'])

    # sites
    with op.batch_alter_table('sites', schema=None) as batch_op:
        batch_op.drop_index('ix_sites_company_id')
        batch_op.drop_column('company_id')
        batch_op.drop_column('url')
        batch_op.create_foreign_key('fk_projects_organization', 'organizations', ['organization_id'], ['id'])
        batch_op.create_index('ix_projects_organization_id', ['organization_id'])
        batch_op.drop_index('ix_sites_id')
        batch_op.create_index('ix_projects_id', ['id'])

    # 7. Drop the dummy tables
    op.drop_table('organizations')
    op.drop_table('projects')

    # 8. Rename companies to organizations, and sites to projects
    op.rename_table('companies', 'organizations')
    op.rename_table('sites', 'projects')


def downgrade() -> None:
    # 1. Create dummy tables to satisfy reflection of old foreign keys pointing to companies and sites
    op.create_table('companies', sa.Column('id', sa.Integer(), primary_key=True))
    op.create_table('sites', sa.Column('id', sa.Integer(), primary_key=True))

    # 2. Add back columns natively (no batch alter to avoid temp table conflicts)
    op.add_column('projects', sa.Column('url', sa.String(255), nullable=True))
    op.add_column('projects', sa.Column('company_id', sa.Integer(), nullable=True))
    op.add_column('signals', sa.Column('site_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('company_id', sa.Integer(), nullable=True))
    op.add_column('assets', sa.Column('company_id', sa.Integer(), nullable=True))
    op.add_column('assets', sa.Column('site_id', sa.Integer(), nullable=True))
    op.add_column('scans', sa.Column('site_id', sa.Integer(), nullable=True))

    # 3. Copy the data from the new columns to the old columns
    op.execute("""
        UPDATE projects
        SET url = (
            SELECT value FROM assets 
            WHERE assets.project_id = projects.id AND assets.asset_type = 'web_application' 
            LIMIT 1
        )
    """)
    op.execute("""
        UPDATE signals
        SET site_id = (
            SELECT project_id FROM assets WHERE assets.id = signals.asset_id LIMIT 1
        )
    """)
    op.execute("UPDATE users SET company_id = organization_id")
    op.execute("UPDATE projects SET company_id = organization_id")
    op.execute("UPDATE assets SET company_id = organization_id, site_id = project_id")
    op.execute("UPDATE scans SET site_id = project_id")

    # 4. Drop the assets that were auto-created
    op.execute("DELETE FROM assets WHERE description = 'Ativo gerado na migração do Site original'")

    # Clear SQLAlchemy reflection cache
    sa.inspect(op.get_bind()).clear_cache()

    # 5. Run exactly ONE batch alter on each table to drop new columns and restore old foreign keys & indexes
    # users
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('ix_users_organization_id')
        batch_op.drop_column('organization_id')
        batch_op.create_foreign_key('fk_users_company', 'companies', ['company_id'], ['id'])
        batch_op.create_index('ix_users_company_id', ['company_id'])

    # assets
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.drop_index('ix_assets_organization_id')
        batch_op.drop_index('ix_assets_project_id')
        batch_op.drop_column('organization_id')
        batch_op.drop_column('project_id')
        batch_op.create_foreign_key('fk_assets_company', 'companies', ['company_id'], ['id'])
        batch_op.create_foreign_key('fk_assets_site', 'sites', ['site_id'], ['id'])
        batch_op.create_index('ix_assets_company_id', ['company_id'])
        batch_op.create_index('ix_assets_site_id', ['site_id'])

    # scans
    with op.batch_alter_table('scans', schema=None) as batch_op:
        batch_op.drop_index('ix_scans_project_id')
        batch_op.drop_column('project_id')
        batch_op.create_foreign_key('fk_scans_site', 'sites', ['site_id'], ['id'])
        batch_op.create_index('ix_scans_site_id', ['site_id'])

    # signals
    with op.batch_alter_table('signals', schema=None) as batch_op:
        batch_op.drop_column('asset_id')
        batch_op.create_foreign_key('fk_signals_site', 'sites', ['site_id'], ['id'])

    # organizations
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.drop_index('ix_organizations_id')
        batch_op.create_index('ix_companies_id', ['id'])

    # projects
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_index('ix_projects_organization_id')
        batch_op.drop_column('organization_id')
        batch_op.create_foreign_key('fk_sites_company', 'companies', ['company_id'], ['id'])
        batch_op.create_index('ix_sites_company_id', ['company_id'])
        batch_op.drop_index('ix_projects_id')
        batch_op.create_index('ix_sites_id', ['id'])

    # 6. Drop the dummy tables
    op.drop_table('companies')
    op.drop_table('sites')

    # 7. Rename projects to sites, and organizations to companies
    op.rename_table('projects', 'sites')
    op.rename_table('organizations', 'companies')
