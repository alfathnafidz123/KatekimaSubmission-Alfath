
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from ..models import Item, PurchaseDetail, SellDetail
from datetime import datetime


class StockReportView(APIView):
    def get(self, request, item_code, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        try:
            item = Item.objects.get(code=item_code, is_deleted=False)
        except Item.DoesNotExist:
            return Response({"error": "Item tidak ditemukan"}, status=404)

        # Konversi string tanggal ke objek date
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Dapatkan semua transaksi dalam rentang tanggal
        purchases = PurchaseDetail.objects.filter(
            item=item,
            header__date__range=[start_date, end_date],
            header__is_deleted=False,
            is_deleted=False
        ).order_by('header__date')

        sells = SellDetail.objects.filter(
            item=item,
            header__date__range=[start_date, end_date],
            header__is_deleted=False,
            is_deleted=False
        ).order_by('header__date')

        # Inisialisasi data laporan
        report_data = {
            "result": {
                "items": [],
                "item_code": item.code,
                "name": item.name,
                "unit": item.unit,
                "summary": {
                    "in_qty": 0,
                    "out_qty": 0,
                    "balance_qty": 0,
                    "balance": 0
                }
            }
        }

        stock_qty = []
        stock_price = []
        stock_total = []
        balance_qty = 0
        balance_value = 0

        # Gabungkan dan urutkan semua transaksi berdasarkan tanggal
        all_transactions = []

        for purchase in purchases:
            all_transactions.append({
                'type': 'purchase',
                'date': purchase.header.date,
                'description': purchase.header.description,
                'code': purchase.header.code,
                'quantity': purchase.quantity,
                'unit_price': purchase.unit_price,
                'total': purchase.quantity * purchase.unit_price
            })

        for sell in sells:
            all_transactions.append({
                'type': 'sell',
                'date': sell.header.date,
                'description': sell.header.description,
                'code': sell.header.code,
                'quantity': sell.quantity,
                'unit_price': None,
                'total': None
            })

        # Urutkan transaksi berdasarkan tanggal
        all_transactions.sort(key=lambda x: x['date'])

        # Proses setiap transaksi
        for transaction in all_transactions:
            if transaction['type'] == 'purchase':
                # Tambahkan ke stock
                stock_qty.append(transaction['quantity'])
                stock_price.append(transaction['unit_price'])
                stock_total.append(transaction['total'])

                balance_qty += transaction['quantity']
                balance_value += transaction['total']

                # Tambahkan ke summary
                report_data["result"]["summary"]["in_qty"] += transaction['quantity']
                report_data["result"]["summary"]["balance_qty"] = balance_qty
                report_data["result"]["summary"]["balance"] = balance_value

                # Tambahkan ke items
                report_data["result"]["items"].append({
                    "date": transaction['date'].strftime('%d-%m-%Y'),
                    "description": transaction['description'],
                    "code": transaction['code'],
                    "in_qty": transaction['quantity'],
                    "in_price": transaction['unit_price'],
                    "in_total": transaction['total'],
                    "out_qty": 0,
                    "out_price": 0,
                    "out_total": 0,
                    "stock_qty": stock_qty.copy(),
                    "stock_price": stock_price.copy(),
                    "stock_total": stock_total.copy(),
                    "balance_qty": balance_qty,
                    "balance": balance_value
                })
            else:
                remaining_qty = transaction['quantity']
                out_total = 0

                # Hitung total penjualan berdasarkan FIFO
                for i in range(len(stock_qty)):
                    if remaining_qty <= 0:
                        break

                    if stock_qty[i] > 0:
                        deduct = min(stock_qty[i], remaining_qty)
                        out_total += deduct * stock_price[i]
                        stock_qty[i] -= deduct
                        remaining_qty -= deduct

                avg_price = out_total / transaction['quantity'] if transaction['quantity'] > 0 else 0

                # Update balance
                balance_qty -= transaction['quantity']
                balance_value -= out_total

                # Tambahkan ke summary
                report_data["result"]["summary"]["out_qty"] += transaction['quantity']
                report_data["result"]["summary"]["balance_qty"] = balance_qty
                report_data["result"]["summary"]["balance"] = balance_value

                # Tambahkan ke items
                report_data["result"]["items"].append({
                    "date": transaction['date'].strftime('%d-%m-%Y'),
                    "description": transaction['description'],
                    "code": transaction['code'],
                    "in_qty": 0,
                    "in_price": 0,
                    "in_total": 0,
                    "out_qty": transaction['quantity'],
                    "out_price": avg_price,
                    "out_total": out_total,
                    "stock_qty": stock_qty.copy(),
                    "stock_price": stock_price.copy(),
                    "stock_total": stock_total.copy(),
                    "balance_qty": balance_qty,
                    "balance": balance_value
                })

        return Response(report_data)
