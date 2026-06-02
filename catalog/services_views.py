from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cobros_view(request):
    socios = request.data.get("socios", [])

    if not isinstance(socios, list) or len(socios) == 0:
        return Response(
            {"detail": "El campo 'socios' debe ser una lista no vacía."},
            status=status.HTTP_400_BAD_REQUEST
        )

    total_cobro = 0
    detalle     = []

    for socio in socios:
        nombre      = socio.get("nombre", "")
        cuota       = float(socio.get("cuota", 0))
        dias_atraso = int(socio.get("dias_atraso", 0))

        # Determinar porcentaje de recargo según días de atraso
        if dias_atraso == 0:
            recargo_pct = 0
        elif dias_atraso <= 7:
            recargo_pct = 5
        elif dias_atraso <= 15:
            recargo_pct = 10
        else:
            recargo_pct = 20

        recargo     = round(cuota * recargo_pct / 100, 2)
        cobro_socio = round(cuota + recargo, 2)
        total_cobro = round(total_cobro + cobro_socio, 2)

        detalle.append({
            "nombre":      nombre,
            "recargo_pct": recargo_pct,
            "total_cobro": cobro_socio,
        })

    return Response({
        "total_socios": len(detalle),
        "total_cobro":  total_cobro,
        "detalle":      detalle,
    })