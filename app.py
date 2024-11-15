from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

inventario = [
    {'nombre': 'Camisa', 'descripcion': 'Camisa de algodón', 'precio': 25000.0, 'cantidad': 10,'categoria': 'Prensa superior'},
    {'nombre': 'Pantalon', 'descripcion': 'Pantalones de mezclilla', 'precio': 35000.0, 'cantidad': 12,'categoria': 'Prenda inferior'},
    {'nombre': 'Chaqueta', 'descripcion': 'Chaqueta de cuero', 'precio': 90000.0, 'cantidad': 5, 'categoria': 'Abrigo'},
    {'nombre': 'Polo', 'descripcion': 'Camisa con cuello', 'precio': 45000.0, 'cantidad': 14, 'categoria': 'Prensa superior'},
    {'nombre': 'Buso', 'descripcion': 'Tiene gorrito', 'precio': 75000.0, 'cantidad': 8, 'categoria': 'Abrigo'},
    {'nombre': 'tenis', 'descripcion': 'Lijeros y comodos', 'precio': 250000.0, 'cantidad': 12, 'categoria': 'Calzado'}
]

categorias_disponibles = ['Prensa superior', 'Abrigo', 'Prenda inferior', 'Calzado']

@app.route('/')
def index():
    return render_template('index.html', inventario=inventario, categorias=categorias_disponibles)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        categoria = request.form['categoria']

        if not nombre or not descripcion or not precio or not cantidad or not categoria:
            flash('Por favor, complete todos los campos antes de agregar el producto.', 'error')
            return redirect(url_for('agregar'))

        producto = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': float(precio),
            'cantidad': int(cantidad),
            'categoria': categoria
        }
        inventario.append(producto)
        flash('Producto agregado exitosamente.')
        return redirect(url_for('index'))

    return render_template('agregar.html', categorias=categorias_disponibles)


@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    producto = inventario[index]
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['descripcion'] = request.form['descripcion']
        producto['precio'] = float(request.form['precio'])
        producto['cantidad'] = int(request.form['cantidad'])
        producto['categoria'] = request.form['categoria']

        flash('Producto actualizado exitosamente.')
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto, categorias=categorias_disponibles, index=index)


@app.route('/eliminar/<int:index>', methods=['POST'])
def eliminar(index):
    del inventario[index]
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('index'))


@app.route('/producto/<int:index>')
def producto(index):
    producto = inventario[index]
    return render_template('producto.html', producto=producto)


@app.route('/buscar', methods=['POST'])
def buscar():
    query = request.form.get('query', '').lower()
    criterio = request.form.get('criterio', 'nombre')
    categoria = request.form.get('categoria', '')

    if criterio == 'nombre':
        resultados = [producto for producto in inventario if query in producto['nombre'].lower()]
    elif criterio == 'precio':
        try:
            precio = float(query)
            resultados = [producto for producto in inventario if producto['precio'] == precio]
        except ValueError:
            flash('Por favor, ingrese un valor numérico válido para el precio.', 'error')
            return redirect(url_for('index'))
    elif criterio == 'categoria':
        resultados = [producto for producto in inventario if producto['categoria'].lower() == categoria.lower()]
    else:
        resultados = inventario

    return render_template('index.html', inventario=resultados, query=query, criterio=criterio, categoria=categoria,
                           categorias=categorias_disponibles)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)