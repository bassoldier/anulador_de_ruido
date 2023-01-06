from pyAudioAnalysis import audioTrainTest as aT

class DetectorAgr:
    
    def procesar(self, ruta, corpus):
        userPath="/Users/diego/Desktop/ILOGICA/ESTUDIO/detector_agresividad/DetectorDeAgresividadEnVoz/MODELOS/"
        if corpus == 'Corpus Chileno':
            model=userPath + "gbSenticChile"
            print("Corpus Chileno")

        if corpus == 'Corpus Híbrido':
            model=userPath + "gbSentic"
            print("Corpus Híbrido")

        if corpus == 'Corpus Británico (SAVEE)':
            model=userPath + "gbSenticSavee"
            print("Corpus SAVEE")

        #resultado=aT.file_classification(ruta, model,"gradientboosting")
        resultado = [
            0.0,
            [0.0000, 1.0000]
        ]
        if resultado[0]==0.0:
            sentimiento="AGRESIVO"
        else:
            sentimiento="NO AGRESIVO"

        print(resultado)
        print(model)
        print("\n Este audio es catalogado como: " + sentimiento + "\n")
        print("Posee un "+ str(resultado[1][0]) + " de Agresividad y un " + str(resultado[1][1]) + " de NO AGRESIVIDAD")

        return resultado