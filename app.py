from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Inventario simulado
inventario = []


# Ruta para mostrar el inventario
@app.route('/')
def index():
    return render_template('index.html', inventario=inventario)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    query = request.form.get('query', '').lower()
    resultados = [producto for producto in inventario if query in producto['nombre'].lower() or query in producto['descripcion'].lower()]
    return render_template('index.html', inventario=resultados, query=query)

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        color = request.form['color']

        # Validación de campos obligatorios
        if not nombre or not descripcion or not precio or not cantidad or not color:
            flash('Por favor, complete todos los campos antes de agregar el producto.', 'error')
            return redirect(url_for('agregar'))

        producto = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': float(precio),
            'cantidad': int(cantidad),
            'color': color
        }
        inventario.append(producto)
        flash('Producto agregado exitosamente.')
        return redirect(url_for('index'))

    return render_template('agregar.html')


# Ruta para editar un producto
@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    producto = inventario[index]
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['descripcion'] = request.form['descripcion']
        producto['precio'] = float(request.form['precio'])
        producto['cantidad'] = int(request.form['cantidad'])
        producto['color'] = request.form['color']

        flash('Producto actualizado exitosamente.')
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto, index=index)
# Ruta para eliminar un producto
@app.route('/eliminar/<int:index>', methods=['POST'])
def eliminar(index):
    del inventario[index]
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('index'))


# Ruta para ver detalles de un producto
@app.route('/producto/<int:index>')
def producto(index):
    producto = inventario[index]
    return render_template('producto.html', producto=producto)


if __name__ == '__main__':
    app.run(debug=True)
