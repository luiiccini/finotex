import pandas as pd
import dash_html_components as html
import base64
# 
FORMATO = {
            # 'display':'block',
            # 'margin':'0 auto'
            'width':'30px',
            'height':'30px',
            'display':'block',
            'margin':'0 auto'
                }
# 

ventas = pd.read_csv('data/fv_ventas_por_linea.csv')

mask = (ventas.Year==2020)&(ventas.TIPO=='PESOS')

resumen = ventas[mask].groupby('MES',as_index=False).agg({
    'TIPO':'count',
    'TOTAL_MX':'sum'
}).round()

total_nov = int(resumen[resumen.MES=='11NOV']['TOTAL_MX'].round().values[0])
total_oct = int(resumen[resumen.MES=='10OCT']['TOTAL_MX'].round().values[0])

cambio_porcentual = round((total_nov/total_oct - 1)*100,2)

unidades_nov = int(resumen[resumen.MES=='11NOV']['TIPO'].round().values[0])
unidades_oct = int(resumen[resumen.MES=='10OCT']['TIPO'].round().values[0])
# 
up_png = 'static/up.png'
up_base64 = base64.b64encode(open(up_png, 'rb').read()).decode('ascii')
static_up = html.Img(src='data:image/png;base64,{}'.format(up_base64),
        style=FORMATO
)