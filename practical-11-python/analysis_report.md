# CI build log analysis

- **Failing test:** `test_total_includes_subtotal_and_tax`
- **Observed:** actual value `8`; expected value `108`.
- **Probable cause:** `calculate_total` computes the tax correctly but returns only the tax amount instead of adding it to the subtotal.
- **Source check:** The current source already contains the correction; the supplied log is from the earlier failing revision.
- **Evidence in the failing run:** with a subtotal of 100 and an 8% tax rate, the observed 8 is the tax amount, while the expected payable total is 108.

Failing revision excerpt:

```python
tax = subtotal * tax_rate
return round(tax, 2)
```

- **Verification:** change the return expression to `round(subtotal + tax, 2)` and rerun the payment tests. A successful rerun confirms this diagnosis for the reproduced regression.
