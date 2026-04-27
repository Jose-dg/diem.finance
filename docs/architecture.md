# Architecture

## App dependency graph

```
apps.fintech          (core domain — all other apps depend on this)
  └── models: User (clients), Credit, Installment, Transaction, Account,
              Seller, Role, Currency, Periodicity, Category/SubCategory,
              Expense, Adjustment, CreditAdjustment
  └── services/
        credit/       → CreditService, CreditQueryService, CreditCalculationService,
                         CreditBalanceService, CreditAdjustmentService, InstallmentService
        payment/      → PaymentService
        transaction/  → TransactionService
        analytics/    → KPIService
        client/       → ClientService
        user/         → UserAnalyticsService
        utils/        → InstallmentCalculator
  └── tasks.py        → Celery tasks (credit recalc, installment maintenance, reminders)
  └── management/commands/ → 15+ admin/ops commands

apps.insights         (analytics layer — reads fintech data, owns CLV/alert models)
  └── models: CustomerLifetimeValue, CustomerActivity, CreditRecommendation,
              FinancialControlMetrics, FinancialAlert, DefaultersReport
  └── services/
        dashboard_service.py         → ExecutiveDashboard, CreditAnalytics
        credit_analysis_service.py   → CreditAnalysis, summary, clients
        financial_control_service.py → FinancialControl, DefaultersList
        clv_service.py               → CLV calculations
        recommendation_service.py    → Credit recommendations
        credit_insights_service.py   → Per-credit insights
        credits_table_service.py     → Dashboard risk table
        credit_status_service.py     → Status list with filters

apps.dashboard        (lightweight views — no own models, reads fintech directly)
  └── views.py        → credit/transaction/expense aggregations

apps.revenue          (earnings tracking)
  └── models: CreditEarnings (OneToOne → fintech.Credit)

apps.forecasting      (early stage, models only)
  └── models: (forecasting models, no endpoints yet)
```

## URL → App mapping

| URL prefix | App | Auth |
|---|---|---|
| `fintech/clients/` | fintech | JWT required |
| `fintech/credits/` | fintech | JWT required |
| `fintech/transactions/` | fintech | JWT required |
| `fintech/collector/*` | fintech | Auth disabled (TODO: restore) |
| `dashboard/*` | dashboard | JWT required |
| `insights/dashboard/*` | insights | Auth disabled (TODO: restore) |
| `insights/credits/*` | insights | Auth disabled (TODO: restore) |
| `insights/financial-control/*` | insights | JWT required |
| `api/token/` | simplejwt | Public |

## Data flow: payment registration

```
POST fintech/transactions/
  → TransactionViewSet.create()
  → CreditService.create_transaction_from_payment()
      → finds Credit by uid
      → creates Transaction
      → creates AccountMethodAmount
      → credit.update_total_abonos(amount)
          → recalculates pending_amount
          → triggers morosidad update via signal
```

## Celery Beat schedule summary

| Time | Task |
|---|---|
| 02:00 | `batch_recalculate_credits`, `calculate_installment_fields_batch` |
| 06:00 | `installment_daily_maintenance`, `calculate_overdue_installments` |
| 08:00 | `update_credit_statuses` |
| 09:00 | `send_payment_reminders` |
| 10:00 | `send_overdue_notifications`, `calculate_periodic_installments` |
| 12:00 | `check_additional_interest_daily` |
| 16:00 | `reconcile_payments` |
| every 30m | `update_installment_statuses` |
| Mon 03:00 | `clear_old_cache` |
