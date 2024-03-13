from flask import Flask, render_template,request,redirect
import Scripts.modbus_conection as Modbus
import Scripts.str2array as str2array
app = Flask(__name__)

@app.route("/",methods =["GET", "POST"])
def main():
    if request.method == "POST":
        state= request.form.get('mb_action')
        match state:
            case "Write Single coil":
                return redirect("http://localhost:5000/coil")
            case "Write Multiple coils":
                return redirect("http://localhost:5000/coils")
            case "Write single register":
                return redirect("http://localhost:5000/holding")
            case "Write multiple register":
                return redirect("http://localhost:5000/holdings")
            case "Read Contacts":
                return redirect("http://localhost:5000/contact")
            case "Read Registers":
                return redirect("http://localhost:5000/input")       
    else:
        return render_template('index.html')
#**************************escritura*****************************
#ESCRITURA DE UN SOLO COIL
@app.route("/coil",methods =["GET", "POST"])
def coil():
    class data:
        title = "Escritura coil"
        add_label = "Dirección coil (Base 0)"
        value_label = "Valor coil"
        function_name = "coil"
        state = False
        data_mb=[]

    if request.method == "POST":
        ip = request.form.get("ip_dir")
        addres= int(request.form.get("Mb_Add"))
        value = int(request.form.get("Mb_val"))
        data.state = Modbus.write_simple_coil(ip=ip,address=addres,value=value)
        return render_template('template.html',data = data)
    else:
        return render_template('template.html',data = data)

#Escritura multiple de coils
@app.route("/coils",methods =["GET", "POST"])
def coils():
    class data:
        title = "Escritura coil"
        add_label = "Dirección coil (Base 0)"
        value_label = "Valor coil"
        function_name = "coils"
        state = False
        data_mb=[]

    if request.method == "POST":
        ip = request.form.get("ip_dir")
        addres= int(request.form.get("Mb_Add"))
        value = str2array.str2array(request.form.get("Mb_val"))
        data.state = Modbus.write_multiple_coils(ip=ip,address=addres,values=value)
        return render_template('template.html',data = data)
    else:
        return render_template('template.html',data = data)

#Escritura un solo holding
@app.route("/holding",methods =["GET", "POST"])
def holding():
    class data:
        title = "Escritura holding"
        add_label = "Dirección registro (Base 0)"
        value_label = "Valor holding"
        function_name = "holding"
        state = False
        data_mb=[]

    if request.method == "POST":
        ip = request.form.get("ip_dir")
        addres= int(request.form.get("Mb_Add"))
        value = int(request.form.get("Mb_val"))
        data.state = Modbus.write_simple_holding(ip=ip,address=addres,value=value)
        return render_template('template.html',data = data)
    else:
        return render_template('template.html',data = data)

#Escritura un solo holding
@app.route("/holdings",methods =["GET", "POST"])
def holdings():
    class data:
        title = "Escritura holdings"
        add_label = "Dirección registro (Base 0)"
        value_label = "Valor holding serparados por comas"
        function_name = "holdings"
        state = False
        data_mb=[]

    if request.method == "POST":
        ip = request.form.get("ip_dir")
        addres= int(request.form.get("Mb_Add"))
        value = str2array.str2array(request.form.get("Mb_val"))
        data.state = Modbus.write_multiple_holding(ip=ip,address=addres,values=value)
        return render_template('template.html',data = data)
    else:
        return render_template('template.html',data = data)

#Lectura de contact
@app.route("/contact",methods =["GET", "POST"])
def contact():
    class data:
        title = "Lectura de contact"
        add_label = "Dirección contact (Base 0)"
        value_label = "Numero de lecturas"
        function_name = "contact"
        state = False
        data_mb=[]
        
    if request.method == "POST":
        ip = request.form.get("ip_dir")
        addres= int(request.form.get("Mb_Add"))
        value = int(request.form.get("Mb_val"))
        data.data_mb = Modbus.read_contacts(ip=ip,address=addres,Length=value)
        if data.data_mb:
            data.state = True
        else:
            data.state = False
        return render_template('template.html',data = data)
    else:
        return render_template('template.html',data = data)

#Lectura de registro
@app.route("/input",methods =["GET", "POST"])
def input():
    class data:
        title = "Lectura de input"
        add_label = "Dirección input (Base 0)"
        value_label = "Numero de lecturas"
        function_name = "input"
        state = False
        data_mb=[]
        
    if request.method == "POST":
        ip = request.form.get("ip_dir")
        addres= int(request.form.get("Mb_Add"))
        value = int(request.form.get("Mb_val"))
        data.data_mb = Modbus.read_inputs(ip=ip,address=addres,Length=value)
        if data.data_mb:
            data.state = True
        else:
            data.state = False
        return render_template('template.html',data = data)
    else:
        return render_template('template.html',data = data)
       
if __name__ == "__main__":
    app.run(debug=True)

