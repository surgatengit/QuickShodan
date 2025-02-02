import shodan

# Configura tu API Key de Shodan
SHODAN_API_KEY = "TU API KEY"
api = shodan.Shodan(SHODAN_API_KEY)

# Lista de IPs a consultar
ip_list = [
    "1.1.1.1", "8.8.8.8", "9.9.9.9", "4.4.4.4",
]

def search_shodan(ip_list):
    results = []
    for ip in ip_list:
        try:
            data = api.host(ip)
            results.append({
                "IP": ip,
                "Organización": data.get("org", "N/A"),
                "ISP": data.get("isp", "N/A"),
                "País": data.get("country_name", "N/A"),
                "Puertos abiertos": data.get("ports", []),
                "Servicios": [f"{item['port']}/{item['transport']} - {item.get('product', 'Desconocido')}" for item in data.get("data", [])]
            })
        except shodan.APIError as e:
            results.append({"IP": ip, "Error": str(e)})
    
    return results

def display_results(results):
    for entry in results:
        print("\n" + "="*50)
        print(f"IP: {entry['IP']}")
        if "Error" in entry:
            print(f"Error: {entry['Error']}")
        else:
            print(f"Organización: {entry['Organización']}")
            print(f"ISP: {entry['ISP']}")
            print(f"País: {entry['País']}")
            print(f"Puertos abiertos: {', '.join(map(str, entry['Puertos abiertos']))}")
            print("Servicios:")
            for service in entry['Servicios']:
                print(f"  - {service}")
    print("="*50)

# Ejecutar búsqueda y mostrar resultados
results = search_shodan(ip_list)
display_results(results)
