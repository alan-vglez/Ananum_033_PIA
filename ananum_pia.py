import pandas as pd
import statsmodels.api as sm

# Load the data
data = pd.read_csv('lakes_data.csv')  
data = data.drop(columns=['LAKENAME', 'Year']).dropna()

# Introduction message
def introduction():
    with open('introduction.txt', 'r') as file:
        print('\n' + file.read())

# Menu
def menu():
    print("\nMenú de Opciones:")
    print("1. Regresión con cinco variables")
    print("2. Nueva regresión con variables seleccionadas")
    print("3. Salir")

# Multiple linear regression
def regression(x, y):
    Y = data[y]
    X = sm.add_constant(data[x])
    
    model = sm.OLS(Y, X).fit()
    return model

# Interpretation of R-squared, significance, and coefficients
def interpretation(model):
    first_iteration = True
    
    print("\nInterpretación de los Resultados:")
    print(f"R-cuadrado: {model.rsquared:.4f} - El {model.rsquared*100:.2f}% de la variación en los niveles de fósforo es explicada" 
           " por las variables independientes.")
    
    for coef, pvalue, name in zip(model.params, model.pvalues, model.params.index):
        significance = "significativo" if pvalue < 0.05 else "no significativo"
        if first_iteration: 
            print(f"Coeficiente para {name}: {coef:.4f}")
            if coef < 0: 
                print("En ausencia de cualquier efecto de las variables independientes, se tendrán niveles de fósforo"
                      " negativos, algo que no es realista.")
            else: 
                print(f"En ausencia de cualquier efecto de las variables independientes, se tendrán {coef:.4f} mg/L de fósforo.")
            first_iteration = False
        else:
            print(f"Coeficiente para {name}: {coef:.4f} ({significance}, p = {pvalue:.4f})")

def main():
    introduction()
    
    Y = 'PTL'
    X = ['NTL', 'Tot_Sdep', 'OmWs', 'AgKffactWs', 'Depth']
    model_five = regression(X, Y)
    
    while True:
        menu()
        choice = input("Seleccione una opción: ")
        
        if choice == '1':
            print("\nModelo de regresión con cinco variables")
            interpretation(model_five)
        elif choice == '2':
            print("\nNuevo modelo de regresión")
            print("Opciones disponibles: NTL, Tot_Sdep, OmWs, AgKffactWs, Depth")
            new_x = input("Nuevas variables (separadas por coma): ").split(',')
            new_x = [x.strip() for x in new_x if x.strip() in X]
            if new_x:
                new_model = regression(new_x, Y)
                interpretation(new_model)
            else:
                print("Variables inválidas.")
        elif choice == '3':
            print("\nAdiós.")
            break
        else:
            print("\nOpción inválida.")
    
if __name__ == '__main__':
    main()
