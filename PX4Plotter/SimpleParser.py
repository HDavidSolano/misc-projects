import csv
import matplotlib.pyplot as plt
import gpxpy
sub_reader = []
formato = []
tiempoUS = []
tiempo = []
dato = []
param = 'MAG2'
column = 4
filename = 'stabilize_correct.log' #ESTE ARCHIVO SE AMLACENA EN EL MISMO FOLDER QUE EL PARSER
                                   #Has el archivo en el ultimo mission planner. El archivo no deberia contener errores
def SimpleParser(archivo,param,column,plotear): #Plotear = 0 te da como output las columnas.
    #Por ejemplo si pones como input:
    #SimpleParser(filename,'MAG',4,0) El parser ignora el plot y te da a conocer el contenido de las columnas asi:
    #['FMT', ' 166', ' 34', ' MAG', ' QhhhhhhhhhBI', ' TimeUS', 'MagX', 'MagY', 'MagZ', 'OfsX', 'OfsY', 'OfsZ', 'MOfsX', 'MOfsY', 'MOfsZ', 'Health', 'S']
    #Para plotear, por ejemplo MagZ, tienes que contar desde la columna 'MAG' como ZERo, IGNORAR el ' QhhhhhhhhhBI' y contar hasta MagZ (en este caso 4)
    #Luego pones simplemente SimpleParser(filename,'MAG',4,1) y ese cambio de cero a 1 te da el plot
    time_index = 0
    index_of_param = 0
    with open(archivo, newline='\n') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            if len(row) > 3:
                if param == row[3] or ' '+param == row[3]:
                    formato = row
                    if plotear == 0:
                        print(formato)
                        return formato
            if param == row[0] or ' '+param == row[0]:
                sub_reader.append(row)
    if plotear == 1:
        time_source1 = 'TimeMS'
        time_source2 = 'TimeUS'
        if time_source1 in formato: #Encontrar el time source que se va a usar para el plotter
            time_index = formato.index(time_source1)
            labelx = time_source1 
        if time_source2 in formato:
            time_index = formato.index(time_source2)  
            labelx = time_source2
        if ' '+time_source1 in formato: #Encontrar el time source que se va a usar para el plotter
            time_index = formato.index(' '+time_source1)
            labelx = time_source1
        if ' '+time_source2 in formato:
            time_index = formato.index(' '+time_source2)  
            labelx = time_source2
        if time_index == 0:
            return print('No tiene timestamp')
        if ' '+param in formato:
            index_of_param = formato.index(' '+param)
        if param in formato:
            index_of_param = formato.index(param) 
        for a_row in sub_reader:
            tiempoUS.append(float(a_row[time_index-index_of_param-1])) 
            dato.append(float(a_row[column]))
        base_time = tiempoUS[0]
        for un_timestamp in tiempoUS:
            tiempo.append((un_timestamp-base_time)/1000)
        labely = formato[column+index_of_param+1]    
        fig, ax = plt.subplots()
        ax.set_title(param)
        ax.set_xlabel(labelx)
        ax.set_ylabel(labely)
        ax.plot(tiempo,dato,'--', linewidth=2)
        ax.grid(True)
        plt.show()  
def PlotearGPX(archivo):
    #Este solo nita la direccion del archivo y hace todo solito'
    gpx_file = open(archivo, 'r') 
    gpx = gpxpy.parse(gpx_file) 
    lat = []
    long = []
    for track in gpx.tracks: 
        for segment in track.segments: 
            for point in segment.points: 
                lat.append(point.latitude)
                long.append(point.longitude)
    fig, ax2 = plt.subplots()
    ax2.set_title('GPS Track')
    ax2.set_xlabel('Longitud')
    ax2.set_ylabel('Latitud')
    ax2.plot(long,lat,'--', linewidth=2)
    ax2.grid(True)
    plt.show()   
SimpleParser(filename,'MAG',4,1)
super_track = 'mission_complete.gpx'
PlotearGPX(super_track)