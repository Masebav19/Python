import Scripts.Modbus_client as Modbus

menu = int(input("Ingrese las opciones\n(1) Escritura de un coil\n(2) Escritura multiples coils\n"+
             "(3) Escritura de un registro\n(4) Escritura multiples registros\n"+
             "(5) Lectura de un contact\n(6) Lectura multiples contact\n"+
             "(7) Lectura de un registro\n(8) Lectura multiples registros\n"))

match menu:
    case 1:
        ip = input("Ingrese la dirección IP: ")
        addres = int(input("Ingrese la dirección en base 0: "))
        value = int(input("Ingrese el valor 1/0: "))
        Modbus.write_simple_coil(ip=ip,address=addres,value=bool(value))
    case 2:
        print(menu) 
    case 3:
        print(menu)
    case 4:
        print(menu)
    case 5:
        print(menu)
    case 6:
        print(menu)
    case 7:
        ip = input("Ingrese la dirección IP: ")
        addres = int(input("Ingrese la dirección en base 0: "))
        n = int(input("El nuermo de datos a leer: "))
        value=Modbus.read_inputs(ip=ip,address=addres,Length=n)
        print(value)
    case 8:
        print(menu)
    case _:
        print("No existe esa opción")