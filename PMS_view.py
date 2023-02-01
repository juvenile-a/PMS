from dash import Input, Output, callback, exceptions
import dash_vtk

##############################
# ビュー
##############################


@callback(
    Output('view-0', 'children'),
    Input('product-picker', 'value')
)
def update_0(product):
    if product is None:
        raise exceptions.PreventUpdate
    match product:
        case 'AAA': dataset = '295012-1070-2'
        case _: dataset = 'no_image'
    txt_content = None
    with open(f'datasets/{dataset}.obj', 'r', encoding='utf-8') as file:
        txt_content = file.read()
    view_0 = dash_vtk.View(dash_vtk.GeometryRepresentation(dash_vtk.Reader(
        vtkClass='vtkOBJReader', parseAsText=txt_content),
        property={'opacity': 0.5, 'color': (1, 0.9, 0.8)}),
        cameraPosition=[0.5, -1, 1], cameraViewUp=[0, 0, 1],)
    return view_0
