"""
ETL: fintech_replica (esquema viejo) → fintech_nueva (esquema nuevo).

Uso:
    DATABASE_URL="postgresql://postgres@localhost/fintech_nueva" \\
    python manage.py migrar_datos --origen "postgresql://postgres@localhost/fintech_replica"
"""
import psycopg
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Migra datos de fintech_replica a fintech_nueva'

    def add_arguments(self, parser):
        parser.add_argument('--origen', default='postgresql://postgres@localhost/fintech_replica')
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        self.dry = options['dry_run']
        if self.dry:
            self.stdout.write(self.style.WARNING('--- DRY RUN ---'))

        with psycopg.connect(options['origen']) as old:
            self.old = old.cursor()
            self.admin_map = {}  # {old auth_user.id: new fintech_user.id}
            self._run()

    # ------------------------------------------------------------------ #

    def _run(self):
        pasos = [
            ('Country',          self._country),
            ('DocumentType',     self._documenttype),
            ('CategoryType',     self._categorytype),
            ('Category',         self._category),
            ('SubCategory',      self._subcategory),
            ('Currency',         self._currency),
            ('Periodicity',      self._periodicity),
            ('Label',            self._label),
            ('Role',             self._role),
            ('PhoneNumber',      self._phonenumber),
            ('Identifier',       self._identifier),
            ('Adjustment',       self._adjustment),
            ('Account',          self._account),
            ('Clientes→User',    self._clientes),
            ('Admins→User',      self._admins),
            ('Seller',           self._seller),
            ('Credit',           self._credit),
            ('Installment',      self._installment),
            ('Transaction',           self._transaction),
            ('AccountMethodAmount',   self._account_method_amount),
            ('Expense',               self._expense),
            ('CreditEarnings',        self._credit_earnings),
        ]
        for label, fn in pasos:
            self.stdout.write(f'→ {label}... ', ending='')
            n = fn()
            self.stdout.write(self.style.SUCCESS(f'{n} registros'))
        self.stdout.write(self.style.SUCCESS('\n✓ Migración completada'))

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _fetch(self, sql, params=None):
        self.old.execute(sql, params)
        cols = [d.name for d in self.old.description]
        return cols, self.old.fetchall()

    def _insert_batch(self, table, cols, rows, batch=500):
        if self.dry or not rows:
            return len(rows)
        placeholders = ', '.join(['%s'] * len(cols))
        col_str = ', '.join(f'"{c}"' for c in cols)
        sql = f'INSERT INTO {table} ({col_str}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING'
        with connection.cursor() as dest:
            for i in range(0, len(rows), batch):
                dest.executemany(sql, rows[i:i+batch])
        return len(rows)

    def _reset_seq(self, table, pk='id'):
        if self.dry:
            return
        with connection.cursor() as c:
            seq = f"{table}_{pk}_seq"
            c.execute(f"SELECT setval('{seq}', COALESCE((SELECT MAX({pk}) FROM {table}), 1))")

    # ------------------------------------------------------------------ #
    # CATÁLOGOS
    # ------------------------------------------------------------------ #

    def _country(self):
        cols, rows = self._fetch("SELECT id, name, utc_offset FROM fintech_country")
        return self._insert_batch('fintech_country', cols, rows)

    def _documenttype(self):
        cols, rows = self._fetch("SELECT id, code, description, country_id_id FROM fintech_documenttype")
        return self._insert_batch('fintech_documenttype', cols, rows)

    def _categorytype(self):
        cols, rows = self._fetch("SELECT id, uid, name, description FROM fintech_categorytype")
        return self._insert_batch('fintech_categorytype', cols, rows)

    def _category(self):
        cols, rows = self._fetch("SELECT id, uid, name, created_at, updated_at, category_type_id FROM fintech_category")
        return self._insert_batch('fintech_category', cols, rows)

    def _subcategory(self):
        cols, rows = self._fetch("SELECT id, uid, name, description, created_at, updated_at, category_id FROM fintech_subcategory")
        return self._insert_batch('fintech_subcategory', cols, rows)

    def _currency(self):
        cols, rows = self._fetch("SELECT id, asset_type, id_currency, currency, exchange_rate FROM fintech_currency")
        return self._insert_batch('fintech_currency', cols, rows)

    def _periodicity(self):
        cols, rows = self._fetch("SELECT id, name, days FROM fintech_periodicity")
        return self._insert_batch('fintech_periodicity', cols, rows)

    def _label(self):
        cols, rows = self._fetch("SELECT id, uid, name, position FROM fintech_label")
        return self._insert_batch('fintech_label', cols, rows)

    def _role(self):
        cols, rows = self._fetch("SELECT id, name, is_staff_role FROM fintech_role")
        return self._insert_batch('fintech_role', cols, rows)

    def _phonenumber(self):
        cols, rows = self._fetch("SELECT id, country_code, phone_number, country_related_id FROM fintech_phonenumber")
        return self._insert_batch('fintech_phonenumber', cols, rows)

    def _identifier(self):
        cols, rows = self._fetch("SELECT id, document_number, country_id, document_type_id FROM fintech_identifier")
        return self._insert_batch('fintech_identifier', cols, rows)

    def _adjustment(self):
        cols, rows = self._fetch("SELECT id, uid, code, name, description, is_positive FROM fintech_adjustment")
        return self._insert_batch('fintech_adjustment', cols, rows)

    def _account(self):
        cols, rows = self._fetch(
            "SELECT id_payment_method, name, account_number, balance, eletronic_software_id, currency_id FROM fintech_account"
        )
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO fintech_account
                   (id_payment_method, name, account_number, balance, eletronic_software_id, currency_id)
                 VALUES (%s, %s, %s, %s, %s, %s)
                 ON CONFLICT (id_payment_method) DO NOTHING"""
        with connection.cursor() as dest:
            dest.executemany(sql, rows)
        return len(rows)

    # ------------------------------------------------------------------ #
    # USUARIOS
    # ------------------------------------------------------------------ #

    def _clientes(self):
        """605 clientes de fintech_user → preservar IDs exactos."""
        cols, rows = self._fetch("""
            SELECT id, password, last_login, is_superuser, username,
                   first_name, last_name, email, is_staff, is_active, date_joined,
                   id_user, billing_address, address_shipping, reference_1, reference_2,
                   electronic_id, city_id, country_id, document_id, label_id, phone_1_id, role_id
            FROM fintech_user
            ORDER BY id
        """)
        if not self.dry:
            sql = """INSERT INTO fintech_user
                       (id, password, last_login, is_superuser, username,
                        first_name, last_name, email, is_staff, is_active, date_joined,
                        id_user, billing_address, address_shipping, reference_1, reference_2,
                        electronic_id, city_id, country_id, document_id, label_id, phone_1_id, role_id)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     ON CONFLICT (id) DO NOTHING"""
            with connection.cursor() as dest:
                dest.executemany(sql, rows)
            self._reset_seq('fintech_user')
        return len(rows)

    def _admins(self):
        """6 admins de auth_user → insertar en fintech_user SIN id explícito.
        PostgreSQL asigna IDs 606+. Se construye admin_map para actualizar FKs."""
        cols, rows = self._fetch("""
            SELECT id, password, last_login, is_superuser, username,
                   first_name, last_name, email, is_staff, is_active, date_joined
            FROM auth_user
            ORDER BY id
        """)
        if self.dry:
            next_id = 606
            for row in rows:
                old_id = row[0]
                self.admin_map[old_id] = next_id
                next_id += 1
            return len(rows)

        sql = """INSERT INTO fintech_user
                   (password, last_login, is_superuser, username,
                    first_name, last_name, email, is_staff, is_active, date_joined,
                    id_user, billing_address, address_shipping, reference_1, reference_2,
                    electronic_id)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,gen_random_uuid(),'','',NULL,NULL,NULL)
                 RETURNING id"""
        with connection.cursor() as dest:
            for row in rows:
                old_id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined = row
                dest.execute(sql, (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined))
                new_id = dest.fetchone()[0]
                self.admin_map[old_id] = new_id

        detalle = ', '.join(f'{k}→{v}' for k, v in self.admin_map.items())
        self.stdout.write(f'\n  Mapa admin IDs: {detalle}')
        return len(rows)

    # ------------------------------------------------------------------ #
    # NEGOCIO
    # ------------------------------------------------------------------ #

    def _seller(self):
        cols, rows = self._fetch("SELECT id, total_sales, commissions, returns, role_id, user_id FROM fintech_seller")
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO fintech_seller (id, total_sales, commissions, returns, role_id, user_id)
                 VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING"""
        with connection.cursor() as dest:
            mapped = []
            for row in rows:
                s_id, total_sales, commissions, returns, role_id, old_user_id = row
                new_user_id = self.admin_map.get(old_user_id)
                if new_user_id is None:
                    raise ValueError(f'Seller id={s_id}: sin mapeo para auth_user.id={old_user_id}. admin_map={self.admin_map}')
                mapped.append((s_id, total_sales, commissions, returns, role_id, new_user_id))
            dest.executemany(sql, mapped)
        return len(rows)

    def _credit(self):
        cols, rows = self._fetch("""
            SELECT id, uid, state, cost, price, earnings,
                   first_date_payment, second_date_payment, credit_days, description,
                   interest, refinancing, total_abonos, pending_amount,
                   installment_number, installment_value, is_in_default,
                   created_at, updated_at, morosidad_level,
                   currency_id, payment_id, periodicity_id,
                   registered_by_id, seller_id, subcategory_id, user_id
            FROM fintech_credit
        """)
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO fintech_credit
                   (id, uid, state, cost, price, earnings,
                    first_date_payment, second_date_payment, credit_days, description,
                    interest, refinancing, total_abonos, pending_amount,
                    installment_number, installment_value, is_in_default,
                    created_at, updated_at, morosidad_level,
                    currency_id, payment_id, periodicity_id,
                    registered_by_id, seller_id, subcategory_id, user_id)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 ON CONFLICT (id) DO NOTHING"""
        with connection.cursor() as dest:
            mapped = []
            for row in rows:
                row = list(row)
                # registered_by_id está en posición 23
                old_rb = row[23]
                if old_rb is not None:
                    row[23] = self.admin_map.get(old_rb, old_rb)
                mapped.append(tuple(row))
            for i in range(0, len(mapped), 500):
                dest.executemany(sql, mapped[i:i+500])
        self._reset_seq('fintech_credit')
        return len(rows)

    def _installment(self):
        cols, rows = self._fetch("""
            SELECT id, number, due_date, amount, paid, paid_on,
                   principal_amount, interest_amount, late_fee, status,
                   notification_sent, reminder_count, last_reminder_date,
                   next_reminder_date, amount_paid, remaining_amount,
                   days_overdue, is_scheduled, scheduled_payment_date,
                   created_at, updated_at, credit_id
            FROM fintech_installment
        """)
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO fintech_installment
                   (id, number, due_date, amount, paid, paid_on,
                    principal_amount, interest_amount, late_fee, status,
                    notification_sent, reminder_count, last_reminder_date,
                    next_reminder_date, amount_paid, remaining_amount,
                    days_overdue, is_scheduled, scheduled_payment_date,
                    created_at, updated_at, credit_id)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 ON CONFLICT (id) DO NOTHING"""
        with connection.cursor() as dest:
            for i in range(0, len(rows), 500):
                dest.executemany(sql, rows[i:i+500])
        self._reset_seq('fintech_installment')
        return len(rows)

    def _transaction(self):
        cols, rows = self._fetch("""
            SELECT id, uid, transaction_type, date, description,
                   category_id, user_id, agent_id, source, status
            FROM fintech_transaction
        """)
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO fintech_transaction
                   (id, uid, transaction_type, date, description,
                    category_id, user_id, agent_id, source, status)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 ON CONFLICT (id) DO NOTHING"""
        with connection.cursor() as dest:
            for i in range(0, len(rows), 500):
                dest.executemany(sql, rows[i:i+500])
        self._reset_seq('fintech_transaction')
        return len(rows)

    def _expense(self):
        cols, rows = self._fetch("""
            SELECT id, uid, amount, description, date,
                   account_id, subcategory_id, registered_by_id, user_id, created_at, updated_at
            FROM fintech_expense
        """)
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO fintech_expense
                   (id, uid, amount, description, date,
                    account_id, subcategory_id, registered_by_id, user_id, created_at, updated_at)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 ON CONFLICT (id) DO NOTHING"""
        with connection.cursor() as dest:
            mapped = []
            for row in rows:
                row = list(row)
                # registered_by_id en posición 7
                old_rb = row[7]
                if old_rb is not None:
                    row[7] = self.admin_map.get(old_rb, old_rb)
                mapped.append(tuple(row))
            dest.executemany(sql, mapped)
        self._reset_seq('fintech_expense')
        return len(rows)

    def _account_method_amount(self):
        cols, rows = self._fetch("""
            SELECT id, payment_code, amount, amount_paid, credit_id, currency_id, payment_method_id, transaction_id
            FROM fintech_accountmethodamount
        """)
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO fintech_accountmethodamount
                   (id, payment_code, amount, amount_paid, credit_id, currency_id, payment_method_id, transaction_id)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                 ON CONFLICT (id) DO NOTHING"""
        with connection.cursor() as dest:
            for i in range(0, len(rows), 500):
                dest.executemany(sql, rows[i:i+500])
        self._reset_seq('fintech_accountmethodamount')
        return len(rows)

    def _credit_earnings(self):
        cols, rows = self._fetch("""
            SELECT id, theoretical_earnings, realized_earnings, earnings_rate, updated_at, credit_id
            FROM revenue_creditearnings
        """)
        if self.dry or not rows:
            return len(rows)
        sql = """INSERT INTO revenue_creditearnings
                   (id, theoretical_earnings, realized_earnings, earnings_rate, updated_at, credit_id)
                 VALUES (%s,%s,%s,%s,%s,%s)
                 ON CONFLICT (id) DO NOTHING"""
        with connection.cursor() as dest:
            dest.executemany(sql, rows)
        self._reset_seq('revenue_creditearnings')
        return len(rows)
