# import json
#
# from celery import shared_task
# from reportlab.pdfgen import canvas
#
# from user.models import Account
# from user.serializers import StudentSerializer
#
#
# @shared_task(bind=True)
# def generate_pdf(self, id):
#     user = Account.objects.get(id=id)
#     serializer = StudentSerializer(user)
#     data = json.dumps(serializer.data)
#     p = canvas.Canvas('report_' + user.name.lower() + '.pdf')
#
#     p.drawString(100, 700, data)
#
#     p.showPage()
#     p.save()