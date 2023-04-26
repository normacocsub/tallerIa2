import numpy as np
import os
import plotly.graph_objs as go
import plotly.io as pio
from PIL import Image
import io

entradas = [[1, 1, 0], [1, 0, 0], [0, 1, 1], [0, 0, 1]]
salidas = [[1, 1], [1, 0], [0, 1], [0, 0]]


total_entradas = len(entradas[0])
total_patrones = len(entradas)
total_salidas = len(salidas[0])

pesos = np.random.uniform(-1, 1, size=(total_entradas, total_salidas))
umbrales = np.random.uniform(-1, 1, size=(total_salidas))
#pesos = [[0.1, 0.8], [0.4, 0.7], [0.2, 0.2]]
#umbrales = [0.1, 0.3]
#valores manipulables 
iterations = 1111
error_maximo_permitido = 0.1
rata_aprendizaje = 0.1

# unicapa
print(pesos, "pesos sin entrenar")
print(umbrales, "umbrales sin entrenar")
# iteramos segun las iteraciones definidas
errores_iteracion = []
for iteration in range(iterations):
    # iteramos cada patron de la matriz
    errores_permitidos = 0
    for patron in range(total_patrones):
        salidas_neuronas = []
        errores = []
        error_permitido = 0
        # iteraciones de salida
        for i in range(total_salidas):
            suma_entrada_pesos = 0
            # iteramos cada elemento del patron
            for j in range(total_entradas):
                suma_entrada_pesos += ((entradas[patron][j] * pesos[j][i]))

            #calculamos la salida (dependiendo el tipo de red neuronal se debe ajustar, si es adaline se deja el valor como tal)
            #usaremos perceptron por lo que agregaremos una validaciones extra
            salida_neurona = suma_entrada_pesos - umbrales[i]
            #aplicamos funcion delta (debo extraer esta parte del codigo)
            if salida_neurona > 0:
                salida_neurona = 1
            else:
                salida_neurona = 0
            salidas_neuronas.append(salida_neurona)
            #calculamos el error 
            error = salidas[patron][i] - salidas_neuronas[i]
            
            errores.append(error)

            #iteramos nuevamente las entradas para ajustar los pesos
            for j in range(total_entradas):
                pesos[j][i] = pesos[j][i] + (rata_aprendizaje * error * entradas[patron][j])
            #ajustamos los umbrales
            umbrales[i] = umbrales[i] + (rata_aprendizaje * error * salidas[patron][i])
            #calculamos el error permitido
            error_permitido += error
        #sumamos los errores permitidos por cada patron de la iteracion
        errores_permitidos += (abs(error_permitido) / total_salidas)
        
    #validamos el si el error permitido es menor al error maximo para ver si concluimos el entrenamiento.
    error_iteracion = (errores_permitidos / total_patrones)
    errores_iteracion.append(error_iteracion)
    if (error_iteracion <= error_maximo_permitido):

        x_grafic = list(range(1, len(errores_iteracion)+1))
        fig = go.Figure(data=[go.Scatter(x=x_grafic, y=errores_iteracion)])
        # Renderizar el gráfico en una imagen
        img_bytes = pio.to_image(fig, format='png')
        # Mostrar la imagen en una ventana de Python
        img = Image.open(io.BytesIO(img_bytes))
        img.show()
        #sns.scatterplot(x=x_grafic, y=errores_iteracion)
        print("Error maximo alcanzado, Iteraciones:", (iteration + 1))
        break

#guardamos los umbrales y pesos en una matriz       
np.savetxt("pesos.txt", pesos)
np.savetxt("umbrales.txt", umbrales)


#consultamos los archivos de pesos y umbrales
if os.path.exists("pesos.txt"):
    pesos = np.loadtxt("pesos.txt")

if os.path.exists("umbrales.txt"):
    umbrales = np.loadtxt("umbrales.txt")

print(pesos, "pesos entrenados")
print(umbrales, "umbrales entrenados")
            

#pip install -U kaleido
#pip install PyQt5              

