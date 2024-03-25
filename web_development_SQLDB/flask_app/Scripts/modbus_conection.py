from pyModbusTCP.client import ModbusClient

def read_inputs(ip,address,Length):
    client = ModbusClient(ip,502,1,auto_open=True)
    input_read = client.read_input_registers(address,Length)
    if input_read:
        print(input_read)
        client.close()
        return input_read
    else:
        print("Error en la lectura")
        client.close()
        return None
    
def read_contacts(ip,address,Length):
    client = ModbusClient(ip,502,1,auto_open=True)
    discret_values = client.read_discrete_inputs(address,Length)
    if discret_values:
        client.close()
        return discret_values
    else:
        print("Error en la lectura")
        client.close()
        return None 

def write_simple_coil(ip,address,value):
    client = ModbusClient(ip,502,1,auto_open=True)
    state = client.write_single_coil(address,value)
    if state:
        print("Coil enviado correctamente")
        client.close()
        return state
    else:
        print("Error en la escritura")
        client.close()
        return state
    
def write_multiple_coils(ip,address,values):
    client = ModbusClient(ip,502,1,auto_open=True)
    state = client.write_multiple_coils(address,values)
    if state:
        print("Coils enviados correctamente")
        client.close()
        return state
    else:
        print("Error en la escritura")
        client.close()
        return state

def write_simple_holding(ip,address,value):
    client = ModbusClient(ip,502,1,auto_open=True)
    state = client.write_single_register(address,value)
    if state:
        print("Coils enviados correctamente")
        client.close()
        return state
    else:
        print("Error en la escritura")
        client.close()
        return state

def write_multiple_holding(ip,address,values):
    client = ModbusClient(ip,502,1,auto_open=True)
    state = client.write_multiple_registers(address,values)
    if state:
        print("Coils enviados correctamente")
        client.close()
        return state
    else:
        print("Error en la escritura")
        client.close()
        return state